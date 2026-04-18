---
title: Quality metadata
weight: 2
draft: true
---

Data quality issues reflect the gap between the business world and the data world. In this view, metadata is not merely documentation for the next person working with the data. It is an indispensable tool for bridging that gap by adding the interpretative context that connects the user to the business reality behind the data. If a column in the source system is called [Valid], renaming it to [Is current name] is not the difference between "having metadata standards" and "not having metadata standards" — it is the difference between comprehensible and incomprehensible data. This bears stressing. Quality metadata adds value in a way that no other technique can. Metadata is also the first impression for any user engaging with the data engineer’s product. It is the first step to trust. It can determine whether a user engages with the product or walks away. Creating quality metadata is not difficult. Compared with the technical demands of data engineering, metadata is perhaps the easiest. All it takes is for the data engineer to ask: "What does this look like to the user? If I were the user, is this something I would want for myself?" Importantly, metadata is not an add-on task. It is part of the modelling task itself that starts with exploratory analysis. In complex cases, starting with metadata is a useful step for laying out the logic in plain language before implementation. A mature data engineer will acquire the habit of writing metadata first, not last. This section covers three aspects of metadata:

- Names

- Business descriptions

- Database keys

## Names

Each site will have its own naming conventions. This chapter is not about defining a specific naming convention, but on universal principles that should be observed in all naming conventions. Names apply to schema, tables, columns, Power BI models, measures, calculation groups, and display folders. In every instance, names should be business centric and plain language. They must not use idiosyncratic acronyms or abbreviations for the developer’s convenience. There

are no justifications for using [Employee cnt] when the meaning is [Employee count]. If the infrastructure supports spaces in column names, they should be used. Names should contain helpful signals. For example, "Is" and "Has" can be used to indicate binary columns, such as [Is non-compliant]. Columns ending with "date" and "datetime" should respectively hint at their precision. Tables starting with Ref indicate a reference table. These signals should not come at the cost of readability. This is why a Power BI dimensional model should not prefix tables with "dim" or "fact." Naming conventions should be consistent across the schema, the database, and the warehouse where possible. Consistency in prefixes, suffixes, casing, and syntax creates a design language for the warehouse. Just as Apple or Google products use consistent icons and layouts to create a seamless experience, a warehouse that speaks a consistent language empowers users. In consistent naming conventions, the data engineer should pay particular attention to conforming concepts. This means that when a data engineer uses a name, it is important to check whether the concept is already named differently and shared by other domains. For example, when adding Cake.RefQualityControl, it is important to check whether RefTesting, RefAudit, or RefInspection are being used to mean the same thing. If so, it is worth reusing an existing name. Consistency applies to all aspects of the name — capitalisation, syntax, semantics. It is better to stick with [Sales date] and [Inspection date] or [Date of sales] and [Date of inspection] and not switch from one to another haphazardly. Names should be explicit and unambiguous. An explicit column name means using [Inspection first of month] rather than [First of month]. An unambiguous name means ensuring the word has only one meaning for the user. For example, does [Last inspection date] mean "previous inspection date" or "the final inspection date"? Does "restricted" mean "less" or "privileged"? Special attention should be paid to words that are both nouns and verbs. They are particularly prone to misinterpretation. An extension of explicit and unambiguous names is for them to be standalone. Data tables and columns can often be taken out of context. For key concepts, it could be worthwhile to make them carry their own context. For example, [Is non-compliant] may be better as [Is financially non-compliant]. This may involve repeating the table name into the column name. Another extension of explicit and unambiguous names is avoiding generic filler words. The words "type", "group", "summary", and "details" are often used by developers without any meaning, much like "ahs" and "umms" in a sentence. These tend to obscure rather than clarify. For example, if a table is called "summary", it should be

