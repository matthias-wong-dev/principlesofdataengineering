---
title: Filtering behaviour
url: /docs/presenting-insights/filtering-behaviour/
description: Learn how Power BI filtering works through relationships, measures, visual-level filters, DAX filter context, and dimensional model design.
lede: Filtering design is what makes a Power BI model feel intuitive—or frustrating.
weight: 5
# draft: true
---

## Filtering as interaction design

Filtering design is what makes a Power BI model feel intuitive—or frustrating.

Many engineers stop too early, treating the job as complete once the correct answer is reachable through some combination of filters.

That is not enough.

> [!SHARE:not-a-puzzle]
> A self-service model is not a puzzle for the user to solve.

The user should not have to discover the one valid route through the model. They should be able to approach the model from different directions—starting with a date, a product, an ID, a measure, or a business process—and still receive sensible results at each step.

The data engineer’s task is therefore not only to make the correct answer possible. It is to anticipate how users will try to reach that answer. More generally, it is to anticipate what buttons the user will click, and what effects the model should produce.

A good dimensional model is designed around the interaction between [buttons and effects](/docs/presenting-insights/dimensional-modelling-for-ux/). Filtering is the mechanism through which this interaction takes place.

This chapter explains how filtering works so the data engineer can anticipate user interaction and design the model’s response deliberately.

The chapter proceeds in two parts.

First, it explains the main ways filtering occurs in Power BI. These are the basic mechanisms the data engineer needs to understand: relationship filtering, common-fact filtering, non-blank measure filtering, visual-level filtering, and measure-defined filtering.

Second, it applies those mechanisms to tricky modelling scenarios. These include displaying unit records, coordinating multiple business processes, cascading filters, aggregating dimension values, filter-by-having, and dynamic Type I behaviour.

The purpose is not to memorise tricks. The purpose is to understand how Power BI responds when users interact with the model, so the data engineer can design those responses deliberately.

## Ways of filtering

There are five common ways filtering appears in Power BI:

- Relationship filtering
- Common-fact filtering
- Non-blank measure filtering
- Visual-level filtering
- Measure-defined filtering

### Relationship filtering

Relationship filtering is the standard case of filtering.

When table X filters table Y, a user who selects a value from X narrows the rows in Y based on the relationship between the two tables. In a dimensional model, the most important case is when dimensions filter facts.

The user touches the dimension. The fact responds.

**Example structure of `'Product'`**

| Product SK | Product name |
|---:|---|
| 1 | Cake |
| 2 | Bread |
| 3 | Pastry |

**Example structure of `'Sale'`**

| Sale ID | Product SK |
|---|---:|
| S1001 | 1 |
| S1002 | 1 |
| S1003 | 2 |

If the user selects `Cake` from `'Product'`, the model filters `'Sale'` to `S1001` and `S1002`. If the user selects `Bread`, it filters to `S1003`. If the user selects `Pastry`, there are no matching sales rows.

New engineers often ask, “Why do we need dimensions at all? Why not leave all the information in the fact table? It is simpler.” That is, why not rely solely on degenerate dimensions?

There are three common problems.

First, non-existence becomes impossible to express. If product were only stored as a degenerate column inside `'Sale'`, then `Pastry` would not exist anywhere in the model. A user would not be able to know that no pastries were sold.

Second, the business meaning becomes buried. Attributes such as region, product, demographic group, or status are no longer presented as coherent business objects. They become miscellaneous columns inside a fact table. A user would have to read every single row to reverse engineer the entity and its grain.


Third, cross-filtering and drillthrough across multiple business processes become harder. A conformed dimension such as `'Calendar'`, `'Product'`, or `'Region'` can filter several facts. A degenerate column inside one fact cannot naturally serve as a shared point of interaction.


### Common-fact filtering

Filtering also appears indirectly through common filtered tables.

This behaviour is often missed by new engineers, but it is essential to the intuitive experience of Power BI. When two dimensions both filter the same fact, Power BI can use the fact to determine which combinations of dimension values are valid.

Consider a simple sales model.

**Example structure of `'Product'`**

| Product SK | Product name |
|---:|---|
| 1 | Cake |
| 2 | Bread |
| 3 | Pastry |

**Example structure of `'Region'`**

| Region SK | Region name |
|---:|---|
| 1 | North |
| 2 | South |
| 3 | West |

**Example structure of `'Sale'`**

| Sale ID | Product SK | Region SK | Sales amount |
|---|---:|---:|---:|
| S1001 | 1 | 1 | 100 |
| S1002 | 1 | 2 | 150 |
| S1003 | 2 | 1 | 200 |

If a visual contains `'Product'[Product name]` and `'Region'[Region name]`, Power BI returns only product-region combinations that exist in `'Sale'`.

The fact table acts as the common filtered table that makes the dimension combination valid.

The result would be:

| Product name | Region name |
|---|---|
| Cake | North |
| Cake | South |
| Bread | North |

`Pastry` does not appear because there is no matching row in `'Sale'`. `West` does not appear because there is no matching row in `'Sale'`. The missing combinations are not shown because they do not exist in the common fact.


This common-fact behaviour is part of what makes a dimensional model feel natural. Users can place dimension fields together, and the model silently removes combinations that do not exist.

If two dimensions do not share any filtered fact table, Power BI cannot determine the valid combinations between them. In that case, the visual may return the Power BI error message: `Can't determine relationships between the fields.`

If multiple fact tables are filtered by both dimensions, Power BI shows combinations where any fact table has a matching row. This behaviour is powerful, but it also means the data engineer must think carefully about which facts share which dimensions.

