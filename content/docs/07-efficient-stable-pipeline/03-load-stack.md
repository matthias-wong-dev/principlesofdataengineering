---
title: Load orchestration
url: /docs/efficient-stable-pipeline/load-orchestration/
description: Explains how to manage dependency-constrained parallel loads using a visible load stack, load candidates, and workers.
lede: Load dependencies are one of the first bottlenecks in a growing warehouse.
weight: 3
# draft: true
---

## Load stack

Load dependencies are one of the first bottlenecks in a growing warehouse.

The previous chapter explained how to load one table safely. A real pipeline must load many tables safely, in the right order, without making independent tables wait unnecessarily.

At small scale, load order can be managed manually. A developer can hard-code that customers load before orders, orders load before order items, and reference tables load before the facts that use them.

This does not last.

As the warehouse grows, dependencies multiply. A pipeline may contain hundreds or thousands of tables, with tens of thousands of dependency relationships between them. At that scale, load order cannot be safely maintained as a hand-coded sequence. 

A **load stack** addresses this by exposing the pipeline’s execution queue as data.

## Orchestrating a load

The load stack approach rests on three objects.

| Object | Role |
|---|---|
| `Pipeline.LoadDependency` | Records dependency structure: which tables depend on which upstream tables. |
| `Pipeline.LoadStack` | Records execution state for the current workflow: which tables have started and ended. |
| `Pipeline.LoadCandidate` | A view which combines dependency structure and execution state to show which tables are ready to load now. |

The dependency table by itself knows the structure of the pipeline, but not what has already loaded.

The load stack by itself knows what has started and ended, but not what depends on what.

The load candidate view combines both. It asks: given the dependency structure, and given the current execution state, which tables are ready to load now?

Once readiness is visible, workers can claim ready tables independently at run-time, without pre-planned orchestration.

### Dependency metadata

Dependency metadata records which tables must be loaded before another table can load.

Suppose a sales pipeline contains six tables:

- `Sales.Customer`
- `Sales.Product`
- `Reference.Calendar`
- `Sales.Order`
- `Sales.OrderItem`
- `Sales.OrderSummary`

The dependency graph might look like this.

{{< svg >}}
<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="360" viewBox="0 0 1080 360"
     style="display:block;width:100%;max-width:42rem;height:auto;background:transparent" role="img"
     aria-label="Example dependency graph for a sales pipeline load">

  <defs>
    <marker id="arrowhead-load-stack-dag" markerWidth="10" markerHeight="8"
            refX="10" refY="4" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L10,4 L0,8 z" fill="#222222"/>
    </marker>
  </defs>

  <!-- Nodes -->
  <rect x="45" y="55" width="220" height="70" rx="14"
        fill="#ffffff" stroke="#222222" stroke-width="1.8"/>
  <text x="155" y="96" text-anchor="middle"
        font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
        font-size="15" font-weight="700" fill="#111111">Sales.Customer</text>

  <rect x="45" y="220" width="220" height="70" rx="14"
        fill="#ffffff" stroke="#222222" stroke-width="1.8"/>
  <text x="155" y="261" text-anchor="middle"
        font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
        font-size="15" font-weight="700" fill="#111111">Sales.Product</text>

  <rect x="325" y="55" width="220" height="70" rx="14"
        fill="#ffffff" stroke="#222222" stroke-width="1.8"/>
  <text x="435" y="96" text-anchor="middle"
        font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
        font-size="15" font-weight="700" fill="#111111">Sales.Order</text>

  <rect x="605" y="138" width="220" height="70" rx="14"
        fill="#ffffff" stroke="#222222" stroke-width="1.8"/>
  <text x="715" y="179" text-anchor="middle"
        font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
        font-size="15" font-weight="700" fill="#111111">Sales.OrderItem</text>

  <rect x="325" y="255" width="220" height="70" rx="14"
        fill="#ffffff" stroke="#222222" stroke-width="1.8"/>
  <text x="435" y="296" text-anchor="middle"
        font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
        font-size="15" font-weight="700" fill="#111111">Reference.Calendar</text>

  <rect x="845" y="138" width="220" height="70" rx="14"
        fill="#ffffff" stroke="#222222" stroke-width="1.8"/>
  <text x="955" y="179" text-anchor="middle"
        font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
        font-size="15" font-weight="700" fill="#111111">Sales.OrderSummary</text>

  <!-- Arrows -->
  <line x1="265" y1="90" x2="305" y2="90"
        stroke="#222222" stroke-width="2.2"
        marker-end="url(#arrowhead-load-stack-dag)"/>

  <path d="M545 90 C575 90, 575 173, 585 173"
        fill="none" stroke="#222222" stroke-width="2.2"
        marker-end="url(#arrowhead-load-stack-dag)"/>

  <path d="M265 255 C430 255, 430 173, 585 173"
        fill="none" stroke="#222222" stroke-width="2.2"
        marker-end="url(#arrowhead-load-stack-dag)"/>

  <line x1="825" y1="173" x2="845" y2="173"
        stroke="#222222" stroke-width="2.2"
        marker-end="url(#arrowhead-load-stack-dag)"/>

  <path d="M545 290 C710 290, 710 205, 825 205"
        fill="none" stroke="#222222" stroke-width="2.2"
        marker-end="url(#arrowhead-load-stack-dag)"/>

