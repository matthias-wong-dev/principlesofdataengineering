---
title: Entity tracking
url: /docs/creating-information/entity-tracking/
description: Shows how mutable business entities are tracked through changing attributes, behaviour, timelines, and end-of-period snapshots.
lede: Entity tracking applies when business entities change over time while remaining the same entity.
weight: 4
# draft: true
---

## Tracking mutable entities

Entity tracking is the main pattern for [mutable business entities](/docs/creating-information/mapping-the-data-world/): those that change over time while still being considered the same entity.

Examples include a customer whose contact details, preferences, or purchasing behaviour evolve; an employee whose qualifications, role, or performance record changes; or a supplier whose compliance status shifts over time.

[Entity processing](/docs/creating-information/entity-processing/) asks what happened to a fixed entity. Entity tracking asks how an entity changed while remaining itself.

Mutable entities share common characteristics:

- **Status**—Instead of "versions", the entity has statuses that change over time.
- **Changing attributes**—the entity has attributes whose changes define its mutation.
- **Actions**—the entity acts within business processes, and its performance or behaviour is of ongoing concern.
- **Audit**—the entity may be audited periodically or in response to events.
- **Registration**—the entity is usually underpinned by a registration process that establishes its initial presence in the system.

These characteristics explain the goals of entity tracking:

- Monitor macro-level trends in the number of entities over time, including changes in the composition of the population.
- Track management activities associated with these entities, such as registration and audit.
- Monitor when entities reach performance milestones defined by business thresholds.
- Detect anomalous entities for targeted action and early intervention.
- Provide drill-down information about the entity and the changes it has undergone.
- Understand the effect of entities on other business outcomes.

## Two ways to track

There are two common ways to track a mutable entity. The first is by its attributes. The second is by its behaviour.

Tracking by attributes records what the entity is over time. An entity is registered into a database, and tables record attributes such as name, address, status, account type, account level, and so on. These tables are usually Type II tables, where each row is labelled with a validity period using columns such as `[Start date]` and `[End date]`.

Tracking by behaviour records what the entity does over time. Behaviour may be observed through audits, transactions, events, or actions taken in business processes.

Many systems have both. A bank, for example, may track accounts in two ways:

- **Attribute**—bank accounts have evolving attributes such as account holder, account type, and account level.
- **Behaviour**—deposits, withdrawals, transfers, and interest accruals are actions associated with the account.

The same three-pass structure applies to both modes, but with different emphasis. Attribute tracking introduces distinctive temporal machinery early. Behaviour tracking enters in the third pass when actions are reduced into entity-level signals over time.

## Building the pipeline

Much of the approach from entity processing still applies. The data engineer must identify the entity of interest, craft [expressive reference tables](/docs/creating-information/reference-data/), preserve necessary detail, and tell a coherent story.

The difference is that mutable entities introduce time into the entity itself. In entity processing, time usually appears around the entity: orders, confirmation, shipment, completion. In entity tracking, time defines the state of the entity.

### First pass—Filter and compress

The first pass removes noise, establishes keys, and builds the basic semantic map.

For attribute tracking, this pass also introduces **temporal compression**. Temporal compression collapses consecutive rows that carry identical information across adjacent time periods. It is akin to run-length encoding.

Consider a bank account whose attributes are recorded over time.

**Example before compression**

| Account ID | Start date | End date | Account type | Account level | Account status |
|---|---|---|---|---|---|
| 12345 | 2022-01-01 | 2022-06-30 | Savings | Silver | Active |
| 12345 | 2022-07-01 | 2023-06-30 | Savings | Silver | Active |

**After compression**

| Account ID | Start date | End date | Account type | Account level | Account status |
|---|---|---|---|---|---|
| 12345 | 2022-01-01 | 2023-06-30 | Savings | Silver | Active |

In addition to compression, the first pass should assign a surrogate key to each validity period. For example, `[Account SK]` may represent the combination of `[Account ID]` and `[Start date]`.

The first pass should also normalise validity periods.

Open-ended histories should be given explicit boundaries. A missing start date can be replaced with a minimum sentinel date such as `1900-01-01`; a missing end date can be replaced with a maximum sentinel date such as `9999-12-31`. This gives every row a bounded interval and makes later timeline construction simpler.

The data engineer should also decide how to handle gaps. In some systems  a record may be deleted and later re-created even though the business regards the entity as continuous. A row may need to be inserted to indicate non-existence, with `lag` functions to fill the dates.

