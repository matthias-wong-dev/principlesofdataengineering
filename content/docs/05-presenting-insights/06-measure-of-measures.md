---
title: Measure of measures
url: /docs/presenting-insights/measure-of-measures/
description: Learn how to use switch measures in Power BI to model structured families of measures with a measure table and formatting calculation group.
lede: Sometimes the measures themselves have dimensional structure, and that structure should be modelled.
weight: 6
# draft: true
---

## Measures as a modelled structure

The previous chapter described measures as the face of facts. A measure compresses fact-table content into business meaning, then unpacks that meaning in user context.

This chapter extends that idea.

When the measures themselves have dimensional structure, that structure should be modelled.

The main idea is that a family of measures may have business dimensions of its own. Measures may vary by process stage, metric type, or reporting perspective. If these dimensions exist only inside measure names, the structure is hidden from the model.

A measure of measures makes this structure explicit.

This should be distinguished from other Power BI approaches that look similar on the surface: create a disconnected table of measure names, let the user choose a measure, and use a `switch` measure to return the selected result. That can be useful, but it is not the main idea here.

Instead, **measure of measures** refers to the modelling pattern of making the underlying structure of measures explicit for user interaction. The `switch` measure is only one component of that pattern.

## The problem

Consider a company that manages three operational stages:

- Manufacture
- Orders
- Shipping

Each stage has three operational metrics:

- Process volume
- Median time to process
- Volume processed on schedule

This creates nine base measures. 

These measures have a clear two-axis structure:

- Process stage
- Metric


| Process stage | Metric | Base measure |
|---|---|---|
| Manufacture | Process volume | `[Manufacture process volume]` |
| Manufacture | Median time to process | `[Manufacture median time to process (days)]` |
| Manufacture | Volume processed on schedule | `[Manufacture volume processed on schedule]` |
| Orders | Process volume | `[Orders process volume]` |
| Orders | Median time to process | `[Orders median time to process (days)]` |
| Orders | Volume processed on schedule | `[Orders volume processed on schedule]` |
| Shipping | Process volume | `[Shipping process volume]` |
| Shipping | Median time to process | `[Shipping median time to process (days)]` |
| Shipping | Volume processed on schedule | `[Shipping volume processed on schedule]` |

That structure matters to business intent. A manager may want to compare process volume across stages. Another may want to see whether time to process is deteriorating across years. Another may want to view operational performance by stage and metric in a single matrix.

If the structure exists only in measure names, the user cannot interact with this structure directly. The report builder has to manually place many separate measures into visuals and repeat derived logic.

Moreover, the complexity quickly explodes. For example, if two additional concepts need to be measured:

- Percentage processed on schedule
- National comparison

Calculating percentage processed on schedule for each process stage leads to 3 additional measures and 12 total. If national versions are created for all 12, the total becomes 24.


## The measure of measures pattern

The measure of measures pattern introduces four elements:

1. A measure table
2. A switch measure
3. Derived measures
4. A formatting calculation group


### Step 1—Create a measure table

The measure table is a small table that lists the measures and annotates them with business attributes.

In this example, create a table called `'Operational metric'`.

**Example structure of `'Operational metric'`**

| Operational metric SK | Measure name | Process stage | Process stage display order | Metric | Metric display order |
|---:|---|---|---:|---|---:|
| 1 | Manufacture process volume | Manufacture | 1 | Process volume | 1 |
| 2 | Manufacture median time to process (days) | Manufacture | 1 | Median time to process | 2 |
| 3 | Manufacture volume processed on schedule | Manufacture | 1 | Volume processed on schedule | 3 |
| 4 | Orders process volume | Orders | 2 | Process volume | 1 |
| 5 | Orders median time to process (days) | Orders | 2 | Median time to process | 2 |
| 6 | Orders volume processed on schedule | Orders | 2 | Volume processed on schedule | 3 |
| 7 | Shipping process volume | Shipping | 3 | Process volume | 1 |
| 8 | Shipping median time to process (days) | Shipping | 3 | Median time to process | 2 |
| 9 | Shipping volume processed on schedule | Shipping | 3 | Volume processed on schedule | 3 |

This table is not a fact table. It is also not a normal business dimension over transactional data. It is a dimension over the measures themselves.

With the table, the model now knows that `[Manufacture process volume]`, `[Orders process volume]`, and `[Shipping process volume]` are the same kind of metric applied to different process stages.

The display order columns are important. Alphabetical order is rarely the same as business order. For example, `[Process stage]` is in order of manufacture, orders, and shipping.

### Step 2—Create a switch measure

The switch measure returns the correct base measure depending on the selected row in `'Operational metric'`.

A simplified version of the measure `[Operational metric]` looks like this:

