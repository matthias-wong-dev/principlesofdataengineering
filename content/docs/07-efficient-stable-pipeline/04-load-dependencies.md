---
title: Load dependencies
url: /docs/efficient-stable-pipeline/load-dependencies/
description: Explains how load dependencies affect efficiency and stability, and how to decide when a dependency is worth creating.
lede: Every dependency is a trade-off between reuse, efficiency, and stability.
weight: 4
# draft: true
---

## Dependency as coupling

A dependency occurs when one object relies on another object for information or logic.

Dependencies are useful because they allow the warehouse to reuse information. A table can calculate a piece of meaning once, persist it, and allow downstream tables to build on it. This improves efficiency because the same information does not need to be recalculated repeatedly. It also improves quality because the same logic is not copied into many places where it can drift out of sync.

But a dependency is also coupling.

When one table depends on another, change can propagate. A failure upstream can affect downstream tables. A small logic change upstream may require many downstream tables to reload. A small reference-data change can trigger large downstream updates.

What improves reuse can also reduce stability.

Therefore:

> [!SHARE:dependency-trade-reuse]
> Every dependency is a trade-off between reuse, efficiency, and stability.

The data engineer therefore has to decide when a dependency is worth creating.

## Load dependencies and view dependencies

Dependencies occur in two important ways.

A **load dependency** occurs when a materialised table selects from another table during its load.

A **view dependency** occurs when a view selects from another table or view.

Both propagate information through the warehouse, but they do so differently.

| Dependency type | What it propagates |
|---|---|
| Load dependency | Persisted information |
| View dependency | Logic |

Load dependencies propagate persisted information. The downstream table stores the result of the dependency at load time.

View dependencies propagate logic. The downstream object does not store the result. Instead, the join, filter, or calculation is evaluated when the view is queried.

This chapter focuses on load dependencies. Whenever the word **dependency** is used in this chapter, it refers to a load dependency unless otherwise stated.

Views are discussed later as an alternative to load dependencies.

## The dependency trade-off

At every turn, the data engineer chooses between recalculating information and reusing existing information.

Recalculation avoids coupling, but may repeat logic or waste compute. Reuse improves efficiency and consistency, but creates a path for upstream change to propagate downstream.

The decision depends on whether the value of reuse exceeds the cost of coupling. This can be determined by the rule:

> [!SHARE:dependency-valuable-targeted]
> A dependency should be valuable, targeted, and stable.

| Criterion | Question |
|---|---|
| Valuable | Is the information worth reusing rather than recalculating? |
| Targeted | Is the dependency narrow enough to match the actual purpose? |
| Stable | Will small source changes avoid causing disproportionate downstream change? |

## Valuable dependencies

A dependency should carry information worth reusing.

Using dependencies to propagate information is convenient in the short term. This can lead data engineers to create dependencies casually. The problem may not appear immediately. It surfaces later, when the pipeline becomes harder to reload, debug, or change.

The first test is therefore value.

A dependency is valuable when the source table contains information that is expensive, difficult, important, or risky to recalculate.

A dependency is weak when it exists only for convenience.

For example, a transaction table may select a country name from a reference table simply for display or debugging. This may be convenient, but it often creates unnecessary coupling. The transaction table may only need the country code. The country name can be joined later in the presentation layer, or exposed through a view.

Another example is the use of standard default values. Suppose the surrogate key for unknown values is always `1`. A transaction table can assign `1` directly for unknown references, rather than joining to a reference table to retrieve the unknown surrogate key by name. The hardcoded value is safe because it is a stable convention, not a fragile business rule.

The principle is simple:

> Do not create a dependency for information that is cheap, obvious, and stable enough to calculate locally.

Dependencies should be reserved for information that is worth propagating.

## Targeted dependencies

A dependency should be targeted.

A targeted dependency selects from a source table whose informational purpose matches the dependency being created.

