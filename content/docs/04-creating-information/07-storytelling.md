---
title: Storytelling
url: /docs/creating-information/storytelling/
description: Explores how data engineers add value by defining good and bad entities, aggregating detail, and shaping business narratives.
lede: Data engineering is not finished when the data is correct. It is finished when the business can see.
weight: 7
# draft: true
---

## Meaning beyond correctness

Source systems record operational events. They do not necessarily expose the outcomes, patterns, and journeys that matter for decision making.

A production system records inspections. A help desk system records escalations. A sales system records transactions. None automatically tell the business whether things are going well or how entities move through business processes.

Data engineering is not finished when the data is correct. It is finished when the business can see.

Storytelling is the process of transforming operational detail into forms that allow the business to recognise outcomes, patterns, and journeys.

This chapter explores three approaches:

- **Good and bad entities**—making business judgement explicit.
- **Trading detail for insight**—reducing noise into categories, combinations, and special cases.
- **Storytelling dimensions**—combining these interpretations into reusable reference data.

## Good and bad entities

Business often sees the world through the lens of “good” and “bad.” A trade makes a profit or a loss. A customer is retained or lost. A production run succeeds or fails.

However, operational systems are often designed to support workflow rather than business judgement. The outcome that matters to the business may not exist explicitly in the source system.

One of the most valuable contributions of a data engineer is therefore to define outcomes that help the business recognise success and failure consistently. Sometimes the definition is obvious to the business user. Other times, it is latent in the way stakeholders talk about the data. The data engineer can proactively surface this latent definition by listening carefully during discussions and asking the right questions.

As a simplified example, a `Cake.Production` process may contain inspection results and operational notes, but not a clear concept of production failure. The data engineer can introduce that concept through a reference table and fragment.

**Example structure of `Cake.RefProductionFailure`**

| Production failure ID | Production failure outcome | Failure reason |
|---:|---|---|
| 1 | Production failure | Spoiled cake |
| 2 | Production failure | Undercooked cake |
| 3 | Production failure | Damaged packaging |
| 4 | Production failure | Missing allergen label |
| 5 | No production failure | No failure detected |

**Example structure of `Cake.ProductionFailure`**

| Production ID | Production failure ID |
|---|---:|
| P1001 | 5 |
| P1002 | 1 |
| P1003 | 5 |
| P1004 | 3 |
| P1005 | 4 |

The source system may record production events and inspection notes, but the business needs to see whether a production run failed and why. The data engineer creates that interpretation as a reusable fragment.

The definition of good and bad can be a significant point of debate in a complex organisation with different business viewpoints. In these situations, it can be extremely challenging to arrive at a consensus. Many organisations fail to do so, crippling their ability to see issues consistently. In this case, it is often [the creativity and technical expertise of the data engineer](/docs/foundations/data-and-organisations/) that can broker between parties by showing the way forward.

## Trading detail for insight

Not every detail contributes equally to understanding. Often the fastest path to insight is to reduce detail rather than increase it.

A sales process may appear noisy when analysed by individual city but reveal a clear trend when grouped by region. A daily pattern may become obvious only after aggregating into weeks or sales seasons. In both cases, detail is traded for visibility.

During development, business stakeholders will often ask for the nth detail. This is understandable, but it can obscure an essential perspective. The problem becomes acute in fast-paced projects where teams tick off requirements and move on. The data engineer must proactively compensate for this tendency. Aggregation should be built into the work plan from the outset.

The data engineer has three common ways of trading details for insights:

- Creating categories
- Pivoting combinations
- Highlighting special cases

### Creating categories

Creating categories is the simplest way to surface insight that is hidden by noise. For example, using age bands rather than individual ages, or grouping days into seasons, can reveal patterns that are otherwise obscured.

A special case of this is the use of binary columns. Suppose a help desk workflow has cases in `Helpdesk.Case` and another `Helpdesk.Escalation` table to record escalation events.

**Example structure of `Helpdesk.RefEscalationTier`**

| Escalation tier | Is escalated |
|---|---|
| Tier 1 | false |
| Tier 2 | true |
| Tier 3 | true |
| Tier 4 | true |

Creating a column such as `[Is escalated]`, defined as false for `Tier 1` and true for `Tier 2` and above, can be immediately useful for business users seeking to understand escalation behaviour.

