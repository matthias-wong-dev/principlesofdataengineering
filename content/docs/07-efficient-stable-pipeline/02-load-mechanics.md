---
title: Load mechanics
url: /docs/efficient-stable-pipeline/load-mechanics/
description: Explains how to load data safely by staging incoming records, checking genuine changes, rejecting unsafe rows, and applying updates in a controlled way.
lede: A mature load applies only genuine changes, after checking that they are safe.
weight: 2
# draft: true
---

## Controlling change

Efficiency and stability both depend on the warehouse remaining in control of change.

Efficiency requires the warehouse to know which rows genuinely changed, so it does not waste work reprocessing rows whose information stayed the same.

Stability requires the warehouse to know whether the proposed changes are safe, so abnormal changes do not spread through the pipeline.

Therefore, the purpose of a load is not only to keep the target table current. The purpose is to keep the warehouse in control of change.

For every change applied to a table, the warehouse should be able to explain why the change happened, whether it should happen, what changed, and when it changed.

A naive load loses this control.

When a table is replaced wholesale, the pipeline can no longer reason precisely about change. Every row may appear new. Unchanged rows are mixed with changed rows. Unsafe rows are mixed with safe rows. Deletes are difficult to distinguish from load failures. Downstream tables cannot respond with precision because the warehouse has not preserved the meaning of what happened.

This is inefficient because downstream tables may need to respond to rows that did not genuinely change. It is unstable because one abnormal load may cause a disproportionate change in the target and downstream tables.

The extra work in controlling change takes effort, but it lays the foundation for an efficient and stable pipeline. This is the topic of **load mechanics**.

The standard pattern has three steps:

| Step | Question |
|---|---|
| Stage | What incoming data is available? |
| Check | Which rows genuinely changed, and are those changes safe? |
| Apply | How should the target table be updated without losing history or spreading faults? |

These are the same steps whether the incoming data is a full extract or an incremental extract.
## The three-step load pattern

Suppose the target table is `Sales.Order`. The goal is to update `Sales.Order` with the latest batch of data.

For this pattern to work, the target table must have a defined primary key.

In this example, `Sales.Order` is keyed by `[Order ID]`.

For any target table, the standard load pattern may create the following artefacts:

| Artefact | Purpose |
|---|---|
| `Sales.Order_staging` | Incoming data before `Sales.Order` is touched. |
| `Sales.Order_upsert` | Rows that are new or genuinely changed. |
| `Sales.Order_delete` | Rows that should be removed from the current target. |
| `Sales.Order_reject` | Rows that violate constraints and should not enter the target. |
| `Sales.Order_history` | Previous versions of rows that were updated or deleted. |

This may seem like a lot of machinery. The rest of this chapter explains why each part exists.

### Step 1—Stage the incoming data

The first step is to load the latest batch of data into a staging table.

The staging table holds incoming data before the target table is touched. For `Sales.Order`, this table is `Sales.Order_staging`.

`Sales.Order_staging` may contain a full extract of the source data. It may also contain only a subset of recently changed records. The latter is an incremental extract.

An incremental extract can reduce the number of records to stage, check, and apply from hundreds of millions to a few thousand. The ways to do this reliably are covered in [Tracking changes](/docs/efficient-stable-pipeline/tracking-changes/) and [Responding to changes](/docs/efficient-stable-pipeline/responding-to-changes/).

The staging step applies regardless of full or incremental extract.

Suppose the current target table looks like this.

**Current `Sales.Order`**

| Order ID | Customer ID | Order reference | Order status | Order amount | Row insert datetime | Row update datetime |
|---|---|---|---|---:|---|---|
| O1001 | C001 | REF-1001 | Submitted | 120.00 | 2025-04-01 09:00 | 2025-04-01 09:00 |
| O1002 | C002 | REF-1002 | Submitted | 95.00 | 2025-04-01 09:05 | 2025-04-01 09:05 |
| O1003 | C003 | REF-1003 | Cancelled | 80.00 | 2025-04-01 09:10 | 2025-04-01 09:10 |

The incoming staging table may look like this.

**Incoming `Sales.Order_staging`**