For behaviour tracking, the first pass usually resembles entity processing. The data engineer filters and structures behaviour records, such as transactions, audit results, observations, or actions. The important temporal requirement is to preserve the event time of each behaviour.

### Second pass—Build the timeline

An entity usually has attributes stored in multiple tables.

For immutable entities, retrieving attributes from multiple tables is usually a matter of joining on the appropriate keys. This is not the case for mutable entities. In a mutable entity, each attribute table may be Type II, meaning each row is defined by a validity period.

Joining attributes in this scenario means solving the overlapping-window problem.

The timeline table is the central artefact of attribute tracking.

A source system may track each changing attribute separately. Account type, account level, and account status may each have their own history table, with their own validity periods. The difficulty is that the business does not usually ask for these histories separately. It asks what the account was at a point in time.

The timeline table answers this question. It converts multiple overlapping histories into one coherent sequence of entity states.

An account may have attributes stored across multiple tables:

- `Bank.AccountTypeHistory`
- `Bank.AccountLevelHistory`
- `Bank.AccountStatusHistory`

The goal is to create `Bank.AccountTimeline`, which expresses the valid combination of attributes for each period.

**Example structure of `Bank.AccountTimeline`**

| Account ID | Account type SK | Account level SK | Account status SK | Start date | End date |
|---|---|---|---|---|---|
| 12345 | 1 | 1 | 1 | 2022-01-01 | 2023-06-30 |
| 12345 | 1 | 2 | 1 | 2023-07-01 | 2024-12-31 |

The core SQL pattern is an interval overlap join.

```SQL
select
      th.[Account ID]
    , th.[Account type SK]
    , lh.[Account level SK]
    , sh.[Account status SK]
    , greatest(th.[Start date], lh.[Start date], sh.[Start date])   as [Start date]
    , least(   th.[End date],   lh.[End date],   sh.[End date]  )   as [End date]
from Bank.AccountTypeHistory   th
inner join Bank.AccountLevelHistory  lh  on   lh.[Account ID] = th.[Account ID]
                                         and greatest(th.[Start date], lh.[Start date])                   < least(th.[End date], lh.[End date])
inner join Bank.AccountStatusHistory sh  on   sh.[Account ID] = th.[Account ID]
                                         and greatest( th.[Start date], lh.[Start date], sh.[Start date]) < least(th.[End date], lh.[End date], sh.[End date] );
```

The timeline table is produced through a temporal join. Notice that, without the time component, this is an ordinary join on the entity key. This is worth remembering. The timeline table is simply what the join would have looked like "at that point in time", but pre-computed for all time intervals in the most computationally compact form.

In this example, we use inner join for simplicity. Real systems also require careful handling of gaps in history. 


> [!NOTE]
> **Advanced note: two kinds of time**
>
> Some tracking problems involve more than one temporal dimension.
> 
> For example, a user may report an account status for a business-effective period, then later change that reported period. The status has business dates describing when it was effective, but the system also has architectural dates describing when that report was recorded or changed.
>
> This creates questions such as:
>
> > How many valid account holders were there at time X, according to what was known at time Z?
>
> These problems can become extremely messy because the data engineer is no longer tracking only what was true in business time, but also what was known in system time.
>
> We do not develop the full pattern here. The important point is that the timeline approach generalises. A timeline can be extended across an additional time dimension, giving the user a disciplined way to answer these questions while maintaining the clarity on the multiple time dimensions.


### Third pass—Create snapshots and infer behaviour

The third pass produces entity-level outputs over time.

For attribute tracking, the main output is an end-of-period table: a snapshot of the entity at regular reporting intervals. This is created by joining the timeline to a calendar table and selecting the row that represents the entity’s state at the end of each period.

For example, joining `Bank.AccountTimeline` on the validity period to a distinct list of end-of-month dates returns `Bank.AccountEndOfMonth`.

**Example structure of `Bank.AccountEndOfMonth`**

| Account ID | Period end date | Account type SK | Account level SK | Account status SK |
|---|---|---|---|---|
| 12345 | 2023-06-30 | 1 | 1 | 1 |
| 12345 | 2023-07-31 | 1 | 2 | 1 |
| 12345 | 2023-08-31 | 1 | 2 | 1 |

