---
title: "Incremental load: responding to change"
url: /docs/efficient-stable-pipeline/responding-to-change/
description: Explains how to translate upstream inserts, updates, and deletes into the correct target upserts and deletes.
lede: Source changes must be translated through query logic before the target can respond correctly.
weight: 6
# draft: true
---

## Change translation

[Tracking changes](/docs/efficient-stable-pipeline/tracking-changes/) tells the pipeline what changed upstream. It does not tell the pipeline what should change downstream.

That second step depends on query logic.

The central problem is this:

> Source inserts, updates, and deletes do not necessarily become target inserts, updates, and deletes.

**Responding to change** is the discipline of translating upstream source changes into the smallest correct set of target actions.

A systematic approach focuses on the primary keys. Responding to change starts by calculating the *target keys* whose result may have changed, then re-running the normal query only for those keys.

A **driver set** is the set of primary keys, or primary key components, that may need action because upstream source rows changed.

There are two main kinds of driver set.

| Driver set | Meaning |
|---|---|
| Upsert driver | Keys whose rows should be recalculated and then inserted or updated in the target. |
| Delete driver | Keys whose rows should be removed from the target. |

## Source changes are not target actions

The relationship between source change and target action is not straightforward.

Consider the following examples.

| Upstream change | Possible downstream action | Example reason |
|---|---|---|
| Insert | Delete | A new row causes a record to no longer qualify under an anti-join. |
| Delete | Update | Removing a row changes an aggregate. |
| Update | Insert | A changed value now passes a filter threshold. |

For example, suppose `Bank.CustomersToFollowUp` contains customers who have not made recent deposits and need service-team follow-up. This table uses `Bank.Transaction` as an input. If a new deposit is inserted into `Bank.Transaction`, that customer may no longer require follow-up. A source insert has triggered a target delete.

Suppose `Bank.AccountSummary` contains account-level aggregates, such as total number of holders and balance per account. If a joint holder is deleted from `Bank.AccountHolder`, the holder count changes. A source delete has triggered a target update.

Suppose `Bank.GoldCustomer` contains customers whose account balance exceeds a threshold. If a row in `Bank.AccountBalance` is updated so that the customer now exceeds the threshold, the customer may newly qualify. A source update has triggered a target insert.

These examples are simple, but the general lesson is that:

> The target response is determined by the query.

## Analysing the query

Suppose two source tables, `X` and `Y`, are used to produce a target table `T`.

The setup is:

- `X` has columns `[Header ID]`, `[Value]`, and `[Status]`, where `[Header ID]` is the primary key.
- `Y` has columns `[Header ID]`, `[Line number]`, `[Value]`, and `[Status]`, where `[Header ID]` and `[Line number]` are the primary key.
- `Y[Header ID]` is a foreign key to `X[Header ID]`.

There may be inserts, updates, and deletes on both `X` and `Y`.

Inserts and updates are considered together as upserts. The possible source changes are:

- upserts from `X`;
- deletes from `X`;
- upserts from `Y`;
- deletes from `Y`.

The goal is to determine which rows in `T` need to be recalculated or removed.

The way to calculate these depends on the shape of the query.

### Common query shapes

The following table summarises several common query shapes and how changes may propagate.