| Order ID | Customer ID | Order reference | Order status | Order amount |
|---|---|---|---|---:|
| O1001 | C001 | REF-1001 | Submitted | 120.00 |
| O1002 | C002 | REF-1002 | Fulfilled | 95.00 |
| O1004 | C004 | REF-1004 | Submitted | 140.00 |
| O1005 |  | REF-1005 | Submitted | 75.00 |
| O1006 | C006 | REF-1003 | Submitted | 160.00 |

At this point, the target table has not yet changed. The incoming data is available for checking.

### Step 2—Check the incoming data

The Check step compares `Sales.Order_staging` against `Sales.Order` before loading data into the target.

The Check step asks three kinds of question:

| Check | Question |
|---|---|
| Genuine change | Which rows should be inserted, updated, or deleted? |
| Instability | Are there abnormally high numbers of inserts, updates, or deletes? |
| Violations | Are there rows that should be rejected rather than loaded? |

Checking for genuine changes is essential. Checking for instability is highly desirable. Checking for violations is a practical way to improve fault tolerance, because a small number of bad rows can be rejected while the rest of the table proceeds. 

The latter two are part of [fault tolerance](/docs/quality-reliability/fault-tolerance/).

#### Check for genuine changes

Not every row in `Sales.Order_staging` is a genuine change.

During a full extract, millions of rows may arrive, but only a small number may differ from the current target. During an incremental extract, the incoming rows may only be candidates for change. Some may still be identical to the current target.
The Check step identifies which rows genuinely need action by comparing rows on the primary key, then comparing non-key values for rows whose primary key already exists.

There are three possibilities:

| Change type | Meaning |
|---|---|
| Insert | A primary key exists in `Sales.Order_staging` but not in `Sales.Order`. |
| Update | A primary key exists in both tables, but one or more non-key values differ. |
| Delete | A primary key exists in `Sales.Order` but should no longer exist in the final target. |

In the example:

| Order ID | Interpretation |
|---|---|
| O1001 | Unchanged. |
| O1002 | Existing row with changed status, so it is an update. |
| O1003 | Missing from a full extract, so it is a delete. |
| O1004 | New row, so it is an insert. |
| O1005 | New row, so it is an insert, but `[Customer ID]` is missing. |
| O1006 | New row, so it is an insert, but its `[Order reference]` clashes with existing order `O1003`. |

Inserts and updates isolated into an upsert table.

The first version of the upsert table contains all rows that are new or genuinely changed. It also has a column `[Is new row]` to indicate whether the row is to be inserted or not.

**Example structure of `Sales.Order_upsert` before checking violations**

| Order ID | Customer ID | Order reference | Order status | Order amount | Is new row |
|---|---|---|---|---:|---|
| O1002 | C002 | REF-1002 | Fulfilled | 95.00 | false |
| O1004 | C004 | REF-1004 | Submitted | 140.00 | true |
| O1005 |  | REF-1005 | Submitted | 75.00 | true |
| O1006 | C006 | REF-1003 | Submitted | 160.00 | true |

`O1001` does not appear because it has not changed.

If `Sales.Order_staging` is a full extract, deletes can be identified by finding rows in `Sales.Order` whose primary key values no longer appear in `Sales.Order_staging`.

**Example structure of `Sales.Order_delete`**

| Order ID |
|---|
| O1003 |

If `Sales.Order_staging` is an incremental extract, delete detection must be tailored to the incremental logic. The staging table may contain only a fraction of the desired final table, so absence from staging does not necessarily mean deletion from the target.

This distinction is covered in [Responding to changes](/docs/efficient-stable-pipeline/responding-to-changes/).

#### Check for instability

Once `Sales.Order_upsert` and `Sales.Order_delete` have been calculated, the pipeline can check whether the proposed changes are abnormal.

These checks are stability thresholds.

A stability threshold does not prove that the proposed change is wrong. It says the proposed change is large enough to require attention before it is allowed to spread.

For example, suppose `Sales.Order` normally changes by a small percentage each day. If half the table is about to be updated or deleted, this may indicate a source-system issue, extraction error, or accidental change in load logic.

**Example stability check**

| Check | Existing rows | Proposed changed rows | Percentage changed | Action |
|---|---:|---:|---:|---|
| Upsert threshold | 100,000 | 2,500 | 2.5% | Proceed |
| Delete threshold | 100,000 | 45,000 | 45.0% | Abort and alert |