This table is a building block. It gives downstream consumers regular access to the entity state without requiring them to solve overlapping validity windows.

For behaviour tracking, the third pass aggregates behaviour back to the entity over time.

Behaviour records are usually at the grain of the action. A bank transaction table, for example, may be at the grain of `[Transaction ID]`. The tracking question is usually at the grain of `[Account ID]` over time.

The data engineer therefore aggregates behaviour into signals about the entity: balances, counts, failures, first occurrences, repeated events, thresholds, or changes in pattern.

Following the previous example, `Bank.Transaction` holds records of an entity’s actions, the withdrawals and deposits of an account. It is at the grain of `[Transaction ID]`, which is much finer than `[Account ID]`. To track behaviour of the bank account, the data engineer can aggregate by `[Account ID]` to produce `Bank.AccountValue`, described by `Bank.RefAccountValue`. Example columns in `Bank.RefAccountValue` would be `[Is a millionaire]` or `[Is a new millionaire in the last 3 months]`.

**Example structure of `Bank.AccountValue` with `Bank.RefAccountvalue`**

| Account ID | Period end date | Closing balance | Is millionaire | Is new millionaire in last 3 months |
|---|---|---:|---|---|
| 12345 | 2023-06-30 | 8700.00 | false | false |
| 12345 | 2023-07-31 | 9200.00 | false | false |
| 12345 | 2023-08-31 | 13700.00 | false | false |

With this table, a consumer should not need to recalculate balances or scan transaction history to find millionaire accounts. The pipeline should produce a fragment where that business state is already visible.

At an advanced level, behavioural fragments can themselves become Type II attributes. For example, once `Bank.AccountValue` identifies whether an account is a millionaire at each period, the data engineer can convert that repeated period-level result into a history of millionaire status over time.

### Summary of the three passes

When complete, the pipeline produces reusable tracking blocks: expressive business entities, clear management of time, in computationally compact form.

These blocks are ready for downstream use where users can access information without struggling with error-prone process of writing time-based queries.

An overview of the three passes and examples is summarised in Figure 1.

{{< svg >}}
<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="360" viewBox="0 0 1080 360"
     style="display:block;width:100%;max-width:42rem;height:auto;background:transparent" role="img"
     aria-label="Three passes of entity tracking with purpose and example artefacts">

  <defs>
    <marker id="arrowhead-entity-tracking" markerWidth="10" markerHeight="8"
            refX="10" refY="4" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L10,4 L0,8 z" fill="#222222"/>
    </marker>
  </defs>

  <!-- Filter -->
  <rect x="45" y="45" width="290" height="235" rx="16"
        fill="#ffffff" stroke="#222222" stroke-width="1.8"/>

  <text x="190" y="83" text-anchor="middle"
        font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
        font-size="24" font-weight="700" fill="#111111">Filter</text>

<text x="190" y="116" text-anchor="middle"
      font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
      font-size="14" fill="#555555">normalise validity periods</text>
