---
title: A good dimensional model
weight: 2
draft: true
---

A data engineer can become familiar with what a good dimensional model in Power BI should look like through two aspects: the expectations and indicators.

## Expectations

A good dimensional model in Power BI should:

- Resonate with the business view

- Be intuitive and unambiguous – it should "just work"

- Anticipate questions

- Be both high-level and detailed

- Be performant to use

## Resonate with the business view

While the data engineer must always focus on expressiveness, nowhere is this more critical than in the dimensional model. In some cases, technically correct representations may need to give way to what better reflects how the business sees the world. For example, relaxing strict grain consistency may allow a model to align more closely with business understanding, rather than having a proliferation of objects that are technically correct but hard to understand. Resonance begins with naming. Models, tables, columns, and measures should use language that is immediately meaningful to the business. This may require creating perspectives the business has not yet articulated. Familiarity can often lead business areas to miss insights; the data engineer, working across domains, is well-placed to offer a fresh view. Metadata plays a key role. Descriptions should speak the business language, clearly state the intent, and for complex cases, include elaboration in near-pseudocode using business terms.

## Be intuitive and unambiguous

As a self-service data model, the user is expecting to drag-and-drop to get answers. For this purpose, the model should just work. If the user must memorise complex technical filtering rules, or memorise a map of the model relationships to get the correct answer, then the model is not intuitive. If the user has to stop and think, or second-guess the logic of the model, then something is wrong. An intuitive model means that the user should be able to operate it without a heavy manual. It should behave in a way that matches expectation with no hassle. A related phenomenon is ambiguity. An ambiguous model means that there are apparently multiple ways of getting the same information, or the same information being open to interpretation. As an example of the former, this could be when a column has been denormalised into multiple fact tables, leaving the user unsure which one to

use for a particular query. As an example of the latter, it could be because a column name such as [Calendar date] is too generic, and it’s not clear which business date the column refers to. An unambiguous model means that the user has only one obvious way of answering a question. The model should either answer it accurately or make it apparent that it cannot.

## Anticipate questions

A good model does not merely satisfy the initial requirements. It anticipates the full range of reasonable business questions. This requires the data engineer to think beyond the immediate requirements and consider all the questions that the model may need to answer over time. There is no way to hide from this reality. If the question is not answered now, at some point, a business area will come back and ask for the question to be answered later. In practice, what this means is that either a business process is out of the model, or if it is included, then all information captured by that process should be accessible in a format to meet the expected usage scenario. Achieving this is much easier than it sounds, and is the subject of the chapter Anticipating questions.

## Be both high-level and detailed

One of the most powerful features of Power BI is the ability for users to interactively move through the data by cross-filtering and drill-through. This invites a natural behaviour where users start at the high-level view, and if something catches their attention, they drill into the details to see exactly what happened. This is an integral part of how users build trust in the model through examining detailed records. Equally, users who operate at the detailed level often start at the transactions for the purposes of troubleshooting, but will eventually want to zoom out in search of broader patterns. This zooming out is a sign of trust and maturity. A data engineer cannot ignore this reality of both satisfying both the high-level and detailed views. While reports and specific queries may have one or the other view, there are many cases where the underlying model must support both.

## Be performant to use

Most queries should return in under a second. Complex or infrequent queries should complete in under two seconds. Longer runtimes are acceptable only in rare cases. Performance is not merely a user-experience consideration. It is a symptom of underlying issues to do with information articulation. A slow model often indicates that

key information has not been pre-computed so that the model must compensate with work at query time. Thus, a slow model may be a concern of business expressiveness.

## Indicators

The following are indicators of a good dimensional model in Power BI. Unlike the expectations, which describe what a model should achieve, indicators reveal whether those qualities are present in practice. They are not all mandatory and occasionally may be violated. However, a good dimensional model should have a strong presence of these indicators. Their absence or frequent violation would hint at a model that is difficult to use. The indicators can be categorised in aspects:

