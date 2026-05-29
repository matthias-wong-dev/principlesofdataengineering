---
title: Designing measures
url: /docs/presenting-insights/designing-measures/
description: Learn how to design Power BI measures that compress fact-table content into business meaning and re-express it through user-selected dimensions.
lede: Measures compress facts into business meaning, then unpack that meaning in user context.
weight: 6
# draft: true
---

## Measures as compression and re-expression

A fact table may contain thousands, millions, or billions of rows. A measure compresses those rows into a business expression, then unpacks that expression again in user context.

A good measure therefore does not merely calculate correctly. It states clearly what business meaning is being compressed, and it behaves predictably as that meaning is re-expressed through the user’s selected dimensions.

Power BI’s implicit calculations can undermine this design. They encourage users to treat raw columns as ready-made measures, even when those columns do not express a clear business answer. For this reason, **Discourage implicit measures** should usually be turned on.

This chapter covers three areas:

- signs of good measures;
- interface roles of measures;
- technical patterns for building measures.

The next chapter, [Measure of measures](/docs/presenting-insights/measure-of-measures/), introduces a pattern for managing structured families of measures.

## Signs of good measures

There are two signs of good measures:

- business centricity;
- technical simplicity.

### Business centricity

A measure is not merely a calculation. It is a business expression made available to the user for unpacking.

Every aspect of a measure should reflect business meaning. This includes its definition, name, description, display folder, and placement alongside related measures.

#### Alignment to business reality

A measure should align with real-world events.

A common mistake is to count a database key and assume that the result is a meaningful business metric.

For example, a data engineer might define `[Inspection count]` as a distinct count of `[Inspection ID]` in the `'Inspection'` fact table. That may be fine if `[Inspection ID]` corresponds to a real inspection. But in many systems, `[Inspection ID]` is only a system-generated record key. It may exist for retrieval, workflow, or database convenience.

If the system later changes so that one real inspection is split into ten records, the measure changes even though inspection effort has not changed. Conversely, if ten records are merged into one, the measure falls even though no real-world activity has disappeared.

That is a measure misaligned with reality.

A better measure quantifies something with real-world business meaning. Depending on the scenario, the data engineer may measure:

- inspection hours;
- entities inspected.

The right choice depends on the business question.

Even `inspection` itself can be unreliable as the basis for a measure. If new inspection types are introduced that are much lighter or heavier than the old ones, then `[Number of inspections]` may drift in meaning over time.

By contrast, `[Total inspection hours]` remains close to concrete reality. An hour is still an hour, even when new inspections get added.

This does not mean `[Number of inspections]` is always wrong. The point is that the data engineer should understand what the measure is really compressing, and where possible, stay closer to concrete reality than abstraction.

#### Business specificity

Measures should be specific to the business question they answer.

A common misstep is to create a single generic measure and expect users to combine it with filters to answer every question.

For example, the model may contain a generic measure:

```DAX
Employee count =
distinctcount ( 'Employee end of month'[Employee ID] )
```

The data engineer may then expect users to filter manually for active employees, separated employees, employees on leave, current employees, and other cases.

This turns the model into a puzzle. Users must remember which filters to apply, which dates matter, and which status values are valid for each business question.

A better model presents specific measures that answer common business questions directly.

For example:

- `[Active employees end of period]`—employees with an active employment status at the end of the selected period.
- `[Separated employees end of period]`—employees with a separated employment status at the end of the selected period.
- `[Current employees]`—the latest value of `[Active employees end of period]`.
- `[Current employees on long service leave]`—current employees who are on long service leave.

These measures are not merely variants of `[Employee count]`. They are specific business expressions that make common questions directly available.

A technical measure such as `[_Employee count]` and `[_Employee count end of period]` may still be useful internally. If it is not useful to users directly, it should be hidden to support business-facing measures without cluttering the interface.

#### Names

Measure names should be explicit, grammatical, and able to stand alone.

Measures can be dragged anywhere on the canvas. Their names should carry enough context to remain meaningful outside their original folder or visual.

Prefer:

```md
[Active employees end of period]
```

over:

```md
[Count]
```

Avoid non-standard abbreviations. Saving a few characters does not help the user or the next engineer.

Names should also support search. Users often find measures by typing keywords in the field list. If the business calls something `commencements`, the measure name may include `commencements`. Anticipating the user search should be part of the measure design.

#### Descriptions

Descriptions should explain business meaning.

