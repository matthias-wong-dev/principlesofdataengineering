---
title: "Incremental load: tracking changes"
url: /docs/efficient-stable-pipeline/tracking-changes/
description: Explains how to detect source inserts, updates, and deletes using refresh bookmarks, polling tables, and change detection columns.
lede: Incremental work begins with reliable knowledge of what changed.
weight: 5
# draft: true
---

## Change observability

The aim of information efficiency is to process only what has changed.

If no records have changed since a table was last processed, the ideal load would spend no time processing that table. In practice, even when there are no input changes, a load still takes time to check its inputs and confirm that nothing needs to happen.

Efficiency improves when downstream tables can reliably identify the records that may have changed and ignore the rest.

Doing this well requires systematic change tracking.

Tracking change is the discipline of establishing a reliable relationship between source change and the pipeline’s own processing state, so we can answer the question: *What source records may have changed since this target table last loaded successfully?*


## The problem of time

Incremental loading depends on a deceptively simple question: *What has changed since this table was last processed?*

The difficulty is that this question does not refer to one time. It refers to a relationship between two states.

There are multiple times, and they are not always comparable. Confusing them can lead to missed records, unnecessary scans, or incorrect incremental loads.

| Time | Meaning |
|---|---|
| Source row change time | The time the row in the source table was changed. |
| Source arrival time | When the row became visible to the warehouse. |
| Target bookmark time | When the target last started a successful load. |
| Target row change time | The time a row in the target table was changed. |

The key distinction is whether a time is **in-sync** or **out-of-sync** with the pipeline.

A time is in-sync when it is created by the pipeline or can be safely compared for processing.

A time is out-of-sync when it belongs to another system and may lag behind, arrive late, or reflect a different notion of change.

The question: *Which source rows changed after the target last loaded successfully?* is only safe when the source change time is in-sync with the target’s processing time.

Doing this systematically and accurately requires additional artefacts: refresh bookmarks and polling tables.

## The simple update-datetime approach

To understand the general approach, it is useful to start with the simplest one.

The most basic approach is to include an update datetime column from the source system and filter on it.

Suppose the pipeline loads from `Raw.Event` into `Curated.Event`.

**Example source table: `Raw.Event`**

| Event ID | Event type | Update datetime |
|---|---|---|
| E1001 | Login | 2021-05-01 07:45 |
| E1002 | Payment | 2021-05-01 08:03 |
| E1003 | Refund | 2021-05-01 08:07 |

**Example target table: `Curated.Event`**

| Event ID | Event type | Update datetime |
|---|---|---|
| E1001 | Login | 2021-05-01 07:45 |

We assume that:

- the source table does not delete rows;
- the target table mirrors the source table row for row, with the same columns;
- `[Update datetime]` is carried from the source into the target.

In the simple approach, the target table remembers how far it has processed by storing the source update datetime. The next extract compares the source table against the maximum `[Update datetime]` already loaded into the target.

In this example, the maximum `[Update datetime]` in `Curated.Event` is `2021-05-01 07:45`.

A simple incremental extract might therefore filter:

```sql
-- Step 1: Find the latest source update datetime loaded in target.
declare @latest_update_datetime datetime2(7);

set @latest_update_datetime =
(
    select max([Update datetime])
    from Curated.Event
);

-- Step 2: Pull only newer rows from the source.
select
    [Event ID],
    [Event type],
    [Update datetime]
from Raw.Event
where [Update datetime] > @latest_update_datetime;
```

This retrieves `E1002` and `E1003`.

The approach is straightforward, but it suffers from several problems.

First, it does not scale to complex transformations. If `Curated.Event` draws from several source tables, it is not practical to carry every source update datetime into the target. A compound update datetime can be created, but this becomes error-prone as the query grows.

Second, it is unstable. If a source system update shifts all values in `[Update datetime]`, the pipeline may reprocess every row. This can cause a blowout in processing time and trigger unnecessary downstream work.