An untargeted dependency selects from a broad table that contains many unrelated columns. This creates more coupling than necessary.

The smallest unit of load dependency is a table. If a downstream table selects one column from a source table, it depends on the source table as a whole. This means wide miscellaneous tables create broad dependency surfaces.

For example, suppose there is a table called `Cake.Everything`.

It contains:

- cake sales;
- cake milestones;
- cake quality scores;
- cake production notes;
- cake marketing categories;
- cake seasonal flags.

If many tables select from `Cake.Everything`, then many tables depend on it. A change to one concept in `Cake.Everything` may force downstream work that has nothing to do with that concept. The dependency graph becomes tangled because it is unclear what information is being passed downstream.

Meaningful fragments reduce this problem.

Instead of `Cake.Everything`, the pipeline could create:

- `Cake.Sales`
- `Cake.Milestone`
- `Cake.Quality`
- `Cake.Season`

A downstream table that needs sales information can depend on `Cake.Sales`. A downstream table that needs quality information can depend on `Cake.Quality`.

The dependency becomes more targeted because the source table has a narrower informational purpose.

This is one reason it is often better to create a new fragment than to add a new column to an existing table, especially when the new column introduces a different concept.

For example, suppose `Cake.RefCalendar` describes dates. A data engineer may need to identify sales seasons. It may be tempting to add `[Is sales season]` to `Cake.RefCalendar`.

That may be acceptable for display. But if sales season becomes part of analytical computation, adding it to `Cake.RefCalendar` increases the dependency weight of the calendar table. Downstream tables interested only in sales seasons now depend on the whole calendar reference.

A better design may be to create `Cake.RefSaleSeason`, keyed by `[First date of week]`, because sales seasons operate at the week grain. Downstream tables that need sales seasons can depend on `Cake.RefSaleSeason`. The dependency is clearer, narrower, and more targeted.

The principle is:

> A dependency should point to the smallest meaningful fragment that carries the required information.

## Stable dependencies

A dependency should be stable.

Stability means that small changes in the source should not create disproportionate downstream change.

A common example is a transaction table that stores a country name from a reference country table. If the country name changes, that single reference-data update may trigger millions of downstream transaction updates.

The underlying business event is small: one name changed.

The data-world effect is large: many rows update.

This is dependency instability.

Where possible, unstable dependencies should be avoided. Where they cannot be avoided, their risk should be understood and mitigated.

There are two common forms of instability:

| Instability type | Description |
|---|---|
| Row-wise instability | One source row affects many downstream rows. |
| Column-wise instability | A source column changes frequently or for reasons unrelated to business meaning. |

### Row-wise instability

Row-wise instability occurs when a small number of source rows drive many downstream rows.

Reference tables are the most common example. A single row in a reference table may be used by millions of transaction rows. If that reference row changes, the downstream impact can be large.

For example, if a transaction table denormalises `[Country name]` from `Reference.Country`, then a name change in `Reference.Country` can update every transaction row for that country.

This may be unnecessary.

The transaction table may only need `[Country code]`. The name can remain in the reference table and be joined later for presentation.

The same principle applies more generally. Information that describes a reference entity should usually remain on the reference table unless there is a strong reason to materialise it downstream.

Row-wise instability can also occur with metadata-driven loads. If a pipeline reads a metadata table to decide what to load, an error in that metadata can cascade into widespread change. The metadata table may be small, but it controls a large execution surface.

Small tables are often sources of instability because one row can affect many downstream rows.

This does not mean small tables should never be dependencies. It means the data engineer should be careful when a small table is used to drive large downstream effects.

### Column-wise instability

Column-wise instability occurs when the source column itself is volatile.

For example, selecting `[Update datetime]` into a downstream table can introduce instability. A source system may refresh update timestamps across many rows as part of routine maintenance. From the application’s point of view, little has changed. From the pipeline’s point of view, every row may appear to have changed.

