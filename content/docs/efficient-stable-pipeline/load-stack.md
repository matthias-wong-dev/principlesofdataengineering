---
title: Load stack
weight: 3
draft: true
---

The chapter Load mechanics look at the details of how a single table is loaded. This chapter looks at how load across multiple tables can be orchestrated across the pipeline. In a data pipeline, tables need to be loaded in the correct order. Even with a small number of tables, such as twenty to fifty, their dependencies can become difficult to manage. Poor implementation, such as manually coding their load order, leads to an unmaintainable pipeline that is hard to debug. In addition, loading tables in parallel is an easy way to reduce the total amount of time to process a large pipeline. Even a four-fold reduction may mean the difference between meeting the start of the business day or not. Load orchestration is the task of ensuring the loads in a pipeline happen correctly, always in order, and in parallel if computational resources are available. There are two main ways of orchestrating a load:

- A centralised approach where a main process assigns work to workers

- A decentralised approach where workers grab work from a queue

In the centralised approach, a software orchestrates other server jobs to load tables in the right order and manages the parallelism. It is often difficult for data engineering teams to create such software at scale and requires the purchase of a vendor product. On the other hand, the decentralised approach in this chapter is easy for any team to implement. All it takes are:

- An accurate record of pipeline lineage as metadata, that is, how one table draws

data from other tables in the pipeline.

- The ability to load one table at a time, that is, there are no procedures or

functions that load two tables in an entangled fashion. The decentralised approach achieves the aim by maintaining a queue of work, making the queue visible, and allowing workers to grab from the queue. We call this queue the load stack.

## Load stack and load candidates

The load stack is a list of tables to be loaded. Each row represents a table to be loaded and annotated with two columns: [Is started] and [Is ended]. These indicate whether the load for that table has begun or finished. If [Is started] = 0, the table has not yet started loading and needs processing. [Screenshot]

But not every table with [Is started] = 0 is ready to load. Loads must follow the correct order. A table is ready only when all the tables it depends on have finished loading, a concept known as execution readiness. These are the load candidates. Identifying the load candidates requires a list of each table’s load dependencies. That is, the tables which directly feed into a table through a load. [Screenshot] It is instructive to visualise the dependencies in a directional graph. Each arrow shows a direct feed from one table into another. [Screenshot] By tracing dependencies upstream, the full set of prerequisites for each table can be found. These are the expanded dependencies of a table. [Screenshot] The load stack and the expanded dependencies are all that are needed to identify the load candidates, that is, the tables that are ready to load. A table is a load candidate if there are none of the tables in its expanded dependencies that have not ended. That is, there are no dependencies where [Is ended] = 0. This logic also works for tables with no dependencies at all, since their expanded dependency list is empty and therefore contains no unfinished loads. When a table has no unfinished loads in an upstream table, it is a candidate to start loading. This logic can be exposed as a view. The view shows the current list of load candidates and can be queried at any time to find which tables are ready to load. [SQL and SCREENSHOT]

## Using the load stack

The load stack table and the load candidate view can be used to implement a parallel load using the following algorithm. Step 1. At the beginning of the load, populate the load stack and set [Is started] and [Is ended] to 0 for all rows. This is called refreshing the load stack and may require deleting existing rows. Step 2. Start any number of workers. These could be functions in sub-processes or stored procedures in independent sessions. Each worker continuously polls the load stack and continues polling until there are no more tables with [Is started] = 0.

If there are still tables to be loaded, the worker queries the load candidate view to pick up a table that is ready to load. If the view returns a table, the worker

1. sets [Is started] = 1 for that table in the load stack. This is claiming the table for

2. 3. loading,

invokes the function or procedure to load the table, and sets [Is ended] = 1 when the load finishes or is aborted due to an error. If the view returns no tables, the worker pauses for two seconds before polling again. The worker exits when there are no more tables in the load stack with [Is started] = 0. Claiming from the load stack must be done in a way that prevents multiple workers from claiming the same table. This can be achieved by wrapping the read from the load candidate view and the update to the load stack in a transaction. This avoids race conditions. In summary, this is all that is necessary to implement parallel load:

- The load candidate view, informed by expanded dependencies, ensures that a

table is only offered for loading if it has no upstream tables still loading. This guarantees correct load order.

- Multiple workers can pick up jobs as soon as they become available.

- Transactions and locks around the claim step ensure that workers do not clash

when selecting the same table. While these steps are sufficient for parallel loading, it is useful to log additional columns.

- Start and end datetimes for each table in the load stack.