<text x="190" y="137" text-anchor="middle"
      font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
      font-size="14" fill="#555555">compress change history</text>

  <line x1="75" y1="180" x2="305" y2="180"
        stroke="#dddddd" stroke-width="1.4"/>

  <text x="190" y="207" text-anchor="middle"
        font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
        font-size="13" fill="#333333">AccountTypeHistory</text>
  <text x="190" y="228" text-anchor="middle"
        font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
        font-size="13" fill="#333333">AccountLevelHistory</text>
  <text x="190" y="249" text-anchor="middle"
        font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
        font-size="13" fill="#333333">AccountStatusHistory</text>
  <text x="190" y="270" text-anchor="middle"
        font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
        font-size="13" fill="#333333">BankTransaction</text>

  <!-- Map -->
  <rect x="395" y="45" width="290" height="235" rx="16"
        fill="#ffffff" stroke="#222222" stroke-width="1.8"/>

  <text x="540" y="83" text-anchor="middle"
        font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
        font-size="24" font-weight="700" fill="#111111">Map</text>

  <text x="540" y="116" text-anchor="middle"
      font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
      font-size="14" fill="#555555">build timelines of</text>
  <text x="540" y="137" text-anchor="middle"
      font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
      font-size="14" fill="#555555">overlapping windows</text> 

  <line x1="425" y1="180" x2="655" y2="180"
        stroke="#dddddd" stroke-width="1.4"/>

  <text x="540" y="217" text-anchor="middle"
        font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
        font-size="13" fill="#333333">AccountTimeline</text>
  <text x="540" y="239" text-anchor="middle"
        font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
        font-size="13" fill="#333333">AccountTransactionSummary</text>

  <!-- Reduce -->
  <rect x="745" y="45" width="290" height="235" rx="16"
        fill="#ffffff" stroke="#222222" stroke-width="1.8"/>

  <text x="890" y="83" text-anchor="middle"
        font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
        font-size="24" font-weight="700" fill="#111111">Reduce</text>

  <text x="890" y="116" text-anchor="middle"
      font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
      font-size="14" fill="#555555">create end-of-period snapshots</text>
  <text x="890" y="137" text-anchor="middle"
      font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
      font-size="14" fill="#555555">aggregate entity behaviour</text>
  <text x="890" y="158" text-anchor="middle"
      font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
      font-size="14" fill="#555555">to entity signal</text>

  <line x1="775" y1="180" x2="1005" y2="180"
        stroke="#dddddd" stroke-width="1.4"/>

  <text x="890" y="207" text-anchor="middle"
        font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
        font-size="13" fill="#333333">AccountEndOfMonth</text>
  <text x="890" y="228" text-anchor="middle"
        font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
        font-size="13" fill="#333333">AccountValue</text>
  <text x="890" y="249" text-anchor="middle"
        font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
        font-size="13" fill="#333333">RefAccountValue</text>

  <!-- Arrows -->
  <line x1="350" y1="162" x2="375" y2="162"
        stroke="#222222" stroke-width="2.2"
        marker-end="url(#arrowhead-entity-tracking)"/>

  <line x1="700" y1="162" x2="725" y2="162"
        stroke="#222222" stroke-width="2.2"
        marker-end="url(#arrowhead-entity-tracking)"/>

</svg>
{{< /svg >}}

<div style="max-width:42rem;text-align:center;font-size:0.95rem;color:#666;margin-top:0.5rem;">
Figure 1. The three passes of entity tracking, showing both the purpose of each pass and example artefacts produced in a bank account pipeline.
</div>

## Common problems

Compared with entity processing, entity tracking has additional difficulties.

**Hidden tracking problems.** It is not always obvious that the business is dealing with an entity tracking problem. Sometimes tracking is hidden within what appears to be a processing task.

**Unregistered entity.** A lack of entity registration undermines the clarity of identity. If the entity is not clearly registered, changes cannot be reliably attributed to the same thing over time.

**Undefined memory.** Behaviour informs performance. Memory of behaviour informs the view of performance. But it may be unclear how much behaviour history is relevant for analysis.

**Gaps in change history.** Tracking mutable entities requires reliable records of historical change. This is difficult when the source system does not track changes natively.

**Multiple timelines.** Confusion arises when there is a lag between when a change occurs, when it is entered, and when it is recorded by the system.

There are three common types of datetime columns:

- **Architectural**—system-generated timestamps, such as those from database triggers.
- **Application**—timestamps defined by application logic, such as `[Update datetime]`.
- **Business**—timestamps tied to the actual business event, such as `[Sales order date]`.

The data engineer must engage early with stakeholders to understand the strengths and weaknesses of each type. Clear naming conventions and consistent usage are essential to avoid confusion and promote expressiveness.

Temporal representation introduces another important decision. Since attributes can change, the data engineer must decide how to represent the entity at a given point in time:

- **Type I**—show the latest available attribute value.
- **Type II**—show the attribute value as it was at a specific point in time.
- **Dynamic Type I**—show the latest value as defined by the user’s context, such as a time filter.

The choice depends on the analytical scenario. The same attribute may require different representations depending on the business question. Fragment modelling and timeline tables are well suited to supporting this flexibility.

Computational performance can also become a bottleneck, especially in end-of-period reporting. Many of these challenges require detailed handling rather than a ready-made approach, and they often require direct engagement with the business.

> [!NOTE]
> **Key ideas**
>
> Entity tracking applies to mutable business entities.
>
> Entity processing asks what happened to a fixed entity. Entity tracking asks how an entity changed while remaining itself.
>
> Mutable entities can be tracked through attributes, behaviour, or both.
>
> Attribute tracking requires timelines and end-of-period snapshots.
>
> Behaviour tracking aggregates actions into information about the entity over time.
>
> The central difficulty of entity tracking is representing change without losing identity.