The same problem can occur with columns such as `[Is archived]`, `[Last viewed datetime]`, or other operational fields that can be updated in bulk.

These columns may matter for the source system, but they may not represent meaningful business change for the warehouse.

A dependency on such a column can cause false downstream changes. It can make stable business information appear unstable.

The mitigation is to separate change detection from business meaning. If a volatile column is only needed for polling or extraction, it should not necessarily be propagated downstream as information. Techniques for managing this are discussed in [Tracking changes](/docs/efficient-stable-pipeline/tracking-changes/#the-role-of-the-filter-step).

The principle is:

> Do not propagate volatile columns unless their volatility is meaningful to the downstream table.

## The case of surrogate keys {#surrogate-key-encoding}

Surrogate keys are a special case of dependency.

A surrogate key is a stand-in for the primary key of a table. It is usually a single integer used in place of a natural or composite key.

Surrogate keys are useful in a warehouse for several reasons.

First, Power BI relationships use single-column relationships. If the natural key consists of multiple columns, a surrogate key may be required to implement the relationship cleanly.

Second, composite keys can be clumsy to carry. This is especially true for storytelling dimensions where the primary key may consist of many binary columns. Carrying ten columns across transaction tables is awkward, and joining on all ten repeatedly is error-prone.

Third, some keys are slow or difficult to join on. Type II dimensions often require inequality joins across validity periods, such as `[Start datetime]` and `[End datetime]`. Long string keys can also be slow or cumbersome.

For these reasons, it is often desirable to retrieve a surrogate key. This involves looking up the table using its primary key and selecting the surrogate key column. In this way, surrogate key retrieval can be a valuable dependency.

However, surrogate keys can also become magnets for dependency.

If downstream tables store a surrogate key, they depend on the table that generated it. If that table is rebuilt and the surrogate keys are regenerated, downstream key values may reshuffle. This can force large reloads and create instability.

There are two main ways to manage this.

The first is to defer the surrogate key lookup until later in the pipeline. If the original business key is simple and join performance is acceptable, downstream tables can carry the business key for longer. The surrogate key can be added only when needed for the semantic model or final presentation layer.

The second is to compute the surrogate key rather than look it up.

For example, suppose a storytelling dimension has five binary columns as its primary key:

- `[Is A]`
- `[Is B]`
- `[Is C]`
- `[Is D]`
- `[Is E]`

If each column is either `0` or `1`, the surrogate key can be calculated with a stable formula:

`[SK] = 1 + [Is A] + 2 * [Is B] + 4 * [Is C] + 8 * [Is D] + 16 * [Is E]`

The same principle can be extended beyond binary flags. The weights are calculated cumulatively. The first field has weight `1`. Each later field has a weight equal to the number of combinations created by all the fields before it.

For example, suppose a dimension contains:

- `[Is A]`, with values `0` and `1`
- `[Is B]`, with values `0` and `1`
- `[Apple]`, with values `0`, `1`, and `2`
- `[Orange]`, with values `0`, `1`, and `2`

The cardinalities are `2`, `2`, `3`, and `3`.

The weights are:

| Field | Cardinality | Weight |
|---|---:|---:|
| `[Is A]` | 2 | 1 |
| `[Is B]` | 2 | 2 |
| `[Apple]` | 3 | 4 |
| `[Orange]` | 3 | 12 |

The surrogate key can therefore be calculated as:

`[SK] = 1 + [Is A] + 2 * [Is B] + 4 * [Apple] + 12 * [Orange]`

This produces `2 × 2 × 3 × 3 = 36` possible keys, from `1` to `36`, with no collisions.

This method—called mixed radix key—gives each combination a stable integer without requiring a lookup. The downstream table gets the benefit of a surrogate key without forming a dependency on a generated key table.

This approach only works when the surrogate key can be computed safely and permanently. Many surrogate keys cannot be managed this way. But when the logic is simple and stable, calculation may be better than lookup.

The principle is:

> A surrogate key dependency is justified when the value of the simplified key exceeds the coupling risk created by the lookup.

## Views as an alternative

Views can sometimes avoid load dependencies.

A load dependency propagates persisted information.

A view dependency propagates logic.

For example, instead of denormalising `[Country name]` into a transaction table, a view can join the transaction table to `Reference.Country` at query time. If the country name changes, no downstream transaction table needs to reload. The updated name appears when the view is queried.

This can be useful when:

- query performance is acceptable;
- instant propagation of source changes is acceptable;
- the result does not need to be persisted;
- long-term historical retention is not required;
- downstream processes do not need row-level change tracking.

Views are especially useful in presentation scenarios. If a user is querying a small section of data through a report, it may be unnecessary to materialise every display attribute into a downstream table.

But views are not a complete substitute for loaded tables.

Views can propagate errors instantly. If the source table contains a bad value, the view exposes it immediately. A materialised table can provide a buffer because it changes only when loaded.

Views also do not track row-level change. As explained in [Load mechanics](/docs/efficient-stable-pipeline/load-mechanics/#check-for-genuine-changes), the Check step of a load determines whether a row has genuinely changed. This allows downstream tables and processes to respond precisely to inserts, updates, and deletes. A view does not provide this kind of change event.

Views also do not preserve history when source systems delete old records. If a view points to a source that no longer contains a record, the view cannot recover it. A materialised warehouse table can preserve the information.

The choice between a load dependency and a view dependency is therefore another trade-off.

| Use a load dependency when | Use a view when |
|---|---|
| The result should be persisted. | The result can be calculated at query time. |
| Downstream processes need change tracking. | Downstream processes only need current logic. |
| Historical retention matters. | Historical retention is not required. |
| Query performance requires materialisation. | Query performance is acceptable without materialisation. |
| A controlled loading buffer is valuable. | Instant propagation is acceptable. |

## Healthy dependency depth

The previous chapter showed how a load stack can make dependency orchestration manageable. That capability is powerful, but it also creates a second-order risk.

Once dependencies are easy to orchestrate, they can grow too freely.

A load stack prevents the pipeline from becoming tangled by execution order. It does not decide whether each dependency is valuable, targeted, and stable. That judgement still belongs to the data engineer.

A good pipeline should contain a healthy level of dependencies.

This may seem counterintuitive after a chapter about dependency risk, but a pipeline with almost no dependencies is usually not mature. It may reflect a garbage-in, garbage-out approach where raw tables are merely copied forward. It may also mean that complex transformation logic has been buried in scripts rather than expressed as reusable data products.

Dependencies are how the warehouse accumulates meaning.

A source system with 10 to 20 raw tables may produce 5 or 6 layers of dependency in the transformation pipeline. A larger system with 30 to 50 tables, especially when integrated with other systems, may produce 10 or more layers.

> [!SHARE:right-dependencies]
> The aim is not to minimise dependencies, but to create the right ones.


A healthy dependency is valuable, targeted, and stable. It propagates meaningful information without creating unnecessary ripple effects.

> [!NOTE]
> **Key ideas**
>
> Every dependency is a trade-off between reuse, efficiency, and stability.
>
> A load dependency occurs when a materialised table selects from another table during its load.
>
> Load dependencies propagate persisted information; view dependencies propagate logic.
>
> Dependencies improve efficiency and quality by allowing information and logic to be reused.
>
> Dependencies reduce stability when small upstream changes cause disproportionate downstream reloads or updates.
>
> A dependency should be valuable, targeted, and stable.
>
> Wide miscellaneous tables create broad dependency surfaces and should often be split into meaningful fragments.
>
> Surrogate keys are useful dependencies, but can become unstable if they are regenerated.
>
> Views can avoid materialised reloads by propagating logic rather than persisted information, but they do not provide the same buffering, persistence, or row-level change tracking as loaded tables.
