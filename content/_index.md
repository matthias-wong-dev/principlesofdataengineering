---
title: A Guide to Enterprise Data Engineering
bookCollapseSection: false
bookToC: false
---

## Business reality made visible

**Principles of Data Engineering** is a guide to building data representations that make business reality visible.

Most data engineering books teach pipelines, platforms, and tools. This book is about something more fundamental: turning fragments of reality into reliable information that organisations can use to understand, decide, and act.

The recurring theme of the book is:

> Data engineering is the process of applying business intent to data to create information, and then insight.

It is underpinned by a central premise:

> Data is a fragment of reality.

That's why data engineering is not about moving records from point A to point B. It is to make reality legible to business.

The book is organised around [six principles](../docs/judgement-under-ambiguity/the-six-principles-of-data-engineering/):

1. **Expressive entities**
2. **Meaningful fragments**
3. **Anticipate errors**
4. **Proportionate change**
5. **Illuminate ambiguity**
6. **Diagnose root causes**

Data representations that make reality visible. Data representations that survive real systems. Data representations that stop organisations from guessing.

## Download the book

<ul>
  <li><a href="/downloads/Principles%20of%20Data%20Engineering.pdf" download="Principles of Data Engineering.pdf">Download the PDF</a></li>
  <li><a href="/downloads/Principles%20of%20Data%20Engineering.epub" download="Principles of Data Engineering.epub">Download the ePub</a></li>
</ul>

## Use the book with AI agents

The book is also published as a skill for AI agents such as Claude Code. An architect holds the business intent, independent authors build, and a fresh reviewer for each chapter checks the work. Read how it works in [Steering AI agents](../docs/judgement-under-ambiguity/steering-ai-agents/).

<ul>
  <li><a href="/downloads/data-engineering-skill.zip" download="data-engineering-skill.zip">Download the skill</a></li>
</ul>

## Some ideas inside

- [What is data, really?](../docs/foundations/what-is-data/)
- [A fundamental difference between mutable and immutable entities](../docs/creating-information/mapping-the-data-world/)
- [Three steps to modelling any system](../docs/creating-information/entity-processing/)
- [Multiple timelines while staying sane](../docs/creating-information/entity-tracking/)
- [Powerful storytelling techniques that make sense for your business](../docs/creating-information/storytelling/)
- [Building a data product that can answer any question](../docs/presenting-insights/anticipating-questions/)
- [Treating dimensional modelling like UX, and not static reports like it is the 90s](../docs/presenting-insights/dimensional-modelling-for-ux/)
- [A row-level security pattern that is simple enough to implement but sophisticated enough to handle anything](../docs/presenting-insights/interactive-row-level-security/)
- [Metadata that is not compliance theatre](../docs/quality-reliability/quality-metadata/)
- [How not to get into a mess with incremental load and messy times](../docs/efficient-stable-pipeline/tracking-changes/)
- [Parallel load orchestration that does not cost you a cent](../docs/efficient-stable-pipeline/load-orchestration/)
- [Why stakeholder confusion is not a defect](../docs/judgement-under-ambiguity/working-with-stakeholders/)
- [Why you cannot rely on the project manager](../docs/judgement-under-ambiguity/construction-planning/)
- [Four steps out of any disaster scenario](../docs/judgement-under-ambiguity/when-things-go-wrong/)
- [A manifesto for your team](../docs/judgement-under-ambiguity/closing-essay-hallmarks-of-quality/)

## Applied to Microsoft Fabric

The principles are technology-agnostic. This book applies them to Microsoft Fabric.

Many of the book's core patterns need to be automated: [automated testing](../docs/quality-reliability/tests-and-assumptions/), [stage-and-merge loading](../docs/efficient-stable-pipeline/load-mechanics/), [fault tolerance](../docs/quality-reliability/fault-tolerance/), [incremental bookmarks](../docs/efficient-stable-pipeline/tracking-changes/), [dynamic measure selectors](../docs/presenting-insights/measure-of-measures/), [metadata as data](../docs/quality-reliability/quality-metadata/), and [dependency-aware load orchestration](../docs/efficient-stable-pipeline/load-orchestration/).

Moreover, a table is a table, whether it is loaded by SQL or by Python. Robust data engineering should not be limited to SQL transforms. Engineers loading files and tables in Python need the same guarantees.

These are fundamental, and data engineers should not have to hand-roll them on every project.

That's why they are implemented in [Weaver](https://weaverstack.dev), an open-source framework for Microsoft Fabric:

- **Testing:** data and calculation tests in Python, SQL and DAX, including unit tests of semantic model measures against independently calculated results.
- **Stage and merge:** a SELECT becomes a managed Warehouse table, with a load procedure, staging and reconciliation on a declared key.
- **Fault tolerance:** rejected rows are kept, unusually large updates or deletes are stopped before they reach your tables, and a failed step does not stop unrelated work.
- **Incremental loading:** each table or folder tracks its own progress, and `load --stale` reruns only the loads that need attention.
- **Measure selectors:** created from standard TMDL annotations, alongside shared modelling standards across semantic models.
- **Metadata as data:** deployed items, dependencies, run results and change statistics are recorded in an ordinary Fabric Warehouse.
- **Orchestration:** one dependency graph across Python, Spark SQL, T-SQL, semantic models and reports, loaded in the right order.

## Who is this book for?

- **New data engineers** who want to think like principal architects from day one.
- **Mid-level engineers** who can already write pipelines, SQL, Spark jobs or semantic models, and want a deeper framework for systems that stay understandable, testable and useful.
- **Senior engineers, architects and data leaders** who are tired of explaining the same lessons to every new team.
- **Senior leaders:** read [Unglamorous data](https://datawithoutguessing.com/articles/unglamorous-data/) for a three-minute summary.

The book is prescriptive and opinionated. It teaches practices learned from production scars, in plain language.

## How to read this site

Read it in order, or start with any of the six sections:

1. [**Foundations**](../docs/foundations/): what data is, and what data engineering is for.
2. [**Creating information**](../docs/creating-information/): turning operational traces into expressive entities and meaningful fragments.
3. [**Presenting insights**](../docs/presenting-insights/): dimensional modelling as user experience.
4. [**Quality & reliability**](../docs/quality-reliability/): metadata, testing and fault tolerance.
5. [**Efficient & stable pipeline**](../docs/efficient-stable-pipeline/): incremental processing and load orchestration.
6. [**Judgement under ambiguity**](../docs/judgement-under-ambiguity/): stakeholders, planning, AI agents and root causes.

## Data Without Guessing

This book is provided as part of [Data Without Guessing](https://datawithoutguessing.com). Comments and questions are welcome: see [*Data Without Guessing*](https://datawithoutguessing.com/principles-of-data-engineering/) for contact information.
