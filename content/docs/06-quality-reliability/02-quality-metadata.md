---
title: Quality metadata
url: /docs/quality-reliability/quality-metadata/
description: Explains how names, descriptions, and keys provide the interpretative context that makes data products understandable, trustworthy, and usable.
lede: Metadata gives data its interpretative context.
weight: 2
# draft: true
---

## Metadata as interpretative context

Data quality issues reflect the gap between the business world and the data world. In this view, metadata is not merely documentation for the next person working with the data. It is an indispensable tool for bridging that gap.

Metadata adds the interpretative context that connects the user to the business reality behind the data.

If a column in the source system is called `[Valid]`, renaming it to `[Is current name]` is not the difference between “having metadata standards” and “not having metadata standards.” It is the difference between comprehensible and incomprehensible data.

This bears stressing. Quality metadata adds value at the point of interpretation. No transformation can help a user who cannot tell what the result means.

Metadata is also the first impression for any user engaging with the data engineer’s product. It is the first step to trust. It can determine whether a user engages with the product or walks away.

Creating quality metadata is not difficult compared with the technical demands of data engineering. It requires the data engineer to ask:

> What does this look like to the user? If I were the user, is this something I would want for myself?

Importantly, metadata is not an add-on task. It is part of the modelling task itself, starting with exploratory analysis. In complex cases, starting with metadata is a useful way to lay out the logic in plain language before implementation. A mature data engineer will acquire the habit of writing metadata first, not last.

This chapter covers three aspects of metadata:

- names;
- business descriptions;
- database keys.

## Names

Each site will have its own naming conventions. This chapter is not about defining one specific convention. It is about universal principles that should be observed in all naming conventions.

Names apply to schemas, tables, columns, Power BI models, measures, calculation groups, and display folders.

In every instance, names should be business-centric and written in plain language. They should not use idiosyncratic acronyms or abbreviations for the developer’s convenience. There is no justification for using `[Employee cnt]` when the meaning is `[Employee count]`. If the infrastructure supports spaces in column names, they should be used.

Names should contain helpful signals. For example, `Is` and `Has` can be used to indicate binary columns, such as `[Is non-compliant]` or `[Has active case]`. Columns ending with `date` and `datetime` should signal their precision. Tables starting with `Ref` can indicate reference tables. These signals should not come at the cost of readability. This is why a Power BI dimensional model should not prefix tables with `dim` or `fact`. Such prefixes describe the modelling technique, not the user-facing meaning.

Naming conventions should be consistent across schemas, databases, warehouses, and semantic models where possible. Consistency in prefixes, suffixes, casing, and syntax creates a design language for the warehouse.

The data engineer should pay particular attention to conformed concepts. When a data engineer uses a name, it is important to check whether the concept is already named differently and shared by other domains.

For example, when adding `Cake.RefQualityControl`, it is important to check whether `RefTesting`, `RefAudit`, or `RefInspection` are already being used to mean the same thing. If so, it may be better to reuse an existing name.

Consistency applies to all aspects of the name: capitalisation, syntax, and semantics. It is better to consistently use `[Sales date]` and `[Inspection date]`, or `[Date of sales]` and `[Date of inspection]`, than to switch from one form to another haphazardly.

Names should also be explicit and unambiguous.

An explicit column name means using `[Inspection first of month]` rather than `[First of month]`.

An unambiguous name means ensuring the word has only one meaning for the user. For example, does `[Last inspection date]` mean the previous inspection date or the final inspection date? Does `restricted` mean less access, or access to restricted data?

Special attention should be paid to words that are both nouns and verbs. They are particularly prone to misinterpretation.

Names should also be able to stand alone. Data tables and columns can often be taken out of context. For key concepts, it may be worthwhile for names to carry their own context.

For example, `[Is non-compliant]` may be better as `[Is financially non-compliant]`. This may involve repeating some of the table meaning in the column name.

Another extension of explicit and unambiguous naming is avoiding generic filler words.

Words such as `type`, `group`, `summary`, and `details` are often used by developers without adding meaning. They can function like “um” and “ah” in a sentence: they fill space but obscure meaning.

If a table is called `summary`, it should usually be renamed to reflect what is being summarised. `Details` should be avoided unless it is truly a finer-grain expansion of a header row.

In choosing names, the data engineer faces a tension between explicit accuracy and succinctness. Sometimes an overly verbose name is not aesthetically pleasing in a report visual. When in doubt, the data engineer should err on the side of explicitness, because it is easier to shorten a name in a Power BI visual than for a user to creatively extend it.

These principles apply just as much to code. Temporary tables and CTEs should be named with business meaning, not cryptic abbreviations like `tmp`. In complex code, column renaming should happen early, on first contact, and persist throughout transformation. This practice promotes clarity and readability.




## Business descriptions

Business descriptions are frequently overlooked by data engineers as an add-on rather than a core task.

Too often, descriptions merely restate the artefact name. For example, `Cake.Sales` may be described as “A list of cakes sold”, or `[Is non-compliant]` as “True if found non-compliant.” These descriptions do nothing more than take up storage space. At worst, they harm trust by conveying shallowness.

Business descriptions are meaning explanations. They enhance data quality by aligning artefacts to business reality through interpretative context.

A good description should focus on:

1. business reality;
2. transformation logic, including assumptions;
3. limitations;
4. linkages and comparisons with related concepts.

### Business reality

Business reality, rather than technical notes, should be the focus of descriptions.

For example, a column such as `[Is non-compliant]` should describe what non-compliance means in business terms, not merely say “if the result code is `F`.”

