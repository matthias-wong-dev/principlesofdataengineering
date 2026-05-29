---
title: Quality metadata
url: /docs/quality-reliability/quality-metadata/
description: Explains how names, descriptions, and keys provide the interpretative context that makes data products understandable, trustworthy, and usable.
lede: Without metadata, everyone is guessing.
weight: 2
# draft: true
---

## When metadata is missing

Metadata is the place where meaning is either carried by the data product or abandoned to the user.

Data quality issues reflect the gap between the business world and the data world. Metadata helps bridge that gap by adding the interpretative context that connects the user to the business reality behind the data.

A source column called `[Valid]` may look harmless until someone has to use it.

Valid for what? Valid now, or valid at creation? Valid according to the source system, the business rule, or the reporting model? Does `false` mean expired, rejected, superseded, or never approved?

Renaming `[Valid]` to `[Is current name]` is not cosmetic. It changes the user’s ability to understand the data.

This is why metadata is a quality issue.

Quality metadata adds value at the point of interpretation. No transformation can help a user who cannot tell what the result means.

Metadata is not an add-on task. It is part of modelling. In complex cases, writing metadata first is a way to lay out the logic in plain language before implementation.

There are three basic kinds of metadata discussed in this chapter:

| Metadata | Question it answers | Danger when compromised |
|---|---|---|
| Names | What is this thing? | Unrecognisable |
| Business descriptions | What does this mean, and when is it unsafe to use? | Incomprehensible |
| Database keys | How does this relate to reality and to other artefacts? | Lost |

Without good names, artefacts become unrecognisable. Without descriptions, artefacts become incomprehensible. Without keys, they become lost: disconnected from reality and from the other artefacts that give them meaning.

## Names answer: what is this thing?

Each site will have its own naming conventions. This chapter is not about defining one specific convention. It is about universal principles that should be observed in all naming conventions.

Names apply to schemas, tables, columns, Power BI models, measures, calculation groups, and display folders.

In every instance, names should be business-centric and written in plain language. They should not use idiosyncratic acronyms or abbreviations for the developer’s convenience. There is no reason to use `[Employee cnt]` when the meaning is `[Employee count]`. If the infrastructure supports spaces in column names, they should be used.

Names can also contain useful signals. `Is` and `Has` can indicate binary columns, such as `[Is non-compliant]` or `[Has active case]`. Columns ending with `date` and `datetime` can signal precision. Terms such as `current`, `historical`, `earliest`, `latest`, `start`, and `end` should be used consistently.

These signals are helpful only when they clarify business meaning. They should not advertise technical structure at the expense of user understanding.

This is why a Power BI dimensional model should not prefix tables with `dim` or `fact`. Such prefixes describe the modelling technique, not the user-facing meaning.

Naming conventions should be consistent across schemas, databases, warehouses, and semantic models where possible. Consistency in prefixes, suffixes, casing, and syntax creates a design language for the warehouse.

The data engineer should pay particular attention to conformed concepts. Before naming something new, check whether the same concept already appears elsewhere under a different name.

For example, when adding `Cake.RefQualityControl`, it is important to check whether `RefTesting`, `RefAudit`, or `RefInspection` are already being used to mean the same thing. If so, it may be better to reuse an existing name.

Names should also be explicit and unambiguous.

An explicit column name means using `[Inspection first of month]` rather than `[First of month]`.

An unambiguous name means ensuring the word has only one meaning for the user. For example, does `[Last inspection date]` mean the previous inspection date or the final inspection date? Does `restricted` mean less access, or access to restricted data?

Names should also be able to stand alone. Data tables and columns can often be taken out of context. For key concepts, it may be worthwhile for names to carry their own context.

For example, `[Is non-compliant]` may be better as `[Is financially non-compliant]`. This may involve repeating some of the table meaning in the column name.

Another extension of explicit and unambiguous naming is avoiding generic filler words.

Words such as `type`, `group`, `summary`, and `details` are often used by developers without adding meaning. They can function like “um” and “ah” in a sentence: they fill space but obscure meaning.

If a table is called `summary`, it should usually be renamed to reflect what is being summarised. `Details` should be avoided unless it is truly a finer-grain expansion of a header row.

When in doubt, the data engineer should err on the side of explicitness, because it is easier to shorten a name in a Power BI visual than for a user to creatively extend it.

These principles apply just as much to code. Temporary tables and CTEs should be named with business meaning, not cryptic abbreviations like `tmp`. In complex code, column renaming should happen early, on first contact, and persist throughout transformation.

## Descriptions answer: what does this mean?

Business descriptions are frequently overlooked by data engineers as an add-on rather than a core task.

