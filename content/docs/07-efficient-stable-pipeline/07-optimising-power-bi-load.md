---
title: Optimising Power BI load
url: /docs/efficient-stable-pipeline/optimising-power-bi-load/
description: Explains practical ways to improve Power BI refresh performance through source design, partitions, and incremental load patterns.
lede: Power BI load is the final expression of pipeline design.
weight: 7
# draft: true
---

## Power BI as the final load boundary

Loading a Power BI model is often one of the longest steps in the delivery of a data product. This is particularly true for models with large fact tables.

New technologies such as DirectLake promise to remove traditional import refresh in some scenarios. Even so, Import mode remains one of the most reliable ways to deliver a fast and responsive user experience.

When refreshing Power BI, the core idea is:

> Power BI should assemble information, not manufacture it.

This is why Power BI performance depends on decisions made far earlier in the pipeline. If upstream data has been shaped into meaningful fragments, if change has been tracked carefully, and if downstream tables respond proportionately to change, then Power BI can load efficiently. If those things have not been done, Power BI refresh becomes the place where all upstream disorder is paid for.

Thus, Power BI load is not merely a Power BI problem, but is the final expression of pipeline design.

There are three main ways to optimise Power BI loads:

- avoiding load with DirectQuery;
- using efficient underlying source tables;
- partitioning the model, with further enhancements through rolling windows and incremental refresh.

This chapter assumes the model sources data from SQL, where purpose-built views or tables act as source tables that map one-to-one with the Power BI model tables.

## Avoiding load with DirectQuery

DirectQuery for fact tables avoids the load entirely by sending DAX queries to the source at report time. To provide a responsive experience, the underlying source table often needs to be materialised as a columnstore table dedicated to this purpose. While materialising a large fact table is costly, it can also be incrementally loaded so that refresh remains minimal.

By using DirectQuery over an incrementally loaded columnstore table, the pipeline can achieve high efficiency in terms of information movement. The Power BI model does not need to import the fact table because the source table is queried directly.

However, DirectQuery has serious drawbacks for user experience:

- DAX queries become noticeably slower.
- Some complex DAX expressions are not supported.
- Certain DAX functions behave differently in Import mode and DirectQuery mode.
- Power BI limits how many rows can be retrieved in DirectQuery for certain operations, which restricts what reports can be built.
- Dimension values can appear blank in filter lists even when the table does not actually contain blanks.

DirectQuery works best when:

- the table is far longer than it is wide, so queries touch fewer attributes;
- queries against the table are simple, such as sums, counts, minimums, and maximums that work well against columnstore tables;
- users are not expected to browse unit records and do not hit Power BI’s retrieval limits.

Where dimensions are shared by both Import and DirectQuery facts, dual mode must be implemented. Dual mode keeps a copy of the dimension for Import while still allowing the engine to query it in DirectQuery when needed. This ensures relationships remain fast for Import facts and correct for DirectQuery facts.

DirectQuery can be powerful, but it is not a universal escape from model refresh. It shifts work from refresh time to query time. If the source is not designed for this workload, the user experiences the cost directly.

## Efficient underlying source tables

One of the biggest factors influencing Power BI load times is the efficiency of the underlying source tables, which are often implemented as views. A source view should be a straightforward join of ready-to-use tables that have been indexed appropriately to support high-performance execution.

The views may have simple logic such as:

- looking up surrogate keys to replace composite primary keys;
- backfilling null values with defaults;
- adding on-demand columns, such as `[Days expired since creation]` using functions like `getdate()`.

However, heavy transformations such as windowing, nested logic, and complex aggregation should be avoided. These belong upstream in curated layers where they can be tested, reused, and incrementally refreshed.

String aggregation for display should also be avoided where possible, as this can often be handled with appropriate DAX measures, as explained in [Designing measures](/docs/presenting-insights/designing-measures/).

The ideal case is to create fragments that are both meaningful and effective for loading into the Power BI model. If a source table still requires elaborate logic to stitch pieces together, the issue is not merely SQL tuning. The deeper issue is that upstream fragments have not been adequately prepared. 

Materialisation of the view is sometimes necessary to ensure the source table loads rapidly. This is especially true when data needs to be rearranged to support fast retrieval of load partitions against the partition key.

In short:

> Power BI source views or tables should be tuned specifically for fast retrieval, not burdened with complex logic.

## Partitioning the model

Defining a table into partitions is the most effective way to reduce Power BI load times when fact tables grow large.

Partitioning a table offers increasing levels of enhancement that can be adopted as the situation requires:

