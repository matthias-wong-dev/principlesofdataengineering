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

String aggregation for display should also be avoided where possible, as this can often be handled with appropriate DAX measures, as explained in [Designing measures](/docs/presenting-insights/designing-measures/#dimensional-measures).

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

This is visualised below:

{{< svg >}}
<svg xmlns="http://www.w3.org/2000/svg"
     width="980" height="760"
     viewBox="0 0 980 760"
     style="display:block;width:100%;max-width:44rem;height:auto;background:transparent"
     role="img"
     aria-label="Book analogy for Power BI partition refresh showing incoming books split by publishing year, old books not processed, and only changed partitions refreshed">

  <defs>
    <marker id="arrowhead-book-partitions" markerWidth="10" markerHeight="8"
            refX="10" refY="4" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L10,4 L0,8 z" fill="#222222"/>
    </marker>

    <style>
      .box {
        fill: #ffffff;
        stroke: #222222;
        stroke-width: 2;
      }

      .lightbox {
        fill: #ffffff;
        stroke: #999999;
        stroke-width: 1.5;
      }

      .label {
        font-family: Inter, Segoe UI, Roboto, Arial, sans-serif;
        font-size: 17px;
        font-weight: 700;
        fill: #111111;
      }

      .small {
        font-family: Inter, Segoe UI, Roboto, Arial, sans-serif;
        font-size: 13px;
        fill: #333333;
      }

      .mono {
        font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
        font-size: 12px;
        fill: #333333;
      }

      .arrow {
        stroke: #222222;
        stroke-width: 2;
        fill: none;
        marker-end: url(#arrowhead-book-partitions);
      }

      .bracket {
        stroke: #222222;
        stroke-width: 2;
        fill: none;
      }
    </style>
  </defs>

  <!-- Title -->
  <text x="60" y="44" class="label">Partition refresh as boxes of books</text>
  <text x="60" y="68" class="small">Incoming books are grouped by publishing date, then mapped to stored boxes by year.</text>

  <!-- Left headings -->
  <text x="105" y="112" class="label">Incoming books</text>
  <text x="105" y="134" class="small">grouped by publishing year</text>

  <!-- Benefit 2 label above incoming box -->
  <text x="105" y="175" class="label">Benefit 2: old books not processed</text>
  <text x="105" y="197" class="small">Very old segments can sit outside the rolling window.</text>
  <text x="105" y="217" class="small">They no longer need to be refreshed.</text>

  <!-- Left incoming vertical box shifted down -->
  <rect x="90" y="250" width="260" height="430" rx="14" class="box"/>

  <!-- Year segments in incoming -->
  <!-- Old segment -->
  <rect x="110" y="270" width="220" height="74" rx="8" class="lightbox"/>
  <text x="130" y="293" class="label">2021 books</text>
  <text x="130" y="315" class="small">very old segment</text>
  <text x="130" y="334" class="mono">latest update: 2026-04-20</text>

  <!-- 2022 -->
  <rect x="110" y="358" width="220" height="74" rx="8" class="lightbox"/>
  <text x="130" y="381" class="label">2022 books</text>
  <text x="130" y="402" class="small">current rolling window</text>
  <text x="130" y="421" class="mono">latest update: 2026-05-03</text>

  <!-- 2023 changed -->
  <rect x="110" y="446" width="220" height="74" rx="8" class="box"/>
  <text x="130" y="469" class="label">2023 books</text>
  <text x="130" y="490" class="small">current rolling window</text>
  <text x="130" y="509" class="mono">latest update: 2026-05-09</text>

  <!-- 2024 -->
  <rect x="110" y="534" width="220" height="74" rx="8" class="lightbox"/>
  <text x="130" y="557" class="label">2024 books</text>
  <text x="130" y="578" class="small">current rolling window</text>
  <text x="130" y="597" class="mono">latest update: 2026-05-04</text>

  <!-- 2025 -->
  <rect x="110" y="622" width="220" height="38" rx="8" class="lightbox"/>
  <text x="130" y="646" class="label">2025 books</text>

  <!-- Bracket showing old segment excluded -->
  <path d="M75 270 L55 270 L55 344 L75 344" class="bracket"/>
  <text x="22" y="311" text-anchor="middle" class="small">outside</text>
  <text x="22" y="329" text-anchor="middle" class="small">window</text>

  <!-- Right partition boxes -->
  <text x="610" y="112" class="label">Received book boxes</text>
  <text x="610" y="134" class="small">stored partitions with refresh bookmarks</text>

  <!-- Benefit 1 label -->
  <text x="610" y="175" class="label">Benefit 1: divide and conquer</text>
  <text x="610" y="197" class="small">Each box can be loaded independently.</text>

  <!-- 2022 box -->
  <rect x="610" y="255" width="260" height="88" rx="14" class="lightbox"/>
  <text x="635" y="286" class="label">2022 box</text>
  <text x="635" y="310" class="mono">bookmark: 2026-05-03</text>
  <text x="635" y="330" class="small">unchanged—do not refresh</text>

  <!-- 2023 box changed -->
  <rect x="610" y="400" width="260" height="108" rx="14" class="box"/>
  <text x="635" y="431" class="label">2023 box</text>
  <text x="635" y="455" class="mono">bookmark: 2026-05-02</text>
  <text x="635" y="475" class="mono">incoming:  2026-05-09</text>
  <text x="635" y="493" class="small">changed—refresh this box</text>

  <!-- 2024 box -->
  <rect x="610" y="540" width="260" height="88" rx="14" class="lightbox"/>
  <text x="635" y="571" class="label">2024 box</text>
  <text x="635" y="595" class="mono">bookmark: 2026-05-04</text>
  <text x="635" y="615" class="small">unchanged—do not refresh</text>

  <!-- Benefit 3 label -->
  <text x="610" y="700" class="label">Benefit 3: refresh only changed boxes</text>
  <text x="610" y="722" class="small">Refresh partitions where polling value differs from its bookmark.</text>

  <!-- Bracketed mapping arrows -->
  <path d="M365 395 C455 395, 520 299, 610 299" class="arrow"/>
  <path d="M365 483 C455 483, 520 449, 610 449" class="arrow"/>
  <path d="M365 571 C455 571, 520 584, 610 584" class="arrow"/>

  <!-- Left bracket for mapping -->
  <path d="M370 360 C390 360, 390 395, 370 395" class="bracket"/>
  <path d="M370 448 C390 448, 390 483, 370 483" class="bracket"/>
  <path d="M370 536 C390 536, 390 571, 370 571" class="bracket"/>

  <text x="405" y="438" class="small">segments map</text>
  <text x="405" y="456" class="small">to year boxes</text>

  <!-- Check marks / comparison labels -->
  <text x="885" y="305" class="label">=</text>
  <text x="885" y="456" class="label">≠</text>
  <text x="885" y="591" class="label">=</text>

</svg>
{{< /svg >}}

<div style="max-width:44rem;text-align:center;font-size:0.95rem;color:#666;margin-top:0.5rem;">
Figure 1. Partitioning is like sorting incoming books into boxes by publishing year. Partitioning enables divide-and-conquer loading. A rolling window means very old books are no longer processed. Incremental refresh compares each incoming segment’s latest update datetime with the stored bookmark on the matching box, then refreshes only the box whose value changed.
</div>

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

Only the `2025-02` partition needs to refresh. When it is completed, the partition bookmark is advanced to match the polling value.

**Power BI partition bookmarks after refresh**

| Partition | Stored refresh bookmark |
|---|---|
| 2025-01 | 2026-05-03 16:45 |
| 2025-02 | 2026-05-09 11:10  |
| 2025-03 | 2026-05-04 18:05 |





## Conclusion

DirectQuery, efficient source tables, and partitioned loads are the main ways to improve Power BI load performance.

| Method | Basic idea | Best suited to | Consideration |
|---|---|---|---|
| DirectQuery | Avoid importing the table. | Very large, simple, narrow fact tables. | Slower report interaction and DAX limitations. |
| Efficient source views or tables | Make import cheap by preparing the source. | Most Import models. | Complexity moves upstream. |
| Partitioning | Refresh the table in slices. | Large fact tables with a stable business date. | Poor partition design can add overhead or miss changes. |

Partitioning also offers several levels of improvement.

| Enhancement | What it does | Benefit | Extra requirement |
|---|---|---|---|
| Parallel partition refresh | Splits one large table into smaller partitions that can be loaded independently. | Reduces refresh duration by allowing multiple partitions to load at once. | The source must retrieve each partition quickly using the partition key. |
| Rolling window | Keeps only recent partitions and drops older ones. | Prevents model size and refresh time from growing indefinitely. | Fact tables, dimensions, and source-retention windows must remain aligned. |
| Incremental partition refresh | Refreshes only partitions whose polling value has changed. | Reduces refresh work when only some partitions have changed. | Requires reliable change detection, partition bookmarks, and fast polling queries or polling tables. |

A single Power BI model may use different strategies for different tables. A small dimension may load fully. A large fact table may use Import mode with incremental partition refresh. A very large, narrow fact table may use DirectQuery over a dedicated columnstore source. The right strategy depends on the shape of the data, the refresh requirement, and the expected user experience.

Whatever the technique, the foundation for a fast-loading Power BI model is set far in advance in the pipeline. It depends on meaningful fragments to avoid complex transforms, planned indexes to support partition retrieval, and careful row-change tracking to enable polling tables.

In the ideal case, information efficiency is maximised end to end:

1. raw tables enter the pipeline incrementally, using polling tables to track changes and annotating rows with change-tracking artefacts;
2. downstream tables transform incrementally with in-sync datetimes and are designed for ease of assembly;
3. source tables for Power BI, whether for DirectQuery or partitioned loads, are also incrementally materialised;
4. Power BI tables themselves are incrementally refreshed using partitions, supported by incrementally refreshed polling tables for fast change detection.

At every stage, the pipeline maintains proportionate change—the amount of computation changes in proportion to the amount of information that has genuinely changed.

The implication is that the data engineer must plan far ahead. Power BI’s efficiency requirements should shape the pipeline even as the first table is built.


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
