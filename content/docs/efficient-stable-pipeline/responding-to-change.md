---
title: Responding to change
description: Shows how downstream tables and models should respond when upstream data, logic, or structure changes over time.
lede: Detecting change is only the first step; the pipeline must also respond intelligently.
weight: 6
draft: true
---

The previous chapter Tracking changes focused on tracking changes in the source. The chapter builds on the previous and addresses the harder task of responding correctly to these changes. This is often known as incremental extract and load. Accurately responding to change can be error-prone. This is because inserts, updates, and deletes upstream do not translate directly into the corresponding changes downstream. The following examples illustrate the possible complexities:

- Inserts can trigger deletes. The Bank.CustomersToFollowUp is a computed

table of customers who have not made recent deposits and require follow-up by the service team. This table takes input from the Bank.Transactions table. In this case, an insert into Bank.Transactions, such as a new deposit, would trigger a delete in Bank.CustomersToFollowUp.

- Deletes can trigger updates. The Bank.AccountSummary is a computed table

of account-level aggregates, such as total number of holders and balance per account. It takes input from Bank.AccountHolder, which records all individuals associated with each account. If a joint holder is removed, resulting in a delete from Bank.AccountHolder, this changes the holder count and may trigger an update in Bank.AccountSummary.

- Updates can trigger inserts. The Bank.GoldCustomer is a computed table of

customers whose account balance exceeds a defined threshold. It takes input from the Bank.AccountBalance table. In this case, updating a row in Bank.AccountBalance to increase the balance may cause a customer to newly qualify for gold status, triggering an insert into Bank.GoldCustomer. These examples are highly artificial. However, it is easy to imagine the possibilities under general circumstances:

- The presence of anti-joins (e.g. not exists) means that inserts upstream can

trigger deletes downstream.

- The presence of aggregation or windowing (e.g. group by) means that deletes

upstream can trigger updates downstream.

- The presence of filters on derived expressions (e.g. having) means that

updates upstream can trigger inserts downstream. The following is an illustrative list of correct ways to respond to upstream changes, and a pattern for applying this response to incrementally loading a table.

## Analysing the query

Suppose there are two tables X and Y, and these are used as inputs to a data pipeline. The set up is as follows:

- X has columns [Header ID], [Value], [Status], where [Header ID] is primary key.

- Y has columns [Header ID], [Line number], [Value], [Status] , where [Header ID]

and [Line number] is primary key. And Y[Header ID] is a foreign key to X[Header ID] and joins on this column. There could be inserts, updates and deletes on X, as well as on Y. Thus, there are six possible input changes each time. In practice, inserts and updates and can often be considered as a single upsert. Thus, the inputs are:

- upserts from X

- deletes from X

- upserts from Y

- deletes from Y

Suppose the target table is T. The goal is to determine which rows in the target table need to be inserted, updated, or deleted. This is done by computing a driver set of primary keys that might be affected by changes in source tables (X and Y). Inserts and updates can be considered as one. Thus, the goal is to calculate:

- primary keys to upsert on T

- primary keys to deletes on T

The way to calculate these depends on the nature of the query. Some possible scenarios include:

1. A straight select of X

2. A filter of X on status

3. X inner join Y

4. X inner join Y group by [Header ID] to sum over Y[value]

5. X left join Y coalesce on [Line number] to 0 where Y[Header ID] does not exist

6. Y left join X

7. X left join Y group by [Header ID] to sum over Y[value]

8. X union Y

9. X left anti-join Y

All of these would require a different treatment. These are summarised in the table: Scenario Primary key Approach Primary keys to upsert in T Primary keys to delete in T

1.

Straight select of X [Header ID] Simple case: X changes map directly to T. Headers from X that were inserted or updated Headers from X that were deleted

2. Filter

of X on status

3. X inner

join Y

4. X inner

join Y with group by

5. X left

join Y with synthetic line 0

6. Y left

join X

7. X left

join Y with group by

8. Union

