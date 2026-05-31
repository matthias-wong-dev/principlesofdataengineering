---
title: Expressiveness and fragment modelling
url: /docs/creating-information/expressiveness-and-fragment-modelling/
description: "Introduces two core principles of data engineering: expressive entities and fragment modelling as the basis for reusable information."
lede: Data engineering begins by shaping data into expressive, reusable fragments.
weight: 1
---

## From data to reusable information

Data engineering reshapes [fragments of reality](/docs/foundations/what-is-data/) into forms the business can use.

This work must be done efficiently, reproducibly, and over sustained periods of time. The goal is not merely to produce isolated reports or one-off datasets, but to create a cost-effective and robust pipeline of valuable, reusable blocks of information that are conducive to business insight.

How does the data engineer do this effectively?

This book introduces five principles of data engineering. The first two are **expressiveness** and **fragment modelling**. The two principles are:

> Instead of accepting garbage-in, garbage-out with raw data, add value through expressive entities.
> 
> Instead of building giant tables, create meaningful fragments.

## Expressiveness

Insight is [information analysed in the light of intent](/docs/foundations/what-is-data-engineering/). A data engineer who takes this seriously becomes invested in the business world, asks how data relates to it, and is driven by the need to organise data in a way that makes sense for business decisions.

This is the task of applying business intent to reshape data. When done successfully, the output is expressive of business intent.

The first and most important principle of data engineering is therefore the search for **expressiveness**.

The data engineer’s work is expressive when its outputs do not merely reflect data as it was found, but correspond strongly to real business entities and processes. It is expressive because the consumer or reviewer of the model can clearly recognise the world the model is attempting to approximate.

If a reasonably competent layperson cannot easily relate the model to the real world, then the model is not expressive. Correspondence to the world by the organisation trying to influence it is therefore the final arbitrator of whether a data model is successful.

Expressiveness has three qualities.

It is **faithful**: it preserves meaningful correspondence with the business reality it represents.

It is **legible**: a competent business user can recognise what the model is attempting to show.

It is **operable**: the model can be used in workflows or decisions with minimal rework.

Expressiveness encompasses all aspects of a good data engineer’s work. It lies in everything: the way the engineer designs tables, chooses names for tables and columns, connects entities through primary and foreign keys, and describes the intent of code to others.

## Fragment modelling

The [fluid nature of business insight](/docs/foundations/what-is-data-engineering/) means that the data engineer cannot know in advance exactly what needs to be built.

At a micro level, this applies to a single data engineering project. Requirements shift as information becomes visible and stakeholders encounter their own business through data. At a macro level, discovering business insight can be a journey of years over multiple teams. In a large organisation, different teams will also want to see the same information in different ways to reflect specific business interests.

This is why the goal of a data engineer is not only to build complete data products, but to produce reusable blocks of information.

When the data engineer shifts focus from building complete products to creating blocks that can be reused for multiple products, the warehouse is no longer seen merely as a repository of data models. It becomes a fragment store of valuable information.

A data engineering approach focused on creating such a store is **fragment modelling**.

Modularity of code is a cornerstone in software engineering. Fragment modelling applies this concept to the modularity of information creation in a data pipeline. The result, as in software engineering, is clarity, flexibility, and reuse.

> The data engineer therefore sees the pipeline primarily as software code, and tables as functions.

A good table in a pipeline performs a defined transformation—it accepts upstream data, applies a specific piece of business meaning, and produces an output that can be reused downstream. 

In this sense, much of the wisdom in the Zen of Python carries to fragment modelling.

Fragment modelling is concerned not only with the informational value of a fragment, but also with its intended use. The data engineer does not rest until the fragment becomes plug-and-play for the end user who can make use of the information with minimal additional engineering.

In most cases, this means designing fragments that integrate cleanly into traditional dimensional models for self-service business intelligence. However, it also means ensuring that fragments can be adapted for other analytical scenarios, such as data science feature engineering.

This combined focus on both information and usability makes fragment modelling especially suited to the demands of the data age, where data analytics is employed in a growing range of contexts.

Fragment modelling is also an important step towards expressiveness.

A wide table with a large number of miscellaneous columns buries multiple business concepts into one undifferentiated "thing" that does not recognisably map to any real-world entity. On the other hand, tightly defined fragments bring clarity to business attributes by giving them sharp relief.

It is impossible to achieve a truly expressive data model without deconstructing source data into meaningful fragments and reorganising them to better reflect real-world entities.

This chapter introduces fragment modelling as a principle. The later chapter [Meaningful fragments](/docs/creating-information/meaningful-fragments/) explores the practice in detail.

Fragment modelling can be disorienting for an engineer used to traditional warehousing approaches. Once familiar, it becomes a powerful approach to creating sustainable and flexible pipelines. The following chapters explain how this is done.

> [!NOTE]
> **Key ideas**
>
> Expressiveness is the principle that data models should recognisably correspond to the business world they represent.
>
> Expressive data is faithful, legible, and operable.
>
> Fragment modelling is the principle of creating reusable blocks of information rather than giant tables.
>
> In a well-designed pipeline, tables can be understood as functions that transform fragments of data into reusable information.