- Names and metadata

- Dimensions

- Facts and measures

- Relationships

## Names and metadata

All names should be business-centric rather than system-centric. It is a common mistake for data engineers to use acronyms or terms that refer to the digital system rather than the business content itself. This should be avoided unless the information to be presented is intentionally about the system itself. Names should not be technical. Terms such as "dim," "fact," or "bridge" should not appear in visible names. These are implementation details and do not reflect business meaning. Names should be explicit. For example, rather than [Date], it is better to use [Sales date]. It may be necessary to repeat the table name in the column name, such as Sales[Date] to Sales[Sales date]. This is useful for clarity but also because the column name is the one that appears in the report visual rather than the table name. Visible names should not repeat across the model. When a user searches a name in the field list, it should return only one result. If a column appears more than once, it presents an immediate ambiguity. If the columns are actually the same but all of them need to be visible to the user, this indicates the model needs to be reworked to resolve duplication of information. If they are different columns but using the same name by accident, then the columns need to be renamed for clarity rather than relying on the table context for resolution. Dimensions represent information or attributes, while facts the business processes. As such, dimensions should be nouns and business process facts should be verbal nouns, or contain a sense of action. For example, in a business system with three processes, manufacture, order, and shipping may have facts called Manufacture, Order, and

Shipping. The dimensions may be called Product, Region, Manufacture date, Order date, and Shipping date. Thus, the facts are the names of the business processes, while the dimensions are attributes that the business processes capture. Naming the facts after the business process is harder to do than to say. It requires a laser focus on the business intent, and familiarity with Power BI functionality to design a model with this simplicity. A common case is the transaction and reference table pair, such as Sales and RefSales. One approach is to use Sales as the fact name and use Sales description as the dimension. Finally, a strong indicator of a good dimensional model is the presence of rich, business-centric descriptions in the hover text of tables, columns, and measures.

## Dimensions

In Power BI, dimensions are the window through which the user interacts with the model. A good dimensional model consciously focuses on dimensions as the user’s point of access. They are the biggest influence on the model’s "look and feel. " On a surface level, dimension table names should be nouns that convey the type of information available to the user. Dimensions should have a reasonable number of columns—approximately 5 to 10. There can be more columns if some of them are simple derivation of the others. For example, text versions of binary flags. Too few columns in a dimension mean that it carries too narrow a business meaning. For example, a dimension called Gender with a single column [Gender] has too few columns. A large number of dimensions with few columns represent a fragmented, rather than a consolidated, view of the business. It may be appropriate to combine Gender with a few other dimensions to form a Demographic dimension. Too few columns may also point to a lack of helpful attributes. For example, the Gender table should at least have a [Gender display order] to sort the values in [Gender] in a useful way. On the other hand, too many columns in a dimension suggest a grouping of attributes that is too complicated and may overwhelm users. It also reflects a view of the business that is insufficiently nuanced. In this case, the dimension may need to be broken down into a few more manageable dimensions. A dimensional model often includes two special types of dimensions that indicate a thoughtful design. The first is the ID dimension. It is a table of the primary keys of the business process. This table allows users to retrieve all the detailed transactions for any business entity by looking up a familiar business key. The second is the storytelling dimension. It sits at the opposite end of the spectrum. As explained in the Storytelling chapter, the storytelling dimension categorises all business entities into a digestible

number of journeys. This provides the best possible high-level portal for users who take a zoomed-out view. The presence of both ID dimensions and storytelling dimensions is an indicator that the data engineer has covered the broad range of needs the data engineer is expected to meet. While it is not a guarantee of quality, it is a good rule-of-thumb for initial assessment. The full set of useful dimensions are in the chapter A primer of dimensional modelling.

## Facts and measures

