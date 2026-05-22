---
title: The craft of dimensional modelling
url: /docs/presenting-insights/the-craft-of-dimensional-modelling/
description: Explains dimensional modelling in Power BI as the craft of turning reusable information into analytical products business users can understand and use.
lede: Dimensional modelling is the craft of turning information into a usable analytical product.
weight: 1
draft: true
---

## From information to insight

The previous section, [Creating information](/docs/creating-information/expressiveness-and-fragment-modelling/), focused on building reusable blocks of information. These are meaningful fragments: expressive entities, reference tables, timelines, mappings, storytelling dimensions, and other prepared pieces of business meaning.

This section, **Presenting insights**, asks a different question.

How should those fragments be assembled into a product that business users can explore, understand, and trust?

Modern data engineers may present insights through machine learning models, embedded analytics, real-time applications, or custom tools. Yet one method remains central to business intelligence: **dimensional modelling**.

Dimensional modelling, pioneered by Ralph Kimball, remains one of the most effective ways to organise information for business analysis. In the Microsoft ecosystem, Power BI semantic models make dimensional modelling especially important because they provide the layer through which many business users interact with data.

A dimensional model in Power BI is therefore not merely a technical artefact. It is a product interface.

## The craft

Building a data pipeline is largely an engineering exercise. It requires correctness, reproducibility, performance, and maintainability.

Building a dimensional model also requires those things, but its central difficulty is different.

The data engineer must anticipate how users will think, filter, compare, drill, summarise, and ask follow-up questions. The model must not only be correct. It must feel natural to use.

This is why dimensional modelling is a craft.

It has technical rules, but rules are not enough. A good model depends on judgement: which tables should be visible, which columns should be hidden, which measures should be defined, which relationships should be active, and how the model should guide the user’s attention.

If the previous section was about creating information, this section is about making that information usable.

## The foundation matters

Dimensional modelling becomes much easier when the upstream pipeline has been built well.

Meaningful fragments become facts. Expressive reference tables become dimensions. Storytelling dimensions become natural filters. Binary flags simplify measures. Milestone fragments make duration analysis straightforward.

When this foundation exists, the dimensional model does not need to compensate for missing business meaning. It can assemble prepared information into a form that supports analysis.

The hard question is therefore not only:

> How do I build the dimensional model?

It is also:

> What should the dimensional model make easy for the user to do?

Two guiding questions organise the chapters in this section:

- What does a good dimensional model do?
- What does a good dimensional model look and feel like?