| Scenario | Target primary key | Approach | Keys to upsert in `T` | Keys to delete from `T` |
|---|---|---|---|---|
| Straight select of `X` | `[Header ID]` | Source rows map directly to target rows. | Headers from `X` that were inserted or updated. | Headers from `X` that were deleted. |
| Filter of `X` on `[Status]` | `[Header ID]` | Filter condition means updates can add or remove rows. | Headers from `X` that were inserted or updated and now pass the filter. | Headers from `X` that were deleted, or updated and no longer pass the filter. |
| `X` inner join `Y` | `[Header ID]`, `[Line number]` | Join means changes on either side can add or remove joined pairs. | Pairs for `Y` rows inserted or updated, plus pairs for changed `X` headers with matching `Y` rows. | Pairs for `Y` rows deleted, plus all pairs for headers deleted from `X`. |
| `X` inner join `Y`, grouped by `[Header ID]` | `[Header ID]` | Deleting a `Y` row can change the aggregate or remove the header. | Headers from `X` or `Y` whose values may have changed, including deletes from `Y` that change the aggregate. | Headers deleted from `X`, or headers that now have zero `Y` rows. |
| `X` left join `Y` with synthetic line `0` | `[Header ID]`, `[Line number]` | Synthetic line `0` appears only when no `Y` rows exist. | Pairs for `Y` rows inserted or updated; `(Header ID, 0)` for headers with no `Y` rows; pairs for new `X` headers. | Pairs for `Y` rows deleted; remove `(Header ID, 0)` when `Y` rows appear; remove all pairs for headers deleted from `X`. |
| `Y` left join `X` | `[Header ID]`, `[Line number]` | Target follows `Y` lines; `X` changes matter only if `Y` lines exist. | Pairs from `Y` inserted or updated, plus pairs under headers in `X` that changed. | Pairs from `Y` that were deleted. |
| `X` left join `Y`, grouped by `[Header ID]` | `[Header ID]` | `X` controls row presence; `Y` changes aggregates. | Headers in `X` inserted, plus headers whose values changed due to changes in `X` or `Y`, including deletes from `Y`. | Headers deleted from `X`. |
| Union of `[Header ID]` | `[Header ID]` | Header exists if present in either `X` or `Y`. | Headers inserted or updated in `X` or `Y`; headers projected from one side but still existing on the other. | Headers deleted from both `X` and `Y`. |
| `X` left anti-join `Y` | `[Header ID]` | Row appears only when `X` exists and `Y` does not. | Headers inserted or updated in `X` with no `Y` rows; headers where `Y` rows were deleted and now qualify. | Headers deleted from `X`; headers that gained a `Y` row. |

The table is not meant to memorise every case. Its purpose is to show that target response depends on query shape.

With more source tables, the analysis can become complicated quickly. A query with ten inputs may have many possible source changes, and each source change may affect the target differently.

### Robustness

For robustness, upsert drivers may be broader than strictly necessary. Delete drivers should be exact.

This asymmetry exists because load mechanics apply upserts only for rows that have genuinely changed. If the upsert driver is too broad, the pipeline may recalculate extra rows, but the staging table is still compared with the target and only genuine inserts or updates are applied.

A broad upsert driver is therefore usually safe, provided it remains performant. For example, it may be acceptable to construct the driver set using part of a primary key rather than the full primary key, causing the load to recalculate a slightly wider set of rows.

Deletes are different.

A delete driver does not ask the pipeline to recalculate a row. It tells the pipeline that a row should be removed from the target. If the delete driver contains extra keys, correct rows may disappear.

A common mistake is to over-delete with the intention of reinserting extra records. This can be tempting because a delete-and-reinsert pattern can be easier to calculate than a finely targeted delete-and-upsert pattern. However, over-deleting is dangerous. If the source system has a bulk update on a column that has no impact on the final output, the entire table may be deleted and reinserted. This can create a server bottleneck and cause downstream tables to treat unchanged rows as changed.

The rule is:

> Upsert drivers may be conservative and include some extra keys. Delete drivers should contain only rows that no longer satisfy the target query’s presence rule.

## Worked examples

The following examples show how source changes are translated through query logic.

### Worked example 1—Filter

Suppose the target table contains only active headers.

```sql
select
    [Header ID],
    [Value],
    [Status]
from X
where [Status] = 'Active';
```

**Before source change: `X`**

| Header ID | Value | Status |
|---|---:|---|
| H100 | 10 | Active |
| H101 | 20 | Inactive |
| H102 | 30 | Active |

**Before target load: `T`**

| Header ID | Value | Status |
|---|---:|---|
| H100 | 10 | Active |
| H102 | 30 | Active |

Now suppose two source rows are updated.

**Source changes in `X`**

| Header ID | Old status | New status | Source change |
|---|---|---|---|
| H101 | Inactive | Active | Update |
| H102 | Active | Inactive | Update |

The source action is the same in both cases: an update.

The target action is different.

`H101` now passes the filter, so it belongs in the upsert driver. It should be inserted into `T`.

`H102` no longer passes the filter, so it belongs in the delete driver. It should be removed from `T`.

**Upsert driver**

| Header ID | Reason |
|---|---|
| H101 | Updated row now passes the filter. |

**Delete driver**