```DAX
Operational metric =
var selected_metric =
    selectedvalue ( 'Operational metric'[Measure name] )
return
    switch (
        selected_metric,
        "Manufacture process volume", [Manufacture process volume],
        "Manufacture median time to process (days)", [Manufacture median time to process (days)],
        "Manufacture volume processed on schedule", [Manufacture volume processed on schedule],
        "Orders process volume", [Orders process volume],
        "Orders median time to process (days)", [Orders median time to process (days)],
        "Orders volume processed on schedule", [Orders volume processed on schedule],
        "Shipping process volume", [Shipping process volume],
        "Shipping median time to process (days)", [Shipping median time to process (days)],
        "Shipping volume processed on schedule", [Shipping volume processed on schedule]
    )
```

The measure table provides the selection. The switch measure provides the value.

The ordinary underlying measures can be called base measures. They calculate directly from facts or from ordinary dimensional context. The switch measure is the first measure that operates over the structure of those base measures.

### Step 3—Define derived measures

Once the switch measure exists, the data engineer can define derived measures over the structure of the measure table.

Suppose the business wants percentage processed on schedule. Without a measure of measures, the data engineer may create one percentage measure per process stage:

- `[Manufacture percentage processed on schedule]`
- `[Orders percentage processed on schedule]`
- `[Shipping percentage processed on schedule]`

With the measure table, the data engineer can define a more general derived measure.

For example, the model may contain these derived measures:

```DAX
Process volume =
calculate (
    [Operational metric],
    keepfilters ( 'Operational metric'[Metric] = "Process volume" )
)
```

```DAX
Volume processed on schedule =
calculate (
    [Operational metric],
    keepfilters ( 'Operational metric'[Metric] = "Volume processed on schedule" )
)
```

The percentage measure can then be written once:

```DAX
Percentage processed on schedule =
divide (
    [Volume processed on schedule],
    [Process volume]
)
```

A national comparison can also be written once:

```DAX
National operational metric =
calculate (
    [Operational metric],
    removefilters ( 'Region' )
)
```

The same measure works across process stages because `[Process stage]` remains in the filter context.

For example, when the process stage is filtered to `Manufacture`, `[Process volume]` resolves to `[Manufacture process volume]`, and `[Volume processed on schedule]` resolves to `[Manufacture volume processed on schedule]`.

When the process stage is filtered to `Orders`, the same measure resolves to the order measures.

### Step 4—Handle formatting

A switch measure does not automatically preserve the original format of each underlying measure.

In practice, this can be handled with a calculation group or another dynamic format-string pattern.

A simplified format string expression may look like this:

```DAX
switch (
    selectedvalue ( 'Operational metric'[Measure name] ),
    "Manufacture process volume", "#,0",
    "Orders process volume", "#,0",
    "Shipping process volume", "#,0",
    "Manufacture median time to process (days)", "#,0.0",
    "Orders median time to process (days)", "#,0.0",
    "Shipping median time to process (days)", "#,0.0",
    "Manufacture volume processed on schedule", "#,0",
    "Orders volume processed on schedule", "#,0",
    "Shipping volume processed on schedule", "#,0",
    selectedmeasureformatstring ()
)
```

The exact implementation depends on the model and the calculation group design. The important point is that dynamic measure selection also requires deliberate formatting design.

Without this step, the measure of measures may return correct numbers but display them poorly.

> [!NOTE]
> In practice, long `switch` measures and matching format-string expressions should usually be generated by code when this pattern is used regularly.

## Benefits

The measure of measures pattern has several benefits.

### Simplified DAX management

Instead of repeating similar logic across many measures, the data engineer can define reusable derived measures.

This reduces duplication and lowers maintenance cost. In some cases, it is the only viable solution without creating a tangle of DAX definitions or nightmare reports.


### Explicit business structure

The measure table expresses the structure of the metrics directly.

Process stage, metric, display order, and other annotations become part of the model rather than being hidden inside measure names.

For example, a matrix can place `[Metric]` on rows, `[Process stage]` on columns, and `[Operational metric]` as the value.

| Metric | Manufacture | Orders | Shipping |
|---|---:|---:|---:|
| Process volume | 12,400 | 11,850 | 11,200 |
| Median time to process | 2.1 | 1.4 | 3.8 |
| Volume processed on schedule | 11,780 | 10,960 | 9,520 |

The numbers are returned by different underlying measures, but the row and column structure comes from `'Operational metric'`.

This visual is difficult to build with separate measures. 

### More powerful reporting

The third benefit is powerful reporting. A visual can place `[Process stage]` and `[Metric]` on rows, `[Reporting year]` on columns, and `[Operational metric]` as the value.

