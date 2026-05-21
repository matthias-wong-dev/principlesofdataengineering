---
title: Comparing entity processing and entity tracking
url: /docs/creating-information/comparing-entity-processing-and-entity-tracking/
description: Compares the two major data engineering patterns for immutable and mutable entities.
lede: Entity processing and entity tracking are different patterns, but they share the same underlying discipline.
weight: 5
draft: true
---

## Two patterns, one discipline

Entity processing and entity tracking are different responses to different kinds of business entity.

Entity processing applies when the entity is treated as fixed once created.

Entity tracking applies when the entity changes over time while remaining the same entity.

The distinction is simple, but its consequences are large. It changes the grain of the pipeline, the treatment of time, the role of aggregation, and the way business meaning is expressed.

## The common structure

Despite their differences, both patterns share the same underlying discipline.

Both begin by identifying the **entity of interest**.

Both require expressive keys.

Both depend on reference tables.

Both use fragments to isolate business meaning.

Both eventually return information to the grain required by business intent.

Both may need to define whether an entity is good or bad.

This common structure matters because it prevents the data engineer from treating the two patterns as unrelated techniques. In both cases, the work is the same at the deepest level: create faithful, legible, and operable information about business entities.

## The main difference

The difference is time.

Entity processing treats time as something that happens around the entity: when it was created, when it moved through milestones, when it was completed, when it failed.

Entity tracking treats time as something that happens to the entity: how its attributes changed, how its behaviour accumulated, how its state evolved, and what it was at a point in time.

This difference changes the shape of the pipeline.

|  | Entity processing | Entity tracking |
|---|---|---|
| Entity type | Immutable | Mutable |
| Core question | What happened? | What changed? |
| Treatment of time | Time around the entity | Time within the entity |
| Main concern | Outcome | State |
| Typical grain | Event or transaction | Entity over time |
| Common outputs | Entity facts, milestone dates, outcome fragments | Timelines, histories, end-of-period snapshots |
| Main difficulty | Business logic | Temporal logic |

## Good and bad entities

Both patterns often require the data engineer to express whether an entity is good or bad.

In entity processing, this usually means classifying the outcome of an event. A sale may be profitable or unprofitable. An import declaration may be compliant or non-compliant. A helpdesk case may be resolved within service level agreement or outside it.

In entity tracking, good and bad usually relate to state or behaviour. A supplier may become high-risk. An employee may meet a performance threshold. A customer may become inactive. A bank account may show suspicious activity.

This distinction matters because the same phrase can hide different technical requirements.

A bad transaction can often be classified once.

A bad account may need to be tracked as a state over time.

## The role of aggregation

Both patterns aggregate detail back to the entity of interest.

In entity processing, aggregation usually reduces details into an entity-level result. Sales items become sales profit. Inspection criteria become inspection outcome. Escalation rows become case escalation summary.

In entity tracking, aggregation often turns behaviour into state. Transactions become account value. Audits become risk status. Repeated actions become performance history.

This is why the third pass is important in both patterns. The data engineer is not merely summarising data. The engineer is returning scattered detail to the business entity that gives it meaning.

## The role of fragments

Both patterns rely on fragment modelling.

In entity processing, fragments isolate pieces of business logic: margin, milestone dates, current version, failure outcome, escalation summary.

In entity tracking, fragments isolate temporal structure: compressed histories, timelines, end-of-period snapshots, behavioural states, memory windows.

The type of fragment differs, but the purpose is the same. Each fragment makes one piece of information reusable, testable, and meaningful.

## Where tracking adds complexity

Entity tracking adds complexity because identity must persist through change.

This introduces questions that entity processing can often avoid:

- When did the change occur?
- When was the change recorded?
- Which date should govern the analysis?
- How much history should count?
- What was true at the end of the reporting period?
- Which attributes changed together?
- Which behaviours should become states?

These are not merely technical questions. They are questions of business meaning.

The data engineer must therefore work closely with stakeholders to determine how the organisation wants to understand change.

## Relation to Type I and Type II

This distinction is related to the classic Type I and Type II approaches in data warehousing, but it is not the same distinction.

Type I and Type II describe how changing attributes are represented. Type I overwrites the previous value. Type II preserves historical values by recording validity periods.

Entity processing and entity tracking operate one level earlier. They ask what kind of business entity is being represented in the first place.

If the entity is treated as immutable, the usual pattern is entity processing. If the entity is treated as mutable, the usual pattern is entity tracking. Type I and Type II then become techniques within the broader tracking problem, not the foundation of the whole design.

This matters because a data engineer can implement Type II correctly and still misunderstand the entity. The deeper question is not merely whether history is stored, but what kind of continuity the business is trying to understand.

## Summary comparison

|  | Entity processing | Entity tracking |
|---|---|---|
| Entity | Immutable | Mutable |
| Main question | What happened? | What changed? |
| Business focus | Event outcome | Entity state and behaviour |
| Time | Milestones and completion | Histories, validity periods, snapshots |
| Identity problem | Which event is this? | Is this still the same entity? |
| Good/bad logic | Outcome classification | State or behaviour classification |
| Aggregation | Detail to event/entity result | Behaviour/history to state |
| Key fragments | Milestones, margins, outcomes, summaries | Timelines, end-of-period tables, behavioural states |
| Common risk | Stopping before aggregation | Misrepresenting time |
| Usual output | Entity-level facts | Entity-level histories and snapshots |

> [!NOTE]
> **Key ideas**
>
> Entity processing and entity tracking are two patterns of the same discipline.
>
> Entity processing asks what happened to an immutable entity.
>
> Entity tracking asks what changed in a mutable entity.
>
> Both patterns use fragments to return scattered detail to the business entity that gives it meaning.
>
> The main additional difficulty in entity tracking is time.