A further special case of binary columns is to link categories to good and bad. For example, an inspection is a common business process. The system records inspection results selected from a finite list.

Binary columns also play an important role in filtering and creating measures, as will be discussed in following chapters.

**Example structure of `Cake.RefInspectionResult`**

| Inspection result | Is bad cake |
|---|---|
| Excellent cake | false |
| Good cake | false |
| Spoiled cake | true |
| Not tasty | true |

The grouping looks straightforward, but it has a large influence downstream in designing reports, exposing filters, and designing measures.

### Pivoting combinations

Another approach is to pivot options in the entity’s detail rows back to the entity grain.

Continuing with the help desk workflow example, escalation tiers can be pivoted into columns such as `[Tier 1]`, `[Tier 2]`, `[Tier 3]`, and `[Tier 4]` to represent whether each tier was reached.

**Source detail rows in `Helpdesk.Escalation`**

| Case ID | Escalation tier |
|---|---|
| H1001 | Tier 1 |
| H1001 | Tier 2 |
| H1001 | Tier 3 |
| H1002 | Tier 1 |
| H1003 | Tier 4 |
| H1004 | Tier 1 |
| H1004 | Tier 2 |

Would be converted to a table of the entity grain.

**Pivoted structure at the case grain**

| Case ID | Tier 1 | Tier 2 | Tier 3 | Tier 4 |
|---|---|---|---|---|
| H1001 | true | true | true | false |
| H1002 | true | false | false | false |
| H1003 | false | false | false | true |
| H1004 | true | true | false | false |

The detail rows, including information such as the timing of the escalation, have been traded for a compact representation of the path. The model can now describe the case at the case grain without double-counting escalation events.

Once pivoted, the data engineer can summarise the escalation path in a variety of ways.

**Example escalation path**

| Case ID | Tier 1 | Tier 2 | Tier 3 | Tier 4 | Escalation path |
|---|---|---|---|---|---|
| H1001 | true | true | true | false | Progressively escalated |
| H1002 | true | false | false | false | Not escalated |
| H1003 | false | false | false | true | Direct escalation |
| H1004 | true | true | false | false | Progressively escalated |

The column `[Escalation path]` communicates an operational pattern that is difficult to see from detail rows alone. A business user does not need to inspect a deluge of tier values to understand whether the case stayed at the first tier, progressed through escalation, or jumped directly to a higher tier.



### Highlighting special cases

Sometimes a single result tells most of the story. For example, if there are multiple results, the most important one may be the worst result, first result, final result, or best result.

In the escalation example, the highest tier reached is often more important than every individual escalation event.

**Extended structure**

| Case ID | Tier 1 | Tier 2 | Tier 3 | Tier 4 | Highest escalation | 
|---|---|---|---|---|---|
| H1001 | true | true | true | false | Tier 3 | 
| H1002 | true | false | false | false | Tier 1 | 
| H1003 | false | false | false | true | Tier 4 |
| H1004 | true | true | false | false | Tier 2 | 

The `[Highest escalation]` column highlights the most significant outcome of the escalation journey. Users do not need to inspect every event individually because the most important result has already been surfaced.

A common scenario is the header-detail structure where the header is the entity and the detail is the result.

For example, in `Cake.InspectionResult`, a single cake may have multiple inspection criteria and therefore multiple inspection results. A simple yet powerful way of storytelling is to compute the worst of the inspection result.

**Source detail rows in `Cake.InspectionResult`**

| Cake ID | Inspection criterion | Inspection result |
|---|---|---|
| C1001 | Appearance | Excellent cake |
| C1001 | Taste | Good cake |
| C1001 | Packaging | Good cake |
| C1002 | Appearance | Excellent cake |
| C1002 | Taste | Not tasty |
| C1002 | Packaging | Good cake |
| C1003 | Appearance | Good cake |
| C1003 | Taste | Good cake |
| C1003 | Packaging | Spoiled cake |

Suppose the reference table includes a binary classification:

**`Cake.RefInspectionResult`**

| Inspection result | Is bad cake |
|---|---|
| Excellent cake | false |
| Good cake | false |
| Not tasty | true |
| Spoiled cake | true |