| Process stage | Metric | 2022 | 2023 | 2024 |
|---|---|---:|---:|---:|
| Manufacture | Process volume | 10,800 | 11,600 | 12,400 |
| Manufacture | Median time to process | 2.4 | 2.2 | 2.1 |
| Manufacture | Volume processed on schedule | 9,900 | 10,850 | 11,780 |
| Orders | Process volume | 10,200 | 11,100 | 11,850 |
| Orders | Median time to process | 1.7 | 1.5 | 1.4 |
| Orders | Volume processed on schedule | 9,300 | 10,100 | 10,960 |
| Shipping | Process volume | 9,800 | 10,600 | 11,200 |
| Shipping | Median time to process | 3.2 | 3.5 | 3.8 |
| Shipping | Volume processed on schedule | 8,950 | 9,350 | 9,520 |

This gives the business a compact view of many measures across time. For example, shipping volume is increasing, but median time to process is also deteriorating. Conditional formatting can then highlight deterioration or improvement.

There are many ways to use the structure expressed by `'Operational metric'`. The `[Process stage]` column can be used for small multiples in line charts, creating a series of visuals in a controlled and automated manner. It can also serve as a legend to compare metrics directly, such as identifying lags or discrepancies in `[Process volume]` between manufacture, orders, and shipping.

If each process is managed by a different team, `[Process stage]` can be used as a report page filter to tailor the view to each manager’s concern.

Used appropriately, the measure of measures enables powerful reports that would otherwise be impractical or impossible.

### Avoiding awkward fact-table unions

Inexperienced data engineers sometimes try to solve the same problem by forcing fact tables into an awkward union so that different process stages can appear as rows in a single table.

That may be appropriate in some models, but not always. If the processes are genuinely different and already have good measures, it may be better to structure the measures rather than reshape the facts.

The measure of measures allows users to operate on the measures directly. It is a form of [horizontal integration](/docs/creating-information/conforming-systems/) when vertical integration of the underlying facts is not appropriate.

## Dangers

The measure of measures pattern is powerful, but it should be used judiciously.

### Performance

Large `switch` measures can perform poorly, especially when the selected field is not the same column used by the switch.

For example, performance may be worse when the visual filters on `[Metric]` or `[Process stage]`, but the switch branches on `[Measure name]`.

With many branches, performance should be tested in practice.

### Dynamism for its own sake

Dynamism can be overused.

In theory, any list of measures can be placed into a switch. That does not mean it should be done.

The criterion is business expressiveness. The pattern is appropriate when the measures form a coherent structure: process stages, business lines, quality criteria, product families, or similar.


### Hiding important information behind clicks

A dynamic report is not automatically a good report.

If users must keep clicking before they can see what matters, the report may be poorly designed. A report with ten selectable metrics is often less intuitive than a report that shows the important comparisons directly.

The measure of measures should be used to create explicitly expressive visuals, not to hide information behind unnecessary interaction.

### Ambiguous aggregation across measures

The measure table often has a composite key. In the example above, `[Process stage]` and `[Metric]` together identify a specific measure.

If the user selects `[Metric] = Process volume` without selecting `[Process stage]`, the switch measure returns blank. This is often correct. The default behaviour prevents summing over items that should not be summed.

If aggregation across measures is required, it should be explicitly defined and tailored to the metric.

## Relationship to switch measures

Many discussions of `switch` measures in Power BI focus on technical convenience: allowing users to choose a measure from a slicer, reducing visual clutter, or reusing a visual for different metrics.

Those uses can be valid, but they are not the main point here.

A measure of measures is not a slicer trick. It is a modelling technique for expressing business intent. The measure table allows the data engineer to:

- make business metrics explicit and navigable;
- build structured visuals by metric and process;
- define derived measures without duplication.

Without anchor in business meaning, dynamic measure selection can easily become frustrating. The model may become clever, but not clearer.

## Key ideas

> [!NOTE]
> **Key ideas**
>
> Sometimes the measures themselves have dimensional structure, and that structure should be modelled.
>
> Measures can themselves be modelled as a business object.
>
> A measure of measures is useful when measures have a coherent structure, such as process stage by metric.
>
> The important idea is not merely that a `switch` measure can change what is displayed. The important idea is that the measure family may have dimensional structure worth modelling.
>
> The pattern uses a measure table, a switch measure, derived measures, and usually a formatting calculation group.
>
> The measure table makes the structure of the measures explicit rather than hiding it in measure names.
>
> Derived measures can often be written once because the process or metric structure is carried by the measure table.
>
> The pattern should be used for business expressiveness, not dynamism for its own sake.
>
> Aggregating across measures must be defined deliberately. Blank results are often a useful safeguard against accidental nonsense.