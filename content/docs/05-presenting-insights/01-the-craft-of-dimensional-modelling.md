---
title: The craft of dimensional modelling
url: /docs/presenting-insights/the-craft-of-dimensional-modelling/
description: Learn dimensional modelling in Power BI and how to turn reusable data into analytical models business users can understand, explore, and trust.
lede: Information does not become insight until users can see it, touch it, and ask it questions.
weight: 1
---

## From information to insight

Insight is information analysed in light of intent. The previous section, [Creating information](/docs/creating-information/expressiveness-and-fragment-modelling/), focused on building reusable blocks of information from data.

This section, **Presenting insights**, asks the next question.

How should that information be assembled into a product that business users can explore, understand, and trust?

Modern data engineers may present insights through machine learning models, embedded analytics, real-time applications, or custom tools. Yet one method remains central to business intelligence: **dimensional modelling**.

Dimensional modelling, systematised by Ralph Kimball, remains one of the most effective ways to organise information for business analysis. In the Microsoft ecosystem, Power BI semantic models make dimensional modelling especially important because they provide the layer through which many business users interact with data.

A dimensional model in Power BI is therefore best understood as a product interface.

## The craft

Building a data pipeline is largely an engineering exercise. It requires correctness, reproducibility, performance, and maintainability.

Building a dimensional model also requires those things. But the work becomes much easier when the upstream tables are ready for assembly: meaningful fragments become facts; expressive reference tables become dimensions; binary flags simplify measures. The technical work of dimensional modelling is greatly simplified when it is built on a strong foundation.

The central difficulty of dimensional modelling lies elsewhere.

When building a pipeline, the data engineer is mainly concerned with informational value: how data can be transformed into faithful, reusable, business-relevant information. When building a dimensional model, the data engineer must also anticipate how users will think, ask, filter, drill, and otherwise use the model.

The model must not only be correct. It must feel natural to use and intuitively aligned to business intent.

This is why dimensional modelling is a craft.

In practice, this craft appears in modelling decisions, many of which are not questions of correctness alone: which tables should be visible, which columns should be hidden, which measures should be defined, which relationships should be active, and how the model should guide the user’s attention.

The hard question is therefore not only: How do I build the dimensional model?

It is also:

> How should the dimensional model behave?

Two guiding questions organise the chapters in this section:

- What does a good dimensional model look and feel like?
- What modelling tools are available to anticipate a range of user behaviours?