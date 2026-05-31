---
title: Fault tolerance
url: /docs/quality-reliability/fault-tolerance/
description: Explains how fault-tolerant pipelines contain record, table, and load failures before they spread through the data product.
lede: Good engineering contains errors before they spread through the pipeline.
weight: 5
# draft: true
---
## Containing failure

Good engineering contains failure before it spreads.

A brittle pipeline treats every error as catastrophic. A fault-tolerant pipeline distinguishes between errors that should stop everything, errors that should stop one table, and errors that should be isolated to a small set of records.

The goal is not to ignore errors. The goal is to keep the rest of the data product usable while surfacing failure clearly.

On the other hand, surfacing failure is not the same as producing endless alerts.

If the same warning appears every day and no one knows what to do with it, the warning becomes background noise rather than a warning.

This is the cry-wolf problem of monitoring. Repeated, unactionable alerts train people to ignore the pipeline.

For this reason, fault tolerance requires judgement. Some errors should abort a load. Some occasional errors should be isolated into reject tables while the rest of the pipeline proceeds. Some recurring errors should be given targeted handling so that the pipeline explicitly represents the known issue rather than repeatedly rediscovering it.

This is fault tolerance.

Fault tolerance is therefore an extension of the third principle of data engineering: anticipate errors.

This chapter introduces three common fault patterns:

| Fault pattern | Core question | Example failure |
|---|---|---|
| Uniqueness | Does one real-world entity correspond to the right number of records? | Duplicate submissions, duplicated incremental loads, or two people sharing one identifier. |
| Existence | Are required records and values present where they should be? | A detail row without a header, a missing sales amount, or a deleted source record not removed downstream. |
| Stability | Are small real-world changes producing proportionate data-world changes? | One source update timestamp causes every historical row to reload. |

These patterns illustrate the mindset of building a fault-tolerant pipeline.

## Uniqueness

Uniqueness faults occur when the relationship between real-world entities and database records breaks down.

If the basic task of data engineering is to represent real-world objects and processes in the data world, then uniqueness is one of the most fundamental expectations.

In the simplest case, one real-world entity should correspond to one database record.

Uniqueness is violated when one real-world entity appears as multiple database records. For example, a staff member may accidentally enter the same transaction twice.

The reverse can also occur. Two distinct real-world entities may be forced to occupy the same database record. For example, if staff are identified only by first and last name, two staff members with the same name may collapse into one identifier value.

Uniqueness violations can arise from business process failures, such as duplicate entry. They can also arise from mechanical failures, such as incremental load logic incorrectly loading the same record twice.

The data engineer must express uniqueness expectations in the warehouse. While they may be implemented as technical constraints, they are better understood as statements of business intent.

If the constraint is violated, the pipeline has several possible responses:

| Response | Use when... |
|---|---|
| Abort the load | The violation suggests the table is unsafe to publish. |
| Reject the violating records | The invalid records can be isolated while the rest of the table remains usable. |
| Deduplicate automatically | The business rule for choosing the accepted record is clear and safe. |

For example, a source table may contain duplicate submissions.

**Example structure before deduplication**

| Submission ID | Customer ID | Submission date | Submission amount |
|---|---|---|---:|
| S1001 | C001 | 2025-04-01 | 120.00 |
| S1002 | C002 | 2025-04-01 | 95.00 |
| S1003 | C001 | 2025-04-01 | 120.00 |
| S1004 | C003 | 2025-04-02 | 80.00 |

If the business expects one submission per customer per date, the duplicate can be separated from the main analytical output.

**Example structure of accepted records**

| Submission ID | Customer ID | Submission date | Submission amount |
|---|---|---|---:|
| S1001 | C001 | 2025-04-01 | 120.00 |
| S1002 | C002 | 2025-04-01 | 95.00 |
| S1004 | C003 | 2025-04-02 | 80.00 |

**Example structure of rejected records**

| Submission ID | Customer ID | Submission date | Submission amount | Rejection reason |
|---|---|---|---:|---|
| S1003 | C001 | 2025-04-01 | 120.00 | Duplicate customer submission for date |