1. load partitions in parallel;
2. apply a rolling window to drop older partitions;
3. incrementally refresh only the partitions that changed.

### Analogy for partitions

Partitions are akin to having a large box of books from multiple publishing years. Batches of books arrive at regular intervals, and the box needs to be updated with the incoming batch. There can be new books, and old books can be updated. Updating the whole box can take a long time if the number of books is huge.

Splitting the books into boxes by publishing year allows a divide-and-conquer approach. Each year’s box can be updated separately. This is the first benefit of partitioning: partitions can be loaded in parallel.

If boxes of books that are too old become unnecessary, they do not need to be kept. The oldest boxes can be dropped. This is the second benefit of partitioning: a rolling window can keep the model from growing indefinitely.

Finally, if the incoming books can be sorted by year, and only some years have new or updated books, then only those boxes need updating. It may take additional effort to track which years changed, but this effort can dramatically reduce total refresh time. This is the third benefit of partitioning: incremental refresh can refresh only the partitions that changed.

Each step is increasingly sophisticated, and corresponds to a deeper level of gain from partitioning Power BI tables.

### Parallel partition refresh

A partition key is a business date or datetime column that divides the data into intervals such as daily, monthly, or yearly. Power BI can load these partitions in parallel.

Depending on the degree of parallelism, this can lead to large improvements in load time with little effort.

To make partitions effective, the source must return a single partition quickly. If the underlying view is complex, the solution is not to push SQL harder but to move complexity upstream and materialise the result with an index on the partition key. This ensures that Power BI can request “give me this month” and receive the data quickly.

Continuing the analogy, the incoming batches of books must be readily accessible by publishing year. If not, it may take longer to fetch each year’s books than the time gained from divide-and-conquer. The optimal solution is to organise the incoming batches by publishing year. In SQL terms, this means storing the source data so it can be efficiently retrieved by the partition key used to define the Power BI partition.

There is a trade-off between load time and query time. Splitting one big box of books into multiple boxes by publishing year increases the total number of objects that need to be managed. Too many small partitions can create overhead. Too few large partitions can reduce the benefit of parallelism. The choice of interval size—year, month, day, or hour—depends on the volume of data, refresh frequency, and query behaviour.

When partitioning, new developers often confuse which date to use. The partition key must be a business date rather than a change-tracking column such as `[Row update datetime]`. Using the same column for partitioning and change detection pushes rows toward the end of the range and breaks the logic. Following the analogy, the date should be the publishing year rather than the year the book arrived in a batch. The latter will always be in the last batch and does not correctly update older books.

### Rolling windows

When partitions are in place, rolling windows provide the next level of efficiency. Power BI allows a data engineer to define the number of partitions to keep, and older partitions are dropped from the model. This keeps the model size under control and prevents refresh times from growing indefinitely.

Boundary points in the window are error-prone. Two details deserve attention.

First, if the SQL source table itself rolls history, its window must be kept in sync with the Power BI table’s rolling window to avoid mismatches.

Second, the boundaries of fact tables must match related dimensions and other facts. This is particularly true for ID dimensions, which may contain keys only because related fact rows still exist. If dimensions are not kept in sync, they may contain primary key values that no longer exist in the fact tables. If a dimension drops keys too aggressively, relationships may break for facts that still remain.

### Incremental partition refresh

Incremental refresh adds change detection on top of partitions so only partitions with changes are refreshed.

The native Power BI interface allows the data engineer to choose a datetime column in the table for change detection. During refresh, Power BI evaluates the maximum value of that column for each partition. This is the polling query. Power BI manages the partition refresh bookmarks internally. Each partition stores the polling value that was observed when that partition was last refreshed successfully.

If the next polling query returns a different value from the value stored internally against the partition, Power BI refreshes that partition. After the partition refresh succeeds, Power BI stores the new polling value as the partition’s bookmark.

Following the analogy, each box of books by publishing year has a label showing the last update datetime observed for that box. This is the bookmark. When batches of books arrive, each year can be checked to see whether any book has an update datetime greater than the label on the box. This is the polling query. This is effective only if incoming batches are organised so that it is easy to find the maximum update datetime for each publishing year.


### Custom polling tables

The native approach offered by Power BI can be limited if the source table is a view that joins multiple tables, and thus there is no single column representing change detection.

It is also not sufficient if partitions have deletes because a normal update datetime cannot reflect delete datetimes. When the native approach is not sufficient, the user can specify a custom polling query with arbitrary M code through XMLA-based configuration.