The description should not simply restate the DAX. Users are not asking for implementation trivia, nor should they be expected to accept complex logic without explanation. They want to know what the measure means and whether they can trust it.

For simple measures, a description may be short:

```md
Counts employees with an active employment status at the end of the selected reporting period.
```

For more complex measures, near-pseudocode in business language may be appropriate:

```md
Counts employees who were active at the end of the selected period and whose leave status indicates long service leave. Uses the latest reporting period in the current user context.
```

The description is part of the interface. It is often the first explanation the user sees, and an opportunity to build trust.

#### Display folders

Display folders help measures appear in business-facing groups.

Measures can be grouped by business process, such as:

- `Workforce`
- `Inspections`
- `Sales`
- `Refunds`

Technical or report-specific measures can be placed in folders such as:

- `Dashboard`
- `Display unit records`

#### Proximity to related measures

The meaning of a measure is influenced by nearby measures.

Related measures should be named so that they appear near each other.

For example:

- `[Active employees end of period]`
- `[Separated employees end of period]`
- `[Current employees]`
- `[Current employees on long service leave]`

The presence of `[Separated employees end of period]` reinforces the meaning of `[Active employees end of period]`. The presence of `[Current employees]` clarifies that `[Active employees end of period]` is a point-in-time measure.

These compare-and-contrast relationships help users form a clearer mental model of the data.

There are two practical forms of proximity:

- alphabetical placement within a display folder;
- keyword-based lookup in the field list.

A data engineer can take advantage of the proximity effect during measure naming and placement.

### Technical simplicity

Measures should be technically simple.

This does not mean every measure must be trivial. It means complex business logic should usually be pushed upstream into the data pipeline.

A measure should aggregate, filter, compare, or display information that is already well prepared.

There are two important foundations for technical simplicity:

- precomputing complex information;
- preparing binary flags.

#### Precomputing complex information

Complex business logic should usually be computed in the data layer.

This frees measures from carrying too much responsibility. A measure should not have to reconstruct a complicated business state every time a user clicks a slicer.

For example, suppose `[Is on long service leave]` requires analysing leave transactions, effective dates, overlapping periods, and employee status. That logic should usually be calculated in the pipeline and stored in a fragment such as `HR.EmployeeLeave` or a related reference table.

Then the measure can remain simple:

```DAX
Current employees on long service leave =
calculate (
    [Current employees],
    keepfilters ( 'Employee leave'[Is on long service leave] )
)
```

The complexity has been moved to the data layer, where it can be tested and reused.

Storytelling dimensions are an important example of this principle. When complex detail has been reduced into business-facing categories, paths, summaries, or special cases, measures can refer to those prepared structures instead of repeating the interpretation in DAX.

Precomputation can be overdone. If the data engineer precomputes too much, the model may lose interactivity. A pre-aggregated string may no longer respond correctly to filters. An average stored at the wrong grain may produce wrong results when aggregated again.

The rule is not “precompute everything.” The rule is:

> Precompute business interpretation when doing so preserves interactivity and simplifies the model.

The data engineer should understand the filtering behaviour of Power BI well enough to know which logic belongs in the pipeline and which logic belongs in a measure.

#### Preparing binary flags

Binary flags are true-or-false columns that express business logic clearly.

Their most common place is in reference tables and dimensions. For example, an `'Employee leave'` dimension may contain `[Is on long service leave]` to indicate whether the employee is on long service leave at the end of the reporting period.

Binary flags simplify measures.

Instead of writing a measure that filters text values directly:

```DAX
Current employees on long service leave =
calculate (
    [Current employees],
    keepfilters ( 'Employee leave'[Leave type] in { "Long service leave", "Extended long service leave" } )
)
```

The measure can use the prepared binary flag:

```DAX
Current employees on long service leave =
calculate (
    [Current employees],
    keepfilters ( 'Employee leave'[Is on long service leave] )
)
```

The reverse can be expressed with `not`:

```DAX
Current employees not on long service leave =
calculate (
    [Current employees],
    keepfilters ( not 'Employee leave'[Is on long service leave] )
)
```

Binary flags have two advantages.

First, they are syntactically checked. If a developer mistypes `Long service leave` as text, the formula may still be valid but return the wrong result. If the developer mistypes the column name `[Is on long service leave]`, the formula fails visibly.

Second, binary flags make the business logic readable. The measure says what it means.

Binary flags also participate cleanly in `and` and `or` logic. For example:

```DAX
Current employees on leave or acting =
calculate (
    [Current employees],
    keepfilters (
        'Employee status'[Is on leave]
            || 'Employee status'[Is acting]
    )
)
```