Too often, descriptions merely restate the artefact name. For example, `Cake.Sales` may be described as “A list of cakes sold”, or `[Is non-compliant]` as “True if found non-compliant.” These descriptions do nothing more than take up storage space. At worst, they harm trust by conveying shallowness.

Business descriptions are meaning explanations. They enhance data quality by aligning artefacts to business reality through interpretative context.

Like names, descriptions should be business-centric and written in plain language. But unlike names, they should be substantial.

A good description should explain:

- what business reality is represented;
- how the value was derived;
- what assumptions were made;
- when the artefact is unsafe or limited;
- how it relates to similar concepts.

A column such as `[Is non-compliant]` should describe what non-compliance means in business terms, not merely say “if the result code is `F`.”

Data engineers and stakeholders often slip into using system names as shorthand for business concepts. Descriptions should refer to business entities and business processes, not merely the systems that implement them.

There will be cases where system names or technical implementation details are necessary for transparency. These should be included as supplementary information, not as standalone descriptions.

For example, the description for `[Is non-compliant]` may be:

> True if the transaction failed to meet the minimum regulatory requirements for importation, based on the department’s published compliance criteria. This includes both automatic and manual assessments. Transactions flagged by automated rules are included regardless of whether they were later manually overridden. This column does not include cases where compliance was not assessed. The result code is derived from the `ResultCode` field in the source system, where `F` indicates failure.

The same principle applies to transformation logic. The transformation should be stated in business terms. Technical statements can be included as elaboration, but not as a substitute for meaning.

For example:

> This column is derived from the inspection result and officer notes. It is true if the inspection outcome was `Spoiled cake` or `Not tasty`, and the inspection was conducted by a certified officer. It excludes inspections conducted during training. The logic is implemented in the `InspectionOutcomeFlag` measure using a combination of result codes and officer certification status.

Limitations should also be framed in terms of business interpretation.

“The column can have a null value” is not a useful limitation by itself.

A better statement is:

> The inspector may not record a result if there are no issues. This means it is not possible to distinguish between a successful inspection and an inspection not performed.

Clear statements of limitation are essential for transparency and reliable application of business insight. They tell the user not only what the artefact means, but when it becomes dangerous to rely on it.

## Keys answer: how does this relate?

Database keys include primary keys, foreign keys, and unique keys. They are also metadata.

Names and business descriptions explain artefacts in themselves. Keys explain how artefacts relate to each other.

Relationships are part of meaning. The relationship between one table and another tells the user something about both tables that neither table can say in isolation.

For example, a foreign key between `Cake.Sales` and `Cake.RefProfitability` immediately signals that some sales may be profitable and some may not.

Database keys also help users navigate the database and perform joins. In this sense, database keys serve as a map for the warehouse. Without them, users are left to guess. This is not acceptable.

Primary keys play a special role. As explained in [Mapping the data world](/docs/creating-information/mapping-the-data-world/), the primary key is what links a database record to its real-world business entity. Therefore, primary keys help convey the meaning of a row to the business user.

Each organisation implements keys differently. Some store them only in conceptual diagrams or third-party tools. The disadvantage is that they cannot be easily read or queried.

The best approach is to house them as standalone tables in the warehouse. This makes them visible and open to querying like every other table in the warehouse.

Ultimately, keys are not just technical constraints. They are statements of relationship.

This makes them a non-negotiable part of metadata.

## Metadata should be data

Data without metadata is data without context.

The primary purpose of metadata is not governance, tagging, discoverability, or data exchange. These are all important, but they are secondary effects.

Metadata should be understood in the context of the data engineer’s task: shaping data in light of business intent. From this perspective, the primary purpose of metadata is to add interpretative context that aligns the data world to its underlying business reality.

Without this context, interpretation is left to the user.

That is not merely a documentation gap. It is abandoning the user to guess.

Finally, whether metadata describes names, descriptions, or keys, it should be stored and made available as data.

If metadata carries meaning, it should be available to the systems and users that need meaning.

Instead of recording metadata only in diagrams, specialist tools, or database constructs, it should also be available as tables. Treating metadata as data enhances the ability to distribute it, automate it, and surface it to appropriate tools through APIs.

## Key ideas

> [!NOTE]
> **Key ideas**
>
> Without metadata, everyone is guessing.
>
> Metadata gives data its interpretative context.
>
> Names prevent users from guessing what an artefact is.
>
> Business descriptions prevent users from guessing what an artefact means and when it is unsafe to use.
>
> Keys prevent users from guessing how artefacts relate to each other.
>
> Metadata should be stored and treated as data.