Polling tables can facilitate rapid evaluation of a polling query for complex cases. A polling table is simply a list of partition values and the datetime the partition was last updated. During refresh, the polling query looks up this update datetime for a partition.

Following the analogy, the incoming batches of books may have a companion spreadsheet that tracks publishing years and the latest update datetime of books for that year. During updates, this spreadsheet is consulted to decide whether that year’s box needs updating.

Power BI does not support custom polling queries in its normal interface. XMLA-based configuration is required.

If Power BI can rapidly evaluate whether a partition needs refreshing and retrieve the data for that partition quickly from the source table, this can lead to substantial improvements in load times. Supporting this requires the data engineer to prepare the data through indexing, sorting, materialising source tables, or constructing dedicated polling tables.

This preparation itself takes time, and any base tables or polling tables should themselves be incrementally refreshed. Consequently, optimising Power BI loads means trading Power BI load time for source-side preparation time. If not done well, these artefacts can take longer to maintain than the time saved through incremental partition refresh.

### Example refresh bookmarks and polling values

Suppose `PBI.Sale` is partitioned monthly using `[Sale date]`.

The source table contains sales across several months. Each row also has a `[Row update datetime]`, which records when that row was last inserted or updated in the pipeline.

**Source table: `PBI.Sale`**

| Sale ID | Sale date | Customer ID | Amount | Row update datetime |
|---|---|---|---:|---|
| S1001 | 2025-01-05 | C001 | 120.00 | 2026-05-01 09:15 |
| S1002 | 2025-01-19 | C002 | 85.00 | 2026-05-03 14:20 |
| S1003 | 2025-01-28 | C003 | 64.00 | 2026-05-03 16:45 |
| S2001 | 2025-02-03 | C004 | 230.00 | 2026-05-02 10:30 |
| S2002 | 2025-02-14 | C005 | 75.00 | 2026-05-09 08:40 |
| S2003 | 2025-02-24 | C006 | 310.00 | 2026-05-09 11:10 |
| S3001 | 2025-03-08 | C007 | 50.00 | 2026-05-04 12:00 |
| S3002 | 2025-03-18 | C008 | 140.00 | 2026-05-04 15:30 |
| S3003 | 2025-03-29 | C009 | 95.00 | 2026-05-04 18:05 |

The Power BI partitions are done per month on `[Sale date]`.

| Partition start of month | Partition filter | Rows |
|---|---|---|
| 2025-01 | `[Sale date] >= 2025-01-01 and [Sale date] < 2025-02-01` | S1001, S1002, S1003 |
| 2025-02 | `[Sale date] >= 2025-02-01 and [Sale date] < 2025-03-01` | S2001, S2002, S2003 |
| 2025-03 | `[Sale date] >= 2025-03-01 and [Sale date] < 2025-04-01` | S3001, S3002, S3003 |

`PBI.SalePolling` is a companion table to `PBI.Sale`. It contains one row per partition and stores the maximum `[Row update datetime]` found inside that partition.

**Companion polling table: `PBI.SalePolling`**

| Partition | Latest update datetime |
|---|---|
| 2025-01 | 2026-05-03 16:45 |
| 2025-02 | 2026-05-09 11:10 |
| 2025-03 | 2026-05-04 18:05 |

The values in `PBI.SalePolling` correspond to the maximum row update datetime in each partition.

| Partition | Row update datetimes in `PBI.Sale` | Latest update datetime in `PBI.SalePolling` |
|---|---|---|
| 2025-01 | 2026-05-01 09:15; 2026-05-03 14:20; 2026-05-03 16:45 | 2026-05-03 16:45 |
| 2025-02 | 2026-05-02 10:30; 2026-05-09 08:40; 2026-05-09 11:10 | 2026-05-09 11:10 |
| 2025-03 | 2026-05-04 12:00; 2026-05-04 15:30; 2026-05-04 18:05 | 2026-05-04 18:05 |

Each Power BI partition also has a stored refresh bookmark. This bookmark records the latest polling value observed when that partition was last refreshed successfully. Power BI manages these partition bookmarks internally.

**Power BI partition bookmarks before refresh**

| Partition | Stored refresh bookmark |
|---|---|
| 2025-01 | 2026-05-03 16:45 |
| 2025-02 | 2026-05-02 10:30 |
| 2025-03 | 2026-05-04 18:05 |

During refresh, Power BI compares the stored refresh bookmark for each partition against the current polling value from `PBI.SalePolling`.

