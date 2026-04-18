---
title: Storytelling
weight: 6
draft: true
---

Many refer to the principle of garbage-in, garbage-out. This principle is well known, but the challenge to the data engineer goes further. It is not only about avoiding poor inputs. It is about the need to proactively add information by reorganising the data or by annotating it with context to create a new, meaningful way of seeing the data that resonates with business decision-making.

So far, the focus has been on achieving this through the creation of expressive entities, ensuring that each object in the model corresponds clearly to business interest. This chapter explores three additional approaches: defining the concept of “good” and “bad” entities, trading details for insights, and the use of storytelling dimensions.

## Good and bad entities

Business often sees the world through the lens of “good” and “bad.” A trade that makes a profit is good; a trade that makes a loss is bad. In government, the distinction is often between compliance and non-compliance. In some cases, only the concept of “bad” exists, as in the case of fraudulent transactions. Yet many digital systems are built mainly to support workflows and lack a nuanced view of good and bad, and thus the concept is missing from the data source.

One of the most effective ways for a data engineer to add value is to apply this lens to business entities. Sometimes the definition is obvious to the business user. Other times, it is latent in the way stakeholders talk about the data. The data engineer can proactively surface this latent definition by listening carefully during discussions and asking the right questions.

Once defined, the concept can be expressed through a reference table and a new fragment. As a simplified example, a `Cake.Production` table can be the basis for a `Cake.ProductionFailure` table and a `Cake.RefProductionFailure` table. The reference table might contain a binary column such as `[Production failure outcome]` with values `Production failure` and `No production failure`. It can also be more nuanced and include `[Failure reason]`. The fragment table itself would contain just two columns: `[Production ID]` and `[Production failure ID]`, pointing to the reference table.

> [!NOTE]
> **TODO**
>
> The manuscript includes example diagrams here.

The definition of good and bad can be a significant point of debate in a complex organisation with different business viewpoints. In these situations, it can be extremely challenging to arrive at a consensus. Many organisations fail to do so, crippling their ability to see issues consistently. In this case, it is often the creativity and technical expertise of the data engineer that can broker between parties by showing the way forward.

## Trading details for insights

As in many fields of endeavour, less is often more. In data engineering, this principle applies directly for surfacing insights.

Take `Cake.Sales` as an example. The business may be trying to identify trends in the market by geography. At the level of individual cities, the data may appear noisy or inconclusive. But when aggregated to the level of region or country, a clear pattern may emerge. Or perhaps date is believed to be a factor in sales. Yet tracking by individual date may show no obvious trend. Instead, aggregating to two-week periods around holidays may reveal a strong seasonal effect. In both cases, a reduction in detail leads to greater predictability or insight.

This is a common phenomenon in data science known as feature aggregation, the process of summarising detailed data into higher-level features that improve model performance and reduce noise.

During development, business stakeholders will often ask for the nth detail. This is understandable, but it can obscure an essential perspective. The problem becomes acute in fast-paced projects where teams tick off requirements and move on. The data engineer must proactively compensate for this tendency. Aggregation should be built into the work plan from the outset.

This is not a compromise, but a necessary step to insight. Aggregation is the act of stepping back to see the forest rather than the trees. When done well, it allows the data engineer to surface insights that are not visible at the level of raw granularity.

The data engineer has three common ways of trading details for insights: creating categories, pivoting combinations, and highlighting special cases.

### Creating categories

Creating categories is the simplest way to surface insight that is hidden by noise. For example, aggregating by region rather than city, using age bands rather than individual ages, or grouping days into seasons can reveal patterns that are otherwise obscured.

A special case of this is the use of binary columns. Suppose a help desk workflow has cases in `Helpdesk.Case` and another `Helpdesk.Escalation` table to record an escalation event in a column `[Escalation tier]` with values from `Tier 1` to `Tier 4`. Creating a new column `[Is escalated]`, defined as false for Tier 1 and true for Tier 2 and above, can be immediately useful for business users seeking to understand escalation behaviour.

A further special case of binary columns is to link categories to good and bad. For example, an inspection is a common business process. The system records inspection results selected from a finite list. If `Cake.InspectionResult` records cake inspections and `Cake.RefInspectionResult` stores values such as `Excellent cake`, `Good cake`, `Spoiled cake`, and `Not tasty`, an obvious category is to create a column `[Is bad cake]` that groups these values into two. This grouping looks straightforward but has a tremendous influence downstream in designing reports, exposing filters, and designing measures.

### Pivoting combinations

Another approach is to pivot options in the entity’s detail rows back to the entity grain. Continuing with the help desk workflow example, escalation tiers can be pivoted into columns such as `[Tier 1]`, `[Tier 2]`, `[Tier 3]`, and `[Tier 4]` to represent whether each tier was reached.

Once pivoted, the data engineer can summarise the escalation path in a variety of ways. For example, a column `[Escalation path]` might contain values such as `Not escalated`, `Progressively escalated`, or `Direct escalation`. This column communicates important insight for decision makers trying to understand operational patterns which are otherwise impossible to see with a deluge of tier values.

### Highlighting special cases

A third approach is to highlight special cases. For example, if there are multiple results, the data engineer may choose to surface the worst result, first result, final result, or best result.

Continuing the help desk example, this could be expressed as a column `[Highest escalation]` with values such as `Tier 1`, `Tier 2`, and so on. This provides a concise summary of the escalation journey.

