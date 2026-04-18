---
title: Expressiveness and fragment modelling
description: "Introduces two core principles of data engineering: expressive entities and fragment modelling as the basis for reusable information."
lede: Good data engineering begins by shaping data into expressive, reusable fragments.
weight: 1
draft: true
---

Insight is information analysed in the light of interest. However, the data engineer starts one step further back than information. Data engineering starts with data.

Data comes from Latin for “given.” Data is, therefore, what is given with no fixed interpretation, and thus not yet information. Starting with the late 1980s, business discovered that data can be mined as a valuable source of information. Over time, this gave rise to the discipline of data engineering. Data engineering is now one of the most privileged disciplines in the modern era because it is the prerequisite step to convert data to information and become the avenue to business insight.

Data is collected by business processes. This collection can be seen as a projection of the business world into the data world of databases. This projection is often imperfect. First, it can be technically challenging and costly to accurately record business events. Moreover, the business processes making the data record may differ from the business interest of the analyst, for example when the source of data is not controlled by the business seeking to analyse it. The most important goal of a data engineer is to deal with these imperfections so that the data is ready for business interest.

In this perspective, data engineering is the task of taking data projected by business processes and refashioning it into a shape required by business interest.

> [!NOTE]
> **TODO**
>
> The manuscript includes a diagram here: `Business world -> Data world -> Business world`.

The data engineer needs to do this in an efficient, reproducible way for vast amounts of data over a sustained period. Therefore, the goal and purpose of data engineering is to create a cost-effective, robust pipeline of valuable, reusable blocks of information that are conducive to business insight.

How would the data engineer go about achieving this effectively? By the end of the text, a total of five principles are introduced. The first two principles are expressiveness and fragment modelling.

## Expressiveness

Insight is information analysed in the light of interest. A data engineer who takes this seriously becomes invested in the business world, asks how data relates to it, and is driven by the need to organise the data in a way that makes sense for business decisions. This is the task of applying business interest to reshape data. When done successfully, the output is expressive of business interest. The first, and most important, principle of data engineering is therefore the search for expressiveness.

Expressive entities refer to the idea that the tables and relationships created in the data warehouse should not merely reflect the data as it was found, but correspond strongly to real business processes. It is expressive because the consumer or reviewer of the model can clearly recognise the world the model is attempting to approximate. If a reasonably competent layperson cannot easily relate the model to the real world, then the model is not expressive. Correspondence to the world by the agent trying to influence it is therefore the final arbitrator of whether a data model is successful.

Expressiveness encompasses all aspects of a good data engineer’s work.

Expressiveness lies in everything, from the way the engineer designs tables, chooses to name tables and columns, to the way they are connected by primary and foreign keys, right through to the way the engineer describes the intent of code to others.

## Fragment modelling

The fluid nature of business insights means that the data engineer cannot know in advance what needs to be built. At a micro level, this applies to a single data engineering project. At a macro level, discovering business insights can be a journey of years over multiple teams. Moreover, in a large organisation different teams will want to see the same information in different ways to reflect specific business interests.

These explain why the goal of a data engineer is to produce reusable blocks of information rather than focus solely on building complete data products. When the data engineer shifts focus from building complete products to creating blocks that can be reused for multiple products, this leads to a shift from seeing the warehouse as a repository of data models to seeing it as a fragment store of valuable information. A data engineering approach focused on creating a store of valuable fragments is fragment modelling.

Modularity of code is a cornerstone in software engineering. Fragment modelling takes this concept and applies it to the modularity of information creation in a data pipeline. The result, as in software engineering, is a benefit of clarity, flexibility, and reusability in information. The data engineer therefore sees the pipeline primarily as software code and tables as functions. In fact, much of the wisdom in the Zen of Python carries to fragment modelling.

Fragment modelling is concerned not only with the informational value of a fragment, but also with its intended use. The data engineer does not rest until the fragment becomes plug-and-play for the end user who can make use of the information with minimal additional engineering. In most cases, this means designing fragments that integrate cleanly into traditional dimensional models for self-service business intelligence. However, it also means ensuring that fragments can be adapted for other analytical scenarios such as data science feature engineering. This combined focus on both information and usability makes fragment modelling especially suited to the demands of the data age where data analytics is employed in a growing range of contexts.

Fragment modelling is also an important step towards expressiveness. A wide table with a large number of miscellaneous columns buries multiple business concepts into one undifferentiated “thing” that does not recognisably map to any real-world entity. On the other hand, tightly defined fragments bring clarity to business attributes by giving them sharp relief. It is impossible to achieve a truly expressive data model without deconstructing source data into meaningful fragments and reorganising them to better reflect real-world entities.

Fragment modelling can be disorienting for an engineer used to traditional warehousing approaches. Once familiar, it becomes a powerful approach to creating sustainable and flexible pipelines. The section *Creating information* explains how this is done.