renamed to reflect what is being summarised. And "details" should be avoided unless it is truly a finer grain expansion of a header row. In choosing names, the data engineer faces the tension between explicit accuracy and succinctness. Sometimes an overly verbose name is not aesthetically pleasing in a report visual. When in doubt, the data engineer should err on the side of explicit because it is easier to shorten a name in Power BI visual than for a user to creatively extend it. These principles apply just as much to code. Temporary tables and CTEs should be named with business meaning, not cryptic abbreviations like tmp. In complex code, column renaming should happen early, on first contact, and persist throughout during transformation. This practice promotes clarity and readability. As the Zen of Python says: Readability counts. The following is an example of naming conventions for prefixes for inspiration:

- Earliest / Latest when referring to timed events or versioning. For example, the

earliest activity date and the latest activity date, or the latest version. Do not use last when one means latest.

- First / Last when enumerating sequences such as 1, 2, 3. Beware that last can be

confused with previous. Use final if acceptable.

- Before / After when emphasising a transition in time. Such as in an audit table of

column value changes, use [Before value] and [After value].

- Previous / Next when referring to consecutive sequences. In the context of code,

not for presentation, self can be used for the current context.

- Primary / Secondary when emphasising importance. For example, the [Primary

supplier] if a shipment of goods has multiple suppliers, or the [Secondary supplier] if there were more than one.

- Start datetime / End datetime when referring to periods, such as in slowly

changing dimensions or referring to statuses. Avoid having one in a table but not the other.

- Creation / Update / Delete when referring to records, such as [Creation date],

[Creation user], [Update user], [Delete datetime]. In source systems there are often markcolumns such as [Last updated] and [Last updated by]. These should standardise to [Update datetime], [Update user ID].

- Current / Historical when referring to records that have changing validity.

Usually, the current record is the one where the end datetime is in the future, such as ‘9999-12-31’, and historical for those end-dated. Do not use history to

2. Transformation logic, including assumptions

refer generically. For example, do not call a table Cake.SalesHistory if it suffices to say Cake.Sales. As a rule of thumb, current/historical should be used for mutable records, and not for immutable records.

## Business description

Business descriptions are frequently overlooked by data engineers as an add-on rather than a core task. Too often, they merely restate the artefact name — describing Cake.Sales as "A list of cakes sold" or [Is non-compliant] as "True if found noncompliant." These descriptions do nothing more than take up storage space. More often, they frustrate users who navigate to the description expecting clarity, only to find something unhelpful. At worst, they harm trust by conveying shallowness. Instead, business descriptions are meaning explanations. They enhance data quality by aligning artefacts to business realities through interpretative context. Like names, descriptions should be business-centric and written in plain language. But unlike names, they should be substantial. A good description should focus on:

1. Business realities

3. Limitations

4. Linkages and comparisons with related concepts

Business realities, rather than technical notes, should be the focus of descriptions. For example, a column like [Is non-compliant] should describe what non-compliance means in business terms, not "if the result code is ‘F’." Data engineers, as well as stakeholders, often slip into using system names as shorthand for business concepts. This is not preferred. Descriptions should refer to business entities and business processes, not the systems that implement them. For example, instead of "Salesforce" or "SAP," use "health care record" or "employee registration." There will be cases where system names or technical implementation details are necessary for transparency. These should be included as supplementary information — not as standalone descriptions. For example, the description for [Is non-compliant] may be: "True if the transaction failed to meet the minimum regulatory requirements for importation, based on the department’s published compliance criteria. This includes both automatic and manual assessments. Transactions flagged by automated rules are included regardless of whether they were later manually overridden. This column does not include cases where compliance was not assessed. The result code is derived from the ResultCode field in the source system, where 'F' indicates failure."

