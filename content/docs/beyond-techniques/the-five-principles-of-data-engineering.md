---
title: The five principles of data engineering
weight: 1
draft: true
---

The earlier sections outlined patterns and practices for data engineering scenarios. They focused on the treatment of information rather than technology. The technologyspecific sections are on Power BI, and even then, we stayed away from syntax to focus on fundamentals. This focus on information rather than technology is deliberate. It points data engineers to underlying principles rather than situational techniques. This last section, Beyond techniques, is where patterns culminate and summarised in five principles.

## The problem with shallow curation

The most common, but incorrect, approach for new data engineers is shallow curation. The typical steps are:

1. Take the source system and map to the target environment, adjusting for names

2. 3. and data types.

Receive a list of business requirements for reporting from stakeholders. Using the source data, apply transformation rules to meet stated requirements, load them into a few big tables for Power BI. A more experienced data engineer may organise these as facts and dimensions. This mindset has many drawbacks. Firstly, it leads to garbage-in, garbage-out. Source applications are not designed for analytical intent and never has the information content to meet business needs. Requirements stated upfront are rarely adequate to be a reliable guide to address this gap. Moreover, this approach focuses on the questions at hand rather than all the questions about the business. Finally, going straight from source to reporting tables means there are no building blocks for use in different scenarios. Using the information for a different scenario, such as ML feature engineering, requires rebuilding logic that embedded in dimensional models. In other words, shallow curation is too easily satisfied. It does not sufficiently push the data as found to meet the demands of business intent. Neither does it break down complexity in building towards advanced levels of achievement. Consequently, the difference is not between merely "good versus poor" quality, but between what is "possible versus impossible" for a team to achieve with this mindset. The problem with shallow curation is that there are some outputs. After all, the data engineer has faithfully reproduced data from the source system for users to gain access. Such an engineer may even feel satisfied for doing an excellent job when reality is far from the potential value. If business users are dissatisfied when business objectives are not fully met, it is possible to blame poor data quality at source or on the unclear business rules. The danger of shallow curation is that, like all mindsets that starts by reducing standards, it settles for less, and by settling for less, creates a blind spot for the engineer who cannot see the failure to reach excellence.

## Five principles

A surer basis for data engineering can be summarised in five principles:

- Instead of garbage-in-garbage-out with raw data, add value through expressive

entities.

- Instead of building giant tables, create meaningful fragments.

- Instead of stopping with what works now, anticipate errors that may occur.

- Instead of reacting to requirements, build momentum through guiding

attention.

- Instead of stopping at the symptoms, diagnose the root cause

That is, instead of finding quick fixes to what is wrong, the expert data engineer focuses on what needs to be right for business intent—now and into the future. These can be remembered through five phrases: expressive entities, meaningful fragments, anticipate errors, build momentum, root cause. It is not a matter of "fast workaround" versus "slow and proper." It is the difference between what gets tangled up in a mess versus what will not. In the long term, the five principles to fast and flexible paths to success. The earlier sections covered three of the principles–expressiveness entities, meaningful fragments and anticipating errors. The remaining section introduces the final principles–build momentum, root cause. The section ends with the chapter Hallmarks of quality. This essay was written years before this text and reproduced with minimal edits. The essay guided the years of work now summarised in this book.