Power BI is designed such that the primary way of interacting with the data is through dimensions and measures rather than facts. This is explained in greater depth in Filtering behaviour. For now, it suffices to note that an indicator of a good Power BI dimensional model is a reduced prominence of the fact tables. In the ideal case, all fact tables are hidden from the user. A related indicator is the absence of, or at least limited use of, degenerate dimensions in fact tables. A proliferation of degenerate dimensions suggests the model is working against the inherent nature of Power BI to propagate filters. It also indicates that certain business information are left as miscellaneous attributes of the business processes instead of being articulated as standalone properties that deserves a dimension table. Measures play a more prominent role that corresponds to the diminished role of fact tables. An indicator of a good dimensional model is one that invests heavily in measures. A rough rule-of-thumb is that each fact table, representing a business process, should have at least ten measures. This simply reflects that there are usually at least ten metrics to understand a business process. For instance, a process such as sales would have measures for sales volume, turnaround time, profit, and cost. If a model has implemented the concept of "good" and "bad", this leads to sub-measures for individual categories. In addition, there will be measures for percentages and other derivatives. This rapidly adds up to more than ten. If a user can easily grab-and-go to use measures with minimal effort to arrive at desired answers, then it is an indicator of a good model. It shows that the data engineer has thought deeply about the business processes and is able to put the necessary information at the user’s fingertips. Conversely, the of lack ready-to-use measures mean that the data engineer has not sufficiently engaged with the business interest of the user. When there are many measures in a model, it can become unwieldy. Good measure management places all measures into a single table at the top of the field list. A suitable name for this table is simply Measure. Power BI promotes this behaviour. If all

columns in a table are hidden and it contains at least one measure, Power BI places this table at the top. This indicates a model that elevates measures to first-class. The measures in the measure table should be organised by display folders. By default, folders should be grouped by business process. For example, a business system with the processes Manufacture, Order, and Shipping can have at least three folders: "Manufacture", "Order", and "Shipping." > [!NOTE]
> TODO: Insert manuscript screenshot or diagram from the source draft. The prominence of measures, their business-centricity, and their organisation through business processes are strong contributors to the look and feel of a good data model.

## Relationships

Relationships in a Power BI model define user interactivity. Following the theme of using dimensions as the main point of interaction, dimensions should filter facts and not the other way around. An indicator of a good dimensional model is that if a piece of information is known to a business process, then the dimension representing that information should filter the corresponding fact. For example, in a business system with Manufacture, Order, and Shipping (in that order, and recorded at the unit level), the Product dimension should filter all three facts because all those processes know about the product. On the other hand, the Shipping date should filter only the Shipping fact. It should filter neither Order nor Manufacture because only the shipping process knows the shipping date but not the earlier processes. This does not mean that each business process is filtered only by its own attributes. For example, all fact tables should be filtered by the Manufacture date, because the shipment tracks back to the order, which tracks back to the manufacture, and therefore all processes know about the manufacture. The criterion is whether the information can be reasonably related to the business process at the time. Relationships are explored in greater depth in Anticipating questions. Since dimensions are the user’s access point to the model, the column on the filtered side of the relationship (fact) is always hidden to avoid ambiguity. Instead, the column on the filtering side (dimension) is used.

## Conclusion

This chapter focuses on sketching out what a good dimensional model looks like. The purpose is not to provide a definitive checklist that guarantees quality, but to attune the data engineer to the look and feel of a good model in Power BI by putting the engineer in the perspective of the user. While a list of indicators is helpful, the best test is for the data engineer to actively test the model personally from the perspective of the user, trying a range of business questions to ask. This is part of conducting visual checks.

This task requires a deep familiarity with the business and a strong curiosity of the subject matter, rather than an attitude of ticking off a set of formal requirements. The common theme behind the indicators is business centricity and intuitive use. An intuitive model is achieved through explicit implementation of answers that pop out, and does not require the user to interpret or guess. The data engineer achieves this by crafting the dimensions and providing a rich set of measures in the model. The Zen of Python is a good guide to designing a dimensional model. Its emphasis on explicit over implicit, and on having one—and preferably only one—way of doing something, applies directly to designing a model in Power BI.
