---
title: Dimensional modelling for UX
url: /docs/presenting-insights/dimensional-modelling-for-ux/
description: Learn how facts, dimensions, filtering, and interaction patterns shape the user experience of a Power BI dimensional model.
lede: In an interactive model, dimensions are what users touch; facts are what respond.
weight: 4
---

## Facts and dimensions as interaction

Dimensional modelling is usually taught as a distinction between table types—facts record activity; dimensions provide context. 

That distinction is correct, but not enough to achieve the expectations of a [good dimensional model](/docs/presenting-insights/a-good-dimensional-model/). The more important distinction is between what the user can touch and what responds—dimensions are what the user touches; facts are what respond.

A model is good when the user can answer questions without guessing. This chapter explains facts and dimensions from that point of view. That is, dimensional modelling for user experience (UX).

## Understanding facts and dimensions

Classical dimensional modelling revolves around two core concepts: facts and dimensions.

In a technical view:

- Facts are transactions, events, or activities that occur in the business.
- Dimensions are reference tables that provide context for those transactions.

Fact tables are fast-moving tables. They grow quickly, have high cardinality, and record frequent business activity. Dimension tables are slower-moving tables. They have lower cardinality and provide meaningful categories for filtering, grouping, and comparison.

From the business view:

- Facts are business processes. They convey action, such as manufacture, order, shipping, inspection, payment, or case handling.
- Dimensions are business objects, attributes, or categories. They convey context, such as product, region, customer, officer, status, or date.

A common explanation says that dimensions filter facts. This is true, but it hides the practical point: filtering is a form of control.

###  An analogy of robots

To make the distinction concrete, think of dimensions as levers and facts as robots.

If filtering is a form of control, then:

1. Levers control robots.
2. Levers may control other levers.
3. Robots may occasionally control other robots.
4. Robots should not control levers.

This analogy helps reinforce a key design principle: interactivity should be driven by dimensions.

Levers are what users control. Robots are what respond. In the same way, dimensions are the user’s interface to the model, while facts contain the machinery that responds to that interaction.

This is also why the controls should not sit on the robots themselves. They should sit on the controller. In practical terms, users should interact with dimensions to drive filtering, grouping, searching, comparison, and other model effects—not with columns embedded in fact tables.

This is the main problem with degenerate dimensions. They may work technically, but they place controls inside the fact table. They make the robot carry its own levers.

For this chapter, we stick with the simpler view of dimensions as tables.

But the wider principle is more general. A dimension is not merely a lookup table. It is anything in the model the user interacts with to produce an effect.

In more advanced scenarios, a dimension may function more like a button than a filter. The user clicks or selects it, and the model responds. The fact tables contain the ingredients that make the response possible.

In this view, the physical relationship pattern is secondary. A dimension may have one relationship, many relationships, or no direct relationship to a fact table. It may work alone, or as part of a set of tables. What matters is that the user interacts with it to produce a controlled effect. If it does that, it is functioning as a dimension.

This abstract view is useful when tackling demanding usage scenarios.

## A repertoire of facts and dimensions

The categories below are not a complete taxonomy of dimensional modelling. They are a practical repertoire for handling usage scenarios. They name the roles tables can play when a model is designed for interaction.

There are 3 types of facts and 9 types of dimensions.

Facts:

1. Measurable fact
2. End-of-period fact
3. Annotation fact

Dimensions:

1. Business dimension
2. Role-playing dimension
3. Histogram dimension
4. Combination dimension
5. Choices dimension
6. Sankey dimension
7. Storytelling dimension
8. Search dimension, a sub-type being the ID dimension
9. Degenerate dimension

## Facts

Facts are the responsive machinery of the model. They contain business activity, business state, or display detail that becomes visible when the user interacts with dimensions.

### Measurable fact

A **measurable fact** records business activity that can be counted, summed, averaged, or otherwise aggregated.

Examples include inspections, sales, orders, payments, helpdesk cases, audit events, or shipments. These are the facts people usually mean when they talk about fact tables.