The accepted records remain available for users. The duplicate record is not silently lost but surfaced for attention. This approach localises the fault.

If uniqueness violations are rare, a reject-record pattern may be sufficient. If violations are frequent, the table needs targeted handling. Repeated alerts can create a cry-wolf effect, dulling attention and undermining the purpose of monitoring.

In such cases, the data engineer should implement a specific treatment for the table. This may include deterministic deduplication, a remediation workflow, or a data quality report.

## Existence

Existence faults occur when required records or values are missing, or when records remain in the data world after their real-world counterpart has disappeared.

Existence is violated when a real-world entity exists but does not appear in the database. For example, a completed sale may be missing its sales amount.

Existence is also violated when a database record exists but the real-world entity no longer does. For example, a record may fail to be deleted during an incremental load.

Some existence expectations are simple. A completed sales record must have a sales amount. This can be expressed through a not-null constraint.

**Example structure of `'Sales'` with missing value**

| Sales ID | Sales date | Customer ID | Sales amount |
|---|---|---|---:|
| S1001 | 2025-04-01 | C001 | 120.00 |
| S1002 | 2025-04-02 | C002 |  |
| S1003 | 2025-04-03 | C003 | 95.00 |

If `[Sales amount]` is required for completed sales, then the missing value should be treated as a fault. Depending on the use case, the row may be rejected, flagged, or excluded from measures that require a sales amount.

More complex existence faults occur between related tables.

For example, a sales item should not exist without a corresponding sales header.

**Example structure of `Sales.Sales`**

| Sales ID | Sales date | Customer ID |
|---|---|---|
| S1001 | 2025-04-01 | C001 |
| S1002 | 2025-04-02 | C002 |

**Example structure of `Sales.SalesItems`**

| Sales item ID | Sales ID | Product ID | Quantity |
|---|---|---|---:|
| SI001 | S1001 | P100 | 1 |
| SI002 | S1001 | P200 | 2 |
| SI003 | S999 | P300 | 1 |

In this example, `SI003` refers to `S999`, but the sales header does not exist.

This may occur because the header failed to load, the item arrived earlier than the header, or the source system produced an invalid relationship.

The data engineer can detect this by left-joining the detail table to the header table, then checking whether the header key is missing.

Conceptually, the check looks like this.

**Example structure after checking for header existence**

| Sales item ID | Sales ID | Product ID | Quantity | Header sales ID |
|---|---|---|---:|---|
| SI001 | S1001 | P100 | 1 | S1001 |
| SI002 | S1001 | P200 | 2 | S1001 |
| SI003 | S999 | P300 | 1 |  |

The existence expectation can then be expressed as a not-null requirement on `[Header sales ID]`. If `[Header sales ID]` is blank, the detail row has no corresponding header.

When the not-null check fails, the pipeline can send the violating rows into a reject table and allow the rest of the detail table to proceed.

**Example structure of accepted sales items**

| Sales item ID | Sales ID | Product ID | Quantity |
|---|---|---|---:|
| SI001 | S1001 | P100 | 1 |
| SI002 | S1001 | P200 | 2 |

**Example structure of rejected sales items**

| Sales item ID | Sales ID | Product ID | Quantity | Rejection reason |
|---|---|---|---:|---|
| SI003 | S999 | P300 | 1 | Missing sales header |

The rest of the table can continue to load, while the missing relationship is surfaced.

This is the same pattern as uniqueness handling: detect the violation, isolate the unsafe rows, preserve them for attention, and allow the safe records to continue.

Existence faults are especially important in batch and incremental pipelines. Tables may be extracted at different times. A header may arrive in one batch and detail records in another. In traditional warehousing this is often discussed as late-arriving data.

The data engineer should not assume that every related record will always arrive in the expected order.

For existence, the best mindset is to design the pipeline as if it were streaming.

Even in a batch pipeline, this is a useful design mindset:

- tables may load continuously, or at least several times a day;
- some tables may fail to load from time to time;
- related records may arrive out of order;
- records may catch up in a later batch.