The threshold for deletes should usually be lower than the threshold for upserts. In many business processes, deletes are rarer than inserts or updates.

A simple default threshold can catch most serious abnormalities across a pipeline. Specific tables may need tailored thresholds based on their normal pattern of change.

Logging change statistics over time helps set these thresholds. If a table normally updates between 0.5% and 2% of rows each day, then a 20% update is worth investigating.

If a table frequently breaches its threshold, the data engineer should not simply increase the threshold until the alert disappears. The extraction logic, source behaviour, and business process should be understood. The alert may be exposing instability that should be fixed.

#### Check for violations

After genuine changes have been identified, the pipeline should check whether any rows in `Sales.Order_upsert` are unsafe to load.

A brittle load may fail the whole table. A fault-tolerant load can move the unsafe row from `Sales.Order_upsert` into `Sales.Order_reject`, then allow the remaining safe rows to proceed.

While the pipeline can contain tailored rules for each table, it is useful to check for two common violations: existence and uniqueness constraints.

For example, if `[Customer ID]` is required for `Sales.Order`, then an incoming order with a null `[Customer ID]` violates the existence expectation for the table.

Checking for uniqueness is more complex.

Suppose `Sales.Order` has a unique column `[Order reference]`. The pipeline needs to check two kinds of uniqueness violation.

First, the incoming rows may contain duplicates within the upsert set itself. This occurs when two rows in `Sales.Order_upsert` have the same `[Order reference]`.

Second, an incoming row may clash with an existing row in `Sales.Order`. This occurs when applying the upsert would create an `[Order reference]` that already exists on another row in the target table.

The second case must be checked carefully. It is not a violation if the incoming row is updating its own existing record and keeping the same `[Order reference]`. It is also not necessarily a violation if another row is changing away from that value in the same load. The question is whether the final target table would contain two rows with the same unique value after the upsert is applied.

These violations should be sent to a reject table.

**Example structure of `Sales.Order_reject`**

| Order ID | Customer ID | Order reference | Order status | Order amount | Rejection reason |
|---|---|---|---|---:|---|
| O1005 |  | REF-1005 | Submitted | 75.00 | Existence violation |
| O1006 | C006 | REF-1003 | Submitted | 160.00 | Uniqueness violation |

After rejection, `Sales.Order_upsert` contains only safe rows to apply.

**Example structure of `Sales.Order_upsert` after checking violations**

| Order ID | Customer ID | Order reference | Order status | Order amount | Is new row |
|---|---|---|---|---:|---|
| O1002 | C002 | REF-1002 | Fulfilled | 95.00 | false |
| O1004 | C004 | REF-1004 | Submitted | 140.00 | true |

The table is now safe to load.

### Step 3—Apply the changes

After the Check step, the pipeline has separated incoming data into the actions it needs to take:

| Artefact | Action |
|---|---|
| `Sales.Order_upsert` | Insert new rows and update changed rows. |
| `Sales.Order_delete` | Remove rows that should no longer be current. |
| `Sales.Order_reject` | Preserve unsafe rows for attention, without loading them into the target. |

The Apply step updates the target table in a controlled way.

First, rows marked for deletion should be removed from the current target. But they should not simply disappear. Their previous values should be preserved in `Sales.Order_history`. This is not merely for archival purposes, but to inform downstream processes which rows have been deleted, so they can respon accordingly.

Second, rows in `Sales.Order_upsert` where `[Is new row] = false` should be used to update existing rows in the target. Again, the previous values should be preserved in `Sales.Order_history`.

Third, rows in `Sales.Order_upsert` where `[Is new row] = true` should be inserted into the target.


The Apply step should also manage architectural columns for change datetimes:

| Column | Meaning |
|---|---|
| `[Row insert datetime]` | When the row, defined by its primary key, first entered the target table. |
| `[Row update datetime]` | When the row, defined by its primary key, was most recently updated with a genuine change. |
| `[Row delete datetime]` | When the row stopped being current. Current rows use `9999-12-31 00:00:00` to indicate that they have not been deleted. |

Because the Check step removed unchanged rows, `[Row update datetime]` is updated only when row content genuinely changes.

As we will see in the later chapter [Tracking changes](/docs/efficient-stable-pipeline/tracking-changes/), these artefacts are necessary for downstream processing. 