</svg>
{{< /svg >}}

<div style="max-width:42rem;text-align:center;font-size:0.95rem;color:#666;margin-top:0.5rem;">
Figure 1. Example dependency graph for a sales pipeline. A table can load only after all upstream tables pointing into it have finished.
</div>

The same dependency structure can be recorded in a metadata table.

**Example structure of `Pipeline.LoadDependency`**

| Table name | Depends on table name |
|---|---|
| Sales.Order | Sales.Customer |
| Sales.OrderItem | Sales.Order |
| Sales.OrderItem | Sales.Product |
| Sales.OrderSummary | Sales.Order |
| Sales.OrderSummary | Sales.OrderItem |
| Sales.OrderSummary | Reference.Calendar |

Each row states one direct dependency.

`Sales.Order` depends on `Sales.Customer`. `Sales.OrderItem` depends on both `Sales.Order` and `Sales.Product`. `Sales.OrderSummary` depends on `Sales.Order`, `Sales.OrderItem`, and `Reference.Calendar`.

Some tables have no dependencies. In this example, `Sales.Customer`, `Sales.Product`, and `Reference.Calendar` can load at the beginning of the workflow because nothing upstream needs to finish first.

### The load stack

The load stack is the list of tables to be loaded in a workflow.

At the beginning of the workflow, the stack is refreshed. Every table that belongs to the workflow is added to `Pipeline.LoadStack`, with `[Is started] = false` and `[Is ended] = false`.

**Initial `Pipeline.LoadStack`**

| Workflow ID | Table name | Is started | Is ended | Worker ID |
|---:|---|---|---|---|
| 9001 | Sales.Customer | false | false |  |
| 9001 | Sales.Product | false | false |  |
| 9001 | Reference.Calendar | false | false |  |
| 9001 | Sales.Order | false | false |  |
| 9001 | Sales.OrderItem | false | false |  |
| 9001 | Sales.OrderSummary | false | false |  |

The load stack records execution state. It does not itself decide which table is ready.

A table is ready only when all the tables it depends on have ended. This condition is called execution readiness.

### Load candidates

A load candidate is a table in the load stack that is ready to load.

At the beginning of the workflow, only tables with no unfinished dependencies are ready. 

Conceptually, a table is a candidate when:

- it is in the current load stack;
- it has not started;
- none of its dependencies are unfinished.

This logic also works for tables with no dependencies. Their dependency list is empty, so they have no unfinished dependencies.

A load candidate view can expose this list at any time. The view can be simplified if `Pipeline.TableDependency` has already been expanded to contain all upstream dependencies, not only direct dependencies.

**Initial `Pipeline.LoadCandidate`**

| Table name | Reason |
|---|---|
| Sales.Customer | No dependencies. |
| Sales.Product | No dependencies. |
| Reference.Calendar | No dependencies. |

## Using the load stack

The load stack can be used to implement dependency-aware parallel loading.

The basic algorithm is simple.

### Step 1—Refresh the load stack

At the beginning of the workflow, populate `Pipeline.LoadStack` with the tables that need to load.

Set `[Is started] = false` and `[Is ended] = false` for all rows. This creates a visible queue of work for the workflow.

The stack may contain the full pipeline, or only a selected part of it. If a subset of tables is being loaded, the stack should include the necessary upstream tables required for that subset to load correctly.

### Step 2—Start workers

Start any number of workers.

Workers may be stored procedures, functions, notebooks, jobs, or other executable units. Each worker repeatedly checks the load stack until there is no more work to claim.

A worker performs the following loop:

1. Check whether any unstarted tables remain in `Pipeline.LoadStack`.
2. Query `Pipeline.LoadCandidate`.
3. If no candidate is available, pause briefly and poll again.
4. If a candidate is available, claim one table by setting `[Is started] = true`.
5. Load the table.
6. Set `[Is ended] = true` when the load finishes, fails, or aborts.
7. Repeat until no unstarted tables remain.

The worker exits when there are no rows in `Pipeline.LoadStack` where `[Is started] = false`.

### Step 3—Claim a candidate

Once the workers have started, they can pick up load candidates for load.

If three workers are available at the start of the example workflow, each can claim one initial candidate.

**After workers claim the initial candidates**

