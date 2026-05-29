---
title: Designing measures
url: /docs/presenting-insights/designing-measures/
description: Explains how to design useful, business-centric measures in Power BI and how to think clearly about their role in a model.
lede: A dimensional model is only as useful as the measures it makes easy to use.
weight: 5
draft: true
---

Measures are the face of facts. If dimensions are the interface of the model, measures present the effect of that interaction. Fact tables provide the content. Measures turn that content into answers. As explained in Filtering behaviour, measures also give the user an explicit way to control filtering. They are part of the interface and deserve deliberate design. For this purpose, Power BI’s implicit calculations can do more harm than good. For this reason, Discourage implicit measures should be turned on.

This chapter covers three areas. First, indicators of good measures. Second, the four types of measures. Third, basic technical patterns for building measures. The next chapter, Measure of measures, introduces techniques for managing many measures in a structured way.

## Indicators of good measures

There are two indicators of good measures, business centricity and technical simplicity.

### Business centricity

Every aspect of a measure should reflect business meaning. This includes its definition, name, its hover text, its display folder, and its placement alongside related measures.

#### Alignment to business reality

When designing measures, one of the most important criteria is alignment to real-world events. A common mistake is to perform a distinct count on a database key and assume it reflects a meaningful metric — even when the key has no real-world correspondence.

For example, a data engineer might define a measure like [Inspection count] as the distinct count of [Inspection ID] in the Inspection fact table. However, [Inspection ID] may simply be a system-generated key used for record retrieval. It carries no inherent meaning. In the future, the system design might change its implementation to split one inspection into ten rows or merge ten into one for record-keeping purposes. This does not reflect a genuine change in inspection effort. The measure is misaligned with reality.

Instead, every measure should quantify real-world business events that users recognise and care about. In this example, the data engineer could:

1. Measure the time taken to conduct an inspection

2. Measure the number of entities inspected

The second option is particularly useful across a wide range of scenarios — whether counting entities inspected, entities failing a criterion, or entities reaching a milestone.

It is easily implemented when the entity of interest has been clearly defined from the outset, and when the pipeline consistently computes and aggregates information at that grain. This is one of the purposes of the Reduce step in the pipeline.

#### Business explicit

The definition of a measure should be explicit on its business meaning, rather than generic. A common misstep among new data engineers is to create a single technical measure—such as [Employee count], a distinct count of employees in an end-of-period fact table—and assume that users will derive all other insights through manual filtering.

This approach places undue burden on users, requiring them to memorise arcane filter combinations to arrive at answers. A more effective model presents a suite of measures that surface answers directly.

In the case of employee metrics, this suite might include:

- [Active employees end of period] — employees with an “active” [Employment status] at the end of each period. If unambiguous, this may be shortened to [Employees end of period].

- [Separated employees end of period] — employees with a “separated” status at the end of the period.

- [Current number of employees] — the latest value of [Active employees end of period], suitable for grab-and-go use.

- [Current employees on long service leave] — a subset of [Current number of employees] filtered by [Is on long service leave].

These examples illustrate the breadth of possible measures beyond a generic [Employee count]. Requiring users to manually filter for each scenario is both error-prone and frustrating.

In most cases, a technical measure such as [Employee count] which is a distinct count of all employees across the organisation’s history, offers little business value. If not directly useful, such measures are better omitted. Where technical measures are needed to support other calculations, they can be hidden from the interface and prefixed with an underscore. For example, [_Employee count] and [_Employee count] end of period may serve as internal components for more meaningful outputs.

#### Names

Names must be explicit, grammatical, and able to stand alone. Measures can be dragged anywhere on the canvas, so the name should carry its context. Prefer [Employee count] to [Count]. Avoid non-standard abbreviations. Saving a few characters does not help the user or the next engineer.

#### Description

Hover-text descriptions should also reflect business meaning. Users should not be expected to accept complex logic without explanation. As the first point of contact for many users, the measure description is an opportunity to build trust. Descriptions should articulate the business logic behind the measure, not restate the DAX syntax.

For more intricate cases, near-pseudocode in business language may be appropriate.

#### Display folder

Display folders offer a practical way to reinforce business centricity. Measures can be grouped by business process, while technical or dashboard-specific measures such as those for colour formatting or data currency can be placed in folders like “Dashboard” or “Data currency.”

#### Proximity to other measures

The business centricity of a measure is influenced by its proximity to other measures.

The two ways of proximity are alphabetical placement within a display folder and keyword-based lookup in the field list. These interactions warrant deliberate consideration from the data engineer.

