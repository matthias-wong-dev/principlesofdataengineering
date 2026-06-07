---
title: Efficiency and stability
url: /docs/efficient-stable-pipeline/efficiency-and-stability/
description: Defines informational efficiency, algorithmic efficiency, and stability as disciplines for keeping pipeline work proportionate to real-world change.
lede: A mature pipeline keeps changes in computation aligned to changes in information.
weight: 1
# draft: true
---

## Correspondence between information and computation

A mature pipeline maintains correspondence between changes in information and changes in computation.

When little has changed in the business world, little should need to change in the data world, and little should need to be recomputed. When that correspondence breaks down, the pipeline becomes inefficient, unstable, or both.

This chapter introduces efficiency and stability as two disciplines for preserving that correspondence.

| Concept | Question |
|---|---|
| Efficiency | Is the pipeline doing more computational work than the information change requires? |
| Stability | Is the data world changing in proportion to the business world? |

This is also the fourth principle of data engineering:

> Instead of wholesale response, maintain proportionate change.

## Efficiency

Developers often talk about fast and slow. But fast and slow are slippery terms.

Is one second fast? Is ten seconds slow? One second to process ten rows may be unacceptably slow. Ten seconds to process ten million rows may be impressively fast.

These judgements depend on infrastructure, data shape, implementation choices, and the value of the information being processed.

Because performance depends on many factors, it is more useful to focus first on efficiency.

**Efficiency** means using the minimum necessary resource to calculate the required information.

There are two kinds of efficiency:

| Kind | Concern |
|---|---|
| Informational efficiency | Does the pipeline process only the information needed to reflect real change? |
| Algorithmic efficiency | Does the pipeline calculate that information as cheaply as the environment allows? |

Informational efficiency is about processing as little information as possible. A pipeline is informationally inefficient if it processes hundreds of millions of rows when only a handful have changed.

Algorithmic efficiency is about computing those changes as cheaply as possible in a given computational environment. A pipeline is algorithmically inefficient if it takes seconds to process one row when the same result could be calculated in milliseconds.

Informational efficiency is largely universal across technologies. Algorithmic efficiency is more technology-dependent and varies from site to site.

Efficiency is important because it is central to sustainable warehouse growth. It also affects how quickly users receive results.

Some performance factors sit outside the data engineer’s immediate control: server configuration, infrastructure limits, source-system behaviour, or the business value of the information being processed. But the data engineer can still ensure that the pipeline does only the necessary work, and no more, to reflect real-world change.

## Stability

**Stability** is closely related to efficiency.

> [!SHARE:proportionate-change]
> Stability means that small changes in the business world should produce proportionate changes in the data world.


An unstable pipeline amplifies change. A small input change creates a large output change.

For example, changing a country name in a reference table might ripple through and rewrite many downstream tables. A more dramatic example was the fear of the Y2K bug, where systems storing years using only two digits risked treating the change from 1999 to 2000 as a catastrophic discontinuity rather than an ordinary date transition.

Stability is important because it shapes the user’s experience of reliability.

Reports that suddenly become empty or radically different undermine trust. There is little value in explaining that the issue came from a small reference-data change, a refreshed update timestamp, or a ripple effect in the pipeline. As far as the user is concerned, the product became unreliable.

A stable pipeline does not merely run successfully. It changes in ways that correspond to changes in the world it represents.

## Efficiency and stability together

Efficiency and stability are related but distinct.

A pipeline can be algorithmically inefficient without being unstable. For example, a pipeline may scan a full source table every night to identify a few changed rows, then update only those changed rows in the warehouse. The final data-world change is proportionate, because only the changed rows are updated. However, the computation is inefficient, because the pipeline read far more source data than the information change required.

A pipeline can also be unstable without being algorithmically inefficient. For example, truncate-and-reload may be the cheapest implementation for a small table. In computational terms, this may be acceptable. But it is unstable because the table temporarily disappears or becomes incomplete during the load. If the reload fails after the truncate, the data product is left in an unsafe state. 

Sometimes inefficiency and instability overlap. For example, a large table with a `[Today’s date]` column may update every row every day. This is unstable because the table changes constantly even when the underlying business entities have not changed. It is also informationally inefficient because the pipeline performs large amounts of work for little business value.

In all cases, the problem is broken correspondence.

The amount of data change and computational work no longer reflects the amount of information change.

Meaningful fragments help preserve this correspondence. When each table has a clear informational purpose, changes can stay local. A change in one concept does not need to churn unrelated data. This makes the pipeline easier to load, easier to test, easier to reason about, and more stable under change.

The chapters in **Efficiency & stability** explore how to build pipelines that are efficient and stable over time.

> [!NOTE]
> **Key ideas**
>
> The fourth principle of data engineering is **proportionate change**.
>
> Informational efficiency means processing only the information needed to reflect real-world change.
>
> Algorithmic efficiency means calculating that information as cheaply as the environment allows.
>
> Stability means that small changes in the business world should produce proportionate changes in the data world.
>
> Inefficiency and instability both occur when pipeline work stops corresponding to information change.
>
> Meaningful fragments help preserve correspondence by keeping change local, legible, and proportionate.