<!-- TODO: Add Performance Analyzer screenshot showing the DAX query generated for common-fact filtering. -->

This “upward” filtering from facts to dimensions enables the intuitive experience of a dimensional model. It is why dimensions alone can serve as the interface, even when facts are hidden. Mastering this behaviour is central to designing good Power BI models.

### Non-blank measure filtering

The previous method relies on implicit filtering through relationships and common facts. In simple models, this is often enough. In complex models with several fact tables, it may not be.

Measures can also control what appears in a visual.

Suppose `'Product'` filters `'Sale'`, and `[Total sales amount]` sums the sales amount in `'Sale'`.

**Visual before adding `[Total sales amount]`**

| Product name |
|---|
| Cake |
| Bread |
| Pastry |

**Visual after adding `[Total sales amount]`**

| Product name | Total sales amount |
|---|---:|
| Cake | 250 |
| Bread | 200 |

`Pastry` disappears because `[Total sales amount]` is blank for that product in the current filter context.

This is non-blank measure filtering. When a measure is added to a table or matrix visual, Power BI tends to retain rows where the measure returns a non-blank value.

If several measures are added, the visual may retain rows where any measure returns a value.

This mirrors fact table filtering, but gives the data engineer more control. Instead of relying only on row existence in a fact table, the data engineer can define the measure logic that determines which values should remain visible.

<!-- TODO: Add Performance Analyzer screenshot showing a visual filtered by non-blank measure value. -->

### Visual-level filtering

Sometimes a measure cannot be placed directly in the visual, or doing so would interfere with the visual’s layout.

For example, a slicer cannot simply display a helper measure as one of its fields. A table visual may also need to be filtered by a measure without showing that measure to the user.

In these cases, the report developer can apply a visual-level filter using the measure value.

For example, `[Has sales]` may return `1` when there is at least one sale in the current context. A slicer on `'Product'[Product name]` can then use `[Has sales]` as a visual-level filter so that only products with sales appear.

<!-- TODO: Add screenshot showing measure used as a visual-level filter. -->

This method is useful, but should be used with care. The evaluation cost can be significant when the visual has a large number of possible values and the measure must be calculated for each one.

### Measure-defined filtering

The previous methods control which dimension values appear in a visual. Sometimes the data engineer needs to apply filters directly inside the measure calculation itself.

This is measure-defined filtering.

Power BI supports this through DAX expressions such as `userelationship` and `crossfilter`. These expressions allow the data engineer to activate a relationship, modify a relationship direction, apply a virtual relationship, or otherwise change the filter context for the duration of the calculation.

Consider a sales model where `'Sale'` has both `[Order date]` and `[Delivery date]`.

**Example structure of `'Calendar'`**

| Date | Month name |
|---|---|
| 2024-01-15 | January |
| 2024-01-20 | January |
| 2024-02-05 | February |

**Example structure of `'Sale'`**

| Sale ID | Product SK | Order date | Delivery date | Sales amount |
|---|---:|---|---|---:|
| S1001 | 1 | 2024-01-15 | 2024-01-20 | 100 |
| S1002 | 1 | 2024-01-16 | 2024-02-05 | 150 |
| S1003 | 2 | 2024-02-01 | 2024-02-06 | 200 |

Suppose `'Calendar'[Date]` has an active relationship to `'Sale'[Order date]` and an inactive relationship to `'Sale'[Delivery date]`.

A normal measure such as `[Total sales amount]` responds to the active relationship. If the user selects January, the measure returns sales ordered in January.

```DAX
Total sales amount =
sum ( 'Sale'[Sales amount] )
```

But the user may also need sales delivered in January. The data engineer can define a second measure that activates the delivery-date relationship only for that calculation.

```DAX
Total delivered sales amount =
calculate (
    [Total sales amount],
    userelationship ( 'Calendar'[Date], 'Sale'[Delivery date] )
)
```

With the example above, selecting January gives `[Total sales amount] = 250`, because `S1001` and `S1002` were ordered in January. The delivered-sales measure gives `100`, because only `S1001` was delivered in January.

The model relationship does not permanently change. The filtering path changes only while `[Total delivered sales amount]` is being evaluated.


<!-- TODO: Add screenshot showing measure-defined filtering in a card visual. -->

Measure-defined filtering is powerful because it allows precise behaviour without permanently changing the model. It is also dangerous because the filtering rule becomes hidden inside the measure. Used well, it solves specific interaction problems. Used carelessly, it creates a model where results are technically correct but difficult to explain.

## Filtering scenarios

The five filtering mechanisms above can be combined to support a wide range of interactivity goals while preserving the standard dimensional model pattern: dimensions filter facts using single-direction relationships.

The scenarios below are not exhaustive. Their purpose is to show how filtering design supports user interaction in real models.

### Displaying unit records for a single business process

A common requirement is to show one row per business transaction.

The obvious approach is to expose the fact table. For example, if the transaction is a sale, the user might expect to drag fields directly from `'Sale'`.

This is usually the wrong interface.

A better approach is to hide `'Sale'` and let dimensions and measures reconstruct the transaction view.

The point of hiding the fact table is not tidiness. It is to protect the user experience. If users interact directly with the fact table, they can produce technically valid but strange results. If they interact through dimensions and measures, the model is much more likely to behave sensibly no matter which direction they approach it from.


#### The model setup

Suppose there is a business process represented by the `'Sale'` fact table.

The setup is as follows:

- A fact table `'Sale'`
- An ID dimension `'Sales ID'` with `[Sales order number]`
- A calendar dimension `'Sales calendar'`
- A business dimension `'Sales product'`
- A measure `[Total sales amount]` that sums the sales amount in `'Sale'`