In this mindset, temporary existence violations are expected. The pipeline should handle them safely.

However, safe handling must not become silent handling.

If a missing header catches up in the next batch, the issue may resolve. If it does not catch up, tests or monitored assumptions should surface the prolonged discrepancy.

## Stability

Stability faults occur when small real-world changes produce disproportionate changes in the data world.

A stable pipeline changes in proportion to the world it represents.

If ten sales changed in the source system, the pipeline should not update ten million downstream records. If one reference value changed, half the warehouse should not change as a side effect.

Stability means that ordinary changes should produce ordinary effects.

This is important because the real world rarely rewrites all historical records at once. But the data world can suffer from massive accidental changes that do not correspond to real-world change.

For example, a source system update may refresh `[Row update datetime]` for every historical row. If the pipeline relies on `[Row update datetime]` for incremental extraction, it may attempt to reload the entire history.

Another example is a non-deterministic ranking. If a row number is assigned using an incomplete sort order, the selected “first” row may change between runs even when the underlying data has not changed.

A third example is a reporting column such as `[Today’s date]`. If this is stored on every row, every row changes every day even though the underlying business entity has not changed.

The data engineer should therefore design pipelines so that changes are commensurate with real-world change.

One way to do this is to avoid unstable elements:

| Unstable element | Why it is risky |
|---|---|
| `[Today’s date]` stored on every row | Causes every row to change every day. |
| Non-deterministic ranking | Causes rows to change between runs without real-world change. |
| Incomplete tie-breaking logic | Makes selected records unstable. |
| Overwritten single-row control tables | Causes downstream volatility when append-only history would be safer. |
| Wide miscellaneous tables | Amplifies small changes because unrelated attributes share one row. |

Another way is to use stability thresholds.

For example, the pipeline may abort or quarantine a table load if more than 5% of records are about to be deleted.

**Example stability threshold**

| Table | Existing rows | Rows proposed for deletion | Deletion percentage | Action |
|---|---:|---:|---:|---|
| `Sales.Sales` | 1,000,000 | 2,500 | 0.25% | Proceed |
| `Sales.Customer` | 250,000 | 180,000 | 72.00% | Abort and alert |

The threshold does not imply that the change is wrong. It says the proposed change is large enough to require attention before it is allowed to spread.

One important habit is to avoid wide tables with miscellaneous attributes. In a wide table, a change in any cell can cause the whole row to update. This amplifies small real-world changes into broad database changes.

Narrow meaningful fragments are more stable. When each table has a clear informational purpose, changes to that table correspond more closely to changes in the thing it represents.

Another habit is to manage dependencies carefully. Small reference tables can have large downstream effects. If a country reference table fails to load, and downstream transformations depend on it early in the pipeline, country data may disappear across many products.

These design habits are developed further in [Load mechanics](/docs/efficient-stable-pipeline/load-mechanics/) and [Load dependencies](/docs/efficient-stable-pipeline/load-dependencies/).

## Conclusion

Uniqueness, existence, and stability are three common fault patterns. But the possibilities of error are limitless. Parallel loads may deadlock. Source systems may change without notice. Files may arrive late.  Users may enter unexpected values.

It is not useful to enumerate every possible fault.

The important thing is the mindset: anticipating errors.

The experienced data engineer designs for what the world might do to the pipeline, not only what the pipeline does to the data.

## Key ideas

> [!NOTE]
> **Key ideas**
>
> Fault tolerance is the discipline of containing failure.
>
> Good engineering contains errors before they spread through the pipeline.
>
> A fault-tolerant pipeline distinguishes between errors that should stop everything, errors that should stop one table, and errors that should be isolated to a small set of records.
>
> Uniqueness faults occur when the relationship between real-world entities and database records breaks down.
>
> Existence faults occur when required records or values are missing, or when records remain after their real-world counterpart has disappeared.
>
> Stability faults occur when small real-world changes produce disproportionate changes in the data world.
>
> Not every error is fatal, but none should pass silently.