| Header ID | Reason |
|---|---|
| H102 | Updated row no longer passes the filter. |

**After incremental load: `T`**

| Header ID | Value | Status |
|---|---:|---|
| H100 | 10 | Active |
| H101 | 20 | Active |

This example shows that a source update can become either a target upsert or a target delete. The filter controls row presence.

### Worked example 2—Aggregation

Suppose the target table contains the total line value for each header.

```sql
select
    [Header ID],
    sum([Value]) as [Total value]
from Y
group by [Header ID];
```

**Before source change: `Y`**

| Header ID | Line number | Value |
|---|---:|---:|
| H100 | 1 | 10 |
| H100 | 2 | 15 |
| H101 | 1 | 20 |

**Before target load: `T`**

| Header ID | Total value |
|---|---:|
| H100 | 25 |
| H101 | 20 |

Now suppose one source row is deleted.

**Source changes in `Y`**

| Header ID | Line number | Value | Source change |
|---|---:|---:|---|
| H100 | 2 | 15 | Delete |

The source action is a delete.

But the target row for `H100` should not be deleted. The header still has another line. Instead, the aggregate must be recalculated.

`H100` belongs in the upsert driver because its total value may have changed.

**Upsert driver**

| Header ID | Reason |
|---|---|
| H100 | Deleted line changes the aggregate. |

**Delete driver**

No rows.

**After incremental load: `T`**

| Header ID | Total value |
|---|---:|
| H100 | 10 |
| H101 | 20 |

This example shows that a source delete can become a target update. Aggregations turn row-level changes into value changes at a higher grain.

### Worked example 3—Anti-join

Suppose the target table contains headers in `X` that do not have any matching rows in `Y`.

```sql
select
    x.[Header ID],
    x.[Value]
from X as x
where not exists
(
    select 1
    from Y as y
    where y.[Header ID] = x.[Header ID]
);
```

**Before source change: `X`**

| Header ID | Value |
|---|---:|
| H100 | 10 |
| H101 | 20 |
| H102 | 30 |

**Before source change: `Y`**

| Header ID | Line number | Value |
|---|---:|---:|
| H100 | 1 | 5 |
| H102 | 1 | 8 |

**Before target load: `T`**

| Header ID | Value |
|---|---:|
| H101 | 20 |

`H101` appears in `T` because it exists in `X` but has no matching row in `Y`.

Now suppose a new row is inserted into `Y`.

**Source changes in `Y`**

| Header ID | Line number | Value | Source change |
|---|---:|---:|---|
| H101 | 1 | 12 | Insert |

The source action is an insert.

But because the target is an anti-join, this insert causes `H101` to stop qualifying. The target action is a delete.

**Upsert driver**

No rows.

**Delete driver**

| Header ID | Reason |
|---|---|
| H101 | Inserted `Y` row means the header no longer satisfies the anti-join. |

**After incremental load: `T`**

No rows.

This example shows that a source insert can become a target delete. Anti-joins reverse the usual intuition because the target row exists only while a matching source row is absent.

## Applying the change

Once the query has been analysed, the transformation can be converted from a full load to an incremental load.

Recall from [Load mechanics](/docs/efficient-stable-pipeline/load-mechanics/) that the differences between incremental extract and full extract are:

- The staging table for the load has only a minimal set of records that is much smaller than the full set, but still covers all the records that would need to be upserted in the current batch. This is what makes the load fast.

- Deletes cannot be done automatically by comparing the full set of primary keys between the staging and the target. Instead, they need to be customised for the query by analysing the impact of changes in source.

The detailed implementation of an incremental extract follows a consistent pattern.

### Step 1—Write the full query

Begin with the full query that expresses the business logic.

For example, suppose the full target query is an inner join between `X` and `Y`. They are used to load `T`.

```sql
select
    X.*,
    Y.*
from       X
inner join Y on Y.[PK] = X.[PK];
```

This query is the definition of the target table. It should be understandable and testable as a full load before it is made incremental.

### Step 2—Fetch the refresh bookmark

At the start of the load, retrieve the refresh bookmark that records the target table’s last successful processing boundary.

This bookmark defines the boundary for upstream change detection.