**Example structure of `'Sale'`**

| Sales order number | Sales date | Product SK | Sales amount |
|---|---|---:|---:|
| SO1001 | 2024-01-15 | 1 | 100 |
| SO1002 | 2024-01-16 | 2 | 150 |

**Example structure of `'Sales ID'`**

| Sales order number |
|---|
| SO1001 |
| SO1002 |

**Example structure of `'Sales calendar'`**

| Sales date | Month name |
|---|---|
| 2024-01-15 | January |
| 2024-01-16 | January |

**Example structure of `'Sales product'`**

| Product SK | Product name |
|---:|---|
| 1 | Cake |
| 2 | Bread |


#### Reconstructing the transaction row

The user should reach the sale through:

- `'Sales ID'[Sales order number]`
- `'Sales calendar'[Sales date]`
- `'Sales product'[Product name]`
- `[Total sales amount]`

Together, these fields give the user the full sale record without exposing the fact table itself.

This works because Power BI returns only combinations of dimension values that correspond to existing rows in `'Sale'` (common-fact filtering).  Since `'Sales ID'[Sales order number]` uniquely identifies the sales transaction, adding `'Sales ID'[Sales order number]`, with either `'Sales calendar'[Sales date]` or `'Sales product'[Product name]` downfilters `'Sales'` to the transactions that exist.

#### Why use a measure for the amount?

`'Sale'` has an amount recorded in `[Sales amount]`. A simplistic approach is to expose `'Sale'[Sales amount]` to the user as though it were an ordinary field. Instead, a better approach is to expose `[Total sales amount]`.

Because `'Sales ID'[Sales order number]` uniquely identifies one row, `[Total sales amount]` returns the sum of that one row in the current context—that is, the same numeric value as `'Sale'[Sales amount]` at the transaction level (non-blank measure filtering).


At the sales order level, the measure returns the value of one transaction. At the product level, the same measure aggregates all matching transactions. The user does not need to choose between a transaction amount and an aggregate amount. The measure behaves correctly in both situations. For example:

| Current context | Result |
|---|---:|
| `SO1001` | `[Total sales amount] = 100` |
| `January` | `[Total sales amount] = 250` |

This sounds complex in the backend, but it is seamless for the user. In the ideal setup, `'Sale'` and `'Sale'[Sales amount]` are hidden. The user sees `[Total sales amount]`, not both the measure and the raw fact column.

This is far superior to exposing both. At the transaction level, both may show the same number, which encourages users to treat them as interchangeable. But in charts, aggregations, and time intelligence, only the measure behaves correctly. That inconsistency is confusing. Something appears to work in one visual, then fails in another.

With this setup, `[Total sales amount]` behaves consistently across situations. The user gets sensible results without needing to remember special cases.

#### Why this remains intuitive

The benefit is that the model behaves sensibly from multiple directions. The user can start with the sales order number, the date, the product, or the measure. In each case, Power BI’s filtering behaviour narrows the model toward valid sales records.

First, suppose the user selects `'Sales ID'[Sales order number]`, then `'Sales calendar'[Sales date]`.

Power BI immediately gives the valid combination of sales order numbers and sales dates because the dimension values are filtered by their common fact. This returns the desired transaction record because the business key selects the correct grain.

Second, suppose the user selects `'Sales ID'[Sales order number]`, then `[Total sales amount]`.

This also gives the transaction record. This time, it is not only because of the common fact. It is also because `[Total sales amount]` returns a non-blank value for the sales order number. If there are sales order numbers without a sales amount, such as unconfirmed sales, those order numbers will not appear. For most use cases, that is the desired outcome.

Third, suppose the user selects `[Total sales amount]`, then `'Sales product'[Product name]`.

The model first returns the total sales amount for the whole model as a single number, then breaks it down by product. When the user adds `'Sales ID'[Sales order number]`, the table expands to unit records.

The experience is correct at every step.

This is the power of a properly designed dimensional model focused on dimensions and measures. Regardless of the sequence of field selection, the model produces sensible business results.

This seamless experience would not occur if the user selected the degenerate `'Sale'[Sales amount]` instead of `[Total sales amount]`. The user would first see a distinct list of sales amount values, then a confusing combination of sales amount and product, and only after adding `'Sales ID'[Sales order number]` would the table make sense.

The experience would be jarring rather than seamless.


Even this simple use case requires careful modelling work. The model must cater for a large number of possible user interaction sequences. These possibilities are handled elegantly when the data engineer focuses on dimensions and measures, and hides facts.

In this example, `'Sales ID'[Sales order number]` is a single-column business key. If the business key has multiple columns, all columns need to be used.

### Displaying unit records for two business processes

The single-process case is difficult enough. The two-process case introduces a new problem: different business processes may share some controls but not others.

Continuing the previous example, suppose sales can be refunded.

The model contains:

- A fact table `'Sale'`
- A fact table `'Refund'`
- A shared ID dimension `'Sales ID'`
- A shared product dimension `'Sales product'`
- A sales calendar dimension `'Sales calendar'`
- A refund calendar dimension `'Refund calendar'`
- A measure `[Total sales amount]`
- A measure `[Total refund amount]`

**Example structure of `'Sale'`**

| Sales order number | Sales date | Product SK | Sales amount |
|---|---|---:|---:|
| SO1001 | 2024-01-15 | 1 | 100 |
| SO1002 | 2024-01-16 | 2 | 150 |
| SO1003 | 2024-01-17 | 1 | 200 |

**Example structure of `'Refund'`**

| Sales order number | Refund date | Refund amount |
|---|---|---:|
| SO1001 | 2024-01-20 | 50 |
| SO1001 | 2024-01-20 | 50 |
| SO1003 | 2024-01-22 | 75 |