of [Header ID] ([Header ID], [Line number]) [Header ID] ([Header ID], [Line number]) ([Header ID], [Line number]) [Header ID] [Header ID] UNOFFICIAL Filter condition means updates can add or remove rows. Headers from X that were inserted or updated and now pass the filter Join means changes on either side can add or remove pairs. Pairs for Y rows inserted/updated, plus pairs for X headers inserted/updated with matching Y rows Deleting a Y row can change the aggregate or remove the header. Headers from X or Y that changed and now have Y rows; include changes in Y, deletes in Y can also change the aggregated value Synthetic line 0 appears only when no Y rows exist. Pairs for Y rows inserted/updated; plus (Header ID, 0) for headers with no Y rows; plus pairs for new X headers T follows Y’s lines; X changes matter only if Y lines exist. Pairs from Y inserted/updated; plus pairs under headers in X that changed X controls row presence; Y only changes the aggregates. Headers in X inserted; headers where values changed due to X or Y changes, including deletes from Y Header exists if present in either X or Y. Headers inserted/updated in X or Y; headers Headers from X that were deleted, or updated and no longer pass the filter Pairs for Y rows deleted, plus all pairs for headers deleted from X Headers deleted from X, or headers that now have zero Y rows Pairs for Y rows deleted; remove (Header ID, 0) when Y rows exist; remove all pairs for headers deleted from X Pairs from Y that were deleted Headers deleted from X Headers deleted from both X and Y

projected headers deleted from one side but still exist on the other

9. X left

anti-join Y [Header ID] Row appears only when X exists and Y does not. Headers inserted/updated in X with no Y rows; headers where Y rows were deleted and now qualify Headers deleted from X; headers that gained a Y row These show an array of considerations for two tables. If there are more tables, even up to 10, the analysis can become complicated. Consider a query that draws from several tables, such as: The first step is to determine conditions for upsert in the target. For each source table, evaluate how changes in that table may influence the result of the query. In general:

- An upsert in a source table typically results in an upsert in the target.

Any insert or update in A, B, or C may alter projected values and therefore requires re-computation.

- A delete in a source table may also result in an upsert in the target.

This occurs when the query includes: o Left joins, where the absence of a row changes a value to a default rather than removing the target row. o Aggregations, where the removal of a contributing row modifies a computed measure. Thus, for each table, the question is: "Could an insert, update, or delete in this table change the values produced by the query?" If so, the corresponding key should be included in the driver set for upserts. The next step is to determine conditions for deletes from the target.

In most cases, this occurs only when the tables that governs row presence loses the corresponding row. For example:

- If the query begins with A left join B left join C ..., then deleting a row from A

removes the target row. Deleting a row from B or C generally does not remove the target row; it only changes values.

- If the query begins with A inner join B left join C, then deleting a row from A or B

removes the target row. But this can also happen through updates or inserts:

- In the case of A left anti-join B, an insert to A can cause a row to delete.

- In the case of A filtered on a row value, an update to the value can cause a

delete. In summary, upserts arise from any change that affects projected values. Deletes occur only when the base row is removed. Filtering predicates and grouping clauses may cause deletes in a source table to behave as upserts in the target, as they alter aggregates or conditions. The same reasoning applies to more complex constructs such as unions or set operations, as these are ultimately composed of similar units. Working through these scenarios can be error prone. Latest innovations in generative AI can provide valuable assistance in this analysis. For example, the table of solutions generated for the 9 scenarios above was generated by GPT-5 using only column 1.

## Applying the change

Analysing the query with respect to changes from the source tables informs an incremental extract. Recall from Load mechanics that the difference between incremental extract and full extract are:

- The staging table for the load has only a minimal set of records that is much

smaller than the full set, but still covers all the records that would need to be upserted in the current batch. This is what makes the load fast.

- Deletes cannot be done automatically by comparing the full set of primary keys

between the staging and the target. Instead, it needs to be customised for the query by analysing the impact of changes in source. The detailed implementation of an incremental extract follows a consistent pattern. Write query as normal Begin with the full query that expresses the business logic. This is the reference point for all subsequent steps.

Fetch the bookmark At the start of the load, retrieve the bookmark that records the last successful refresh. This value defines the boundary for change detection. The bookmark for all tables loaded by the pipeline should be logged to a central location and easily retrieved. Create minimal staging table Using the analysis of the query, create a temporary table of keys to upsert to the target. In these examples, the driver table has the full key. In practice, it may be a primary key part in the case of multi-columns primary keys. Attach the driver set as an inner join to the original query. If performance requires, add a clustered index to the driver table.

