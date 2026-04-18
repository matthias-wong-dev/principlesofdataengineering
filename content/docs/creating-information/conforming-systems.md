---
title: Conforming systems
description: Explains how to integrate multiple systems through conformed reference data without losing clarity of grain or business meaning.
lede: Integration works best when systems are conformed through shared meaning rather than forced together.
weight: 5
draft: true
---

One of the highest-value contributions of a data engineer is the ability to integrate information across systems. Yet new engineers often fall into two traps: forcing a union of tables that do not naturally fit, or performing large joins that result in ambiguous grain and duplicated data. Both lead to unclear meaning and models that are hard to maintain.

The insight of Kimball’s dimensional modelling is that integration can be achieved through conformed dimensions, reference tables shared across business processes. These allow disparate systems to speak the same language, even when their purposes or implementation differ.

There are two major approaches:

- **Vertical integration.** This applies when the same type of entity is spread across multiple systems or tables.
- **Horizontal integration.** This applies when there are different types of entities, but they share some common denominator for comparison.

## Vertical integration

Vertical integration is appropriate when a business entity is recorded across multiple systems. This commonly occurs when a new digital system replaces an older one and the goal is to integrate information from both in a way that preserves historical continuity.

Take the example of a cake company using two systems, `CakeV1` and `CakeV2`, to record sales. The newer system adds fields and improves logic, but the core attributes remain similar. Integration proceeds in three steps:

- Model the two systems individually
- Build reference tables
- Integrate the transaction tables as a union of transaction tables

### Step 1 — Model systems individually

A common mistake is to integrate too early. Instead, model each system independently using the principles from earlier chapters. This ensures clarity and prepares each for integration.

Suppose, in the case of integrating `CakeV1` and `CakeV2`, that both systems have sales and status, but `V2` has a new attribute for marketing campaign. The tables would be:

- `CakeV1.Sales`, `CakeV1.RefSales`, `CakeV1.RefStatus`
- `CakeV2.Sales`, `CakeV2.RefSales`, `CakeV2.RefStatus`, `CakeV2.RefCampaign`

> [!NOTE]
> **TODO**
>
> The manuscript includes ER diagrams here.

### Step 2 — Build reference tables

The second step is to build conformed reference tables that provide the interface for joining the old and new systems. The conformed reference represents the unified business meaning across both systems.

In the example of Cake, just as the individual systems required `RefSales`, `RefStatus`, and `RefCampaign`, the golden references would be `Cake.RefSales`, `Cake.RefStatus`, and `Cake.RefCampaign`.

The golden tables can be created in a variety of ways. They can be created manually or derived from the system data. The important thing is to express semantic equivalence where both the old and new system point to the same real-world business concept.

For instance, suppose:

- `CakeV1.RefStatus` uses codes `O`, `C`, `A` for Open, Completed, and Abandoned.
- `CakeV2.RefStatus` uses `OP`, `CO`, `WD`, and `RF` for Open, Completed, Withdrawn, and Refunded.

We might hypothesise that:

- `O` and `OP` both mean Open
- `C` and `CO` both mean Completed
- `A` and `WD` both mean Withdrawn
- `RF` introduces a new concept: Refunded

This leads to a proposed golden reference: Open, Completed, Withdrawn, Refunded.

But this is only a hypothesis. It must be validated with the business. Even subtle differences in meaning can undermine the integration. In addition to aligning codes, the golden reference tables should:

- Include default rows for unknown values
- Add analytical columns such as `[Is finished sale]` to support downstream use
- Be documented with metadata to support clarity and reuse

Finally, build mapping tables such as `Cake.StatusMap` and `Cake.CampaignMap` to translate system-specific codes to the golden reference.

### Step 3 — Integrate the transactions

The final step is to integrate the transaction records. It is at this step, and not earlier, that the union of tables is applied to produce an integrated view.

Following the earlier example, create `Cake.Sales` as a union of `CakeV1.Sales` and `CakeV2.Sales`. If there are columns that exist only in one system, populate them with default values in the other, including default foreign-key values to reference tables.

During the union, apply the reference data mapping tables to translate system-specific codes to the conformed ones. This completes the task of conforming both systems to a shared business standard.

> [!NOTE]
> **TODO**
>
> The manuscript includes ER diagrams and code examples here. Convert the code to fenced blocks when the underlying text becomes available.

The final structure includes:

- `Cake.Sales` — the unified transaction table
- `Cake.RefSales` — the conformed reference for sales
- `Cake.RefStatus` — the conformed status reference
- `Cake.RefCampaign` — the conformed campaign reference

The separation into three steps, modelling, reference building, and integration, allows each system to be developed independently, supports incremental delivery, and makes it easier to refactor or extend the model later.

The manuscript intentionally over-engineers the example to illustrate the concept. In practice, simplifications may be appropriate. The decision to simplify should be left to the data engineer, guided by expressiveness, fragment modelling, and the need to build a stable pipeline.

## Horizontal integration

Horizontal integration applies when the entities differ conceptually but share enough commonality to make comparison valuable. The challenge is not technical; it is recognising when this pattern is appropriate.

Consider a cake company that both produces and sells cakes. The core tables are `Cake.Production` and `Cake.Sales`. These entities are distinct: one records manufacturing, the other records transactions. However, they share common attributes such as region, time, cost, and staff, making comparison meaningful.

New engineers may mistakenly force these into a single abstract table such as `Cake.Event` by taking a union of the two. This creates a model that is difficult to understand and prone to error. A better approach is to keep them distinct and rely on shared reference data to support comparison.

For example, both `Cake.Production` and `Cake.Sales` may use:

- `Cake.RefCalendar` to align by date
- `Cake.RefRegion` to align by geography

This allows comparisons such as:

- Cost and staff count by region and month
- Production volume versus sales performance

> [!NOTE]
> **TODO**
>
> The manuscript includes ER diagrams and SQL screenshots here for the horizontal-integration examples.

This approach integrates the data cleanly without distorting the grain of either table. It also fits naturally into a dimensional model, which is covered in the next section, *Presenting insights*.

## Finer-grained integration

Sometimes, business interest demands integration at a finer level than conformed reference tables offer. For example, a company may want to understand how specific production batches relate to sales. However, the data may not capture this link directly.

Suppose the business proposes a rule: cakes produced in a region are sold in the same region, in the same month, in the order they were produced. This logic is fuzzy because there may be multiple production batches per region per month.

New engineers may attempt to enforce this link by adding `[Production ID]` to `Cake.Sales`, or `[Sales ID]` to `Cake.Production`. Both approaches are problematic because they change the grain of the table in a way that is difficult to understand.

The correct approach is to create a bridge table, `Cake.SalesProductionMap`, that encapsulates the logic as a standalone fragment. This table contains only two columns:

- `[Sales ID]`
- `[Production ID]`

This preserves the integrity of both source tables and allows the mapping logic to evolve independently. The code for `Cake.SalesProductionMap` can be as complex as needed and refined based on business feedback.

Whether it is the vertical integration or the horizontal integration approach, the key principle is to prioritise expressiveness and good programming. The technical convenience of the data engineer is not sufficient to outweigh these.