```sql
declare @refresh_bookmark_datetime datetime2(7);

select @refresh_bookmark_datetime =
(
    select [Bookmark datetime]
    from Pipeline.RefreshBookmark
    where [Table name] = 'T'
);
```

### Step 3—Create the upsert driver

Using the query analysis, create a temporary table of target keys to upsert.

In this example, changes from either `X` or `Y` may affect rows in `T`, so the upsert driver takes keys from both source tables.

```sql
drop table if exists #keys_to_upsert;

-- Upserts from X.
select
    X.[PK]
into #keys_to_upsert
from X
where X.[Row update datetime] > @refresh_bookmark_datetime

union

-- Upserts from Y.
select
    Y.[PK]
from Y
where Y.[Row update datetime] > @refresh_bookmark_datetime;
```

In these examples, the driver table has the full target key. In practice, it may contain only part of a multi-column primary key, depending on the grain of the target table.

If performance requires, add an index to the driver table before joining it to the full query.

```sql
create clustered index cix_keys_to_upsert
on #keys_to_upsert ([PK]);
```

The upsert driver is then joined to the full query.

```sql
drop table if exists #T_staging;

select
    X.*,
    Y.*
into #T_staging
from       X
inner join Y                on Y.[PK] = X.[PK]
inner join #keys_to_upsert  as U on U.[PK] = X.[PK]; -- downfilter original query for smaller staging
```

This produces a minimal staging table. It contains only rows whose target values may have changed, but the row values still come from the normal business query.

In other query shapes, deletes may also belong in the upsert driver. For example, in an aggregation, deleting a contributing row changes the aggregate value and therefore requires recalculation.

### Step 4—Create the delete driver

Using the query analysis, create a temporary table of target keys to delete.

For an inner join between `X` and `Y`, a target row should disappear if the corresponding key no longer exists on either side of the join.

If deleted rows are preserved in history tables, the delete driver can be calculated from those histories.

```sql
drop table if exists #keys_to_delete;

-- Deletes from X.
select
    X_History.[PK]
into #keys_to_delete
from      X_History
left join X         on X.[PK] = X_History.[PK]
where X_History.[Row delete datetime] > @refresh_bookmark_datetime -- recently deleted rows
  and X.[PK] is null;                                             -- truly deleted

union

-- Deletes from Y.
select
    Y_History.[PK]
from      Y_History
left join Y         on Y.[PK] = Y_History.[PK]
where Y_History.[Row delete datetime] > @refresh_bookmark_datetime -- recently deleted rows
  and Y.[PK] is null;                                             -- truly deleted
```

The delete driver should contain only target keys that no longer satisfy the target query’s presence rule.

Once the delete driver has been calculated, deleting from the target is straightforward.

```sql
delete T
from       T
inner join #keys_to_delete as D on D.[PK] = T.[PK];
```

### Step 5—Apply load mechanics

After the minimal staging table and delete driver have been created, the normal load mechanics can apply.

The pipeline can:

- compare staging rows with the target to identify genuine upserts;
- check stability thresholds;
- reject unsafe rows;
- apply updates and inserts;
- apply deletes;
- preserve history;
- record load statistics and bookmarks.

This means full and incremental loads share the same business query and load mechanics. The difference is that incremental loads add driver sets to reduce the work.

### Full incremental extract pattern

Putting the steps together, the full pattern is:

```sql
-- 1. Fetch the refresh bookmark, which is the point to resume.
declare @refresh_bookmark_datetime datetime2(7);

select @refresh_bookmark_datetime =
(
    select [Bookmark datetime]
    from Pipeline.RefreshBookmark
    where [Table name] = 'T'
);


-- 2. Determine the upsert driver table.
drop table if exists #keys_to_upsert;

-- Upserts from X.
select
    X.[PK]
into #keys_to_upsert
from X
where X.[Row update datetime] > @refresh_bookmark_datetime

union

-- Upserts from Y.
select
    Y.[PK]
from Y
where Y.[Row update datetime] > @refresh_bookmark_datetime;


-- 3. Create the minimal staging table by downfiltering the full query.
drop table if exists #T_staging;

select
    X.*,
    Y.*
into #T_staging
from       X
inner join Y               on Y.[PK] = X.[PK]
inner join #keys_to_upsert as U on U.[PK] = X.[PK]; -- downfilter original query for smaller staging


-- 4. Determine the delete driver table.
drop table if exists #keys_to_delete;

-- Deletes from X.
select
    X_History.[PK]
into #keys_to_delete
from      X_History
left join X         on X.[PK] = X_History.[PK]
where X_History.[Row delete datetime] > @refresh_bookmark_datetime -- recently deleted rows
  and X.[PK] is null;                                             -- truly deleted

union

-- Deletes from Y.
select
    Y_History.[PK]
from      Y_History
left join Y         on Y.[PK] = Y_History.[PK]
where Y_History.[Row delete datetime] > @refresh_bookmark_datetime -- recently deleted rows
  and Y.[PK] is null;                                             -- truly deleted


-- 5. Apply the deletes.
delete T
from       T
inner join #keys_to_delete as D on D.[PK] = T.[PK];

-- 6. Continue upsert using standard load mechanics...
```