Using binary flags makes measures faster to write, easier to maintain, and easier to understand. The business logic has been named and surfaced in the model.

## Interface roles of measures

Measures do not all play the same role in the user experience. Some measures answer business questions directly. Some display contextual information. Some control whether rows appear. Some support the presentation of a dashboard.

These are interface roles. There are four common roles:

- aggregating measures;
- dimensional measures;
- filtering measures;
- dashboard measures.

### Aggregating measures

Aggregating measures are the measures most people think of first.

Examples include:

- `[Total sales amount]`
- `[Total inspection hours]`
- `[Average inspection duration]`
- `[Active employees end of period]`
- `[Median time to resolve]`

For measurable facts, aggregating measures may use functions such as `sum`, `countrows`, `distinctcount`, `averagex`, or `medianx`.

For end-of-period facts, they often need to identify the relevant reporting period before aggregating. For example, `[Current employees]` may evaluate `[Active employees end of period]` at the latest period in the current filter context.

Aggregating measures should usually be business-facing. They are the main way facts become visible to users.

### Dimensional measures

A dimensional measure turns dimension values into a measure result.

This sounds unusual because dimensions are normally used for grouping or filtering. But sometimes a user wants a dimension value displayed as a measure.

For example, in [Filtering behaviour](/docs/presenting-insights/filtering-behaviour/), the user may want to show all products refunded on a particular day. The product names come from `'Sales product'`, but the result is displayed as a measure.

A simplified example is:

```DAX
Refunded products =
calculate (
    concatenatex (
        values ( 'Sales product'[Product name] ),
        'Sales product'[Product name],
        ", "
    ),
    crossfilter ( 'Sales product'[Product SK], 'Refund'[Product SK], both )
)
```

This is not an aggregating measure in the normal sense. It is not summing or counting fact rows. It is retrieving dimension values under a particular filter context and turning them into display text.

Dimensional measures can be confused with dimension columns.

A dimension column such as `'Sales product'[Product name]` can be used in slicers, rows, columns, and cross-filtering.

A dimensional measure such as `[Refunded products]` cannot do the same thing. It is a displayed result. It does not provide the same interactive control.

Its chief purpose is display.

### Filtering measures

Filtering measures exist to control what appears.

As explained in [Filtering behaviour](/docs/presenting-insights/filtering-behaviour/), Power BI often retains visual rows where at least one measure returns a non-blank value. A measure can therefore be used as a filtering device.

Filtering measures typically return `1` or blank.

Examples include:

- `[Has sales]`
- `[Has refund]`
- `[Display sales transaction]`
- `[Display refund transaction]`

A simple filtering measure might be:

```DAX
Has sales =
if (
    countrows ( 'Sale' ) > 0,
    1
)
```

This can be added to a visual or used as a visual-level filter to show only products, dates, or IDs that have sales under the current filter context.

Display unit-record measures are a special case. They are used to control whether transaction records should appear. They may include functions such as `isinscope` to ensure that rows appear only when the relevant ID dimension is present.

Filtering measures are technical, but they still need business meaning. Their descriptions should explain how they are intended to be used.

### Dashboard measures

Dashboard measures support report presentation.

They may provide:

- dynamic titles;
- selected-value labels;
- data currency messages;
- conditional formatting values;
- colour rules;
- icons;
- arrows;
- warning messages.

For example:

```DAX
Selected product label =
if (
    hasonevalue ( 'Sales product'[Product name] ),
    selectedvalue ( 'Sales product'[Product name] ),
    "Multiple products"
)
```

Dashboard measures often inspect user context. They commonly use functions such as `selectedvalue`, `hasonevalue`, `isfiltered`, and `isinscope`.

## Technical patterns for measures

Most measures fall into a small number of technical patterns.

The first three fall under the standard case:

- base measures;
- derived measures;
- context-aware measures.

These patterns cover most ordinary scenarios.

Some measures become difficult because the model contains a more demanding semantic problem. The final part of this section discusses three advanced scenarios:

- polymorphic keys;
- embedded grain;
- unsupported relationships.

These are not measure types. They are situations where the data engineer must be especially clear about grain, meaning, and filter context.

The techniques in this section assume that the model has been prepared properly. They work best when the data engineer has preserved business keys, built useful dimensions, hidden facts, prepared binary flags, and created meaningful fragments in the pipeline.

