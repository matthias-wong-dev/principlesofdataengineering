---
title: The six principles of data engineering
url: /docs/judgement-under-ambiguity/the-six-principles-of-data-engineering/
description: "Introduces the six principles of data engineering as disciplines for resisting shallow curation and exercising judgement under ambiguity."
lede: The epitome of data engineering is judgement under ambiguity.
weight: 1
# draft: true
---

## Judgement under ambiguity

In the chapter [What is data engineering?](/docs/foundations/what-is-data-engineering/), we began with the aim of data engineering, its task, and its challenges.

The aim of data engineering is insight.

The task is to reshape data in light of intent.

The challenge is the fluid nature of data engineering:

- Easy substitutes—business areas have access to quick alternatives to insight that avoid the hard work of data engineering.
- Open-endedness—business areas may pursue new or different questions as they see more data.
- Ambiguity of aim—business areas may not be clear about how they want to use data, or different areas may have different aims.

But throughout this book, we have seen that the business is not the problem.

> The data engineer’s greatest enemy is not the stakeholder asking for shortcuts, but the engineer’s own willingness to provide them.

The business will often ask for the fastest and easiest outcome. This is to be expected. It is the data engineer who must decide how to respond.

Many data engineers, new or experienced, respond through what we may call *shallow curation*:

1. take the source system and map it into the target environment, adjusting names and data types;
2. receive a list of business requirements for reporting from stakeholders;
3. use the source data to apply transformation rules that meet those stated requirements, then load the results into a few large tables for Power BI visualisation.

In this way, a data engineer can reproduce source data in a cleaner environment, build reporting tables, refresh dashboards, and fix visible errors while still avoiding the deeper work.

The result may look technically correct. It may even be appreciated. But it remains a substitute for real data engineering.

Real data engineering refuses easy answers that simplify the genuine complexity of business and data reality. It requires accepting, and operating within, the fluid nature of data engineering.

This means the mark of the best data engineer is **sustained judgement under ambiguity**.

## The six principles

The principles of data engineering can be seen in this light. We introduced four in the preceding sections. This final section introduces the last two.

The six principles are:

- Instead of garbage-in-garbage-out with raw data, add value through **expressive entities**.
- Instead of building giant tables, create **meaningful fragments**.
- Instead of stopping with what works now, **anticipate errors** that may occur.
- Instead of wholesale response, maintain **proportionate change**.
- Instead of waiting for clarity, **illuminate ambiguity**.
- Instead of stopping at the symptoms, diagnose the **root cause**.

Instead of applying quick fixes to what is visibly wrong, the expert data engineer asks what must be right for business intent—now and into the future.

The six principles are disciplines that guard against the temptation of easy substitutes. They help the data engineer keep working until data has been shaped into information that can serve business intent.

It is not a matter of fast workaround versus slow and proper. It is the difference between what gets tangled up in a mess and what remains usable under change.

The chapters [Working with stakeholders](/docs/judgement-under-ambiguity/working-with-stakeholders/) and [Construction planning](/docs/judgement-under-ambiguity/construction-planning/) apply the principle **illuminate ambiguity**. The chapter [Sound judgement](/docs/judgement-under-ambiguity/sound-judgement/) applies the principle **root cause**.

The final chapter is the essay [Hallmarks of quality](/docs/judgement-under-ambiguity/closing-essay-hallmarks-of-quality/). This essay was written years before this text and is reproduced with minimal edits. It guided the years of work that preceded this book. Although it is written in a different register and uses different terms, it can be read as a summary of the book.

> [!NOTE]
> **Key ideas**
>
> The epitome of data engineering is judgement under ambiguity.
>
> The data engineer’s greatest enemy is not the stakeholder asking for shortcuts, but the engineer’s own willingness to provide them.
>
> Shallow curation reproduces source data in a cleaner environment, applies stated requirements, and produces reporting tables without doing the deeper work of shaping data toward business intent.
>
> The six principles guard against the temptation of easy substitutes.
>
> The six principles are **expressive entities**, **meaningful fragments**, **anticipate errors**, **proportionate change**, **illuminate ambiguity**, and **root cause**.
>
> These principles help the data engineer keep working until data has been shaped into information that can serve business intent.