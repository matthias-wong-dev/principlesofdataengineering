---
title: Entity tracking
url: /docs/creating-information/entity-tracking/
description: Shows how mutable business entities are tracked through changing attributes, behaviour, timelines, and end-of-period snapshots.
lede: Mutable entities require timelines, snapshots, and careful handling of change history.
weight: 4
draft: true
---

The second most common pattern in data engineering work is that of entity tracking. This pattern applies to mutable business entities, those that can change over time while still being considered the same entity. Examples include a customer whose contact details, preferences, or purchasing behaviour evolve; an employee whose qualifications, role, or performance record changes; or a supplier whose compliance status shifts over time.

Mutable entities often share certain characteristics:

- **Status:** They have no clear “versions” in the sense used for immutable entities, but they do have statuses that change over time.
- **Changing attributes:** They possess multiple detailed attributes, and changes to these attributes define the entity’s mutation.
- **Actions:** They are often actors in business processes, and their performance or behaviour is of ongoing concern.
- **Audit:** They may be the subject of additional business processes that audit them periodically or in response to events.
- **Registration:** They are typically underpinned by an entity registration process, which establishes their initial presence in the system.

The usual goals of entity tracking are to:

- Monitor macro-level trends in the number of entities over time, including changes in the composition of the population.
- Track management activities associated with these entities, such as registration and audit.
- Monitor when entities reach performance milestones defined by business thresholds.
- Detect anomalous entities for targeted action and early intervention.
- Provide drill-down information about the entity and the changes it has undergone.
- Understand the effect of entities on other business outcomes.

## Two ways to track

There are two common approaches to tracking an entity. The first is by its attributes; the second is by its behaviour.

Tracking by attributes means that an entity is registered into a database, and tables record its attributes such as name, address, status, and so on. These tables are usually Type II tables, where each row is labelled with its validity period using columns like `[Start date]` and `[End date]`.

The other approach is to track an entity by its behaviour. In this case, the business is interested in insights about the entity through observing the way it behaves over time. A business can observe an entity’s behaviour through audits of its state or through records of its actions.

Many systems have elements worth tracking. A bank, for example, may want to track its account holders in two ways:

- **Attribute:** Bank accounts have evolving attributes such as account holder, account type, and account level.
- **Behaviour:** Deposits, withdrawals, transfers, and interest accruals are recorded as actions taken by the account holder.

## Building the pipeline to track attributes

Much of the approach from entity processing applies. The same practices, identifying the entity of interest, crafting expressive reference tables, maintaining detail, and telling a coherent story, remain central. The difference is that for mutable entities, the pipeline has the additional task of tracking attribute changes, which introduces new techniques.

Consider the example of a bank tracking its account holders. The core table is `Bank.Account`, which contains evolving attributes such as account type, account level, and account status. These attributes may change over time, and the business is interested in understanding how accounts evolve.

### First pass — Filter

The first step is to remove noise, build a semantic map of the basic information, and create reference tables to support meaningful context. Compared to entity processing, entity tracking introduces an additional step for tracking attributes: temporal compression.

Temporal compression collapses consecutive rows that carry identical information across time periods. It is akin to run-length encoding.

**Example before compression**

| Account ID | Start date | End date | Account type | Account level | Account status |
| --- | --- | --- | --- | --- | --- |
| 12345 | 2022-01-01 | 2022-06-30 | Savings | Silver | Active |
| 12345 | 2022-07-01 | 2023-06-30 | Savings | Silver | Active |

**After compression**

| Account ID | Start date | End date | Account type | Account level | Account status |
| --- | --- | --- | --- | --- | --- |
| 12345 | 2022-01-01 | 2023-06-30 | Savings | Silver | Active |

In addition to compression, the first pass should assign a surrogate key to each validity period. For example, `[Account SK]` would represent the combination of `[Account ID]` and `[Start date]`.

### Second pass — Compute the timeline

An entity usually has attributes stored in multiple tables. For immutable entities, retrieving attributes from multiple tables into one result set is a simple matter of joining on the appropriate keys. This is not the case for mutable entities. In a mutable entity, each attribute table is Type II, meaning each row is defined by a validity period. Joining attributes in this scenario means solving the overlapping window problem.

The second pass simplifies this complexity by creating timeline fragments. These are precomputed temporal joins so that users can easily and accurately retrieve the entity’s set of attributes for any point in time.