If those foundations are missing, the same DAX patterns may become difficult or impossible to apply. A measure cannot recover a grain if the key for that grain has been discarded. It cannot express a business category if the category has never been modelled. It cannot follow a relationship path if the relevant identifier has not been preserved.

### Base measures

Base measures interact directly with fact tables.

They are the first layer of measure design. They should usually be simple, explicit, and reusable.

For example:

```DAX
Total sales amount =
sum ( 'Sale'[Sales amount] )
```

```DAX
Sales transaction count =
countrows ( 'Sale' )
```

```DAX
Total inspection hours =
sum ( 'Inspection'[Inspection duration hours] )
```

For end-of-period facts, base measures often include logic to select a reporting period.

For example, a current-state measure may select the latest period in context:

```DAX
Employees end of period =
var latest_period =
    max ( 'Reporting calendar'[Period end date] )
return
    calculate (
        distinctcount ( 'Employee end of month'[Employee ID] ),
        keepfilters ( 'Reporting calendar'[Period end date] = latest_period )
    )
```

The exact formula depends on the calendar design, but the pattern is common: identify the relevant period, then evaluate the base measure there.

For annotation facts, base measures may use `concatenatex` to display detail.

For example:

```DAX
Inspection comments =
concatenatex (
    'Inspection comments',
    'Inspection comments'[Comment text],
    " , ",
    'Inspection comments'[Comment sequence number]
)
```

Base measures should carry as little business complexity as possible. They should aggregate prepared facts and use prepared dimensions. For example, failed inspections should be:

```DAX
Failed inspection count =
calculate (
    [Inspection count],
    keepfilters ( 'Inspection outcome'[Is failed inspection] )
)
```

### Derived measures

Derived measures build on base measures.

They include ratios, rates, comparisons, rolling periods, and time-intelligence measures.

For example:

```DAX
Inspection failure rate =
divide ( [Failed inspection count], [Inspection count] )
```

Derived measures should usually be built from other measures rather than repeating base logic.

Population comparison measures are another important derived pattern. These measures escape part of the filter context to compare the current value with a larger population.

For example:

```DAX
National inspection count =
calculate (
    [Inspection count],
    removefilters ( 'Region' )
)
```

The meaning should be explicit. The user should understand which filters are removed and which remain.

### Context-aware measures

Context-aware measures inspect the user’s current selection and respond accordingly.

Dashboard measures are often context-aware, but aggregating and filtering measures can be context-aware too.

Common functions include:

- `selectedvalue`
- `hasonevalue`
- `isfiltered`
- `isinscope`
- `values`
- `isblank`

A report title may use:

```DAX
Sales title =
"Sales for "
    & if (
        hasonevalue ( 'Sales product'[Product name] ),
        selectedvalue ( 'Sales product'[Product name] ),
        "all products"
    )
```

A display measure may require an ID dimension before returning a value:

```DAX
Display sales transaction =
if (
    isinscope ( 'Sales ID'[Sales order number] )
        && countrows ( 'Sale' ) > 0,
    1
)
```

Context-aware measures are useful because Power BI users interact with the model in many sequences. A measure can inspect the current context and choose an appropriate response.

But context-aware logic should remain explainable. If a measure behaves differently in different visuals, its description should make that behaviour clear.

### Advanced scenario: polymorphic keys

Polymorphic keys occur when the meaning of one key column depends on another column.

For example, a business process may inspect travellers and bags. Both are recorded in the same `'Inspection'` fact table. A column such as `[Inspection item type]` has values such as `Traveller` and `Bag`. Another column, `[Inspected item SK]`, stores the inspected item key.

The meaning of `[Inspected item SK]` depends on `[Inspection item type]`.

**Example structure of `'Inspection'`**

| Inspection SK | Inspection item type | Inspected item SK |
|---:|---|---:|
| 1 | Traveller | 1001 |
| 2 | Traveller | 1002 |
| 3 | Bag | 1001 |
| 4 | Bag | 1003 |

A simple distinct count of `[Inspected item SK]` gives the wrong answer. It treats traveller `1001` and bag `1001` as the same item.

The correct logic must count distinct items within each item type, then add the results.

In a well-designed model, the determining column should usually be expressed in a dimension such as `'Inspection type'`. The measure can then group by the determining column.

Conceptually:

```DAX
Inspected item count =
var inspection_per_type =
    summarize (
        'Inspection type', -- group by dimension
        'Inspection type'[Inspection item type], -- on the polymorphic resolving column
        "Inspection count",
            distinctcountnoblank ( 'Inspection'[Inspected item SK] ) -- aggregating fact per segment
    )
return
    sumx ( inspection_per_type, [Inspection count] ) -- adds up the result from each segment
```