The dimensions relate to the two facts differently.

Sales and refunds share a sales order and product. They do not share the same process date. Sales occur on sales dates; refunds occur on refund dates. Sales are usually one row per order; refunds may have multiple rows per order.


| Dimension | `'Sale'` | `'Refund'` | Meaning |
|---|---|---|---|
| `'Sales ID'` | 1 → * | 1 → * | Shared sales order identifier |
| `'Sales product'` | 1 → * | 1 → * | Product sold and later refunded |
| `'Sales calendar'` | 1 → * |  | Date of sale |
| `'Refund calendar'` |  | 1 → * | Date of refund |

The data engineer therefore has to anticipate which process the user is trying to display. Showing sales, showing refunds, and showing sales with refunds are three different interaction problems.

This is the source of the complexity.

Some controls are shared. `'Sales ID'` and `'Sales product'` can filter both sales and refunds.

Some controls are process-specific. `'Sales calendar'` filters sales. `'Refund calendar'` filters refunds.

The model therefore behaves differently depending on what the user is trying to display:

- Sales transactions
- Refund transactions
- Sales and refund information together

### Displaying sales

When displaying sales records, everything works as if there were only the `'Sale'` fact table.

This is because every refund comes from a sale. `'Sale'` is therefore a superset of `'Refund'`. Adding `'Refund'` to the model does not interfere with the display of sales transactions.

The superset relationship matters. If there were sales order numbers in `'Refund'` that did not exist in `'Sale'`, then selecting `'Sales calendar'[Sales date]` and `'Sales ID'[Sales order number]` would not correctly identify the list of sales transactions.

Single-direction filters also matter. If the report canvas has a filter on `'Refund calendar'`, that filter does not interfere with the presentation of sales transactions because `'Refund calendar'` filters `'Refund'`, not `'Sale'`.

This would not be true if the model used bidirectional filters carelessly. The refund date could unexpectedly affect sales visuals.

### Displaying refunds

When displaying refund records, the user is interested in `[Total refund amount]`, but they may also need the sales context, such as `'Sales ID'[Sales order number]` and `'Sales product'[Product name]`.

While the outcome—displaying refund—is the same, the user may come from two angles: starting with refund information, or starting from sales information. Both need to work. In a properly designed dimensional model, that is the case.

If the user selects `[Total refund amount]` first, the model returns the total refund amount for the whole dataset (non-blank measure filtering). Adding sales attributes breaks that number down. Adding the relevant ID dimension returns unit-level records.

If the user selects sales attributes first, Power BI initially displays the list of sales orders and products, regardless of whether they were refunded. When the user adds either `'Refund calendar'[Refund date]` or `[Total refund amount]`, the table filters down to refund transactions. The former because of common-fact filtering, the latter because of non-blank measure filtering. And both happens because those fields are linked to `'Refund'`.

Whether the user starts with the sales attributes or the refund-specific fields, the dimensional model gives a sensible path.

However, the situation is more complicated than it first appears.

Suppose a sales order of `$100` (`SO1001` in the example) is refunded in two partial refunds of `$50` on the same day. Because there is no primary key for refunds, the refund for that sales order may appear as a single transaction with `[Total refund amount] = 100`, rather than two rows of `$50`.

For many scenarios, showing the total refund amount, regardless of the partial breakdowns, may be sufficient. In some cases, it is not.

When the user must see each refund action as a separate transaction, the data engineer needs a key that distinguishes each refund transaction.

One option is to create `[Refund SK]`, a unique integer for each refund, and expose it as `'Refund ID'[Refund SK]`. This is usually not preferable:

- `[Refund SK]` is high cardinality, increasing model size through the `'Refund ID'` dimension and relationship columns.
- `[Refund SK]` has no natural business meaning and creates an additional learning burden for users.

A better approach is often to create `[Refund number]`, a sequence number for each refund action within a sales order. The composite key becomes `[Sales order number]` and `[Refund number]`.

`[Refund number]` can be exposed through `'Refund ID'[Refund number]`. This is a partial ID dimension because it supplies one part of the full key needed to identify a refund.

This dimension is low cardinality, has minimal model-size impact, and is natural for users.

From the user’s perspective:

- `[Total refund amount]` gives the refund value for the transaction.
- Adding `'Refund ID'[Refund number]` breaks the sale into separate refund actions.

This is natural at every step.

The use of `[Total refund amount]`, rather than the degenerate `'Refund'[Refund amount]`, is essential. Suppose the user selects the raw value `'Refund'[Refund amount]` instead. In the absence of a refund primary key, Power BI may display one row of `$50` for the sales order rather than the correct total of `$100`.

This is another example of why degenerate numeric columns are problematic and why fact tables are better hidden.

### Displaying sales and refunds together

The user may want to see sales and refund business processes simultaneously. This is not one problem. There are three common intentions:

- Show the sales and refund processes side by side.
- Show sales transactions with supplementary refund detail.
- Show refund transactions with the original sales amount.

Each intention has a different grain and therefore a different filtering problem.

#### Side-by-side visuals

Displaying sales and refunds side by side on the same report page is the simplest case.

Suppose there is a table visual for sales with:

- `'Sales ID'[Sales order number]`
- `'Sales product'[Product name]`
- `'Sales calendar'[Sales date]`
- `[Total sales amount]`

And a table visual for refunds with:

- `'Sales ID'[Sales order number]`
- `'Sales product'[Product name]`
- `'Refund calendar'[Refund date]`
- `[Total refund amount]`

These two tables work well because each visual keeps its own business-process grain.