Transformation logic is the heart of a data pipeline. Describing the transformation logic and any important assumptions is necessary for transparency and trust. This is especially important for complex or fuzzy logic. The same principles apply. The transformation should be stated in business terms. Technical statements can be included as elaboration, but not as a substitute for meaning. For example: "This column is derived from the inspection result and officer notes. It is true if the inspection outcome was ‘Spoiled cake’ or ‘Not tasty’, and the inspection was conducted by a certified officer. It excludes inspections conducted during training. The logic is implemented in the InspectionOutcomeFlag measure using a combination of result codes and officer certification status." Transformation logic can include lineage from data sources where relevant. Limitations, should similarly be framed in terms of business interpretation. "The column can have a null value" is not a limitation. A better statement is: "The inspector may not record a result if there are no issues. This means it is not possible to distinguish between a successful inspection and an inspection not performed." Clear statements of limitation are essential for transparency and reliable application of business insight. Linkages and comparisons are often valuable for users exploring complex business processes. Where relevant, pointing out related concepts in descriptions can be tremendously helpful for users navigating the warehouse. These are akin to the "Related links" in an encyclopaedic website. In terms of storage, if the same description applies in multiple places, it should be included in the reference table, not the transaction table. Reference tables are the carrier of meaning and the user’s primary interface to the model. Of special importance are storytelling dimensions, which should have the richest and most articulate descriptions to capture the complex logic they encapsulate. Descriptions on database artefacts — tables, columns, measures — will inevitably be piecemeal. Therefore, standalone documentation is also necessary to provide an endto-end view of the business problem and its data model.

## Database keys

Database keys include primary keys, foreign keys, and unique keys. They, too, are metadata. While names and business description explain artefacts in and of themselves, keys are necessary to explain how they relate to each other. First, relationships are part of meaning. The relationship of a table with another table tells the user something about both tables that neither one can in isolation. For example, a foreign key between Cake.Sales and Cake.RefProfitability immediately signals the idea that some sales may be profitable and some are not. Second, database keys help users navigate the database and perform joins. In this sense, database keys serve as a map for the warehouse. Without them, users are left to guess. This is not acceptable. Third, primary keys play a special role. As explained in [Mapping the data world](/docs/creating-information/mapping-the-data-world/), the primary key is what links a database record to its real-world business entity. Therefore, they are necessary to convey the meaning of a row to the business user. In addition, primary keys are the foundation for fault tolerance and change detection. They allow the data engineer to identify duplicates, track changes, and implement incremental loads. These techniques are covered in [Fault tolerance](/docs/quality-reliability/fault-tolerance/) and [Load mechanics](/docs/efficient-stable-pipeline/load-mechanics/). There are cases where primary keys are difficult to define. If the answer is "each row is a new entity," such as in a log table, the data engineer can still express this with an increasing integer and load incrementally. In other cases, the grain of the fact table may be unclear or difficult to compute, especially when business centricity requires compacting several grains into one fact table for presentation. Even so, it is worth the effort of computing a key if possible. Each organisation implements keys differently. Some store them only in conceptual diagrams or third-party tools. The disadvantage is that they cannot be easily read or queried. The best approach is to house them as standalone tables in the warehouse. This makes them visible and open to querying like every other table in the warehouse. In other words, metadata should be stored and treated as data. Ultimately, keys are not just technical constraints. They are statements of relationship. This makes them a non-negotiable part of metadata.

## Conclusion

Data without metadata is data without context. Consequently, the primary purpose of metadata is not governance, tagging, discoverability, or data exchange. These are all important, but they are secondary effects.

Instead, metadata should be seen in the context of the data engineer’s task is to shape data in light of business interest. From this perspective, the primary purpose of metadata is to add interpretative context that aligns the data world to its underlying business realities. Without this context, interpretation is left to the user who must fill in the gap by guesswork. When the user must guess, the data engineer has failed to shape the data to meet business interest. Quality metadata is not difficult to do. It comes naturally with the habit of looking at the product from the user’s perspective, and a taste for the satisfaction that comes from articulate writing. Finally, whether it be names, descriptions or keys, metadata should be stored and available as data. Instead of recording them in diagrams, specialist tools, or database constructs alone, they need to be available as tables. Treating metadata as data enhances the ability to distribute them, perform automation, or surface to appropriate tools using APIs. This maximises the impact of metadata. Large language models are also adept at reasoning with such structures and putting them to good use. Creating standalone names makes it easier for large language models to reason correctly on top of metadata.