When similar measures are defined explicitly, they help users form a clearer mental model of the data. For example, the presence of [Separated employees end of period] reinforces the meaning of [Active employees end of period], reminding users of the separated employees that may have been unconsciously forgotten. Likewise, [Current number of employees] clarifies that [Active employees end of period] is a point-in-time measure. These compare-and-contrast relationships benefit from thoughtful naming that places related measures adjacent to one another.

A data engineer can take advantage of the proximity effect by consciously placing these compare-and-contrast measures next to each other through alphabetical naming.

### Technical simplicity

Measures in Power BI should be technically simple. The foundations for technical simplicity are laid when building the data pipeline, not when designing the dimensional model. There are two ways to achieve this – precomputing complex information and relying on binary flags for simplification.

#### Precomputing complex information

Complex information should be computed and stored in the data layer. This frees the measures from the burden of handling business logic and allows them to focus solely on supporting user interaction. If the DAX is non-trivial, it is a sign that the model design may be sub-optimal.

Throughout Creating information, the emphasis is on creating meaningful fragments that can be used as plug-and-play by users. For instance, if [Is on long service leave] is a complex calculation that requires windowing across an employee’s attendance, then this calculation can be precomputed in a fragment called HR.EmployeeLeave.

The most important case of precomputing complex information is that of summary dimensions. In many scenarios, the complexity of information comes from having a lot of finer details in subprocesses for an entity of interest. Precomputing these, and pushing their expression to reference data tables, allows the data engineer to access all this complex information without repeating it in DAX. Of the summary dimensions, the most important is the storytelling dimension. These are explained in the Storytelling chapter.

Precomputing complex information can be overdone. Data engineers who are unfamiliar with the features of Power BI can end up repeating heavy computation that could be extracted from the model data itself with the appropriate configuration or DAX definitions. More significantly, precomputing information can lead to loss of interactivity, such as pre-aggregated string values that can no longer be filtered down.

In some cases, precomputation can even lead to wrong results, such as taking averages of averages rather than using the unit-record data in the model to calculate non-additive measures.

In general, precomputing complex information should not result in an awkward distortion of the dimensional model. Data engineers can avoid this by being familiar with the content of Filtering behaviour and the techniques introduced later in this chapter.

#### Preparing binary flags

Binary flags are columns with true or false values. Their main place is in the reference tables, and hence dimensions in the dimensional model. For example, an ‘Employee leave’ dimension may have an [Is on long service leave] column to indicate whether the employee is on service leave at the end of the period of the ‘Employee end of month’ fact table.

Binary flags have a special place in simplifying DAX formulas. As an example, [Is on long service leave] can replace text filters such as [Leave status type] in (“Long service leave”, “Extended leave”). But they can also replace more complex calculations, such as checking the employee’s attendance, by pushing this to the data layer.

Binary flags are preferred because, firstly, they are syntactically checked. A developer misspelling “Long service leave” in text does not result in a syntax error. However, the same spelling mistake in the column name [Is on long service leave] will result in an error. This is a small enhancement, but over a model with hundreds of measures, the possibility of spelling mistakes drastically adds up. Binary flags help mitigate the risk.

Secondly, binary flags are simple to use in a DAX formula. As a binary column, it does not require any equality operators. For example, instead of

```dax
[Current employees on long service leave] =
CALCULATE(
    [Current number of employees]
    , KEEPFILTERS(‘Employee leave’[Is on long service leave] = TRUE)
)
```

The formula is simply:

```dax
[Current employees on long service leave] =
CALCULATE(
    [Current number of employees]
    , KEEPFILTERS(‘Employee leave’[Is on long service leave])
)
```

The reverse can be expressed with a NOT, as in:

```dax
KEEPFILTERS(NOT ‘Employee leave’[Is on long service leave])
```

As a binary column, they participate elegantly in AND, and OR operators.

> [!NOTE]
> TODO: Insert manuscript screenshot or diagram from the source draft. Source PDF note: `[SCREENSHOT]`.

As a binary column, they participate elegantly in AND and OR operators.

Using binary flags, the measures are faster performing, easier to maintain, and easier to understand. The business logic has been suitably abstracted so that each measure is self-explanatory.

## Four types of measures

It is useful to distinguish four types of measures. These are not technical categories, but functional ones.

- Aggregating measures

- Dimensional measures

- Filtering measures

- Dashboard measures

### Aggregating measures

Aggregating measures are the ones most people think of when they think of measures.

These include counts of rows or sums of values against the fact tables. In more complex cases, they may need to respond to the user’s evaluation context, such as calculating the number of employees at the end of a period.

### Dimensional measures

Dimensions contain attributes that are generally used for grouping other measures.