**Shared dimensions behave well.**

If there is a slicer on `'Sales product'[Product name]`, both visuals filter down to the selected product.

If there is a slicer on `'Sales ID'[Sales order number]`, the user can look up a specific sales order and retrieve details of both the sale and any refund.

A user can also click on a row in the sales table and cross-filter to any refund. This works because `'Sales ID'` is a conformed dimension for both `'Sale'` and `'Refund'`.

For the business user, this is extremely convenient. It is one reason the ID dimension is one of the most powerful dimensions and an indicator of a good model.

The same experience cannot be achieved if `[Sales order number]` is used only as a degenerate dimension inside `'Sale'`. If degenerate dimensions are used, the filtering experience becomes frustrating because the shared point of interaction is missing.

**Process-specific dimensions are harder.**

The user experience is seamless when operating on conformed dimensions such as `'Sales ID'` and `'Sales product'`.

It becomes more complicated with the process-specific calendar dimensions.

Users expect to slice by time. But neither calendar works perfectly in every context:

- A slicer on `'Refund calendar'` has no effect on the sales table because it does not filter `'Sale'`.
- A slicer on `'Sales calendar'` correctly filters the sales table, but in the refund table, it returns refunds for products sold on that date—not refunds that occurred on that date.

In simple examples, users may interpret this correctly. In real-world scenarios with multiple dates, this nuance is often difficult to understand. In the worst case, it silently misleads users.

One solution is to create a role-playing `'Reporting calendar'` that links `[Reporting date]` to both `'Sale'[Sales date]` and `'Refund'[Refund date]`.

When used as a slicer, both tables return rows for the selected date. This works because the selection filters the sales and refund facts directly, and the visuals then filter out combinations without matching fact rows.

The chain of filtering behind the scenes creates a seamless experience for the user.

#### Sales with refund details

If the user wants a single table of sales transactions with refund amount, the visual should remain at the sales grain.

Use the sales table columns and add `[Total refund amount]`.

The table visual then has two measures:

- `[Total sales amount]`
- `[Total refund amount]`

The result is:

- All sales transactions display with `[Total sales amount]`.
- Rows with refunds show a value in `[Total refund amount]`.
- Rows without refunds show a blank refund amount.

This works because Power BI displays rows where any measure is non-blank.

In addition, if a refund exists without a sales amount, the row stands out with a blank `[Total sales amount]` and a non-blank `[Total refund amount]`.

However, the user cannot simply add `'Refund calendar'[Refund date]` to this sales-grain visual.

The technical reason is that `'Refund calendar'` relates only to `'Refund'`, not `'Sale'`. The business reason is that one sale can have multiple refunds on different days. It is therefore not logically correct to add refund date to a visual whose intent is one row per sale.

If displaying refund dates is necessary, the data engineer can create a measure such as `[Sales refund dates]` that returns the unique refund date if there is one, or concatenates distinct dates if there are several.

#### Refunds with sales details

The reverse scenario does not mirror cleanly.

If the user creates a refund table and adds `[Total sales amount]`, Power BI may return incorrect results by cross-joining sales and refunds. This happens because `'Refund calendar'[Refund date]` relates only to `'Refund'` and does not filter `'Sale'`. There is no valid relationship path for `[Total sales amount]` to work naturally.

Users may expect to drag `[Total sales amount]` into the refund table and see the original sales amount. Instead, they may get a cross-join of rows.

This is one of the situations where the default dimensional model is not intuitive out of the box and requires additional tuning.

There are several solutions while staying within dimensional modelling:

- Define `[Total sales amount]` to behave differently depending on context using DAX functions such as `treatas`.
- Denormalise the sales amount into `'Refund'` as a value such as `[Sales amount before refund]`, then expose a specific measure for that use case.

The first option gives the most seamless experience for the user, but adds complexity and performance cost to a core business measure. It is often not advisable to complicate a central measure for a narrow scenario.

The second option adds a more narrowly defined measure, such as `[Sales amount before refund]`. This is more explicit, easier to explain, and usually keeps DAX complexity lower overall.

The measure is unlikely to be useful everywhere, but it is useful in the refund context.

### Displaying unit records for three or more business processes

The techniques above rely on conformed dimensions and the existence of fact rows to filter. The ID dimension plays a special role.

This does not scale neatly.

With three or more facts, it becomes difficult to know which combinations of dimension values still have at least one row in any fact. Managing multiple ID dimensions is also complicated because some are conformed across some facts but not others. Many processes also lack a ready business key.

A practical solution is to control display with measures.

The data engineer can create one display measure per business process:

- `[Display sales transaction]`
- `[Display refund transaction]`
- `[Display ... transaction]`

Each measure returns `1` when there is at least one row in its fact under the current filter context.

These measures should be placed in a display folder named `Display unit records`.

A refinement is to return a value only when the relevant ID is in scope. For example, `[Display sales transaction]` may return a value only when `'Sales ID'[Sales order number]` is being used. This can be done with functions such as `ISINSCOPE`.

<!-- TODO: Add screenshot showing display unit-record measures in a table visual. -->

Adding one of these measures to a table visual filters dimension values to those with a matching fact row. This is non-blank measure filtering.

The user can hide the helper column by renaming it and shrinking its width to zero.

<!-- TODO: Add screenshot showing helper display measure hidden by shrinking width. -->

An alternative is to use the measure as a visual-level filter. This is convenient but may have a noticeable performance penalty on large facts.

<!-- TODO: Add Performance Analyzer screenshot showing visual-level filter performance impact. -->