Data engineers and stakeholders often slip into using system names as shorthand for business concepts. This is not preferred. Descriptions should refer to business entities and business processes, not merely the systems that implement them.

For example, instead of only saying `Salesforce` or `SAP`, use the relevant business concept, such as health care record, employee registration, inspection outcome, or sales transaction.

There will be cases where system names or technical implementation details are necessary for transparency. These should be included as supplementary information, not as standalone descriptions.

For example, the description for `[Is non-compliant]` may be:

> True if the transaction failed to meet the minimum regulatory requirements for importation, based on the department’s published compliance criteria. This includes both automatic and manual assessments. Transactions flagged by automated rules are included regardless of whether they were later manually overridden. This column does not include cases where compliance was not assessed. The result code is derived from the `ResultCode` field in the source system, where `F` indicates failure.

### Transformation logic

Transformation logic is the heart of a data pipeline. Describing transformation logic and important assumptions is necessary for transparency and trust.

This is especially important for complex or fuzzy logic.

The transformation should be stated in business terms. Technical statements can be included as elaboration, but not as a substitute for meaning.

For example:

> This column is derived from the inspection result and officer notes. It is true if the inspection outcome was `Spoiled cake` or `Not tasty`, and the inspection was conducted by a certified officer. It excludes inspections conducted during training. The logic is implemented in the `InspectionOutcomeFlag` measure using a combination of result codes and officer certification status.

Transformation logic can include lineage from data sources where relevant.

### Limitations

Limitations should also be framed in terms of business interpretation.

“The column can have a null value” is not a useful limitation by itself.

A better statement is:

> The inspector may not record a result if there are no issues. This means it is not possible to distinguish between a successful inspection and an inspection not performed.

Clear statements of limitation are essential for transparency and reliable application of business insight.

### Linkages and comparisons

Linkages and comparisons are often valuable for users exploring complex business processes.

Where relevant, descriptions should point out related concepts. These links help users navigate the warehouse and understand how one concept differs from another.

In terms of storage, if the same description applies in multiple places, it should be included in the reference table, not repeated in the transaction table. Reference tables are carriers of meaning and the user’s primary interface to the model.

Storytelling dimensions are especially important. They should have the richest and most articulate descriptions because they often encapsulate complex interpretative logic.

Descriptions on database artefacts—tables, columns, and measures—will inevitably be piecemeal. Standalone documentation is also necessary to provide an end-to-end view of the business problem and its data model.

## Database keys

Database keys include primary keys, foreign keys, and unique keys. They are also metadata.

Names and business descriptions explain artefacts in themselves. Keys explain how artefacts relate to each other.

First, relationships are part of meaning. The relationship of one table with another table tells the user something about both tables that neither table can say in isolation.

For example, a foreign key between `Cake.Sales` and `Cake.RefProfitability` immediately signals that some sales may be profitable and some may not.

Second, database keys help users navigate the database and perform joins. In this sense, database keys serve as a map for the warehouse. Without them, users are left to guess. This is not acceptable.

Third, primary keys play a special role. As explained in [Mapping the data world](/docs/creating-information/mapping-the-data-world/), the primary key is what links a database record to its real-world business entity. Therefore, primary keys help convey the meaning of a row to the business user.

Primary keys are also the foundation for fault tolerance and change detection.

They allow the data engineer to identify duplicates, track changes, and implement incremental loads. These techniques are covered in later chapters.

There are cases where primary keys are difficult to define. If the answer is “each row is a new entity,” such as in a log table, the data engineer can still express this with an increasing integer and load incrementally.

In other cases, the grain of the fact table may be unclear or difficult to compute, especially when business centricity requires compacting several grains into one fact table for presentation. Even so, it is worth the effort of computing a key if possible.

Each organisation implements keys differently. Some store them only in conceptual diagrams or third-party tools. The disadvantage is that they cannot be easily read or queried.

The best approach is to house them as standalone tables in the warehouse.

This makes them visible and open to querying like every other table in the warehouse. In other words, metadata should be stored and treated as data.

Ultimately, keys are not just technical constraints. They are statements of relationship.

This makes them a non-negotiable part of metadata.

## Metadata as data

Data without metadata is data without context.

The primary purpose of metadata is not governance, tagging, discoverability, or data exchange. These are all important, but they are secondary effects.

Metadata should be understood in the context of the data engineer’s task: shaping data in light of business intent. From this perspective, the primary purpose of metadata is to add interpretative context that aligns the data world to its underlying business reality.

Without this context, interpretation is left to the user, who must fill in the gap by guesswork. When the user must guess, the data engineer has failed to shape the data to meet business intent.

Quality metadata is not difficult to create. It comes naturally with the habit of looking at the product from the user’s perspective, and a taste for the satisfaction that comes from articulate writing.

Finally, whether metadata describes names, descriptions, or keys, it should be stored and made available as data.

Instead of recording metadata only in diagrams, specialist tools, or database constructs, it should also be available as tables. Treating metadata as data enhances the ability to distribute it, automate it, and surface it to appropriate tools through APIs.

Structured metadata also makes it easier for tools, including large language models, to reason correctly over the warehouse.

## Key ideas

> [!NOTE]
> **Key ideas**
>
> Metadata gives data its interpretative context.
>
> Quality metadata helps bridge the gap between the data world and the business world.
>
> Names should be business-centric, explicit, unambiguous, and consistent.
>
> Business descriptions should explain meaning, transformation logic, assumptions, limitations, and related concepts.
>
> Keys are metadata because they explain how artefacts relate to each other.
>
> Metadata should be stored and treated as data.