Dimensional measures are those where dimensional values become measure values themselves. One example was described in the chapter Filtering behaviour under the scenario Aggregating dimension values. In that example, the requirement was to display all products that had been refunded on a particular day.

It is important to recognise dimensional measures as a separate category for two reasons. First, the values are often drawn from the dimension tables rather than the fact tables. This means they are not subject to the usual filtering setup in a dimensional model and may require special adjustment in DAX formulas to support interactive behaviour.

Second, dimensional measures are often mentally confused with the dimension value itself. A dimension value can be used to cross-filter, and can be placed as rows or columns in a matrix visual. A dimensional measure, however, cannot be used for either.

Its chief purpose is display and does not offer cross-filtering interactivity. That interactivity must come from other dimensions in the visual.

In the case of a degenerate dimension in a fact table, such as displaying a concatenated list of free-text comments in an annotation fact, it becomes academic whether the measure is dimensional or aggregating. The distinction is less important than recognising that attributes can become measure values as well, with its different filtering properties.

### Filtering measures

As explained in Filtering behaviour, measures offer a way for the data engineer to explicitly control filtering. This is done through non-blank measure values and through use in a visual-level filter. Consequently, the model may contain measures whose sole purpose is to control filtering. These typically return either 1 or blank.

Examples include the [Display unit records] measures described in Filtering behaviour.

Other examples may be [Has sales] or [Has employee leave], which also return either 1 or blank. The difference is that [Display unit records] are intended to be used strictly with the ID dimensions to list out business transactions. This enforcement may be done via the function ISINSCOPE.

Even in the case of filtering measures, they must remain meaningful for the user. The description should explain how the measure is to be used.

### Dashboard measures

Dashboard measures refer to measures designed specifically for creating a visually attractive and informative report. These may include coloured arrows, icons, or expressions that display the user’s selection context via SELECTEDVALUE. Power BI supports their use in a wide range of scenarios, including report titles, chart titles, and chart colours.

## Technical patterns

The following introduces technical patterns that cover a wide range of usage scenarios.

The first three fall under the standard case:

- Base measures

- Derived measures

- Dashboard measures

Then three more scenarios that are more complex:

1. Polymorphism

2. Hidden grain

3. Unsupported relationships

The next chapter will introduce an additional technical pattern using switch measures.

Measures in Power BI require unit testing. This is especially the case for more complex ones. This is covered in the chapter on Automation.

### Base measures

Base measures interact directly with the fact tables in a straightforward way.

For measurable facts, these include SUMX, DISTINCTCOUNTNONBLANK, COUNTROWS, and similar aggregations.

For end-of-period facts, these include an additional detection of evaluation context to find the latest date in context and then evaluate an aggregate measure for that period.

For annotation facts, these include CONCATENATEX to display detailed textual values.

As explained in Technical simplicity, these measures should be simple and largely a direct aggregation of the fact tables, supported by a KEEPFILTERS on a binary column to narrow to specific business usage. For example, [Current employees on long service leave] should be derived from [Current number of employees] on the [Is on long service leave] column.

### Derived measures

Derived measures are the next level from basic measures. These include ratios, time-intelligence, and population comparisons.

Ratios apply DIVIDE to two basic measures.

Time-intelligence applies standard techniques for calculating rolling periods, same period last year, and similar scenarios.

Population measures “escape” from the filter context to compare the measure with a larger population, such as comparing a team’s metric with the national metric. These can be achieved using functions such as REMOVEFILTERS.

Derived measures often follow repetitive patterns such as calculating a number for the same period last year. This could be better managed using calculation groups or switch measures.

### Context-aware measures

Dashboard measures are one of the four types described earlier. They are designed to create visually attractive and informative dashboards. As such, they often need to “reach out” to inspect the filtering context that the user has chosen. For example, a report title may display the product name if one product is selected, or show “Multiple products” if more than one is selected.

DAX supports a wide range of context-awareness functions including ISFILTERED, ISINSCOPE, HASONEVALUE, and SELECTEDVALUE. They explicitly target what the user has selected. The functions VALUES and ISBLANK can be used to query dimensions to inspect what values exist in the filter context, which can inform the measure outcome.

Another common pattern is to select the maximum reporting date from the model’s chief reporting calendar to reflect the latest date selected by the user.

For simple business processes, these patterns cover the bulk of usage scenarios.

However, there are occasions when the dimensional model does not allow such straightforward implementation. The following scenarios allow a DAX solution without making drastic changes to the model.

### Polymorphism