| Partition | Stored refresh bookmark | Latest update datetime | Changed? | Action |
|---|---|---|---|---|
| 2025-01 | 2026-05-03 16:45 | 2026-05-03 16:45 | No | Do not refresh |
| 2025-02 | 2026-05-02 10:30 | 2026-05-09 11:10 | Yes | Refresh partition |
| 2025-03 | 2026-05-04 18:05 | 2026-05-04 18:05 | No | Do not refresh |

Only the `2025-02` partition needs to refresh.

The refresh then proceeds in steps.

### Step 1—Poll each partition

Power BI checks the current polling value for each partition.

Conceptually, the polling query asks:

```sql
select
    [Latest update datetime]
from PBI.SalePolling
where [Partition] = '2025-02';
```

For `2025-02`, the polling query returns `2026-05-09 11:10`.

### Step 2—Compare polling value with stored bookmark

The stored refresh bookmark for `2025-02` is `2026-05-02 10:30`.

Because the polling value is different, Power BI marks the partition for refresh.

### Step 3—Refresh only the changed partition

Power BI reloads only the rows belonging to the changed partition.

Conceptually, the partition query is:

```sql
select
    *
from PBI.Sale
where [Sale date] >= '2025-02-01'
  and [Sale date] <  '2025-03-01';
```

The partition key is `[Sale date]`, not `[Row update datetime]`.

`[Sale date]` decides which partition the row belongs to. `[Row update datetime]` decides whether that partition has changed.

### Step 4—Store the new bookmark

After the `2025-02` partition refreshes successfully, Power BI stores the new polling value as the partition’s refresh bookmark.

**Power BI partition bookmarks after refresh**

| Partition | Stored refresh bookmark |
|---|---|
| 2025-01 | 2026-05-03 16:45 |
| 2025-02 | 2026-05-09 11:10 |
| 2025-03 | 2026-05-04 18:05 |

The next refresh repeats the same process. If the polling value for `2025-02` remains `2026-05-09 11:10`, the partition does not need to refresh again.


## Conclusion

Loading a Power BI model is time intensive. Using DirectQuery over a columnstore table can avoid the load entirely, but DirectQuery imposes serious limits on the queries that can be made. Consequently, the most common factor for a fast Power BI load is the efficiency of the underlying source tables. These should be simple assemblies of well-defined fragments that join easily and avoid complex transformations.

When fact tables become substantial, partitions can deliver a major speed boost by enabling parallel loads. This often requires rearranging data or implementing dedicated indexes to support retrieval by partition date.

When partitions are in place, rolling windows provide further benefit by dropping older partitions and keeping model size controlled. This introduces room for error and requires attention to detail at boundary points.

Incremental refresh adds another layer of efficiency by refreshing only the partitions that have changed. This relies on a polling query to detect changes. Dedicated polling tables can support instant evaluation of polling queries, including complex cases where change detection cannot be represented by one column in the source table.

Whatever the technique, the foundation for a fast-loading Power BI model is set far in advance in the pipeline. It depends on the availability of meaningful fragments to avoid complex transforms, the planned placement of indexes to support partition keys, and the careful tracking of row changes to enable polling tables.

In the ideal case, information efficiency is maximised end to end:

1. raw tables enter the pipeline incrementally, using polling tables to track changes and annotating rows with change-tracking artefacts;
2. downstream tables transform incrementally with in-sync datetimes and are designed for ease of assembly;
3. source tables for Power BI, whether for DirectQuery or partitioned loads, are also incrementally materialised;
4. Power BI tables themselves are incrementally refreshed using partitions, supported by incrementally refreshed polling tables for fast change detection.

All this means the data engineer plans far ahead, letting Power BI’s efficiency requirements shape the pipeline even as the first table is built.

Power BI refresh is therefore the point at which the quality of the pipeline becomes visible.

> [!NOTE]
> **Key ideas**
>
> Power BI refresh is the point at which the quality of the pipeline becomes visible.
>
> Power BI should assemble information, not manufacture it.
>
> Source tables for Power BI should be simple, prepared fragments rather than complex transformation views.
>
> DirectQuery avoids import refresh, but shifts cost to query time and imposes user-experience limits.
>
> Partitioning improves refresh by dividing large tables into independently loadable slices.
>
> The partition key should normally be a business date, not a change-tracking datetime.
>
> Rolling windows keep model size and refresh time under control, but require careful boundary alignment.
>
> Incremental partition refresh depends on polling queries and partition bookmarks.
>
> Power BI manages partition bookmarks internally, but the pipeline may need to supply fast polling tables.
>
> Optimising Power BI load requires planning backward from the semantic model into the pipeline.
```