The worst inspection result for each cake can then be calculated as the maximum of `[Is bad cake]`.

**Result at the cake grain**

| Cake ID | Is bad cake |
|---|---|
| C1001 | false |
| C1002 | true |
| C1003 | true |

The business no longer needs to inspect every individual inspection result. The most significant outcome has been surfaced at the grain of the cake itself.

## Storytelling dimensions

A storytelling dimension brings multiple acts of interpretation together into a single reusable business view.

Categories, combinations, special cases, and journeys can each be useful individually. A storytelling dimension combines them into a coherent way of seeing the entity. The aim is to tell the overall story of the entity. This means stepping back from what is written in the database and asking what kind of journey the entity undertook through business processes. The emphasis is on the business view of the situation. The story is then expressed through [reference data](/docs/creating-information/reference-data/) rather than in the transaction table itself.

Continuing the help desk example:

**Example structure of `Helpdesk.RefCaseEscalation`**

| Case escalation ID | Tier 1 | Tier 2 | Tier 3 | Tier 4 | Is escalated | Highest escalation | Escalation path | Escalation summary | Display order |
|---:|---|---|---|---|---|---|---|---|---:|
| 1 | true | false | false | false | false | Tier 1 | Not escalated | Closed without escalation | 1 |
| 2 | true | true | false | false | true | Tier 2 | Progressive escalation | Closed after escalation | 2 |
| 3 | true | true | true | false | true | Tier 3 | Progressive escalation | Closed after escalation | 2 |
| 4 | true | true | true | true | true | Tier 4 | Progressive escalation | Closed after escalation | 2 |
| 5 | false | true | false | false | true | Tier 2 | Direct escalation | Closed, started with escalation | 3 |
| 6 | false | false | true | false | true | Tier 3 | Direct escalation | Closed, started with escalation | 3 |
| 7 | false | false | false | true | true | Tier 4 | Direct escalation | Closed, started with escalation | 3 |
| 8 | true | false | true | false | true | Tier 3 | Escalated with skipped tier | Closed after escalation | 2 |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| 16 | false | false | false | false | false | Not applicable | Not applicable | Case still open | 99 |

This single reference table contains several layers of interpretation:

- Tier combinations
- Special cases
- Journey descriptions
- Business summaries

Together they tell the story of the case. 

Creating and applying a storytelling dimension follows three basic steps:

- Build the reference table
- Map to the facts
- Visual check

### Step 1—Build the reference table

The storytelling dimension begins with a reference table that describes the journeys that matter to the business.

Returning to the help desk example, the starting point is the escalation pattern. The data engineer can represent whether each tier was reached using columns such as `[Tier 1]`, `[Tier 2]`, `[Tier 3]`, and `[Tier 4]`.

Those tier columns can then support `[Highest escalation]`, which identifies the most severe escalation reached by the case.

The same combination can also support `[Escalation path]`, with values such as:

- Not escalated
- Progressive escalation
- Direct escalation
- Escalated with skipped tiers

These values describe how the case moved through the escalation process, not merely where it ended.

The story can then be enriched with `[Escalation summary]`, which combines escalation path, highest escalation, and case status into a small set of business-facing categories.

Example summaries include:

- Closed without escalation
- Closed after escalation
- Closed, started with escalation
- Case still open

When creating a summary, resist the temptation to include too much detail. A summary is useful because it compresses many possibilities into a handful of categories the business can hold mentally. Adding detail creates more combinations and defeats the point of the summary.

These summaries often imply a ranking. A `[Display order]` column should be included to support this ranking in visualisations and filters.

The reference table should be heavily annotated with useful business descriptions. Each column should describe the business rule it represents in a way that is close to pseudo-code for business understanding.

Such tables are often composed from underlying binary flags. The exact SQL depends on the platform, but the pattern is usually:

 - generate all combinations of the binary flags;
 - assign each combination a stable key;
 - compute mechanical columns such as `[Highest escalation]`;
 - add business interpretation columns manually or through controlled rules.