A measurable fact is designed to work through measures. Users should normally not consume the raw fact table directly. They should interact with dimensions, and the fact should respond through measures such as inspection count, failure rate, total value, or average processing time.

**Example structure of `'Inspection'`**

| Inspection SK | Inspection date | Location SK | Officer SK | Inspection status SK | Inspection duration minutes |
|---:|---|---:|---:|---:|---:|
| 1001 | 2024-01-15 | 12 | 31 | 1 | 45 |
| 1002 | 2024-01-16 | 18 | 44 | 2 | 70 |

This fact can support measures that use functions such as `COUNTROWS`, `SUMX`, and `COUNTX`. The user interacts with dimensions such as `'Location'`, `'Officer'`, and `'Inspection status'`. The measures respond from `'Inspection'`.


This example is at the grain of a single inspection, but a measurable fact does not have to be at event grain. It may already be aggregated before it reaches the model. What matters is not the physical grain of the table, but the role it plays: it supplies measurable material for measures to calculate against and for dimensions to control.

**Example structure of `'Inspection daily aggregates'`**

| Inspection date | Location SK | Inspection status SK | Inspection count | Total inspection duration minutes | Failed inspection count |
|---|---:|---:|---:|---:|---:|
| 2024-01-15 | 12 | 1 | 18 | 720 | 0 |
| 2024-01-15 | 18 | 2 | 7 | 490 | 7 |
| 2024-01-16 | 12 | 1 | 22 | 860 | 0 |

This is also a measurable fact. It is not at the grain of a single inspection. It has already been aggregated by inspection date, location, and inspection status before it reaches the model.

The measures still respond from the fact. A measure may sum `[Inspection count]`, divide `[Failed inspection count]` by `[Inspection count]`, or calculate average duration from `[Total inspection duration minutes]` and `[Inspection count]`.

The physical grain is different, but the modelling role is the same: `'Inspection daily aggregates'` supplies measurable material for measures to calculate against and for dimensions to control.


Measurable facts are the default facts for [entity processing](/docs/creating-information/entity-processing/) scenarios.

### End-of-period fact

An **end-of-period fact** records the state of an entity at a regular reporting point.

This pattern applies when the business needs to ask what existed, or what state something was in, at the end of a period. Examples include an account at the end of each month, an employee at the end of each pay cycle, or a supplier at the end of each reporting quarter.