This has a learning curve, but it can be helpful. A model with more than four or five business processes is already likely to be complicated. For a user dealing with this level of complexity, the additional complexity of display measures is minimal. In fact, an explicit menu of display measures can clarify which business process the user is trying to display.

### Cascading filters

Cascading filters refer to the behaviour where selecting a value in one filter narrows the choices in another so that only valid options remain.

For example, if a report page has a slicer for `'Sales product'[Product name]` and another for `'Sales calendar'[Sales date]`, then choosing a product should limit the dates to dates where that product was sold. Choosing a date should limit products to products sold on that date.

This feels obvious to users, but it is not always automatic.

Relationship filtering requires a chain of relationships from one table to the other. In this case, there is no direct relationship path from `'Sales product'` to `'Sales calendar'`. Both filter `'Sale'`, but neither directly filters the other.

Common-fact filtering and non-blank measure filtering usually apply inside a single visual where dimension values and measures are evaluated together. They do not automatically make two slicers filter each other.

The solution is to use visual-level filtering. For example, a measure such as `[Has sales]` can return `1` if there is at least one row in `'Sale'` under the current filter context. The slicer can then use `[Has sales]` as a visual-level filter.

A simple measure might be conceptually:

```DAX
Has sales =
if (
    countrows ( 'Sale' ) > 0,
    1
)
```

The slicer for `'Sales product'[Product name]` can then be filtered to values where `[Has sales]` is not blank. The same can be done for `'Sales calendar'[Sales date]`.

<!-- TODO: Add screenshot showing cascading slicers implemented with a measure visual-level filter. -->

The solution relies on a common fact table and a measure that passes information back to the dimension against the default filter direction.

This is a case where the dimension is on the receiving end of the button-and-effect relationship. The data engineer can support this without using bidirectional relationships across the whole model.

### Aggregating dimension values

Cascading filters aim to filter one dimension by another. Sometimes the goal is to aggregate dimension values by another dimension.

Following the sales and refunds example, suppose the user wants to display a concatenated list of distinct products refunded on each refund date.

If `[Product name]` were already included in `'Refund'` as a raw value, the measure could take the distinct values in `'Refund'[Product name]` and use `CONCATENATEX`.

However, this approach is often not available or desirable.

For example:

- `'Sales product'[Product name]` may be linked to `'Refund'` through `[Product SK]`.
- The user may want to aggregate another column from `'Sales product'`, such as `[Product type]`.
- It is not practical to include all such columns in the fact table.

An inexperienced data engineer might denormalise the required column into the fact table, or even precompute string concatenation in the data layer so the column can be used like a degenerate dimension.

Sometimes this is pragmatic. In general, it is not desirable. It is heavy work to modify a large fact table for every dimension column that users may want to aggregate. Pre-aggregation is also limited because it cannot respond flexibly to user filter context.

The better solution is to notice that the information is already in the model. It only needs to be retrieved under the right filter context.

Measure-defined filtering provides the answer.

The DAX pattern is to concatenate values from `'Sales product'[Product name]` while using `calculate` and `crossfilter` to temporarily allow `'Refund calendar'` to filter `'Sales product'`.

Conceptually:

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

The exact DAX depends on the model, but the principle is the same: temporarily change the filter path for this calculation only.

<!-- TODO: Add screenshot showing refunded products measure and resulting visual. -->

This avoids compromising the whole model with bidirectional relationships or denormalised columns. The model remains clean, and the special behaviour is contained inside the measure that needs it.

### Filter by having

Sometimes the user does not want to filter a dimension by the value it currently has. They want to filter by whether the entity has ever had an attribute.

This is filter by having.

Filter by having means: filter the entity by whether it has, or once had, a matching attribute, rather than filtering only the rows where the attribute currently appears.

Consider an organisation’s HR system. The model contains:

- A dimension `'Employee'` that stores details such as name, email, date of birth, and role.
- `'Employee'` is Type II, so it stores historical changes to employee attributes.
- The key columns are `[Employee ID]`, `[Start datetime]`, and `[End datetime]`.
- `[Employee SK]` is used as the surrogate key for Power BI relationships.
- An end-of-month fact table `'Employee end of month'` stores the employee’s attributes at the end of each month.


**Example structure of `'Employee'`**

| Employee SK | Employee ID | Start date | End date | Employee name | Role |
|---:|---|---|---|---|---|
| 1 | E1001 | 2023-01-01 | 2023-06-30 | Alice Chen | Data analyst |
| 2 | E1001 | 2023-07-01 | 9999-12-31 | Alice Chen | Senior analyst |
| 3 | E1002 | 2023-01-01 | 9999-12-31 | Ben Smith | Finance officer |

**Example structure of `'Employee end of month'`**

| Employee SK | Period end date | FTE |
|---:|---|---:|
| 1 | 2023-06-30 | 1.0 |
| 2 | 2023-07-31 | 1.0 |
| 2 | 2023-08-31 | 1.0 |
| 3 | 2023-08-31 | 1.0 |

`'Employee'` is a dimension filtering the fact `'Employee end of month'`.

| Dimension | `'Employee end of month'` | Meaning |
|---|---|---|
| `'Employee'` | 1 → * via `[Employee SK]` | Point-in-time employee attributes |

In this model, filtering `'Employee'[Role]` filters the fact through `[Employee SK]`. This is correct for point-in-time reporting. It returns the employee-month rows where the selected Type II employee row is active.

That is not always the desired search behaviour.

The user wants to search an employee’s history by personal attributes such as name or role.

Since `'Employee'` is Type II, a direct search returns only the end-of-period states that match the selected point-in-time attribute values. If the user filters `'Employee'[Role]` to `Data analyst`, the model returns only rows where the employee was a data analyst. In the example above, it returns Alice’s June row, but not Alice’s later history as a senior analyst.