```SQL

select
          1
        + cast([Tier 1].value as int) * 1
        + cast([Tier 2].value as int) * 2
        + cast([Tier 3].value as int) * 4
        + cast([Tier 4].value as int) * 8        as [Case escalation ID]

    ,     cast([Tier 1].value as bit)            as [Tier 1]
    ,     cast([Tier 2].value as bit)            as [Tier 2]
    ,     cast([Tier 3].value as bit)            as [Tier 3]
    ,     cast([Tier 4].value as bit)            as [Tier 4]

    ,     ...                                    as [Is escalated]
    ,     ...                                    as [Highest escalation]
    ,     ...                                    as [Escalation path]
    ,     ...                                    as [Escalation summary]
    ,     ...                                    as [Display order]

from        string_split('0,1', ',') [Tier 1]
cross apply string_split('0,1', ',') [Tier 2]
cross apply string_split('0,1', ',') [Tier 3]
cross apply string_split('0,1', ',') [Tier 4];

```

In dimensional modelling, this type of reference table is sometimes called a junk dimension or transaction profile dimension.


### Step 2—Map to facts

Once the storytelling dimension exists, the entity of interest can be mapped to it.

**Example structure of `Helpdesk.CaseEscalation`**

| Case ID | Case escalation ID |
|---|---:|
| H1001 | 3 |
| H1002 | 1 |
| H1003 | 7 |
| H1004 | 2 |

The calculation should be done at the grain of the entity of interest during the reduce stage of the pipeline, as described in the chapter on [Entity Processing](/docs/creating-information/entity-processing/).

The calculation can be added to an existing aggregation table if appropriate or implemented as a new fragment. Continuing the help desk example, this would result in a `Helpdesk.CaseEscalation` table paired with `Helpdesk.RefCaseEscalation`.
**Example result after joining to `Helpdesk.RefCaseEscalation`**

| Case ID | Is escalated | Highest escalation | Escalation path | Escalation summary |
|---|---|---|---|---|
| H1001 | true | Tier 3 | Progressive escalation | Closed after escalation |
| H1002 | false | Tier 1 | Not escalated | Closed without escalation |
| H1003 | true | Tier 4 | Direct escalation | Closed, started with escalation |
| H1004 | true | Tier 2 | Progressive escalation | Closed after escalation |

A table like this tells the business far more about the case than a simple list of escalation events is able to.

### Step 3—Visual check

Storytelling dimensions should always be reviewed visually.

A quick chart or summary table often reveals whether the intended story is actually visible.

For example:

| Escalation summary | Cases |
|---|---:|
| Closed without escalation | 8,450 |
| Closed after escalation | 2,130 |
| Closed, started with escalation | 18 |
| Case still open | 742 |

The distribution may reveal unexpected patterns, data-quality issues, or opportunities to refine the storytelling dimension itself. A quick bar chart may reveal that there are almost no directly escalated records, and these cases occur only due to data entry errors. Alternatively, the chart may show a high number of directly escalated cases, suggesting a deeper operational issue or a more nuanced story worth exploring.

Visual checks are therefore not merely validation. They are part of the iterative design process.

### Multiple storytelling dimensions

Complex business processes may require multiple storytelling dimensions.

A help desk workflow may need one dimension describing escalation behaviour and another describing service-level agreement outcomes. A production process may need one dimension describing inspection outcomes and another describing manufacturing quality. 
## Storytelling and the organisation

Storytelling is important because correctness is not enough. A table can be accurate and still fail to show the business what happened.

The data engineer’s task is to create forms of information that make the business visible: its outcomes, patterns, and journeys. 

This involves decisions and compromise: details to discard, or journeys to emphasise. Consequently, storytelling is a central place where the [organisation negotiates meaning](/docs/foundations/data-and-organisations/), and where the data engineer plays an influential role in how organisation understands its own business.

## Key ideas

> [!NOTE]
> **Key ideas**
>
> Data engineering is not finished when the data is correct. It is finished when the business can see.
>
> Storytelling creates business meaning that is not explicitly present in the source system.
>
> Defining outcomes is one of the most powerful ways to make business performance visible.
>
> Trading detail for insight reveals patterns that are often hidden at the lowest level of granularity.
>
> Storytelling dimensions combine categories, combinations, special cases, and journeys into reusable business interpretations.
>
> Storytelling dimensions should be implemented as reference data and mapped back to the entity of interest.
>
> Visual checks are an essential part of developing storytelling dimensions.