End-of-period facts are usually produced from [entity tracking](/docs/creating-information/entity-tracking/#third-pass-create-snapshots-and-infer-behaviour) pipelines. They let the model answer point-in-time questions without requiring users to solve validity-window logic inside the report.

**Example structure of `'Account end of month'`**

| Account SK | Period end date | Account status SK | Account level SK | Closing balance |
|---:|---|---:|---:|---:|
| 501 | 2024-01-31 | 1 | 2 | 8700.00 |
| 501 | 2024-02-29 | 1 | 3 | 13700.00 |

This fact supports questions such as:

- How many accounts were active at the end of February?
- How many accounts were gold-level accounts at the end of the quarter?
- What was the total closing balance for the selected period?

The important point is that the fact records state at a reporting boundary. It turns a changing entity into something the user can query at a stable point in time.

### Annotation fact

An **annotation fact** records display detail attached to another fact, usually where the detail is too fine-grained or too high-cardinality to belong in the main fact table.

Examples include inspection comments, certificate details, notes, attachments, or free-text descriptions. These details are often not designed for aggregation. They are designed for display after the user has already arrived at a transaction.

**Example structure of `'Inspection comments'`**

| Inspection SK | Comment sequence | Comment datetime | Comment text |
|---:|---:|---|---|
| 1001 | 1 | 2024-01-15 10:32 | Missing supporting document. |
| 1001 | 2 | 2024-01-15 10:47 | Officer requested follow-up evidence. |

The reason to move these details into a separate fact is grain.

One inspection may have many comments. If the comments are placed directly in `'Inspection'`, the data engineer must either change the grain of `'Inspection'` or concatenate the comments into a single field. Both options are undesirable.

Changing the grain bloats `'Inspection'` by repeating inspection-level information once for every comment. This increases model size and load cost, but it also creates a deeper pipeline problem: the inspection and its comments may change on different rhythms. Inspection status may be updated while comments remain unchanged, or comments may be appended while the inspection itself is stable. Combining them forces change detection and partitioned loading to treat these different behaviours as one table.

Concatenation preserves the grain of `'Inspection'`, but destroys the structure of the comments. The comments become a block of text rather than records with their own sequence, datetime, author, category, and display behaviour. The user may be able to read the comments, but the model can no longer sort them, filter them, display them individually, or apply separate security and formatting logic to them.

An annotation fact avoids both problems. It lets `'Inspection'` remain at the inspection grain, while `'Inspection comments'` carries the finer-grain detail.

Annotation facts are one of the rare cases where fact-to-fact filtering can be appropriate. Here, the `[Inspection SK]` column would the related column to the same in `'Inspection'` fact. The typical usage scenario is one where the business user has arrived at a set of transaction records through a dimension and would like to see additional details about that transaction. This is also why they are filtered through another fact, not a dimension.



Often, a measure is still needed to display annotation detail in a controlled way. For example, `SELECTEDVALUE` can ensure that a comment or detail field is only displayed when the relevant transaction has been selected.

An annotation fact is therefore not a second business process. It is an adjunct fact. It carries detail that describes another fact.

<!-- TODO: add PBI diagram -->

## Dimensions

Dimensions are the controlled surfaces of interaction. They give users handles for filtering, grouping, searching, comparing, and storytelling.

A dimension is not merely a lookup table. In an interactive model, it is a control.

### Business dimension

A **business dimension** is an ordinary control surface that lets users filter and group facts using familiar business categories.

Examples include statuses, locations, officers, inspection types, customers, products, regions, suppliers, and programs. These dimensions often come from source-system reference tables, but the data engineer may supplement them with additional columns that make business meaning clearer.

**Example structure of `'Inspection status'`**

| Inspection status SK | Inspection status | Is completed | Is failed |
|---:|---|---|---|
| 1 | Passed | true | false |
| 2 | Failed | true | true |
| 3 | In progress | false | false |

This dimension filters `'Inspection'`. A user can place `[Inspection status]` on a slicer, group inspection counts by `[Is failed]`, or compare completed and incomplete work.

The important point is not only that `'Inspection status'` is a low-cardinality lookup table. The important point is that it is a natural thing for the user to touch.

### Role-playing dimension

A **role-playing dimension** is a dimension that takes different meanings depending on which fact column it filters.

The most common example is a calendar. The same `'Reporting calendar'` table may be used against multiple date columns. It may filter orders by order date, shipments by shipment date, and completions by completion date.

**Example structure of `'Reporting calendar'`**

| Reporting date | Financial year | Month name | Month end date |
|---|---|---|---|
| 2024-01-15 | 2023-24 | January | 2024-01-31 |
| 2024-02-15 | 2023-24 | February | 2024-02-29 |

The same `'Reporting calendar'` table may filter a fact through different columns, such as `[Order date]`, `[Shipment date]`, and `[Completion date]`.

A user selecting January may be asking for orders placed in January, shipments sent in January, or cases completed in January. Role-playing dimensions play an important role in comparing different business processes using a common denominator, as explained in the chapter [Conforming systems](/docs/creating-information/conforming-systems/).

The model should make that role clear. If a role-playing dimension is exposed to users, the field names, measure names, or hover text should explain which role is being used.

A dimension is not role-playing merely because it filters many facts. The related columns must have different meanings.

For example, suppose `[Manufacture date]` appears on `'Manufacture'`, `'Order'`, and `'Shipping'`, and `'Reporting calendar'` relates to each fact through `[Manufacture date]`. Even though the calendar filters three facts, it is not role-playing. It means the same thing in each case: manufacture date. It is better understood as a business dimension, and may be better named `'Manufacture calendar'`.


### Histogram dimension

A **histogram dimension** turns numeric values into a filterable and visualisable dimension.

This pattern is useful when the user needs to filter or chart records by a numeric value, such as days to resolve, hours to process, number of attempts, or value bands.

Measures do not work as ordinary slicer fields. If users need to filter by a numeric result, that result often needs to be expressed as a dimension.

**Example structure of `'Days to resolve'`**

| Days to resolve SK | Minimum days | Maximum days | Days to resolve band |
|---:|---:|---:|---|
| 1 | 0 | 1 | 0 to 1 days |
| 2 | 2 | 5 | 2 to 5 days |
| 3 | 6 | 10 | 6 to 10 days |
| 4 | 11 | 9999 | More than 10 days |

The fact table can carry `[Days to resolve SK]`, or it can carry a numeric value that maps to `'Days to resolve'`.

Care is needed around boundaries. The data engineer must decide whether boundaries are inclusive or exclusive and ensure that maximum and minimum values are handled consistently.

As well as allowing the user to filter the model on a numeric value, the dimension is useful for creating histogram visuals—hence the name. The visual counts entities against a dimension of days, hours, attempts, amounts, or other numeric bands.

This is especially useful for time-to-process metrics. Instead of showing only an average processing time, the model can show the distribution: how many cases took 0 to 1 days, 2 to 5 days, 6 to 10 days, or more than 10 days.

### Combination dimension

A **combination dimension** represents combinations of related binary properties at the entity grain.

This pattern is useful when an entity can have several related properties at once, and the business wants to filter by combinations of those properties.

For example, a business entity may pass through multiple systems. The detail may be recorded at a lower grain, with one row per system touchpoint. But the user often wants to filter the business entity, not the system touchpoints.

**Example structure of `'System combination'`**

| System combination SK | Has System A | Has System B | Has System C | System combination |
|---:|---|---|---|---|
| 1 | false | false | false | No system |
| 2 | true | false | false | System A |
| 3 | false | true | false | System B |
| 4 | false | false | true | System C |
| ... | ... | ... | ... | ...|
| 8 | true | true | true | System A, System B, System C |

The fact table carries `[System combination SK]`. The user interacts with the flags in `'System combination'`.

A combination dimension pushes lower-grain detail back to the entity level, then exposes the result as a controlled surface of interaction.

A common case is the header-detail pattern. A consignment may be the header entity, while the cargo line items are the detail rows. Some line items may be fresh produce. Others may be inanimate goods. The user often wants to filter consignments by the types of cargo they contain, not analyse each line item separately.

**Example structure of `'Cargo combination'`**

| Cargo combination SK | Has fresh produce | Has inanimate cargo | Cargo combination | Has mixed cargo |
|---:|---|---|---|---|
| 1 | false | false | No cargo | false |
| 2 | true | false | Fresh produce only | false |
| 3 | false | true | Inanimate cargo only | false |
| 4 | true | true | Fresh produce and inanimate cargo | true |

The consignment fact carries `[Cargo combination SK]`. The user interacts with `'Cargo combination'` to find consignments containing fresh produce, inanimate cargo, or both.

Combination dimensions are especially useful for `and` logic. They allow the user to ask for entities that have this property and that property while keeping the model at the correct grain.

### Choices dimension

A **choices dimension** is a low-cardinality, multi-valued dimension that lets users filter for entities that have any selected attribute.

Choices dimensions are related to combination dimensions, but the interaction is different. A combination dimension is useful when the user cares about combinations of properties. A choices dimension is useful when the user wants any matching choice.

The simplest example is a drink preference question where a person may choose tea, coffee, both, or neither. The fact table stays at the grain of the person. It does not expand to one row per drink.

**Example structure of `'Table order'`**

| Table order ID | Order date | Drink choice group SK |
|---:|---|---:|
| 1 | 2024-01-15 | 2 |
| 2 | 2024-01-15 | 3 |
| 3 | 2024-01-16 | 3 |
| 4 | 2024-01-16 | 1 |
| 5 | 2024-01-17 | 4 |
| 6 | 2024-01-17 | 4 |

**Example structure of `'Drink choice'`**

| Drink choice group SK | Drink choice |
|---:|---|
| 1 | No drink |
| 2 | Tea |
| 3 | Coffee |
| 4 | Tea |
| 4 | Coffee |

The fact table carries `[Drink choice group SK]`. The choices dimension contains one row per selected choice within each group.

If the user selects `Tea`, the model returns table orders `1`, `5`, and `6`. If the user selects `Coffee`, the model returns table orders `2`, `3`, `5`, and `6`. Table orders `5` and `6` appear in both results because their group contains both choices. The grain of `'Table order'` has not changed. 

Without a choices dimension, there are two common alternatives.

The first is to store each choice as a separate Boolean column in the fact table, such as `[Has tea]` and `[Has coffee]`. But it is awkward when the user wants to find tables with tea *or* coffee—the filter will pick rows that have tea *and* coffee instead.

The second is to change the grain of the fact table so that each order appears once per drink choice. This makes the choice easy to filter, but `'Table order'` is no longer at the grain of an order. It is now at the grain of an order-choice. That may be correct for some models, but often not.

A choices dimension avoids both problems. The fact remains at the order grain, while the user can still select individual choices using `or` logic. Thus, a choices dimension is a set-membership bridge expressed as a dimension. It preserves the entity grain while still letting the user interact with individual choices.

A common business example is data quality. A transaction row may have multiple issues: missing date, missing officer, invalid status, or missing location. A data quality report needs to show records that have any selected issue, while still preserving one row per transaction. 


**Example structure of `'Transaction'`**

| Transaction SK | Transaction date | Issue group SK |
|---:|---|---:|
| 1001 | 2024-01-15 | 2 |
| 1002 | 2024-01-16 | 3 |
| 1003 | 2024-01-17 | 4 |
| 1004 | 2024-01-18 | 1 |

**Example structure of `'Data quality issue'`**

| Issue group SK | Data quality issue |
|---:|---|
| 1 | No issue |
| 2 | Missing date |
| 2 | Missing officer |
| 3 | Missing location |
| 3 | Invalid status |
| 4 | Missing date |
| 4 | Missing officer |
| 4 | Missing location |

The fact table carries `[Issue group SK]`. The choices dimension contains one row per issue within each group.

This allows a user to select `Missing date` and see all transactions whose issue group includes `Missing date`. It also allows the user to select several issues without forcing `'Transaction'` to expand to one row per issue.

Physically, a choices dimension is created by taking the possible sets of choices from a finite list and assigning each set a group key. The relationship between the fact and the choices dimension is on that group key.

Choice and combination dimensions are closely related. A combination dimension can often be unpivoted to create a choices dimension.

For example, `'System combination'` may contain `[Has System A]`, `[Has System B]`, and `[Has System C]`. This can be unpivoted into a `'System touch point'` choices dimension with values such as `System A`, `System B`, and `System C`.

**Example structure of `'System touch point'`**

| System combination SK | System touch point |
|---:|---|
| 1 | No system |
| 2 | System A |
| 3 | System B |
| 4 | System C |
| 5 | System A |
| 5 | System B |
| 6 | System A |
| 6 | System C |
| 7 | System B |
| 7 | System C |
| 8 | System A |
| 8 | System B |
| 8 | System C |

The decision depends on the question. If the business wants combinations, use a combination dimension. If the business wants any selected value, use a choices dimension. Since they are lightweight, it is always possible to have both if beneficial.


### Sankey dimension

A **Sankey dimension** represents possible paths through a sequence of checkpoints.

This pattern is useful when the business wants to visualise movement through a process. The source fact should not be reshaped just to create a flow visual. Instead, each possible path can be represented as a dimension.

For example, an entity may move through follow-on systems: System A, System B, and System C. Some entities begin in System A and continue through all systems. Some begin in System B. Some skip System B and move directly from System A to System C.

A `'System path'` dimension can represent each possible path as a set of edges.

**Example structure of `'System path'`**

| System combination SK | From system | To system |
|---:|---|---|
| 1 | Start | No system |
| 2 | Start | System A |
| 3 | Start | System B |
| 4 | Start | System C |
| 5 | Start | System A |
| 5 | System A | System B |
| 6 | Start | System A |
| 6 | System A | System C |
| 7 | Start | System B |
| 7 | System B | System C |
| 8 | Start | System A |
| 8 | System A | System B |
| 8 | System B | System C |

The fact table carries `[System combination SK]`. The Sankey dimension expands that path into the rows required by the Sankey visual. 

This lets the user see process flow without changing the grain of the fact. The fact remains at the entity grain. The dimension supplies the visual structure.

Notice that `[System combination SK]` is the same key used by `'System combination'`, `'System touch point'`, and `'System path'`.

This is the same underlying structure expressed for different usage scenarios.

`'System combination'` presents the systems as a combination of binary choices. It answers: which exact combination of systems was involved?

`'System touch point'` presents the same structure as a choices dimension. It answers: did the entity involve any selected system?

`'System path'` presents the same structure as a Sankey dimension. It answers: how did the entity move through the systems?

Computationally these are low costs and low complexity translations.

The key is to recognise the underlying axes of binary choice. Once those axes are identified, the data engineer can express them in different dimensional forms depending on the interaction the user needs. Thus, the data engineer is not merely arranging tables, but recognising the latent structure of interaction in the business problem.


<!-- > [!NOTE]
> TODO: Add diagram showing a fact table with `[Path ID]` filtering a Sankey dimension. -->



### Storytelling dimension

A **storytelling dimension** groups entities into meaningful business journeys.

This pattern is used when the raw process is too detailed for the user’s first point of entry. Instead of beginning with many statuses, events, checkpoints, or paths, the model gives users a small set of meaningful journeys.

Where a Sankey dimension shows movement, a storytelling dimension translates these movements into manageable categories that are business-meaningful.

For example, the [Storytelling](/docs/creating-information/storytelling/#storytelling-dimensions) chapter describes a help desk escalation dimension that combines tier combinations, highest escalation, escalation path, escalation summary, and display order. The point is not merely to record the path a case took, but to express what that path means to the business.

A storytelling dimension is created when the data engineer steps back from raw data and asks how the business understands the movement of the entity.

In a self-service model, storytelling dimensions often act as the first portal into the data. They divide the population into meaningful strata and help users begin analysis before drilling into detail.


### Search dimension

A **search dimension** is a high-cardinality dimension that gives users a controlled way to find, retrieve, drill through, or cross-filter records.

Most dimensions are useful because they support aggregation. Search dimensions are useful because they provide a way into the model.

In traditional dimensional modelling, a transaction is usually modelled as a fact table, not as a dimension. Transaction identifiers are often kept inside fact tables as degenerate dimensions. In an interactive Power BI model, this is not always enough. Sometimes the user needs to search for a specific transaction, use it for drillthrough, or cross-filter related facts across multiple business processes.

In that case, a transaction-level value can become a search dimension.

An important special case is the **ID dimension**.

An ID dimension is a minimal search dimension that contains only the key fields needed for search, usually the surrogate key and one or more business identifiers.

**Example structure of `'Inspection ID'`**

| Inspection SK | Inspection number |
|---:|---|
| 1001 | INS-2024-0001 |
| 1002 | INS-2024-0002 |

This dimension lets a user retrieve records using an identifier they already know. In traditional dimensional modelling, this pattern may be treated as an exception. In interactive reporting, it is often practical and necessary because users frequently arrive with a known business key. They want to paste or search an ID and see the relevant records.

Search dimensions can also support high-cardinality text values that users treat as search handles.

**Example structure of `'Package search'`**

| Package SK | Package reference | Package description |
|---:|---|---|
| 7001 | PKG-2024-0001 | Refrigerated seafood consignment |
| 7002 | PKG-2024-0002 | Machinery parts and spare components |

The modelling decision depends on the user’s intent.

If the user expects to search using the field, model it as a search dimension. If the user only expects to display the field after arriving at a record, model it as an annotation fact.

Search dimensions can significantly increase model size. They should be used deliberately, and they are not ideal for aggregation.

Due to Power BI filtering behaviour, search dimensions often need to be used with a unit-record display measure. This is explained in the [Filtering behaviour](/docs/presenting-insights/filtering-behaviour/#displaying-unit-records-for-three-or-more-business-processes) and [Designing measures](/docs/presenting-insights/designing-measures/#filtering-measures) chapters.



### Degenerate dimension

A **degenerate dimension** is a dimension-like field retained inside a fact table rather than lifted into a separate dimension table.

This usually occurs for one of two reasons:

- The field does not have enough business weight to justify a standalone dimension.
- The field has high cardinality and would increase model size if lifted into a dimension.

**Example of a degenerate dimension `[Inspected goods]` inside `'Inspection'`**

| Inspection SK | Inspection number | Inspection date | Inspection status SK | Inspected goods |
|---:|---|---|---:|---|
| 1001 | INS-2024-0001 | 2024-01-15 | 1 | Refrigerated seafood consignment |
| 1002 | INS-2024-0002 | 2024-01-16 | 2 | Machinery parts and spare components |
| 1003 | INS-2024-0003 | 2024-01-16 | 1 | Fresh mangoes and tropical fruit |
| 1004 | INS-2024-0004 | 2024-01-17 | 3 | Timber pallets and packaging materials |
| 1005 | INS-2024-0005 | 2024-01-18 | 2 | Laboratory testing equipment |

Here, `[Inspected goods]` is the degenerate dimension, and can be used for searching. This works technically, but it can weaken the interaction logic of the model. It makes the fact table behave like a control surface.

Degenerate dimensions should therefore be treated with caution. They are sometimes necessary, but they are often a sign that a field has not been properly expressed as a business dimension, search dimension, or annotation fact.

For example, if `Inspected goods` is only needed for display, the column can remain hidden in the model and be exposed through a measure using `SELECTEDVALUE`. If it is needed for search or cross-filtering, it may be better expressed as an `'Inspected goods'` search dimension related by `[Inspection SK]`.

The question is not whether the field can remain in the fact table. The question is whether the user needs to touch it. The three problems of degenerate dimensions are discussed in the next chapter.

If the user needs to touch it, it probably belongs on the controller, not on the robot.


## Pushing detail back to the entity

One common theme in this chapter is the movement from information at a finer grain than the entity back to the entity level, and then into a dimension.

Combination dimensions, choice dimensions, Sankey dimensions, and storytelling dimensions all follow this pattern. 

{{< svg >}}
<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="360" viewBox="0 0 1080 360"
     style="display:block;width:100%;max-width:42rem;height:auto;background:transparent" role="img"
     aria-label="Three stage movement from lower-grain detail to entity-level signal to dimension value">

  <defs>
    <marker id="arrowhead-pushing-detail-entity" markerWidth="10" markerHeight="8"
            refX="10" refY="4" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L10,4 L0,8 z" fill="#222222"/>
    </marker>
  </defs>

  <!-- Detail rows -->
  <rect x="45" y="45" width="290" height="235" rx="16"
        fill="#ffffff" stroke="#222222" stroke-width="1.8"/>

  <text x="190" y="83" text-anchor="middle"
        font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
        font-size="24" font-weight="700" fill="#111111">Entity process details</text>

  <text x="190" y="116" text-anchor="middle"
        font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
        font-size="14" fill="#555555">finer grain than entity</text>
  <text x="190" y="137" text-anchor="middle"
        font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
        font-size="14" fill="#555555">many rows per entity</text>
  <text x="190" y="158" text-anchor="middle"
        font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
        font-size="14" fill="#555555">hard to expose directly</text>

  <line x1="75" y1="180" x2="305" y2="180"
        stroke="#dddddd" stroke-width="1.4"/>

  <text x="190" y="207" text-anchor="middle"
        font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
        font-size="13" fill="#333333">Cargo 1001 · System A</text>
  <text x="190" y="228" text-anchor="middle"
        font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
        font-size="13" fill="#333333">Cargo 1001 · System B</text>
  <text x="190" y="249" text-anchor="middle"
        font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
        font-size="13" fill="#333333">Cargo 1001 · System C</text>

  <!-- Entity signal -->
  <rect x="395" y="45" width="290" height="235" rx="16"
        fill="#ffffff" stroke="#222222" stroke-width="1.8"/>

  <text x="540" y="83" text-anchor="middle"
        font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
        font-size="24" font-weight="700" fill="#111111">Entity of interest</text>

  <text x="540" y="116" text-anchor="middle"
        font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
        font-size="14" fill="#555555">pushed back to entity grain</text>
  <text x="540" y="137" text-anchor="middle"
        font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
        font-size="14" fill="#555555">one value per entity</text>
  <text x="540" y="158" text-anchor="middle"
        font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
        font-size="14" fill="#555555">safe to join and filter</text>

  <line x1="425" y1="180" x2="655" y2="180"
        stroke="#dddddd" stroke-width="1.4"/>

  <text x="540" y="217" text-anchor="middle"
        font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
        font-size="13" fill="#333333">Cargo 1001</text>
  <text x="540" y="239" text-anchor="middle"
        font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
        font-size="13" fill="#333333">System A + B + C</text>

  <!-- Dimension value -->
  <rect x="745" y="45" width="290" height="235" rx="16"
        fill="#ffffff" stroke="#222222" stroke-width="1.8"/>

  <text x="890" y="83" text-anchor="middle"
        font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
        font-size="24" font-weight="700" fill="#111111">Dimension value</text>

  <text x="890" y="116" text-anchor="middle"
        font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
        font-size="14" fill="#555555">exposed for interaction</text>
  <text x="890" y="137" text-anchor="middle"
        font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
        font-size="14" fill="#555555">manageable set of values</text>
  <text x="890" y="158" text-anchor="middle"
        font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
        font-size="14" fill="#555555">usable on the canvas</text>

  <line x1="775" y1="180" x2="1005" y2="180"
        stroke="#dddddd" stroke-width="1.4"/>

  <text x="890" y="207" text-anchor="middle"
        font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
        font-size="13" fill="#333333">'System combination'</text>
  <text x="890" y="228" text-anchor="middle"
        font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
        font-size="13" fill="#333333">System A + B + C</text>

  <!-- Arrows -->
  <line x1="350" y1="162" x2="375" y2="162"
        stroke="#222222" stroke-width="2.2"
        marker-end="url(#arrowhead-pushing-detail-entity)"/>

  <line x1="700" y1="162" x2="725" y2="162"
        stroke="#222222" stroke-width="2.2"
        marker-end="url(#arrowhead-pushing-detail-entity)"/>

</svg>
{{< /svg >}}

<div style="max-width:42rem;text-align:center;font-size:0.95rem;color:#666;margin-top:0.5rem;">
Figure 1. Lower-grain detail is pushed back to the entity grain, then exposed as a dimension value that users can interact with safely.
</div>


This movement is powerful because it keeps the focus on the entity of interest, both technically and business-wise.

Technically, the entity of interest remains the common denominator for joins. The user gets a meaningful control surface without forcing the model into lower-grain chaos.

Business-wise, user interactions remain centred on the entity the business actually cares about.

The purpose of this chapter is not to define an exhaustive list of all possible artefacts in a dimensional model. Ultimately, each table is either a dimension or a fact, and the sub-categorisation does not significantly change this.

Rather, the purpose of listing these elements is to help data engineers shift to a mindset of seeing dimensions and facts through usage scenarios, and to recognise that they can play functionally different roles depending on the interactivity requirements.

In the end, the final test is this: can the business user answer a question without needing to guess?

That is the heart of dimensional modelling in an interactive model.


> [!NOTE]
> **Key ideas**
>
> In an interactive model, dimensions are what users touch and facts are what respond.
>
> Facts contain business activity, business state, or display detail.
>
> Dimensions provide controlled surfaces for filtering, grouping, searching, comparing, and storytelling.
>
> A fact table should not become the user’s control panel. The controls belong on the controller, not on the robot.
>
> Some dimensions exist to push lower-grain complexity back to the entity grain and expose it as something users can interact with safely.
>
> A good dimensional model lets users interact with business activity reliably without guessing how the model works.