That is correct Type II behaviour, but it is not the desired search behaviour.

The desired behaviour is different. The user wants to find employees who have ever had `Data analyst` as a role, then return their full history.

New data engineers often try to solve this by restructuring the fact table. This leads to complex code and confusing artefacts.

A simpler solution is to note that `[Employee ID]` is the identifier of the "true" employee across time, and add a search dimension keyed on this column.

Create `'Employee search'` as a duplicate `'Employee'`. It relates to `'Employee'` on `[Employee ID]` in a snowflake configuration. The relationship is many-to-many and single direction.

**Example structure of `'Employee search'`**

| Employee ID | Employee name | Role |
|---|---|---|
| E1001 | Alice Chen | Data analyst |
| E1001 | Alice Chen | Senior analyst |
| E1002 | Ben Smith | Finance officer |

The revised model looks like this.

| Dimension | `'Employee'` | `'Employee end of month'` | Meaning |
|---|---|---|---|
| `'Employee search'` | * → * via `[Employee ID]` |  | Search by any historical employee attribute |
| `'Employee'` |  | 1 → * via `[Employee SK]` | Point-in-time employee attributes |

Using `'Employee search'`, the user can look up any historical attribute of the employee, retrieve `[Employee ID]`, and return all rows in `'Employee'` that match that ID.

When the user selects `Data analyst` in `'Employee search'[Role]`, the model first finds `[Employee ID] = E1001`. It then filters `'Employee'` to all rows for `E1001`, not only the row where the role was `Data analyst`.

The user searched by a historical attribute, but the model returned the full entity history.

Under this view, `'Employee search'` and `'Employee'` work together as one logical dimension that acts as a search interface for the model.

This pattern generalises. The data engineer can add `'Compliance search'`, `'Qualification search'`, or other derived attribute search dimensions as additional branches of the snowflake.

From the user’s perspective, these are search tables that allow searching employees by their history.

Unlike tampering with fact tables, this solution is non-destructive. The fact table has not changed. The ordinary point-in-time path remains intact. The search dimension adds a new interface path for a different user intention.

### Dynamic Type I

A common workforce reporting request sounds like this: *"When I choose August, show me the last 12 months using the organisation structure as at August."*

This sounds simple, but it is not the default behaviour of a Type II dimension.

Type II dimensions show an entity at its point-in-time attribute. Type I dimensions show the latest attribute value. Neither meets the user intention. What the user would like is Dynamic Type I—latest attribute value as at a user-selected time.


Consider employees and organisation units. The fact table `'Employee end of month'` returns employee metrics at the end of each month. The dimension `'Organisation unit'` is Type II because organisation structures change over time.

**Example structure of `'Organisation unit'`**

| Team unit SK | Team unit ID | Start date | End date | Team name | Group name |
|---:|---|---|---|---|---|
| 1 | T1001 | 2023-01-01 | 2023-06-30 | Data engineering | Group A |
| 2 | T1001 | 2023-07-01 | 9999-12-31 | Data engineering | Group B |
| 3 | T1002 | 2023-01-01 | 9999-12-31 | Finance operations | Group A |

**Example structure of `'Employee end of month'`**

| Team unit SK | Team unit ID | Period end date | Commencements |
|---:|---|---|---:|
| 1 | T1001 | 2023-06-30 | 2 |
| 2 | T1001 | 2023-07-31 | 1 |
| 2 | T1001 | 2023-08-31 | 1 |
| 3 | T1002 | 2023-08-31 | 1 |

In the ordinary Type II model, `'Employee end of month'` relates to `'Organisation unit'` through `[Team unit SK]`.

| Dimension | `'Employee end of month'` | Meaning |
|---|---|---|
| `'Organisation unit'` | 1 → * via `[Team unit SK]` | Point-in-time organisation hierarchy |

In the example, Team `T1001` belonged to `Group A` in June, then moved to `Group B` in July.

If the user selects August and asks for commencements in the last twelve months, they may expect all activity for Team `T1001` to appear under `Group B`, because that is the organisation structure as at August. The correct answer is a total of 4 commencements.

The ordinary Type II relationship does not do that. It reports each fact row using the organisation structure that was valid at the time of the row. June remains under `Group A`; July and August appear under `Group B`. This returns 2 commencements, the incorrect result.

Thus, Dynamic Type I changes the lens. It says: use the selected reporting date to decide which organisation-unit row is current, then view the relevant historical facts through that selected-date structure.



#### Solving Dynamic Type 
The problem is notoriously complex to solve by amending the fact table. It requires associating the organisation unit’s full history with each fact row. That approach is complex, fragile, and expensive.

The key is to recognise that the model already has the history in `'Organisation unit'`. The information is already in the model, and what's missing is to surface it. The better solution is to surface it at query time.

There are two steps.

First, broaden the relationship for evaluation.

The problem with the existing relationship is that it is too "narrow"—locking the dimension into a smaller set of data than intuitive to business sense. The first step is to "unlock" this relationship between the organisation unit to the activity rows that are relevant to it.

This means relating each fact row not only to a single point-in-time row in `'Organisation unit'`, but to all rows for that `[Team unit ID]`. This requires a many-to-many, single-direction relationship on `[Team unit ID]`. Each fact row now has the full history of its team available during calculation. 

The relationship becomes:

| Dimension | `'Employee end of month'` | Meaning |
|---|---|---|
| `'Organisation unit'` | * → * via `[Team unit ID]` | Relates all rows based on the persistent team unit identity |

Second, select the valid row at query time.