Polymorphism refers to the idea that the value of one column depends on the value of another. A common case is the header–details situation where actions can take place on either. For example, a business process may inspect travellers (header) and their bags (details) for contraband goods. The 'Inspection' table may record inspections on both. A column such as [Inspection item type] with values “Traveller” and “Bag” determines the meaning of [Inspected item SK].

In this scenario, a simple DISTINCTCOUNT of [Inspection item SK] will not give the total number of distinct items inspected. In a well-designed dimensional model, the determining column would be expressed in a dimension. For example, an 'Inspection type' dimension would contain [Inspection item type], while the aggregated value [Inspection item SK] is in the 'Inspection' fact table.

The solution is to create a temporary table using SUMMARIZE to group on the determining column, apply per-segment aggregation on the fact table, and then aggregate over the segments.

```dax
var inspection_per_type =
    SUMMARIZE(
        ‘Inspection type’    # group by dimension
        , ‘Inspection type’[Inspection item type’   # on the polymorphic resolving column
        , “Inspection count”
        , DISTINCTCOUNTNOBLANK(‘Inspection’[Inspection item SK])  # aggregating fact per segment
    )
return sumx(inspection_per_type, [Inspection count]) # adds up the result from each segment
```

If there are any sub-selection necessary, KEEPFILTERS can be applied to SUMMARIZE by wrapping it inside CALCULATETABLE.

New data engineers often tackle this sort of problem by creating an artificial single column, such as a concatenation of the item type name and the item SK, and applying a distinct count on that composite column. The approach above avoids any model change.

As with many complex DAX challenges, the idea is to treat it almost as if it were a SQL problem and translate the solution to DAX.

### Hidden grain

A generalisation of the previous problem is the case of hidden grain. Power BI supports greater flexibility in DAX and has a more relaxed requirement on table grain compared to traditional dimensional modelling. This allows a single fact table to work at the details with the embedded header rather than having one for header and one for details.

Or even present multiple subprocesses of incompatible granularity as one fact table.

This is explored further in the chapter Anticipating questions.

In these scenarios, the model may have granularity embedded through denormalisation, and not explicitly available as its own grain. In this case, some important aggregating measures such as SUMX, AVERAGEX, and MEDIANX no longer work.

ID dimensions provide a ready solution. They preserve the primary keys of a business process and allow reconstruction of information at the grain defined by that key.

The implementation is to use SUMMARIZE on the ID dimension, either directly or through its storage on the fact table as a relationship column, selecting any relevant columns to reconstruct the grain into a temporary table, and then performing aggregation on that table.

Following the previous example of traveller inspection, there is a record of the total inspection time for the traveller which includes the inspection of the traveller as well as any bags on person. Suppose this is recorded as [Inspection duration (mins)] and [Traveller SK] and have been denormalised into the Inspection fact table. A measure that calculates [Median time to inspect a traveller] can do so by re-extracting the grain through SUMMARIZE:

```dax
var inspection_time_per_traveller = SUMMARIZE(
    ‘Inspection’
    , ‘Inspection’[Traveller SK]
    , ‘Inspection’[Inspection duration (mins)]
) # reconstruct the table at the traveller grain
Return MEDIANX(inspection_time_per_traveller, [Inspection duration (mins)])
```

In SQL terms, this is similar to using “select distinct” on a set of columns in a denormalised table to retrieve the desired grain, and then aggregating over the result set. The selection of a primary key ensures the resulting grain is correct.

### Unsupported relationships

Unsupported relationships refer to scenario when the default filtering configuration of using single-direction, dimension to fact relationships does not easily support a query.

Rather than making large structural changes to the model, the data engineer may approach the challenge through DAX.

The most powerful tools for writing queries not naturally supported by the model’s relationships are CROSSFILTER, TREATAS, and USERELATIONSHIP.

As seen in Aggregating dimension values in Filtering behaviour, CROSSFILTER can be used to temporarily turn a relationship to bidirectional. This allows the retrieval of dimension values by another dimension.

TREATAS allows the data engineer to work as if a relationship has been defined, even when none exists. This is particularly powerful in a model with ID dimensions that allow the lookup of any information at the unit-record level. There is a performance penalty for this sort of usage, but it can be the right tool for the correct situation, especially under tight timeframes where adding new relationships is not possible. TREATAS can still be used as long as the information is in the model.

If two tables have two relationships between them where one is active and one is inactive, then USERELATIONSHIP can activate the inactive one and use that as the filtering path. If both relationships are active, one will have precedence, and USERELATIONSHIP can be used to deactivate the primary one. This usage implies that the data engineer has consciously built an additional relationship to support specific measures that use a relationship path different from the model’s default. An example is described in Dynamic type I in Filtering behaviour.