An account may have attributes stored across multiple tables, for example:

- `Bank.AccountTypeHistory`
- `Bank.AccountLevelHistory`
- `Bank.AccountStatusHistory`

The goal is to create a `Bank.AccountTimeline` table that expresses the valid combination of attributes for each period.

**Example structure of `Bank.AccountTimeline`**

| Account ID | Account type SK | Account level SK | Account status SK | Start date | End date |
| --- | --- | --- | --- | --- | --- |
| 12345 | 1 | 1 | 1 | 2022-01-01 | 2023-06-30 |
| 12345 | 1 | 2 | 1 | 2023-07-01 | 2024-12-31 |

> [!NOTE]
> **TODO**
>
> The manuscript includes an example code listing here for solving the temporal join / overlapping-window problem.

### Third pass — Compute end-of-period tables

The final pass produces end-of-period tables, snapshots of the account at regular reporting intervals. These are created by joining the timeline to a calendar table and selecting the row that represents the account’s state at the end of each period.

For example, joining `Bank.AccountTimeline` on the validity period to a distinct list of end-of-month dates returns `Bank.AccountEndOfMonth`, a ready-to-consume table that captures the correct attributes for each account at the last day of each month.

## Building the pipeline to track behaviour

The first and second passes apply the same techniques from entity processing onto behaviour records, such as audit results or records of an entity’s actions in business processes. These steps filter and structure the raw behavioural data into clean fragments, then compute reusable blocks of information that reflect business intent.

The third pass is where the data engineer infers performance from behaviour. This is still the reduce step, as it involves aggregating detailed behavioural information into insights about the entity. The inference can be simple, such as identifying entities that failed an audit for the first time, or those that have failed three consecutive audits. It can also be complex, requiring statistical techniques such as time series analysis to detect changing trends.

Following the previous example, `Bank.Transaction` holds records of an entity’s actions, the withdrawals and deposits of an account. It is at the grain of `[Transaction ID]`, which is much finer than `[Account ID]`. To track behaviour of the bank account, the data engineer can aggregate by `[Account ID]` to produce `Bank.AccountValue`, described by `Bank.RefAccountValue`. Example columns in `Bank.RefAccountValue` would be `[Is a millionaire]` or `[Is a new millionaire in the last 3 months]`.

At an advanced level, behaviours can be converted into Type II attributes, effectively transforming behaviour tracking into attribute tracking.

> [!NOTE]
> **TODO**
>
> The manuscript contains draft formatting notes here, including italic markup annotations around this behaviour-tracking example.

## Common problems

Compared with entity processing, entity tracking has additional difficulties.

**Hidden tracking problems.** It is not always obvious that the business is dealing with an entity tracking problem. Sometimes tracking is hidden within what appears to be a processing task.

**Unregistered entity.** A lack of entity registration undermines the clarity of identity.

**Undefined memory.** Behaviour informs performance. Memory of behaviour informs the view of performance. But it may be unclear how much of the behaviour history is relevant for analysis.

**Gaps in change history.** Tracking mutable entities requires reliable records of historical changes. This can be difficult if the source system does not track changes natively.

**Multiple timelines.** Confusion often arises when there is a lag between when a change occurs and when it is recorded.

There are three common types of datetime columns:

- **Architectural** — system-generated timestamps, such as those from database triggers.
- **Application** — timestamps defined by application logic, such as `[Update datetime]`.
- **Business** — timestamps tied to the actual business event, such as `[Sales order date]`.

The data engineer must engage early with stakeholders to understand the strengths and weaknesses of each type. Clear naming conventions and consistent usage are essential to avoid confusion and promote expressiveness.

Temporal representation introduces another important decision. Since attributes can change, the data engineer must decide how to represent the entity at a given point in time:

- **Type I** — show the latest available attribute value.
- **Type II** — show the attribute value as it was at a specific point in time.
- **Dynamic Type I** — show the latest value as defined by the user’s context, such as a time filter.

The choice depends on the analytical scenario. The same attribute may require different representations depending on the business question. Fragment modelling and timeline tables are well suited to supporting this flexibility.

Computational performance can also become a bottleneck, especially in end-of-period reporting. Many of these challenges require detailed handling rather than a ready-made approach, and they often require direct engagement with the business.
