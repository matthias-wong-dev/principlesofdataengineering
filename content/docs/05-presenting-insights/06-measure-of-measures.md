---
title: Measure of measures
url: /docs/presenting-insights/measure-of-measures/
description: Introduces the measure of measures pattern for structuring related Power BI measures and managing derived calculations.
lede: Measures can be organised as a business dimension, not just a list of calculations.
weight: 6
draft: true
---

In a complex organisation, there are always multiple business processes, and multiple measures per process. Quite often, there is an underlying structure to these measures.

Consider a company that handles its own manufacturing, orders, and shipping. These are three business processes, each represented by a measurable fact table:

Manufacture, Orders, and Shipping.

Each process has three metrics for operational efficiency:

1. Process volume

2. Median time to process

3. Volume processed on schedule

This results in nine base measures:

1. [Manufacture process volume]

2. [Manufacture median time to process (days)]

3. [Manufacture volume processed on schedule]

4. [Orders process volume]

5. [Orders median time to process (days)]

6. [Orders volume processed on schedule]

7. [Shipping process volume]

8. [Shipping median time to process (days)]

9. [Shipping volume processed on schedule]

These are base measures and is one of the types of measures in Designing measures.

From these, two derived measures are needed:

1. Percentage processed on schedule

2. National comparison

Calculating percentage processed on schedule for each process stage leads to 3 additional measures and 12 total. If national versions are created for all 12, the total becomes 24. This is manageable, but there are two problems with this approach.

- Unarticulated structure. The measures clearly have a structure to them, but this is not expressed formally. They exist only in the naming convention of the measures.

- Complex DAX maintenance. Even a simple set up of three processes lead to 24 measures just on basic measures and not including other metrics such as quality control or profitability. This could easily overwhelm.

## Pattern for a measure of measures

The measure of measures pattern introduces structure to the measures. Building it requires three elements:

1. A measure table

2. Switch measure

3. Formatting calculation group

The measure table is simply a list of measure names, annotated by columns that describe the measure. Continuing with the example, a table called ‘Operational metric’ with three columns:

4. [Measure name] – the names of all the nine measures

5. [Process stage] – “Manufacture”, “Orders”, and “Sales”

6. [Metric] – “Process volume”, “Time to process”, “Volume processed on schedule”

The full table is thus nine rows, one for each measure:

| Measure name | Process stage | Metric |
| --- | --- | --- |
| Manufacture process volume | Manufacture | Process volume |
| Manufacture median time to process (days) | Manufacture | Time to process |
| Manufacture volume processed on schedule | Manufacture | Volume processed on schedule |
| Orders process volume | Orders | Process volume |
| Orders median time to process (days) | Orders | Time to process |
| Orders volume processed on schedule | Orders | Volume processed on schedule |
| Shipping process volume | Shipping | Process volume |
| Shipping median time to process (days) | Shipping | Time to process |
| Shipping volume processed on schedule | Shipping | Volume processed on schedule |

In defining this table, it is important to apply a display order where there is a rank. For example, [Process stage] is in order of manufacture, orders, and shipping. It happens these are already ordered correctly alphabetically and the [Process stage display order] is not necessary in this case. In general, such ranking columns are necessary to express the business order.

The switch measure returns the correct base measure based on the selected row in ‘Operational metric’:

This is a switch measure because it uses a switch to decide on the calculation. And since the switch is simply to select the value of another measure, it is thus a measure of measures.

After defining [Operational metric], three business metrics can be defined by filtering [Operational metric] on the [Metric] value:

Derived measures can now be written once rather than 3 times:

National comparisons can also be written once:

In this case, the nine base measures are first order measures, while [Operational metric], [Process volume], [Percentage processed on schedule], [National operational metric] are second order measures because they are calculated base off the switching of the first order measures.

The final element is a formatting calculation group. Power BI does not support dynamic formatting in switch measures by default. Consequently, all values returned by the switch measure do not honour the original format. A calculation group can reapply the format with the appropriate formatStringDefinition:

```dax
switch(
    selectedvalue('Measure'[Measure name]),
    “Manufacture process volume”, ‘TODO’,
    “Orders process volume”, ‘TODO’,
    “Shipping process volume”, ‘TODO’,
    …,
    selectedmeasureformatstring()
)
```

## Benefits

The measure of measures has important implications for measure management and report building. In some cases, it is the only viable solution without creating a tangle of DAX definitions or nightmare reports.

The first benefit is simplified DAX management. Instead of repeating near-identical logic across multiple measures, such as three versions of percentage processed on schedule or twelve national metrics, the measure of measures allows a single point of definition.

The second benefit is explicit structure. The underlying logic of the nine base measures is now expressed explicitly in a single table. This enables visuals that are otherwise impossible. For example, a matrix with [Metric] as rows, [Process stage] as columns, and [Operational metric] as values:

| Metric | Manufacture | Order | Shipping |
| --- | --- | --- | --- |
| Time to complete | | | |
| Process volume | | | |
| Volume completed on time | | | |
| Percentage processed on schedule | | | |

The formatting calculation group can be used here to ensure all the measure values are presented in the correct format – whole numbers, decimals, percentages.

This visual is impossible to build with 12 separate measures.

The third benefit is powerful reporting. A matrix with [Process stage], [Metric] as rows, [Reporting year] as columns, and [Operational metric] as values allows immediate comparison across years, with conditional formatting to highlight deterioration:

| Process stage | Metric | 2022 | 2023 | 2024 |
| --- | --- | --- | --- | --- |
| Manufacture | Time to complete | | | |
| Manufacture | Process volume | | | |
| Manufacture | Volume completed on time | | | |
| Manufacture | Percentage processed on schedule | | | |
| Orders | Time to complete | | | |
| Orders | Process volume | | | |
| Orders | Volume completed on time | | | |
| Orders | Percentage processed on schedule | | | |
| Shipping | Time to complete | | | |
| Shipping | Process volume | | | |
| Shipping | Volume completed on time | | | |
| Shipping | Percentage processed on schedule | | | |

This allows the user to see the changes of all measures changing across years in a single visual, with conditional formatting to highlight any significant deterioration.

There are many ways to use the structure expressed by 'Operational metric'. The [Process stage] column can be used for small multiples in line charts, creating a series of visuals in a controlled and automated manner. It can also serve as a legend to compare metrics directly, such as identifying lags or discrepancies in [Process volume] between manufacture, orders, and shipping.

If each process is managed by a different team, [Process stage] can be used as a report page filter to tailor the view to each manager’s concern.

Used appropriately, the measure of measures enables powerful reports that would otherwise be impractical or impossible.

Finally, the measure of measures allows the users to perform operations on the measures rather than the fact tables behind the measures. Inexperienced data engineers attempting the similar outcomes often would try to tackle the problem by forcing the fact table rows into an awkward union. The measure of measures avoids this. In the perspective of Conforming systems, the measure of measures allow the data engineer to use the horizontal integration pattern when the vertical integration pattern is not appropriate.

## Dangers

Data engineers should use a measure of measures judiciously.

The SWITCH function can be suboptimal when filtering on a column other than the switch value, such as [Metric] instead of [Measure name], or a conformed dimension off [Process stage]. With 40 or 50 branches, performance degrades noticeably. The pattern should be tested in practice for each model.

Dynamism can be overused. In theory, any list of measures can be placed into a switch, but this is not always helpful. The criterion is business expressiveness. The pattern is appropriate when the measures form a coherent structure such as process stages, business lines, or quality criteria in a product line. The pattern is not appropriate when the measures are unrelated or when the structure is unclear.

Report builders can also get carried away. Dynamism is often a sign of bad design. If users must click before seeing what is important, the report is likely poor. A report with ten selectable metrics is not intuitive. The measure of measures should be used to create explicitly expressive visuals, not to hide information behind implicit interaction.

Finally, the measure of measures requires the user to select enough of the measure table’s primary key columns to resolve to a specific measure. Without this, the switch returns no value. For example, selecting [Metric] = "Process volume" without specifying [Process stage] will not return a result. This is by design. The pattern is intentionally built not to aggregate across measures by default. It prevents accidental errors such as summing what should not be summed or averaging averages. If aggregation across measures is needed, such as summing [Process volume] across all stages or computing a weighted average of [Median time to process], then it must be explicitly defined and tailored to the metric.

## Conclusions

Most discussions of the SWITCH function in Power BI focus on its technical role — selecting between multiple measures based on user input, typically via a disconnected slicer table. This is often described as a UI convenience or a way to reduce visual clutter.

However, the measure of measures is not about UI convenience but is about business meaning. Instead of using SWITCH merely to toggle between measures, it is used here to express the structure of the measures themselves. The measure table is a business dimension that categorises measures by meaningful attributes like process stage, metric type, or quality indicator. Consequently, the measure of measures serves, not merely as a technical trick, but a modelling technique that:

- Makes the business metrics, as implemented by the measures, explicit and navigable

- Enables structured reporting (e.g. matrix visuals by metric and process)

- Supports derived measures (e.g. percentages, comparisons) without duplication

In short, the measure of measures is another application of the principles of expressiveness and fragment modelling. Without the anchor in expressiveness, the data engineer is at risk of creating dynamism for its own sake and creating a frustrating report for the user.

Finally, the pattern highlights the philosophy of a good Power BI dimensional model that measures are the face of fact tables, and can be directly manipulated rather than reshaping the facts. The pattern is a natural fit within the horizontal integration pattern from Conforming systems.