Third, it does not scale well to continuous or high-frequency loading. For example, if `Curated.Event` filters `Raw.Event` for rare events, then the maximum update datetime in `Curated.Event` does not represent the latest processing time of `Raw.Event`. The simple approach may force the pipeline to rescan too far back.

The problem is not that the simple approach is wrong. It is that it makes the target remember its processing state through a source business column. That is only safe when the target remains close to the source.

A more scalable pattern separates the time-tracking artefacts from the data content itself.

## Refresh bookmarks

As explained in [Load mechanics](/docs/efficient-stable-pipeline/load-mechanics/#log-bookmarks-and-change-statistics), each successful table load should record a refresh bookmark.

A **refresh bookmark** is target-side state. It records how far the target table has successfully refreshed, without relying on the target table’s business columns to remember that state.

In the simplest update-datetime approach, the target table carries the source `[Update datetime]`, and the next load compares the source against the maximum value already loaded into the target. Thus, a business column is used as the marker for the processing cut-off.

A refresh bookmark separates this processing state from the target’s business data.

The bookmark records the starting datetime of a successful load. This becomes the target table’s processing boundary. If the load fails or aborts, the bookmark should not advance. The next load should resume from the last successful boundary.

The bookmark has no necessary relationship with the business datetime in the source column. They may be minutes apart, days apart, or years apart. One belongs to the pipeline’s processing time. The other belongs to the source system’s business or application time.

**Example structure of `Pipeline.RefreshBookmark`**

| Table name | Load ID | Bookmark datetime |
|---|---:|---|
| Curated.Event | 10001 | 2026-05-01 08:01 |

In this example, `Curated.Event` last completed a successful load that began at `2026-05-01 08:01`—five years after the events themselves.


Fetching the refresh bookmark is simple.

```sql
declare @refresh_bookmark_datetime datetime2(7);

-- Step 1: Look up the refresh bookmark datetime for Curated.Event.
-- This is when the previous successful load started.
select @refresh_bookmark_datetime =
(
    select [Bookmark datetime]
    from Pipeline.RefreshBookmark
    where [Table name] = 'Curated.Event'
);
```

The refresh bookmark tracks the target table’s last successful processing state. It does not, by itself, identify source changes.

To identify source changes, the pipeline needs a source-side change signal.

## The source time problem

The refresh bookmark is in pipeline time. It records when the target table last started a successful load.

A source `[Update datetime]` may be in source time. It records when the source system says a row changed.

These two datetimes are not automatically comparable.

In our example, `Curated.Event` last refreshed at `2026-05-01 08:01`, but `Raw.Event[Update datetime]` contains business events from 2021.

The following filter to fetch the next batch of records would make no sense:

```sql
where Raw.Event.[Update datetime] > '2026-05-01 08:01'
```

It compares a source-system datetime with a pipeline refresh datetime. The result would incorrectly return no rows, even though new records may have arrived in the warehouse since the target last loaded.

A target refresh bookmark tells the pipeline where the target got to. It does not necessarily tell the pipeline what source update datetime had been safely observed at that point.

To use source update datetimes safely, the pipeline must know how source time relates to pipeline time.

There are two cases:

| Case | Meaning | Consequence |
|---|---|---|
| In-sync source | The source change datetime is created by the pipeline or safely comparable with pipeline time. | The refresh bookmark can be compared directly to the source row change datetime. |
| Out-of-sync source | The source change datetime belongs to another system and may lag behind arrival in the warehouse. | A polling table is needed to map pipeline time to source time. |

External raw tables are often out-of-sync. Even if they contain an `[Update datetime]`, that value may record when the row changed in the source system, not when the row became visible to the warehouse.

When datetimes are out-of-sync, the pipeline needs a polling table.

## Polling tables

A polling table is source-side state.

It records how far the source’s update timeline was safely observable at particular points in pipeline time. Its purpose is to let the pipeline translate the target’s refresh bookmark into the source’s own update timeline.

A polling table should be much faster to query than the source table itself. Ideally, the polling query should be close to zero time so that it can support frequent or continuous loads.

Suppose `Raw.Event[Update datetime]` is out-of-sync with the refresh bookmark for `Curated.Event`. There may be an unknown lag between the source update timestamp and the row’s arrival in the warehouse. The only safe assumption is that `Raw.Event[Update datetime]` increases monotonically within the source system.

A polling table provides a way to map pipeline time to source time.

For example, the pipeline may append a row to `Raw.Bookmark` each time it checks `Raw.Event`.

```sql
insert into Raw.Bookmark
(
    [Source table name],
    [Refresh datetime],
    [Bookmark datetime]
)
select
    'Raw.Event',
    sysutcdatetime(),
    max([Update datetime])
from Raw.Event;
```

**Example structure of `Raw.Bookmark`**

| Source table name | Refresh datetime | Bookmark datetime |
|---|---|---|
| Raw.Event | 2026-05-01 07:55 | 2021-05-01 07:48 |
| Raw.Event | 2026-05-01 08:00 | 2021-05-01 07:56 |
| Raw.Event | 2026-05-01 08:05 | 2021-05-01 08:02 |
| Raw.Event | 2026-05-01 08:10 | 2021-05-01 08:08 |

The columns have different meanings:

| Column | Meaning |
|---|---|
| `[Source table name]` | The source table being polled. |
| `[Refresh datetime]` | The pipeline datetime when the polling row was created. This is in-sync with the pipeline. |
| `[Bookmark datetime]` | The maximum `Raw.Event[Update datetime]` observed at that polling moment. This is in the source system’s time-world. |

The refresh bookmark datetime of `Curated.Event` is now in-sync with `[Refresh datetime]` in `Raw.Bookmark` because they are both managed by the pipeline. `Raw.Bookmark[Refresh datetime]` is linked to the source system’s update timeline through `Raw.Bookmark[Bookmark datetime]`.

With the polling table as the bridge, we can now ask: *When the target last refreshed, how far through the source’s update timeline had the source safely arrived?*

Suppose `Curated.Event` last successfully started at `2026-05-01 08:01`.

The polling table shows that, at pipeline time `2026-05-01 08:01`, the latest observed source bookmark was `2021-05-01 07:56`.

The next extract should therefore consider:

```sql
Raw.Event[Update datetime] > '2021-05-01 07:56'
```

The query pattern is:


```sql
declare @refresh_bookmark_datetime datetime2(7);
declare @latest_process_datetime datetime2(7);

-- Step 1: Look up the refresh bookmark datetime for Curated.Event.
-- This is when the previous successful load started.
select @refresh_bookmark_datetime =
(
    select [Bookmark datetime]
    from Pipeline.RefreshBookmark
    where [Table name] = 'Curated.Event'
);

-- Step 2: Obtain the latest source update datetime that was
-- safely observable at or before that refresh bookmark.
select top 1
    @latest_process_datetime = [Bookmark datetime]
from Raw.Bookmark
where [Source table name] = 'Raw.Event'
  and [Refresh datetime] <= @refresh_bookmark_datetime
order by [Refresh datetime] desc;

-- Step 3: Fetch rows whose source update is newer than what
-- the previous target load had safely captured.
select
    e.*
from Raw.Event as e
where e.[Update datetime] > @latest_process_datetime;
```

In the example, this returns `E1002` and `E1003`:

| Event ID | Event type | Update datetime |
|---|---|---|
| E1002 | Payment | 2021-05-01 08:03 |
| E1003 | Refund | 2021-05-01 08:07 |

The relationship between the source update time, the translation to pipeline time using the polling table, and the refresh bookmark on the target table to find the source records to update can be visualised as two parallel timelines.

{{< svg >}}
<svg xmlns="http://www.w3.org/2000/svg"
     width="1080" height="520"
     viewBox="0 0 1080 520"
     style="display:block;width:100%;max-width:42rem;height:auto;background:transparent"
     role="img"
     aria-label="Source update time maps to pipeline time through polling rows and target refresh bookmarks">

  <defs>
    <marker id="arrowhead-refresh-map" markerWidth="10" markerHeight="8"
            refX="10" refY="4" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L10,4 L0,8 z" fill="#222222"/>
    </marker>
  </defs>

  <!-- Headings -->
  <text x="70" y="54"
        font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
        font-size="18" font-weight="700" fill="#111111">Source update time</text>

  <text x="70" y="318"
        font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
        font-size="18" font-weight="700" fill="#111111">Pipeline time</text>

  <!-- Timeline baselines -->
  <line x1="180" y1="150" x2="960" y2="150"
        stroke="#222222" stroke-width="2.4"
        marker-end="url(#arrowhead-refresh-map)"/>

  <line x1="180" y1="390" x2="960" y2="390"
        stroke="#222222" stroke-width="2.4"
        marker-end="url(#arrowhead-refresh-map)"/>

  <!-- Source date caption -->
  <text x="180" y="190"
        font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
        font-size="13" fill="#666666">2021-05-01</text>

  <!-- Pipeline date caption -->
  <text x="180" y="430"
        font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
        font-size="13" fill="#666666">2026-05-01</text>

  <!-- Source ticks / polling bookmark values -->
  <g font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
     font-size="13" fill="#333333">
    <line x1="300" y1="139" x2="300" y2="161" stroke="#222222" stroke-width="1.7"/>
    <text x="300" y="128" text-anchor="middle">07:48</text>

    <line x1="430" y1="133" x2="430" y2="167" stroke="#222222" stroke-width="2.4"/>
    <text x="430" y="128" text-anchor="middle">07:56</text>

    <line x1="560" y1="139" x2="560" y2="161" stroke="#222222" stroke-width="1.7"/>
    <text x="560" y="128" text-anchor="middle">08:02</text>

    <line x1="690" y1="139" x2="690" y2="161" stroke="#222222" stroke-width="1.7"/>
    <text x="690" y="128" text-anchor="middle">08:08</text>
  </g>

  <!-- Source event crosses and labels ABOVE line -->
  <g stroke="#222222" stroke-width="2">
    <!-- E1001 -->
    <line x1="262" y1="142" x2="278" y2="158"/>
    <line x1="278" y1="142" x2="262" y2="158"/>
    <text x="270" y="108" text-anchor="middle"
          font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
          font-size="13" font-weight="100" fill="#333333">E1001</text>

    <!-- E1002 -->
    <line x1="572" y1="142" x2="588" y2="158"/>
    <line x1="588" y1="142" x2="572" y2="158"/>
    <text x="580" y="108" text-anchor="middle"
          font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
          font-size="13" font-weight="100" fill="#333333">E1002</text>

    <!-- E1003 -->
    <line x1="642" y1="142" x2="658" y2="158"/>
    <line x1="658" y1="142" x2="642" y2="158"/>
    <text x="650" y="108" text-anchor="middle"
          font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
          font-size="13" font-weight="100" fill="#333333">E1003</text>
  </g>



  <!-- Bracket showing included events -->
  <path d="M430 82 C505 45, 590 45, 650 82"
        fill="none" stroke="#222222" stroke-width="1.8"
        marker-end="url(#arrowhead-refresh-map)"/>
  <text x="545" y="34" text-anchor="middle"
        font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
        font-size="14" fill="#333333">next extract considers source events after 07:56</text>

  <!-- Pipeline polling times, mostly before target starts -->
  <g font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
     font-size="13" fill="#333333">
    <line x1="300" y1="379" x2="300" y2="401" stroke="#222222" stroke-width="1.7"/>
    <text x="300" y="426" text-anchor="middle">07:55</text>

    <line x1="430" y1="373" x2="430" y2="407" stroke="#222222" stroke-width="2.4"/>
    <text x="430" y="426" text-anchor="middle">08:00</text>

    <line x1="560" y1="379" x2="560" y2="401" stroke="#222222" stroke-width="1.7"/>
    <text x="560" y="426" text-anchor="middle">08:05</text>
  </g>

  <!-- Two target refresh starts -->
  <line x1="470" y1="365" x2="470" y2="415" stroke="#222222" stroke-width="2.4"/>
  <circle cx="470" cy="390" r="8" fill="#ffffff" stroke="#222222" stroke-width="2.2"/>
  <text x="470" y="455" text-anchor="middle"
        font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
        font-size="13" font-weight="700" fill="#111111">previous Curated.Event</text>
  <text x="470" y="474" text-anchor="middle"
        font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
        font-size="13" fill="#333333">refresh start</text>

  <line x1="720" y1="365" x2="720" y2="415" stroke="#222222" stroke-width="2.4"/>
  <circle cx="720" cy="390" r="8" fill="#ffffff" stroke="#222222" stroke-width="2.2"/>
  <text x="720" y="455" text-anchor="middle"
        font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
        font-size="13" font-weight="700" fill="#111111">current Curated.Event</text>
  <text x="720" y="474" text-anchor="middle"
        font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
        font-size="13" fill="#333333">refresh start</text>

   <!-- Downward polling map arrows -->
  <g stroke="#222222" stroke-width="1.7" stroke-dasharray="6 5"
     marker-end="url(#arrowhead-refresh-map)">
    <line x1="300" y1="174" x2="300" y2="365"/>
    <line x1="430" y1="174" x2="430" y2="365"/>
    <line x1="560" y1="174" x2="560" y2="365"/>
  </g>

  <!-- Polling dots -->
  <circle cx="300" cy="390" r="6" fill="#222222"/>
  <circle cx="430" cy="390" r="7" fill="#222222"/>
  <circle cx="560" cy="390" r="6" fill="#222222"/>

  <text x="240" y="348" text-anchor="middle"
        font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
        font-size="13" fill="#333333">Raw.Bookmark</text>
  <text x="240" y="365" text-anchor="middle"
        font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
        font-size="13" fill="#333333">updated</text>

  <text x="370" y="348" text-anchor="middle"
        font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
        font-size="13" fill="#333333">Raw.Bookmark</text>
  <text x="370" y="365" text-anchor="middle"
        font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
        font-size="13" fill="#333333">updated</text>

  <!-- Current target compares from previous refresh bookmark -->
  <path d="M720 350 C675 292, 520 292, 470 350"
        fill="none" stroke="#222222" stroke-width="1.8"
        marker-end="url(#arrowhead-refresh-map)"/>
  <text x="650" y="285"
        font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
        font-size="13" fill="#333333">current refresh resumes from</text>
  <text x="650" y="303"
        font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
        font-size="13" fill="#333333">previous target bookmark</text>

  <!-- Right-side explanatory label -->
  <text x="790" y="210"
        font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
        font-size="14" fill="#333333">polling table maps</text>
  <text x="790" y="230"
        font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
        font-size="14" fill="#333333">source update time</text>
  <text x="790" y="250"
        font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
        font-size="14" fill="#333333">to pipeline time</text>

</svg>
{{< /svg >}}

<div style="max-width:42rem;text-align:center;font-size:0.95rem;color:#666;margin-top:0.5rem;">
Figure 1. <code>Raw.Bookmark</code> polling rows map source update time to pipeline time. The previous <code>Curated.Event</code> refresh used the latest polling row available when it started, mapping its target bookmark to source boundary <code>07:56</code>. The current refresh resumes from that target bookmark, so it considers source events after <code>07:56</code>.
</div>

In theory, refreshing the polling table continuously would allow the pipeline to translate pipeline time into source time at any point. In practice, the refresh frequency should align with the pipeline cadence and business need.

A single polling table can store bookmarks for multiple source tables. It does not need to be one polling table per source table.

> [!NOTE]
> **Advanced note: moving source boundaries**
>
> If the source is continuously loading, source records may arrive while the target load is running.
>
> There are two safe ways to handle this.
>
> The first is to freeze the source boundary. The load processes only the source records that were safely observable at the start of the target load. Records that arrive later are picked up in the next batch.
>
> The second is to allow deliberate overlap. The next load resumes from an earlier safe bookmark, or from the previous source boundary, so that late-arriving records are read again. This may re-extract records that were already processed, but the load mechanics should treat them as upserts and apply only genuine changes.
>
> Overlap is often safer than trying to make the boundary too precise. It is acceptable for an incremental extract to read a little too much, provided the downstream load is idempotent and unchanged rows are ignored.

## When polling tables can be skipped

Polling tables are needed when the source change datetime is out-of-sync with pipeline time.

They are not usually needed when the source table was created by the pipeline itself.

If the source table was created by the pipeline, its row change datetimes are reliable pipeline-managed datetimes. These include:

- `[Row insert datetime]`
- `[Row update datetime]`
- `[Row delete datetime]`

Because these datetimes are created by the pipeline, they are in-sync with the refresh bookmark. This is possible if a source table is landed into the warehouse through change data capture or other replication technologies, with datetimes automatically created on transaction. 

**Example pipeline-managed source table: `Filtered.Event`**

| Event ID | Event type | Row insert datetime | Row update datetime | Row delete datetime |
|---|---|---|---|---|
| E1001 | Login | 2026-05-01 07:40 | 2026-05-01 07:40 | 9999-12-31 00:00:00 |
| E1002 | Payment | 2026-05-01 08:03 | 2026-05-01 08:03 | 9999-12-31 00:00:00 |
| E1003 | Refund | 2026-05-01 08:07 | 2026-05-01 08:07 | 9999-12-31 00:00:00 |

If the refresh bookmark for the target is `2026-05-01 08:00`, then `E1002` and `E1003` are candidates for processing because their insert or update datetimes are after the bookmark.

In this case, the target’s refresh bookmark can be compared directly against the source table’s row change datetimes.

```sql
select
    e.*
from Filtered.Event as e
where
    e.[Row insert datetime] > @refresh_bookmark_datetime
    or e.[Row update datetime] > @refresh_bookmark_datetime
    or e.[Row delete datetime] > @refresh_bookmark_datetime;
```

This is one of the reasons why the [Filter step](/docs/creating-information/entity-processing/#first-pass-filter) is important. Once external source data has passed through a controlled pipeline load, it receives architectural row change datetimes that are in-sync with the pipeline. Downstream tables can then process incrementally without needing to reinterpret the source system’s update timeline.

## The role of the filter step

Three themes occur when tracking inserts, updates, and deletes.

First, datetimes that are synchronised with the pipeline’s processing time are easy to use.

Second, architectural artefacts are more reliable than business artefacts for change tracking.

Third, deletes are very hard to track unless they have been architecturally managed.

When these conditions are absent, tracking change becomes complex or even impossible.

This is one reason pipelines often begin with a [Filter step](/docs/creating-information/entity-processing/#first-pass-filter) that keeps transformation minimal. The Filter step is the first controlled interaction with the source data. It extracts the necessary rows and columns, then annotates them with pipeline-managed architectural columns. It also tracks deletes.

The Filter step may look like low-value work because it performs little transformation. But it provides a critical foundation. Once source data has passed through a properly designed load process, downstream tables can rely on `[Row insert datetime]`, `[Row update datetime]`, and `[Row delete datetime]` to track change.

The optimal case is:

1. incoming data is incrementally extracted using source change detection or polling tables;
2. the Filter step applies [load mechanics](/docs/efficient-stable-pipeline/load-mechanics/#check-for-genuine-changes) to detect genuine change;
3. the resulting pipeline table has reliable row change datetimes, and deleted rows are stored in a history table;
4. downstream tables can process incrementally using those pipeline-managed datetimes.

In this way, the Filter step converts fragile or out-of-sync source change signals into reliable pipeline change artefacts.

> [!NOTE]
> **Key ideas**
>
> Incremental work begins with reliable knowledge of what changed.
>
> Refresh bookmarks track the target table’s last successful processing state.
>
> Source change detection columns can be in-sync or out-of-sync with the pipeline’s processing time.
>
> Polling tables map out-of-sync source timestamps to in-sync pipeline timestamps.
>
> Inserts and updates are easier to track than deletes because deleted rows disappear.
>
> Architectural change artefacts are more reliable than business columns for detecting change.
>
> The Filter step converts source change signals into reliable pipeline change artefacts for downstream processing.