The consequence of the relationship is that, though the data is available in the filter context, too many rows are selected for display. We now need to narrow this again.

In the measure, we take the latest date in the current context and filter `'Organisation unit'` to the row whose validity covers that date:

```md
[Start date] <= selected date < [End date]
```

For a given `[Team unit ID]`, this should return one row because the primary key is `[Team unit ID]` and `[Start date]`.

Under this filter, the table behaves like a one-to-many join for that evaluation. The measure returns values only for the valid organisation-unit row. Other rows go blank and drop out through non-blank measure filtering.

For August 2023, `T1001` resolves to the row where `[Group name] = Group B`. The measure can then report prior-period activity using the August 2023 organisation view.

This creates a problem. The original `'Organisation unit'` no longer behaves as before. This could be problematic. If the original behaviour needs to be preserved, there are two broad implementation options.

#### Option A—Keep one dimension and switch in measures

The first option is to do the switching in the measure.

In this scenario, we keep the normal one-to-many, single-direction relationship on `[Team unit SK]`, and then add a many-to-many, single-direction relationship on `[Team unit ID]`. It remains dormant by default.

In measures that need dynamic Type I, deactivate the `[Team unit SK]` path and allow the `[Team unit ID]` path to apply for the calculation. Then filter to the valid row as above.

<!-- TODO: Add screenshot of DAX for dynamic Type I measure using dormant relationship. -->

In this implementation, `'Organisation unit'` works as Type II by default, and the user chooses the dynamic Type I perspective through measures.

#### Option B—Add a new dimension

The second option is to switch through dimensions. This is done by duplicating `'Organisation unit'` as `'End of period organisation unit'`, and adding `[Team unit ID]` to `'Employee end of month'`. 

The fact now carries:

- `[Team unit SK]` for the normal relationship to `'Organisation unit'`
- `[Team unit ID]` for the many-to-many relationship to `'End of period organisation unit'`

<!-- TODO: Add screenshot showing duplicate End of period organisation unit relationship. -->

The revised evaluation model is therefore:

| Dimension | `'Employee end of month'` | Meaning |
|---|---|---|
| `'Organisation unit'` | 1 → * via `[Team unit SK]` | Ordinary Type II path |
| `'End of period organisation unit'`| * → * via `[Team unit ID]` | Dynamic Type I evaluation path |

Measures that need dynamic Type I behaviour can be wrapped.

For example, rename `[Employee commencements]` to `[_Employee commencements]`. Then define `[Employee commencements]` so that it evaluates `[_Employee commencements]` inside `calculate`, filtering `'End of period organisation unit'` to the valid row as at the latest date in context.
<!-- TODO: Add screenshot of DAX for dynamic Type I measure using duplicate dimension. -->
In this option, the user chooses perspective by choosing the dimension:

- `'Organisation unit'` gives Type II.
- `'End of period organisation unit'` gives dynamic Type I.


Under both options, the original dimension keeps its normal behaviour. Existing measures continue to work. Both options are non-destructive.

The distinction is whether the user chooses Type II or dynamic Type I through different dimensions, or through different measures.

The important point is that Dynamic Type I does not rewrite history in the fact table. It changes the reporting lens at query time.


## Buttons and effects

The take-away from above is not exhaustive list of filtering techniques. That would be a book in itself.

Their purpose is to illustrate a philosophy of seeing Power BI as an interface that users touch to produce effects.

In this philosophy, every table tends to have one of two roles:

- Tables that define the interface as buttons to click, usually dimensions
- Tables that define the content that drives the effect, usually facts

A good model keeps these roles separate.

Every table should have one clear purpose. Tables should not mix interface and content unless there is a deliberate reason. This is why an indicator of quality is that fact tables are hidden.

The first scenarios showed how dimensions present information from facts through the difficult case of displaying transaction records. They illustrate that fact tables, which are the natural focus for new data engineers, are not the artefacts to expose to users.

Trying to expose fact tables and degenerate dimensions causes issues. Dimensions should act as the entry point to the data.

The same philosophy explains why degenerate dimensions and bidirectional relationships often frustrate users. They blur the line between tables that act as buttons and tables that create effects.

The examples of cascading filters and aggregating dimension values show that the data engineer can handle cases where a dimension is on the receiving end of a button-and-effect relationship without compromising the model with degenerate dimensions or broad bidirectional relationships.

The final examples generalise the idea of a dimension to a set of tables. A dimension is not simply a lookup table. If the user sees it as intuitive and gets the desired outcome unambiguously and quickly, that is what matters.

In this view, a dimension’s chief purpose is to be the user’s interface to the model.

This is the philosophy of separation of concerns from software design. It maintains a clear distinction between the interface layer and the content layer.

Power BI supports this through the five filtering mechanisms described at the start of the chapter. This perspective pushes the data engineer to see a data model as software and to design a clean interface that is business-centric and intuitive for the user.



> [!NOTE]
> **Key ideas**
>
> Filtering design is what makes a Power BI model feel intuitive—or frustrating.
>
> A self-service model is not a puzzle for the user to solve. The correct answer should not merely be reachable; it should be reachable through likely paths of interaction.
>
> Filtering is the mechanism that turns model structure into user experience.
>
> Dimensions usually provide the buttons: the things users select, slice, search, group, and compare.
>
> Facts and measures provide the effects: the activity, state, and values that respond.
>
> Power BI filtering commonly occurs through relationships, common facts, non-blank measures, visual-level filters, and measure-defined filtering.
>
> Degenerate dimensions and broad bidirectional relationships often blur the distinction between buttons and effects.
>
> Good filtering design anticipates how users will interact with the model and makes sensible behaviour occur naturally.