This is now a minimal staging table for incremental load. Create the delete set Using the analysis of the query, create a temporary table of keys to delete from the target. This can be used to delete records that should no longer be retained by logic of the query. Retrieving the records that are deleted would vary depending on how they are tracked. Consider the case where overwritten or deleted records are moved to a history table. Then the examples would be: This step works even if the source rows were inserted and deleted in between the load of the target table, for example, if the target table failed to load in the interim. Inexperienced engineers can make the mistake of over-deleting with the idea of reinserting extra records. This can be tempting because a delete + insert can be easier to calculate than a finely targeted delete + upsert. However, this approach is harmful because it is a source of potential instability. In unpredictable circumstances, this may

trigger the whole table to delete. Instead, deletes should be perfect and remove only rows that no longer satisfy the query’s presence rule. The full script follows.

This workflow offers several advantages. Uniformity. The same query logic underpins both full loads and incremental loads. The difference lies only in the addition of a driver set join. Idempotency. The process works regardless of how many times it runs within an interval. If a load fails and is retried, the bookmark ensures correctness. If the load runs more frequently than usual, the outcome remains consistent. Graceful fallback. If upstream changes touch many rows, say due to a system update, the driver set expands and the incremental load behaves like a full load. The fully load staging table would be compared to the target and only genuinely updated records are applied. There is no explosion of deletes that would cause a blow out in operations.

## Best practice workflow

Given the complexity of responding to change, this section outlines a step-by-step recipe for developing and validating pipelines that respond to upstream inserts, updates, and deletes. The workflow balances technical correctness with performance assurance and safe deployment. Start with a unit test

- Compare row counts between the target table and the expected query.

- Use a datetime filter for performance, but ensure it’s independent of the extract

datetime. Simulate data needing update

- Load the table in full, then wait for source data to change to simulate an

incremental load. Build the upsert driver

- As each source table is added, re-run the driver query to check performance.

- Apply indexes if performance degrades.

Test the query filter

- Ensure the inner join between the driver and the original query is performant.

Calculate deletes

- Ensure the delete driver query runs quickly.

Simulate deletes

- Rather than actually deleting, use a select to simulate deletes during

development to avoid accidental data loss.

Apply changes and validate Uniqueness, existence, and stability violations

- Apply upserts and deletes.

- Compare the result with a fully loaded copy of the table.

- The unit test should pass.

Zero-load benchmark

- After loading, re-run the upsert and delete drivers.

- They should return no rows and run in near-zero time.

- The time it takes to do this is the fastest the query can ever run.

Run incrementally over time

- Continue loading incrementally over multiple days.

- The unit test should continue to pass.

## Conclusion

A transformation query can be seen as a formula that takes inputs and produces output. Information efficiency is achieved when changes in the input are accurately tracked and correctly translated into changes in the output. The difficulty of doing this depends not on the volume of data, but on the shape of the query. Anti-joins, aggregations, filters, and window functions all introduce complexity in determining which rows to upsert and which to delete. This determination should be made by analysing the query through the lens of relational algebra. Modern tools, including generative AI, can assist in this analysis by surfacing the logical structure of the query and identifying the propagation of change. Once the analysis is complete, the transformation can be converted from full to incremental using a standardised approach. This is to fetch the refresh bookmark of the target, compute the upsert driver table, downfilter the original query, and compute the delete driver table. Care must be taken not to over-delete and reinsert. Deletes should perfectly represent only the rows that should no longer be part of the target as of query. When coupled with the use of refresh bookmarks and the techniques described in Tracking changes, this approach yields an efficient and resilient pipeline. Given the intricacies involved, careful implementation and testing is essential. A unit test is critical to catch errors during development, and silent failures in production. Performance evaluation should be done step by step, with each component tested in isolation. The zero-load scenario provides a baseline benchmark for performance and correctness. This disciplined workflow ensures that the pipeline responds to change with both accuracy and speed.