If additional filters are needed, `summarize` can be wrapped inside `calculatetable` with `keepfilters`.

New data engineers often solve this by concatenating item type and item key into a single artificial column. That can work, but it changes the model to solve a calculation problem. The approach above keeps the model stable and handles the polymorphism inside the measure.

The idea is similar to SQL: group by the resolving column, aggregate each segment, then aggregate the result.

### Advanced scenario: embedded grain

Embedded grain occurs when a table is physically stored at one grain, but contains enough repeated keys or attributes to recover another grain.

Power BI is more flexible than traditional dimensional modelling. A single fact table can sometimes contain detail rows with header-level values repeated on each row. This can be practical, but it creates a measure problem.

For example, suppose `'Inspection'` records inspections at the traveller level, but also contains bag results.

**Example structure of `'Inspection'`**

| Inspection SK | Traveller SK | Bag SK | Inspection duration minutes |
|---:|---:|---:|---:|
| 1 | 1001 | 501 | 45 |
| 1 | 1001 | 502 | 45 |
| 3 | 1002 | 503 | 30 |

The inspection duration for `SK = 1` is repeated on bag rows. If the data engineer averages or sums directly over `'Inspection'`, the row may be aggregated twice.

The solution is to reconstruct the intended grain before aggregating.

For example, to calculate median inspection duration per traveller:

```DAX
Median time to inspect traveller =
var inspection_time_per_sk =
    summarize (
        'Inspection',
        'Inspection'[Inspection SK],
        'Inspection'[Inspection duration minutes]
    )
return
    medianx (
        inspection_time_per_sk,
        [Inspection duration minutes]
    )
```

In SQL terms, this is similar to using `select distinct` on the columns that define the intended grain, then aggregating over that result.

ID dimensions can help because they preserve the keys needed to reconstruct the grain. This is another reason ID dimensions are powerful in Power BI models.

The broader lesson is that measures must know the grain of the thing being measured. If the grain is embedded inside a denormalised fact, the measure may need to recover it explicitly.

### Advanced scenario: unsupported relationships

Unsupported relationships occur when the standard single-direction dimension-to-fact relationship structure does not naturally support the required calculation.

The answer is not always to change the model. Sometimes the data engineer can use DAX to create the required filter path for one measure.

The most useful tools are:

- `crossfilter`
- `treatas`
- `userelationship`

`crossfilter` temporarily changes relationship direction for a calculation. As shown in [Filtering behaviour](/docs/presenting-insights/filtering-behaviour/), it can be used to retrieve dimension values through a relationship path that normally flows the wrong way.

`treatas` applies values from one table as though they filtered another table. It is powerful when the information is already in the model but no physical relationship exists.

For example, a refund table may need to retrieve the original sale amount through sales order numbers. If the default relationship path does not support the calculation, `treatas` may be used to apply the refund’s sales order numbers to `'Sale'` for that measure.

`userelationship` activates an inactive relationship for the duration of a calculation.

For example, suppose `'Calendar'[Date]` has an active relationship to `'Sale'[Order date]` and an inactive relationship to `'Sale'[Delivery date]`. A delivered-sales measure can activate the delivery-date relationship:

```DAX
Total delivered sales amount =
calculate (
    [Total sales amount],
    userelationship ( 'Calendar'[Date], 'Sale'[Delivery date] )
)
```

These functions are powerful because they allow specific measures to behave differently without changing the whole model.

They should be used deliberately. If many measures require complex relationship overrides, the model may need redesign. But when the exception is narrow and well understood, measure-defined filtering is often cleaner than adding confusing bidirectional relationships or distorting facts.

## Key ideas

> [!NOTE]
> **Key ideas**
>
> Measures compress fact-table content into business meaning, then unpack that meaning in user context.
>
> Good measures should be business-centric and technically simple.
>
> Business-facing measures should answer common questions directly rather than forcing users to memorise filter combinations.
>
> Complex business logic should usually be prepared in the data pipeline, reference data, binary flags, or storytelling dimensions.
>
> Measures can play different interface roles: aggregating, dimensional, filtering, or dashboard-oriented.
>
> Business keys help with difficult measure challenges by preserving recoverable meaning across time, grain, and modelling complexity.
>
> If measure logic becomes difficult to explain, the data engineer should consider whether the model or pipeline should be improved.