After applying the change, the target may look like this.

**Updated `Sales.Order`**

| Order ID | Customer ID | Order reference | Order status | Order amount | Row insert datetime | Row update datetime | Row delete datetime |
|---|---|---|---|---:|---|---|---|
| O1001 | C001 | REF-1001 | Submitted | 120.00 | 2025-04-01 09:00 | 2025-04-01 09:00 | 9999-12-31 00:00:00 |
| O1002 | C002 | REF-1002 | Fulfilled | 95.00 | 2025-04-01 09:05 | 2025-05-01 08:00 | 9999-12-31 00:00:00 |
| O1004 | C004 | REF-1004 | Submitted | 140.00 | 2025-05-01 08:00 | 2025-05-01 08:00 | 9999-12-31 00:00:00 |


`O1001` remains unchanged. `O1002` has been updated. `O1003` has been deleted from the current table. `O1004` has been inserted. `O1005` has been rejected because `[Customer ID]` is missing. `O1006` has been rejected because its `[Order reference]` clashes with an existing target row.

The history table preserves previous versions of updated and deleted rows.


**Example structure of `Sales.Order_history`**

| Order ID | Customer ID | Order reference | Order status | Order amount | Row insert datetime | Row update datetime | Row delete datetime |
|---|---|---|---|---:|---|---|---|
| O1002 | C002 | REF-1002 | Submitted | 95.00 | 2025-04-01 09:05 | 2025-04-01 09:05 | 2025-05-01 08:00 |
| O1003 | C003 | REF-1003 | Cancelled | 80.00 | 2025-04-01 09:10 | 2025-04-01 09:10 | 2025-05-01 08:00 |


## After the load

The loading process finishes with cleaning up temporary artefacts and logging what happened.

### Clean up temporary artefacts

If there are no errors, temporary tables such as `Sales.Order_staging`, `Sales.Order_upsert`, and `Sales.Order_delete` do not usually need to be retained.

`Sales.Order_history` may also be purged after a suitable period, once downstream tables have had time to respond to updates and deletes. In Delta table contexts, purging old removed rows is often known as vacuuming.

If there are errors, temporary artefacts and `Sales.Order_reject` may need to be retained for troubleshooting.

These artefacts should be secured in the same way as the target table. Temporary load tables can contain the same sensitive information as the production table. They should not become a source of unintended data leakage.

### Log, bookmarks and change statistics

The pipeline should log enough information to explain what happened during each load.

At minimum, the log should record whether the load succeeded, failed, or was aborted, along with any associated failure message.

**Example structure of `Pipeline.LoadLog`**

| Load ID | Table name | Load start datetime | Load end datetime | Load status | Failure message |
|---:|---|---|---|---|---|
| 10001 | Sales.Order | 2025-05-01 08:00 | 2025-05-01 08:03 | Succeeded |  |
| 10002 | Sales.Customer | 2025-05-01 08:03 | 2025-05-01 08:05 | Succeeded |  |
| 10003 | Sales.Payment | 2025-05-01 08:05 | 2025-05-01 08:06 | Failed | Source extract timeout |
| 10004 | Sales.Product | 2025-05-01 08:06 | 2025-05-01 08:06 | Aborted | Delete threshold exceeded |

For incremental processing, the pipeline should also log the table’s refresh bookmark.

A refresh bookmark records when the table started reading from its source data, if the load completed successfully. Suppose `Sales.Order` draws from several source tables. Any source records that appear after the bookmark belong to a later load.

This bookmark gives the next load a safe starting point for incremental extraction. This is explained in greater detail in [Tracking changes](/docs/efficient-stable-pipeline/tracking-changes/).

The refresh bookmark should only be advanced when the load succeeds. If the load fails or aborts, the bookmark should not move forward, because the next load still needs to consider the same source period.

**Example structure of `Pipeline.RefreshBookmark`**

| Table name | Load ID | Refresh bookmark datetime |
|---|---:|---|
| Sales.Order | 10001 | 2025-05-01 08:00 |
| Sales.Customer | 10002 | 2025-05-01 08:03 |

In this example, `Sales.Order` completed successfully, so its bookmark is set to `2025-05-01 08:00`. `Sales.Payment` failed, so no bookmark is recorded. `Sales.Product` was aborted by a stability threshold, so its bookmark is also not advanced.