A common scenario is the header-detail structure where the header is the entity and the detail is the result. For example, in `Cake.InspectionResult`, a single cake may have multiple inspection criteria and thus multiple inspection results. A simple yet powerful way of storytelling is to compute the worst of the inspection result. If the data engineer has created a binary column `[Is bad cake]` to categorise the result of a single inspection, then the computation would simply be the max of `[Is bad cake]`.

### Summary of trading details for insights

Trading details for insights happens by zooming out. Quite often this is done by aggregating information back to the entity-of-interest grain. The third pass stage, reduce, in entity processing and tracking is designed specifically to cater for this step in the pipeline.

One useful effect of aggregation is to eliminate problems of double-counting at the grain of the business entity. For example, in the help desk scenario, the pivot of options means that, even though a case may have multiple levels of escalation, the presentation of result can be done at the case level.

In each of these approaches, the expression is best placed in a reference table rather than embedded in the transaction table itself. The data engineer will need to create these reference tables from scratch as they would not be built into the source system.

These three approaches, creating categories, pivoting combinations, and highlighting special cases, can be combined as one powerful reference data construct that tells the story of the entity. This reference data is the storytelling dimension.

## Storytelling dimension

The concept of dimension will be explored further in the next chapter. For now, it is helpful to introduce a specific type: the storytelling dimension.

The mindset of a storytelling dimension is straightforward. The aim is to tell the overall story of the entity. This means stepping back from what is written in the database and asking what kind of journey the entity undertook through business processes. The emphasis is on the business view of the situation. The story is then expressed through a reference table rather than in the transaction table itself.

There are no fixed rules for creating a storytelling dimension. What matters is that the result communicates a meaningful story about the entity and can be expressed cleanly in a reference table.

Creating a storytelling dimension follows the standard steps for applying reference data: first build the reference table, then map the entity of interest to the appropriate record. The difference with other reference tables lies in the mindset and creativity. There are three basic steps:

- Build the reference table
- Map to the facts
- Visual check

### Step 1 — Build the reference table

The storytelling dimension begins with a reference table that captures the entity’s journey through business processes. Each row represents a distinct path the entity might take, its decisions, escalations, outcomes, or transitions.

Returning to the help desk example, a simple storytelling dimension might be `Helpdesk.RefEscalation` with a column `[Highest escalation]` that labels each case by its most severe escalation tier. This can be extended with a column `[Escalation path]`, derived from pivoting `[Tier 1]` to `[Tier 4]`, with values such as:

- Not escalated
- Progressively escalated
- Directly escalated

These values reflect how the case moved through the escalation process, not only how it ended in the highest tier.

The column `[Escalation path]` can be further enriched when combined with `[Highest escalation]`. In addition, adding a column `[Is closed]` may be necessary to tell the complete story for all cases in the business system. The full combination of `[Is closed]`, `[Escalation path]`, and `[Highest escalation]` can be used to create `[Escalation summary]` with values such as:

- Closed, directly escalated to Tier 4
- Closed, directly escalated to Tier 3
- Closed after progressive escalation
- Closed without escalation
- Case still open

These summaries often imply a ranking. A `[Display order]` column should be included to support this ranking in visualisations and filters.

The reference table should be heavily annotated with useful business descriptions. Each column should describe the business rule it represents in a way that is close to pseudo-code for business understanding.

In dimensional modelling, this type of reference table is sometimes called a junk dimension or transaction profile dimension.

### Step 2 — Map to facts

Designing the reference table is the bulk of the work. Once complete, the data engineer only needs to compute the information that matches the business rules described in the reference table’s metadata and column descriptions.

Since the storytelling dimension describes the entity of interest’s journey through business processes, the calculation should be done at the grain of the entity of interest. Most often, this requires aggregating finer-level details, and the computation is performed in the third pass, the reduce stage of the data pipeline.

The calculation can be added to an existing aggregation table if appropriate or implemented as a new fragment. Continuing the help desk example, this would result in a `Helpdesk.CaseEscalation` table paired with `Helpdesk.RefCaseEscalation`.

### Step 3 — Visual check

Visual check is the idea that the data engineer should visually review the outcome of the pipeline, for example in a bar chart. This should be a constant habit to ensure that implementation matches intent and that no accidental mistakes have crept in.

Visual check is especially important in storytelling dimensions. Crafting a storytelling dimension is a creative act. It often takes multiple iterations to arrive at the real story. Seeing the outcomes visually through charts, summaries, or dashboards can influence and refine the story being told.

Returning to the help desk example, a quick bar chart may reveal that there are almost no directly escalated records, and these cases occur only due to data entry errors. Alternatively, the chart may show a high number of directly escalated cases, suggesting a deeper operational issue or a more nuanced story worth exploring.

Arriving at the right story is only possible through visual checks. These checks help validate assumptions, uncover unexpected patterns, and guide refinement of the storytelling dimension.

### Additional comments

In complex cases, more than one storytelling dimension may be necessary. For example, `Helpdesk.RefCaseEscalation` may tell the story of the work to escalate, but another `Helpdesk.RefCaseSla` may need to tell the story of whether the case was resolved within service-level agreement with a `[Is within SLA]` column.

Storytelling dimensions are one of the most powerful tools in a data engineer’s toolkit. They allow the engineer to take a fresh look at the raw data and prioritise the perspective of business interest by capturing the journey of an entity in a way that aligns with how the business makes decisions. When done well, they become an effective bridge between data and business understanding.