- A single [Workflow ID] assigned to every table in the load stack when it is

refreshed. This ID represents the batch of load.

- A [Worker ID] generated by each worker, recorded against the table to show how

jobs are distributed.

## Advantages

The advantages of the load stack are numerous. No special code for parallelism There is no special code for parallelism. The logic looks identical whether one worker or many are used. The primary purpose of the load stack and the load candidate view is to ensure that tables load in the correct order. The ability to load multiple tables simultaneously is a natural side-effect of the design. The only difference between serial and parallel load is the number of workers started at a given moment. This does not

need to be known to any central orchestrator. In fact, the load stack does not even track how many workers are active. Unlimited and dynamic workers The number of workers is unlimited and can be turned on or off at any time. Many parallel load algorithms decide on the number of workers at the beginning and launch them accordingly. The load stack approach allows the platform engineer to respond to server resources in real time by adjusting the number of workers. Only minor changes are needed to allow workers to exit the polling loop early. Greedy and balanced work assignment The algorithm is well load-balanced by default. It uses a greedy approach to assigning work. As soon as a load candidate is ready, a worker picks up the job. There are no situations where a table is ready to load and a worker is available, but the load does not happen. While this does not guarantee optimal load time, it minimises idle workers. For further improvements, the load candidate view can be adjusted to return the next table based on a more fine-tuned balancing logic. Partial pipeline support It is easy to load only a portion of the pipeline. The expanded dependencies show exactly which tables are upstream from any given set. Loading only part of the pipeline can be achieved by populating the load stack with just those tables. This allows a subset of the pipeline to run more frequently or on a different schedule than the full pipeline, without needing changes to a central orchestration plan. Mid-load interference Since load is controlled by making tables available on the load stack, the approach supports mid-load interference by editing the load stack. For example, tables can be put back on the load stack during a load by setting [Is started] = 0 for those tables. This supports error correction and retries mid-load. Increased load frequency Most warehouses run loads in a daily batch, but some business needs require more upto-date information that could be hourly or minutes latency, demanding a higher load frequency. In practice, higher load frequencies are only practical if each of the table in the pipeline is incrementally processed. It is unlikely that every table in a large warehouse would be implemented this way. The load stack makes it a possible to load any portion of the pipeline. This means that it is easy to select a path within the overall pipeline for increased load frequency while allowing the rest to happen in usual batches. In the most demanding case, editing the load stack mid-load can be used to implement continuous loads. For example, workers start to process the pipeline, while another

process periodically resets one or more tables by setting [Is started] = 0 on the load stack. This puts the tables back on the queue for continuous processing. The load stack allows a data engineering team to treat low and high frequency loads with the same orchestration. A path within a pipeline where all the tables are efficient can be loaded more regularly, increasing the frequency from once a day to multiples times in an hour, and ultimately to run continuously. It only depends on the investment in making each of the table in the path to process within the required response time. This graduation allows "just-enough" investment to meet frequency targets. This gives teams a continuous-load option before considering the need to adopt dedicated streaming platform. Cross-technology orchestration The load stack supports orchestration across multiple technologies. While many pipelines run on a single stack, complex problems may require different technologies for different parts of the load. The usual solution is to purchase orchestration software with connectors for each technology. The load stack reverses this. The only requirement is that the central load stack table is visible to all technologies. There is no need for a central worker to have connectors. For example, the load stack and load candidate view may be implemented in a SQL database, with claiming done through a stored procedure. As long as other technologies, such as Spark or other SQL warehouses, can connect via ODBC, they can participate. The load stack enables cross-technology orchestration with minimal requirements.

## Conclusion

Load orchestration is the task of ensuring tables in a data pipeline load correctly with respect to their dependencies, even when doing so in parallel. It is easy for load orchestration to go out of hand, creating pipelines that are opaque and impossible to maintain. When the pipeline becomes complex, some organisations may purchase orchestration software and additional servers to host them. The load stack approach is a simple alternative. It does not require additional servers or software. Only minor amendments using tools already available to a data engineer are needed. The only requirements for the data engineer are to capture each table with its direct dependencies in a metadata table, and to modularise code so that each table can be loaded independently. The load candidate view computes execution readiness by consulting the state of the load stack to know what jobs have been complete and comparing it to the metadata table of dependencies. This ensures the load happens in the correct order no matter the level of complexity in dependencies, and no matter the number of workers, even in the absence of a centralised orchestrator. Compared to other common approaches towards orchestration, the load stack is a queue-based coordination adjusted for lineage-awareness. At any given point, it uses