The Check step also calculates useful change statistics. Since these statistics have already been calculated as part of the load, they are worth logging.

**Example structure of `Pipeline.LoadStatistics`**

| Load ID | Rows staged | Rows inserted | Rows updated | Rows deleted | Rows rejected | Target row count |
|---:|---:|---:|---:|---:|---:|---:|
| 10001 | 5 | 1 | 1 | 1 | 2 | 3 |
| 10002 | 1,250 | 12 | 34 | 0 | 0 | 42,810 |

The change statistics should normally be logged only for successful loads. For failed or aborted loads, the failure is recorded in `Pipeline.LoadLog`, but the bookmark and final change statistics are not advanced.

Over time, these logs form a history of how each table behaves.

That history is valuable for troubleshooting, setting stability thresholds, capacity planning, and understanding whether a table’s behaviour has changed. For example, if `Sales.Order` normally updates between 1% and 3% of rows each day, a load that updates 40% of rows is immediately suspicious. Without change statistics, the pipeline has no memory of what normal looks like.


## Is the extra work worth it?

At first glance, the three-step load pattern looks like overhead.

For one target table, the pattern may create several temporary or supporting artefacts: staging, upsert, delete, reject, and history tables. It also creates architectural columns such as `[Row insert datetime]`, `[Row update datetime]`, and `[Row delete datetime]`. The logic is much more complex than dropping a table and replacing it.

In a small environment, this may be unnecessary. If there are few tables, little downstream dependency, and low business risk, a simpler approach may be enough.

But as the pipeline grows, the calculation changes.


The extra work is necessary because the warehouse needs to know and control every change that happens within it. Each artefact preserves a distinction that the warehouse needs in order to achieve this.

| Artefact | Why it matters |
|---|---|
| `Sales.Order_staging` | Holds incoming data separately so the target is not touched until the batch has been checked. |
| `Sales.Order_upsert` | Identifies candidate inserts and updates before they are applied, allowing the pipeline to separate genuine changes from unchanged rows. |
| `Sales.Order_delete` | Identifies candidate deletes before they are applied, allowing the pipeline to check whether the volume of deletion is safe before rows are removed from the current target. |
| `Sales.Order_reject` | Isolates unsafe changed rows so they can be reported and remediated without contaminating the target or stopping safe rows from loading. |
| `Sales.Order_history` | Preserves previous versions of updated and deleted rows. This is not merely archival: downstream tables need history to know that a row changed or stopped being current. |
| Row change datetimes | Allow downstream incremental processing to respond precisely to inserts, updates, and deletes. |
| `Pipeline.LoadLog` | Records success, failure, aborts, and error messages, so the pipeline can be troubleshot and audited. |
| `Pipeline.RefreshBookmark` | Records where the next incremental load should restart, but only after a successful load. |
| `Pipeline.LoadStatistics` | Builds a history of how each table changes over time, supporting stability thresholds, capacity planning, and diagnosis of abnormal behaviour. |

This is the price of controlled change.

Without these artefacts, the warehouse may still produce a current-looking table, but it cannot explain how that table changed. It cannot reliably tell downstream processes which rows require action. It cannot distinguish genuine change from noisy candidate change. It cannot isolate unsafe rows and report on errors. It cannot remember what happened during the load.

The value of the pattern grows with scale. On one table, the extra machinery may seem excessive. Across a serious pipeline, it becomes the backbone of efficiency, stability, and fault tolerance.

Investment in automation or appropriate technology ensures that this logic can be applied by default, without requiring the data engineer to handcraft every part for every table.

> [!NOTE]
> **Key ideas**
>
> A mature load applies only genuine changes, after checking that they are safe.
>
> Drop-and-replace loading is simple, but it hides genuine change, creates instability, and magnifies failure.
>
> The standard load pattern is stage, check, and apply.
>
> Staging tables hold incoming data before the target table is touched.
>
> Upsert, delete, and reject tables separate genuine changes from unsafe rows.
>
> History tables preserve previous versions of updated and deleted rows for downstream processing.
>
> Row change datetimes allow downstream tables to respond precisely to inserts, updates, and deletes.
>
> Load logging records bookmarks, change statistics, and success or failure so the pipeline can explain what happened.