| Workflow ID | Table name | Is started | Is ended | Worker ID |
|---:|---|---|---|---|
| 9001 | Sales.Customer | true | false | W01 |
| 9001 | Sales.Product | true | false | W02 |
| 9001 | Reference.Calendar | true | false | W03 |
| 9001 | Sales.Order | false | false |  |
| 9001 | Sales.OrderItem | false | false |  |
| 9001 | Sales.OrderSummary | false | false |  |

A table that has started but not ended is not available to other workers. Downstream tables also remain blocked until their dependencies have ended.

Claiming from the load stack must be done in a way that prevents multiple workers from claiming the same table. This can be achieved by wrapping the read from the load candidate view and the update to the load stack in a transaction. This avoids race conditions.

A simplified claim pattern is:

```sql
begin transaction;

select top 1
    [Table name]
from Pipeline.LoadCandidate
where [Workflow ID] = 9001
order by [Table name];

update Pipeline.LoadStack
set
    [Is started] = 1,
    [Worker ID] = 'W01',
    [Load start datetime] = current_timestamp
where
    [Workflow ID] = 9001
    and [Table name] = @TableName
    and [Is started] = 0;

commit transaction;
```

The exact syntax will vary by SQL platform. The important point is that the worker should not select and claim a candidate in two unsafe steps. The claim should happen atomically.

### Step 4—Load, end, and repeat

When a table finishes loading, the worker marks it as ended.

```sql
update Pipeline.LoadStack
set
    [Is ended] = 1,
    [Load end datetime] = current_timestamp
where
    [Workflow ID] = 9001
    and [Table name] = 'Sales.Customer'
    and [Worker ID] = 'W01';
```

Suppose `Sales.Customer` finishes first.

**After `Sales.Customer` ends**

| Workflow ID | Table name | Is started | Is ended | Worker ID |
|---:|---|---|---|---|
| 9001 | Sales.Customer | true | true | W01 |
| 9001 | Sales.Product | true | false | W02 |
| 9001 | Reference.Calendar | true | false | W03 |
| 9001 | Sales.Order | false | false |  |
| 9001 | Sales.OrderItem | false | false |  |
| 9001 | Sales.OrderSummary | false | false |  |

`Sales.Order` now becomes a load candidate because its only dependency, `Sales.Customer`, has ended.

**Current `Pipeline.LoadCandidate`**

| Table name | Reason |
|---|---|
| Sales.Order | `Sales.Customer` has ended. |

A worker can now claim `Sales.Order`.

**After `Sales.Order` is claimed**

| Workflow ID | Table name | Is started | Is ended | Worker ID |
|---:|---|---|---|---|
| 9001 | Sales.Customer | true | true | W01 |
| 9001 | Sales.Product | true | false | W02 |
| 9001 | Reference.Calendar | true | false | W03 |
| 9001 | Sales.Order | true | false | W01 |
| 9001 | Sales.OrderItem | false | false |  |
| 9001 | Sales.OrderSummary | false | false |  |

Suppose `Sales.Product`, `Reference.Calendar`, and `Sales.Order` have all finished.

**After `Sales.Product`, `Reference.Calendar`, and `Sales.Order` end**

| Workflow ID | Table name | Is started | Is ended | Worker ID |
|---:|---|---|---|---|
| 9001 | Sales.Customer | true | true | W01 |
| 9001 | Sales.Product | true | true | W02 |
| 9001 | Reference.Calendar | true | true | W03 |
| 9001 | Sales.Order | true | true | W01 |
| 9001 | Sales.OrderItem | false | false |  |
| 9001 | Sales.OrderSummary | false | false |  |

`Sales.OrderItem` is now ready because both of its dependencies have ended.

**Current `Pipeline.LoadCandidate`**

| Table name | Reason |
|---|---|
| Sales.OrderItem | `Sales.Order` and `Sales.Product` have ended. |

`Sales.OrderSummary` is not ready yet. Even though `Sales.Order` and `Reference.Calendar` have ended, `Sales.OrderItem` has not.

After a worker claims and finishes `Sales.OrderItem`, the stack looks like this.

**After `Sales.OrderItem` ends**

| Workflow ID | Table name | Is started | Is ended | Worker ID |
|---:|---|---|---|---|
| 9001 | Sales.Customer | true | true | W01 |
| 9001 | Sales.Product | true | true | W02 |
| 9001 | Reference.Calendar | true | true | W03 |
| 9001 | Sales.Order | true | true | W01 |
| 9001 | Sales.OrderItem | true | true | W02 |
| 9001 | Sales.OrderSummary | false | false |  |

`Sales.OrderSummary` is now ready.

**Current `Pipeline.LoadCandidate`**

| Table name | Reason |
|---|---|
| Sales.OrderSummary | `Sales.Order`, `Sales.OrderItem`, and `Reference.Calendar` have ended. |

After `Sales.OrderSummary` ends, the workflow is complete.

**Completed `Pipeline.LoadStack`**