This script illustrates the complete pattern:

1. fetch the target refresh bookmark;
2. calculate the upsert driver;
3. downfilter the full query into a minimal staging table;
4. calculate the delete driver;
5. apply the target deletes.

Visually the procedure looks like:

{{< svg >}}
<svg xmlns="http://www.w3.org/2000/svg"
     width="760" height="980"
     viewBox="0 0 760 980"
     style="display:block;width:100%;max-width:38rem;height:auto;background:transparent"
     role="img"
     aria-label="Vertical incremental load SQL pattern from bookmark to upsert driver, staging, delete driver, deletes, and load mechanics">

  <defs>
    <marker id="arrowhead-incremental-pattern" markerWidth="10" markerHeight="8"
            refX="10" refY="4" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L10,4 L0,8 z" fill="#222222"/>
    </marker>

    <style>
      .box {
        fill: #ffffff;
        stroke: #222222;
        stroke-width: 2;
        rx: 14;
      }

      .label {
        font-family: Inter, Segoe UI, Roboto, Arial, sans-serif;
        font-size: 18px;
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
        font-size: 13px;
        fill: #333333;
      }

      .arrow {
        stroke: #222222;
        stroke-width: 2;
        fill: none;
        marker-end: url(#arrowhead-incremental-pattern);
      }

      .dash {
        stroke: #222222;
        stroke-width: 1.8;
        stroke-dasharray: 6 5;
        fill: none;
        marker-end: url(#arrowhead-incremental-pattern);
      }
    </style>
  </defs>

  <!-- Title -->
  <text x="60" y="44" class="label">Full incremental extract pattern</text>
  <text x="60" y="68" class="small">A vertical view of the SQL block: each artefact is created in sequence, then used by load mechanics.</text>

  <!-- Step 1 -->
  <rect x="170" y="105" width="420" height="86" class="box"/>
  <text x="380" y="138" text-anchor="middle" class="label">1. Fetch refresh bookmark</text>
  <text x="380" y="164" text-anchor="middle" class="mono">@refresh_bookmark_datetime</text>
  <text x="380" y="182" text-anchor="middle" class="small">target processing boundary for T</text>

  <!-- Arrow 1 -->
  <path d="M380 191 L380 235" class="arrow"/>

  <!-- Step 2 -->
  <rect x="170" y="235" width="420" height="96" class="box"/>
  <text x="380" y="268" text-anchor="middle" class="label">2. Determine upsert driver</text>
  <text x="380" y="294" text-anchor="middle" class="mono">#keys_to_upsert</text>
  <text x="380" y="314" text-anchor="middle" class="small">keys from X and Y changed after the bookmark</text>

  <!-- Source notes left -->
  <text x="70" y="272" text-anchor="start" class="small">from X</text>
  <text x="70" y="294" text-anchor="start" class="small">from Y</text>
  <path d="M125 280 C145 280, 150 280, 170 280" class="dash"/>
  <path d="M125 302 C145 302, 150 302, 170 302" class="dash"/>

  <!-- Arrow 2 -->
  <path d="M380 331 L380 375" class="arrow"/>

  <!-- Step 3 -->
  <rect x="170" y="375" width="420" height="116" class="box"/>
  <text x="380" y="408" text-anchor="middle" class="label">3. Create minimal staging table</text>
  <text x="380" y="434" text-anchor="middle" class="mono">#T_staging</text>
  <text x="380" y="456" text-anchor="middle" class="small">run the normal full query</text>
  <text x="380" y="475" text-anchor="middle" class="small">inner join to #keys_to_upsert</text>

  <!-- Query annotation right -->
  <text x="615" y="421" class="small">full query</text>
  <text x="615" y="443" class="small">inner join to upsert driver</text>
  <path d="M590 438 C610 438, 610 438, 590 438" class="dash"/>

  <!-- Arrow 3 split -->
  <path d="M380 491 L380 535" class="arrow"/>

  <!-- Step 4 -->
  <rect x="170" y="535" width="420" height="112" class="box"/>
  <text x="380" y="568" text-anchor="middle" class="label">4. Determine delete driver</text>
  <text x="380" y="594" text-anchor="middle" class="mono">#keys_to_delete</text>
  <text x="380" y="616" text-anchor="middle" class="small">keys deleted from X or Y history</text>
  <text x="380" y="635" text-anchor="middle" class="small">and no longer present in the current source</text>

  <!-- History notes left -->
  <text x="60" y="586" text-anchor="start" class="small">from X_History</text>
  <text x="60" y="608" text-anchor="start" class="small">from Y_History</text>
  <path d="M140 592 C150 592, 155 592, 170 592" class="dash"/>
  <path d="M140 614 C150 614, 155 614, 170 614" class="dash"/>

  <!-- Arrow 4 -->
  <path d="M380 647 L380 691" class="arrow"/>

  <!-- Step 5 -->
  <rect x="170" y="691" width="420" height="86" class="box"/>
  <text x="380" y="724" text-anchor="middle" class="label">5. Apply deletes</text>
  <text x="380" y="750" text-anchor="middle" class="mono">delete T using #keys_to_delete</text>
  <text x="380" y="768" text-anchor="middle" class="small">remove rows whose presence is no longer valid</text>

  <!-- Arrow 5 -->
  <path d="M380 777 L380 821" class="arrow"/>

  <!-- Step 6 -->
  <rect x="170" y="821" width="420" height="98" class="box"/>
  <text x="380" y="854" text-anchor="middle" class="label">6. Apply upserts using load mechanics</text>
  <text x="380" y="880" text-anchor="middle" class="mono">#T_staging → T</text>
  <text x="380" y="900" text-anchor="middle" class="small">compare, insert, update, preserve history, log bookmark</text>

  <!-- Target marker -->
  <rect x="610" y="718" width="86" height="128" class="box"/>
  <text x="653" y="774" text-anchor="middle" class="label">T</text>
  <text x="653" y="798" text-anchor="middle" class="small">target</text>
  <path d="M590 734 C600 734, 600 734, 610 734" class="arrow"/>
  <path d="M590 870 C612 870, 620 846, 638 846" class="arrow"/>

  <!-- Bottom doctrine -->
  <text x="60" y="950" class="small">Upsert path may be conservative. Delete path must be exact.</text>

</svg>
{{< /svg >}}

<div style="max-width:38rem;text-align:center;font-size:0.95rem;color:#666;margin-top:0.5rem;">
Figure 1. The incremental extract pattern follows the SQL script from top to bottom. The refresh bookmark defines the change boundary. The upsert driver creates a minimal staging table by downfiltering the normal query. The delete driver identifies rows to remove from <code>T</code>. Load mechanics then applies exact deletes and genuine upserts.
</div>


## Why this pattern works

This workflow has several advantages.

### Uniformity

The same query logic underpins both full loads and incremental loads.

The difference lies in the driver set. A full load runs the query for all target keys. An incremental load runs the same query for only the keys that may have changed.

This reduces the risk that the incremental load becomes a different definition from the full load.

### Idempotency

The process works even if it runs more than once over the same interval.

If a load fails and is retried, the refresh bookmark ensures that the pipeline considers the same source change window again.

If the load runs more frequently than usual, the outcome remains consistent. There may simply be fewer source changes to respond to.

### Graceful fallback

If upstream changes touch many rows, the driver set expands, but the final result set may have minimal changes because the touched column is not selected for the target table.

Using this approach, the incremental load will behave like a full load. This is acceptable. The staging table is still compared to the target, so only genuinely changed rows should be applied.

## Best-practice workflow

Given the complexity of responding to change, incremental logic should be developed as a controlled workflow rather than assembled all at once.

The goal is to prove that the incremental load produces the same result as the full query, while doing less work.

The following is a 9 steps pattern.

### Step 1—Create a full-load comparison test

Start by creating a test that compares the incrementally maintained target table with the expected result of the full query.

This may include:

- row counts;
- primary key comparison;
- sample selection.

The test establishes the standard of correctness. A correct incremental load should produce the same final target as a full load.

A datetime filter can be used for performance during development, but it should be independent of the extract datetime being tested.

### Step 2—Create a realistic change window

Load the table in full, then wait for source data to change or create controlled test changes.

This gives the developer a realistic incremental window. The aim is to test the logic against actual source changes, not merely against an abstract query.

### Step 3—Build the upsert driver

Build the upsert driver for one source table at a time.

As each source table is added, re-run the driver query and check both correctness and performance. Add indexes if performance degrades.

The upsert driver should include every key whose target values may need recalculation. It may be slightly broader than necessary, provided it remains performant.

### Step 4—Test the minimal staging table

Join the upsert driver to the full query.

This creates the minimal staging table. It should contain only the rows that may need to be inserted or updated, while preserving the same business logic as the full query.

Check that the staging table is both correct and performant.

### Step 5—Build the delete driver

Build the delete driver separately from the upsert driver.

The delete driver should contain only rows that no longer satisfy the target query’s presence rule.

Special attention should be paid to performance because finding deletes often requires complex scans.

### Step 6—Simulate deletes before applying them

During development, simulate deletes with a `select` rather than immediately applying them.


The result set should be examined and compared with the correct result.

Simulating the delete reduces the risk of deleting data while the delete logic is being tested, causing rework to load the data again.


### Step 7—Apply changes through load mechanics

Apply the upserts and deletes through normal load mechanics.

The load should:

- compare staging rows with the target;
- apply only genuine inserts and updates;
- apply exact deletes;
- preserve history;
- record load statistics and bookmarks.

Then compare the incrementally maintained target with a fully loaded copy of the same target. The two should match.

### Step 8—Run a zero-load benchmark

After a successful load, rerun the upsert and delete drivers.

They should return no rows, or near zero rows, and should run quickly.

This is the fastest the incremental load can ever be. It is also a useful baseline for detecting unnecessary work.

### Step 9—Run incrementally over time

Continue loading incrementally over multiple days.

The full-load comparison test should continue to pass. If it fails, the incremental response logic is likely missing a source change condition, over-deleting, or failing to handle a query shape correctly.

## Using AI as a reviewer

Analysing source-change propagation through a complex query can be error-prone.

This is a useful place to use generative AI as a reviewer. A model can propose how source inserts, updates, and deletes may propagate through joins, filters, aggregations, anti-joins, and set operations.

A useful prompt is to provide the query shape, source keys, target key, and the possible source changes, then ask for:

- target keys to upsert;
- target keys to delete;
- reasons for each driver.

The output should then be tested against the full-load result.

## Conclusion

Tracking changes identifies which source rows changed. Responding to change determines what those source changes mean for the target.

The difficulty of incremental loading depends not only on data volume, but on query shape. Filters, joins, aggregations, anti-joins, window functions, and set operations all affect whether source changes become target upserts or deletes.

The standard pattern is to fetch the refresh bookmark, compute the upsert driver, create a minimal staging table from the normal query, compute the delete driver, and then apply normal load mechanics.

The complexity comes from analysing the query. Generative AI is helpful for this part.

Together, the two steps—tracking changes and responding to change—apply the principle of proportionate change.

> [!NOTE]
> **Key ideas**
>
> Tracking change identifies which source rows have changed. Responding to change determines what those source changes mean after they pass through the target query.
>
> Source actions do not map directly to target actions. A source insert can cause a target delete, a source delete can cause a target update, and a source update can cause a target insert.
>
> The query is the translation layer between source change and target action.
>
> A driver set contains the keys that may need action because upstream source rows changed.
>
> Upsert drivers identify rows to recalculate. They may be conservative, provided they remain performant.
>
> Delete drivers identify rows that no longer satisfy the target query’s presence rule. They must be exact.
>
> The goal of an incremental load is to apply proportionate computational change.