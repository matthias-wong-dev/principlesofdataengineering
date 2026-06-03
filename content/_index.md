---
title: Welcome
bookCollapseSection: false
bookToC: false
---

## Make business reality visible

**Principles of Data Engineering** is a guide to building data representations that make business reality visible.

Most data engineering books teach pipelines, platforms, and tools. This book is about something more fundamental. It explains what data engineering is really for: turning fragments of reality into reliable information that organisations can use to understand, decide, and act.

The recurring theme of the book is:

> Data engineering is the process of applying business intent to data to create information, and then insight.

It is underpinned by a central premise:

> Data is a fragment of reality.

That's why data engineering is not about moving records from point A to point B.

It is to make reality legible to business.

The book is organised around [six principles](../docs/judgement-under-ambiguity/the-six-principles-of-data-engineering/):

1. **Expressive entities**—make data recognisable as the business world.
2. **Meaningful fragments**—compose information from reusable, purposeful parts.
3. **Anticipate errors**—design for the failures real systems produce.
4. **Proportionate change**—keep computation aligned with informational change.
5. **Illuminate ambiguity**—turn ambiguous business intent into ordered progress.
6. **Diagnose root causes**—act on the conditions that make problems recur.

This book is written from deep delivery experience and focuses on patterns tested for complexity.

It is for organisations that want data representations that do more than run.

Data representations that make reality visible.

Data representations that survive real systems.

Data representations that stop organisations from guessing.

## For senior leaders

If you are a senior leader, read this instead: [Unglamorous data](https://irisnotes.com/posts/unglamorous-data/), a three-minute summary of the book.

## Download the book

The book is available for offline reading:

<ul>
  <li><a href="/downloads/Principles%20of%20Data%20Engineering.pdf" download="Principles of Data Engineering.pdf">Download the PDF</a></li>
  <li><a href="/downloads/Principles%20of%20Data%20Engineering.epub" download="Principles of Data Engineering.epub">Download the ePub</a></li>
</ul>


## Who is this book for?

This book is for **new data engineers** who want to think like principal architects from day one. It explains not only what to build, but why good data engineers build in a particular way.

It is for **mid-level engineers** who can already write pipelines, SQL, dbt models, Spark jobs, semantic models, or orchestration code, but want a deeper framework for designing systems that remain understandable, testable, and useful over time.

It is for **senior engineers, architects, and data leaders** who are tired of explaining the same lessons to every new team. This book gives language, diagrams, and patterns for teaching the craft clearly.

It is for **analytics engineers and data engineers** who want a technology-agnostic view of the discipline. Tools change. dbt, Spark, SQL, Fabric, Airflow, Power BI, and whatever comes next all matter. But the underlying judgement carries across a whole career.


## What to expect

This book is prescriptive and opinionated.

It does not try to be neutral about every possible pattern. It teaches hard-earned practices learned from production scars: how to model business entities, how to avoid pipeline mess, how to detect and mitigate errors, how to do incremental transformation properly, and how to work with stakeholders when nobody yet knows exactly what should be built.

The book explains advanced concepts in plain language. It assumes the reader is serious, but not that the reader already knows the vocabulary of data architecture.

Most of the material is technology-agnostic. The only strongly technology-specific sections are the chapters on Power BI, where the book explains dimensional modelling, semantic models, user experience, and row-level security in a practical enterprise context.

The goal is not to optimise for a particular tool stack.

The goal is principles that last.

## Some ideas inside

This book covers topics such as:

- [What is data, really?](../docs/foundations/what-is-data/)
- [A fundamental difference between mutable and immutable entities](../docs/creating-information/mapping-the-data-world/)
- [Three steps to modelling any system](../docs/creating-information/entity-processing/)
- [Powerful storytelling techniques that make sense for your business](../docs/creating-information/storytelling/)
- [Building a data product that can answer any question](../docs/modelling-reality/anticipating-questions/)
- [Treating dimensional modelling like UX, and not static reports like it is the 90s](../docs/presenting-insights/dimensional-modelling-for-ux/)
- [A row-level security pattern that is simple enough to implement but sophisticated enough to handle anything](../docs/presenting-insights/row-level-security/)
- [Metadata that is not compliance theatre](../docs/quality-reliability/metadata/)
- [How not to get into a mess with incremental load and messy times](../docs/efficient-stable-pipeline/incremental-processing/)
- [Parallel load orchestration that does not cost you a cent](../docs/efficient-stable-pipeline/programmatic-load-stack/)
- [Why stakeholder confusion is not a defect](../docs/judgement-under-ambiguity/working-with-stakeholders/)
- [Why you cannot rely on the project manager](../docs/judgement-under-ambiguity/construction-planning/)
- [Four steps out of any disaster scenario](../docs/judgement-under-ambiguity/when-things-go-wrong/)
- [A manifesto for your team](../docs/judgement-under-ambiguity/closing-essay-hallmarks-of-quality/)

## How to read this site

Start with the foundations:

- [What is data engineering?](../docs/foundations/what-is-data-engineering/)
- [What is data?](../docs/foundations/what-is-data/)
- [Data and organisations](../docs/foundations/data-and-organisations/)

While the book is best read sequentially, the six sections are loosely independent and can be read on their own:

1. [**Foundations**](../docs/foundations/)—start here for the core argument: what data is, what data engineering is for, and why organisations need data to make reality legible.
2. [**Creating information**](../docs/creating-information/)—learn the central craft of the book: turning raw operational traces into expressive entities, meaningful fragments, reference data, conformed systems, and reusable information.
3. [**Presenting insights**](../docs/presenting-insights/)—treat dimensional modelling as user experience, not report production; build semantic models that let users ask real business questions without guessing.
4. [**Quality & reliability**](../docs/quality-reliability/)—move beyond generic data quality language into practical methods for metadata, testing, assumptions, human curation, precise rules, and fuzzy logic.
5. [**Efficient & stable pipeline**](../docs/efficient-stable-pipeline/)—build pipelines that are fast, stable, observable, and maintainable, including incremental processing and programmatic orchestration patterns.
6. [**Judgement under ambiguity**](../docs/judgement-under-ambiguity/)—learn the senior craft: working with stakeholders, planning uncertain delivery, and diagnosing root causes when things go wrong.