| Workflow ID | Table name | Is started | Is ended | Worker ID |
|---:|---|---|---|---|
| 9001 | Sales.Customer | true | true | W01 |
| 9001 | Sales.Product | true | true | W02 |
| 9001 | Reference.Calendar | true | true | W03 |
| 9001 | Sales.Order | true | true | W01 |
| 9001 | Sales.OrderItem | true | true | W02 |
| 9001 | Sales.OrderSummary | true | true | W03 |

The workflow ends when there are no rows in `Pipeline.LoadStack` where `[Is started] = false`.

### Handling failure

If the table fails or aborts, the worker can still mark the table as ended, but should also record the outcome.

```sql
update Pipeline.LoadStack
set
    [Is ended] = 1,
    [Load end datetime] = current_timestamp,
    [Load status] = 'Failed',
    [Failure message] = 'Source extract timeout'
where
    [Workflow ID] = 9001
    and [Table name] = 'Sales.Order'
    and [Worker ID] = 'W01';
```

Whether downstream tables should proceed after a failure depends on the pipeline’s policy.

A strict pipeline may treat failed upstream loads as incomplete and block downstream work.

A more fault-tolerant pipeline may allow downstream tables to proceed if they can safely use the previous successful version of the upstream table.


## Advantages of the load stack

### Correct order is computed, not hard-coded

The load candidate view ensures that a table is offered for loading only when its upstream dependencies have ended.

This means correct order does not depend on a developer manually maintaining a sequence of execution steps. The order emerges from dependency metadata and the current state of the load stack.

When a new table is added, the data engineer adds its dependency metadata. The load candidate view uses that metadata to determine when it is ready. The orchestration logic does not need to be rewritten for every new dependency path.

### Parallelism is free

Parallelism is a consequence of the readiness rule.

If three independent tables are ready, three workers can claim them. If ten independent tables are ready, ten workers can claim them. If only one table is ready, only one table is available.

There is no need for a central process to decide in advance which tables should run side by side. Workers simply claim tables that are ready.

The number of workers can be adjusted according to available resources. The load stack does not need to know how many workers exist. It only needs to expose which tables are ready.

Moreover, the algorithm is load-balanced by default with a greedy approach to assigning work. As soon as a load candidate is ready, a worker picks up the job. There are no situations where a table is ready to load and a worker is available, but the load does not happen.

### Execution state is visible and manipulable

Because the load stack is a table, the state of the workflow can be inspected while the load is running.

The data engineer can see:

- which tables have not started;
- which tables are currently loading;
- which tables have ended;
- which worker claimed each table;
- which tables are blocked;
- which tables failed or aborted.

But visibility is only part of the value.

Because execution state is stored as data, it can also be manipulated. A table can be placed back on the stack by setting `[Is started] = false` and `[Is ended] = false`. A subset of tables can be added to the stack for a targeted repair load.

This makes the workflow controllable while it is running.

The load is no longer a hidden procedural state inside a scheduler. It is visible and editable execution state.

### Higher-frequency loads

Most warehouses run in daily batches, but some parts of a warehouse may need to load more frequently.

A load stack allows a selected path through the pipeline to be loaded more often than the whole warehouse. This works if the tables in that path are efficient enough to meet the required frequency, but the orchestration pattern does not need to change.

A path that is incrementally processed can be loaded hourly, every few minutes, or continuously, while the rest of the warehouse remains on its normal batch schedule.

This gives the data engineering team a gradual path toward higher-frequency loading.

### Cross-technology loading requires shared state, not shared tooling

The load stack can also support orchestration across technologies.

A complex pipeline may use SQL stored procedures, Spark notebooks, Python functions, or other processing technologies. A central orchestration product may provide connectors for each of these technologies, but the load stack takes a different approach.

The only requirement is that each worker can read and update the shared load stack.

For example, `Pipeline.LoadStack` and `Pipeline.LoadCandidate` may be implemented in a SQL database. A SQL procedure, Spark notebook, and Python process can all participate as workers if they can connect to the database, claim candidates, and update the stack.

This makes the load stack technology-agnostic. The coordination happens through shared execution state.

> [!NOTE]
> **Key ideas**
>
> Load dependencies are one of the first bottlenecks in a growing warehouse.
>
> A load stack exposes the pipeline’s execution queue as data.
>
> Dependency metadata records which tables depend on which upstream tables.
>
> The load stack records which tables in the current workflow have started and ended.
>
> A load candidate is a table whose upstream dependencies have all ended.
>
> The load candidate view combines dependency metadata with the current state of the load stack.
>
> Workers can claim load candidates independently, allowing dependency-aware parallel loading without a central scheduler.
>
> The load stack makes orchestration visible, controllable, and easier to debug.
>
> The same pattern supports partial loads, higher-frequency loads, and cross-technology orchestration.