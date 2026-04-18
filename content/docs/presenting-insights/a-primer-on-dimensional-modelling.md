---
title: A primer on dimensional modelling
description: A practical primer on facts, dimensions, and the core building blocks of a Power BI dimensional model, explained through how users interact with them.
lede: Facts and dimensions are best understood through how users interact with them.
weight: 3
draft: true
---

Dimensional modelling is a well-established discipline. Power BI, by contrast, is a more recent technology that brings a new approach to implementing dimensional models. Its unique features allow for a special kind of dimensional modelling that fully supports the classical approach, but permissive enough to break traditional rules when appropriate. New starters often swing between two extremes. On one end, they apply Kimball dimensional modelling techniques too literally in Power BI, resulting in a proliferation of fact tables that makes the model difficult to understand. On the other, they abandon dimensional modelling altogether, allowing Power BI’s flexibility to take over and creating a model that quickly becomes a relationship nightmare. What follows is a practical guide to dimensional modelling as seen through the implementation in Power BI. The aim is to help developers build models that are intuitive and robust. This approach does not contradict traditional dimensional modelling but supplements it.

## Understanding facts and dimensions

Classical dimensional modelling revolves around two core concepts: facts and dimensions. In a technical view,

- Facts are the transactions—the events or activities that occur in the business.

- Dimensions are the reference data —low cardinality tables that provide look-up

of contextual information for the transactions. Fact tables are fast-moving tables. They grow quickly, have high cardinality, and record frequent business activity. Dimension tables are slow-moving tables and usually have a low cardinality. In contrast to the technical view, a business view sees:

- Facts as business processes—these are the verbal nouns and convey action,

such as Manufacture, Order, or Shipping.

- Dimensions as attributes or information—these are the nouns and convey

objects, such as Product, Region, or Customer. While most data engineers are familiar with the technical view, the business view is also essential to building a business-centric dimensional model. In most explanations of Power BI, dimensions are described as filtering facts. This is technically accurate, but it is also helpful to think about it from the users’ experience when they interact with the model. To use an analogy, think of dimensions as levers or switches, and facts as robots or machines. If we think of filtering as a form of control, then:

1. Levers control robots

2. Levers occasionally control other levers

3. Robots occasionally control other robots

4. Robots should never control levers

This analogy helps reinforce a key design principle: interactivity should be driven by dimensions. In the same way that levers are what users control, so the dimensions are the users’ interface to the model. In addition, rather than switches on the robots themselves, they are placed on the controller. In practical terms, this means users should interact with dimensions to drive filtering, not with columns embedded in fact tables (degenerate dimensions). In this primer, we stick with a simpler view of dimensions. In more advanced scenarios, dimensions can be seen as buttons that users click to produce certain effects. The fact tables contain the ingredients to generate those effects. Abstractly, a dimension may even be a set of tables working together, and they do not even need to filter the fact tables, or any table at all. The only criterion is that it operates as a button. If it is something the user interacts with to create a certain effect, then it can qualify as a dimension.

## Elements of a dimensional model

Literature abounds on dimensional modelling. This section does not seek to replace it but reframes the well-understood artefacts of dimensional modelling as a repertoire of building blocks for the data engineer. These blocks allow the data engineer to construct an interactive Power BI model that addresses a range of usage scenarios. The view here is functional, not technical. As elements of a Power BI dimensional model, there are 3 types of facts and 9 types of dimensions. Facts:

1. Measurable fact

2. End-of-period fact

3. Annotation fact

Dimensions:

1. Business dimension

2. Role-playing dimension

3. Combination dimension

4. Choices dimension

5. Sankey dimension

6. Histogram dimension

7. Storytelling dimension

8. Transaction or search dimension, a sub-type being the ID dimension

9. Degenerate dimension

## Facts

Measurable facts are the basic transactions and are what people usually think of when they think of facts. Examples include inspections, sales, and audit events. What makes measurable facts stand out is that they are designed to work with aggregated measures, such as SUMX and COUNTX, and their content are presented via these measures. Measurable facts form the backbone of most analytical models and are the primary source of business metrics. They are the default facts for entity processing scenarios. End-of-period facts capture the state of an entity at the end of each reporting period. An example is the attributes of an employee at the end of each month. They are designed to support end-of-period measures, such as count of employees at the end of the user selected period. End-of-period facts are the default facts for entity tracking scenarios, allowing the model to reflect the evolving state of entities at specific points in time. They can be read in from the end-of-period fragments in the data pipeline. Annotation facts provide additional, finer grain, details of a transactional such as freetext comments for an inspection or certificate details for a product. The reason for moving the additional details to its own fact, rather than leaving them as a degenerate dimension, is when the additional details have a higher cardinality than the transaction itself. For example, one inspection may have many comments. Including them in the business process fact would either force an unwelcome change in grain, or require the use of string concatenation. When neither option is desirable, the annotation fact is the right solution. Annotation facts hang off another fact by being in a child relationship with it. The information in an annotation fact is designed for display rather than for aggregation. The typical usage scenario is one where the business user has arrived at a set of transaction records through a dimension and would like to see additional details about that transaction. This is also why they are filtered through another fact, not a dimension.

In general, the relationship would be many-to-many. For example, an Inspection fact table may have multiple inspection results. On the other hand, one inspection may have multiple comments which are represented by the ‘Inspection comments’ annotation fact. These both relate to the inspection itself, the relationship would be many-to-many on [Inspection SK]. Annotations are one of the rare cases where bidirectional filtering and fact-to-fact filtering is advisable. This relationship setup is not problematic because annotation facts sit at the tail end of a filtering path and thus pose limited usability issues. Since they are not usually aggregated, they also pose no performance problems. > [!NOTE]
> TODO: Insert manuscript screenshot or diagram from the source draft. Often, a measure is still needed to display the additional details in a controlled way. For example, the SELECTEDVALUE function can ensure that additional details are only shown when a primary key value, the full key or parts thereof, for a transaction is used. In linguistics, an adjunct noun is a noun that functions as an adjective to describe another noun, such as vegetable in vegetable soup. In this sense, an annotation fact is an adjunct fact.

## Dimensions

Business dimensions are the common dimensions that most people think of when thinking of dimensions. Examples include processing statuses, locations, officers, inspection types. They are usually available out-of-the-box from source systems, though they may be supplemented with additional useful columns by the data engineer. These dimensions are necessary for presenting basic information and form the foundation of most models. Role-playing dimensions are dimensions that have different meanings depending on the facts they filter. Technically, a role-playing dimension can be identified through a primary key that links to multiple different foreign keys. For example, a reporting calendar may filter on three facts — Manufacture, Order, and Shipping — simultaneously. It is visible as a role-playing dimension if the foreign key columns — [Manufacture date], [Order date], [Shipping date] — are different columns. However, if the calendar filters on the same foreign key, for example [Manufacture date] on all three facts via inheritance of information, then the calendar is not a role-playing dimension. In this case, the calendar always means the manufacture date. Role-playing dimensions are important when comparing multiple measures against the same reference point, such as calendar or staff. The hover text description for a roleplaying dimension should clarify the meaning it takes in the different scenarios it can play.

A combination dimension is a set of binary columns that describe whether a business entity exhibits one or more similar properties. The presence of multiple flags allows the model to express combinations of these properties. A simple example is a ColourFilterCombination dimension with the columns:

- [Has red filter]

- [Has blue filter]

- [Has yellow filter]

This structure allows the model to represent entities that have any combination of these colours. Some business entities, especially in complex organisations, may have more than one digital system touchpoint. In this scenario, business users are often interested in which systems the business entity was processed through. A SystemCombination dimension with the binary columns [System A], [System B], and [System C] will easily support this scenario. The combination dimension is particularly useful when a business entity may carry multiple types in its details. For instance, a cargo may contain line items. Some are fresh produce, and some are inanimate goods. A combination dimension would express this as:

- [Has fresh produce]

- [Has inanimate cargo]

From these base flags, the data engineer may derive additional columns such as:

- [Has mixed cargo] — a computed flag indicating the presence of both types.

These derived columns are not part of the combination itself but are logical consequences of it. They are useful for storytelling, filtering, and simplifying measure definitions. The key benefit of this use is that it aggregates detail-level complexity back to the entity level, avoiding grain expansion and preventing double-counting. Choices dimensions are multi-valued dimensions of low cardinality. They are like combination dimensions but differ in intent. The business is interested in whether the entity has any of the attributes, such as in multi-select scenarios. Choices dimensions are particularly useful when the number of possibilities exceeds ten or more. A use case is displaying data quality issues. For example, if a transaction row has multiple problems — missing date field, missing officer name, etc — then a choices dimension allows users to display on transaction rows that have any of the issues.

Physically, choice dimensions are created through taking all possible choices of a finite list and then assigning each set of choice with a group number. The relationship is between the fact and the dimension is on this group number. > [!NOTE]
> TODO: Insert manuscript screenshot or diagram from the source draft. Choice dimension takes advantage of Power BI’s ease at handling many-to-many relationships. Like the combination dimension, it allows the data engineer to work push information back to the entity of interest level. Without this dimension, joining any information to the choices would require changing the grain of the original information. This can create an unwieldy output. By using the choice dimension, the desired information can propagate conveniently to all business processes without changing the grain of any of the interim output. Choice and combination dimensions are closely related. Combination dimensions are ideal for expressing and logic; choices dimensions are ideal for expressing or logic. In addition, the data engineer can create a choices dimension by in pivoting a combination dimension and discarding empty values. For example, the SystemCombination dimension with columns [System A], [System B], and [System C] can be unpivoted to create a System dimension with column [System touch point] with values "System A", "System B" and "System C." Depending on the scenario, the business may be interested in seeing records that involve a combination of systems to process a business entity (combination dimension), or seeing records that require any of the system (choice dimension). > [!NOTE]
> TODO: Insert manuscript screenshot or diagram from the source draft. Thus, a data engineer can always build both in the data pipeline and use one or the other, or both, in the dimensional model as needed. A Sankey dimension is used to represent possible paths through a series of sequential checkpoints. Suppose there is a business process with a list of checkpoints which are sequential, but some are optional. Consider all the possible paths through these checkpoints, and designate them with a number "Path ID." A Sankey dimension is a table with three columns [Path ID], [From checkpoint], and [To checkpoint] where each row is an edge in this path. For example, a helpdesk may have escalation points ranging from Tier 1 to Tier 3. There are 7 possible pathways depending on whether a case reached any of the checkpoints. The Sankey dimension is a table of all possible transition from tier to tier. A starting row may be necessary to illustrate the entry point for every path. The table would then be:

Path ID From checkpoint To checkpoint 1 Start Tier 1 2 Start Tier 2 3 Start Tier 3 4 Start Tier 1 4 Tier 1 Tier 2 5 Start Tier 1 5 Tier 1 Tier 3 6 Start Tier 2 6 Tier 2 Tier 3 7 Start Tier 1 7 Tier 1 Tier 2 7 Tier 2 Tier 3 This dimension is perfect for creating flow diagrams without tampering with the grain of the fact tables. A case in the help desk must go through one of these seven possible journeys, and thus have an associated [Path ID] value. This case in the fact table can relate to the dimension on [Path ID]. Like the choice dimension, it is a many-to-many dimension. > [!NOTE]
> TODO: Insert manuscript screenshot or diagram from the source draft. In practice, a Sankey dimension can be created through a combination dimension, and then unpivoting the checkpoint columns, and then calculating a LEAD() to bring in the next checkpoint ordered by the sequence. Computationally, this can become unmanageable if the number of checkpoints grow quickly. > [!NOTE]
> TODO: Insert manuscript screenshot or diagram from the source draft. Histogram dimensions are used when it is necessary to filter the model by a numeric value. For example, finding the number of helpdesk cases that take more than 3 days to resolve. Measures such as [Total days to process] cannot be used because measures

do not work as normal filters in Power BI. Instead, the numeric value needs to be expressed as a dimension. A histogram dimension is table of values that span a range of numeric in incremental steps. This range can be absolute numbers moving in even steps, such as integers from

-100 to 100 in steps of 0.5, or it can be expressed as band of numbers, such as 0 to 10,

11 to 20, …, 91 to 100. This dimension map to the fact tables on the numeric value and thus translates them to a dimension for interaction. Care must be taken on the boundary steps to ensure correct assignment, especially on the maximum and minimum. An additional display column may be necessary for cases such as "Greater than 100" and "Less than -100". As well as allowing the user to filter the model on a numeric value, the dimension is useful for creating histogram visuals – hence the name. This chart is perfect for visualising time-to-process metrics by counting the number of entities against a dimension of days or hours to process. Storytelling dimensions are covered in detail in the Storytelling chapter. They are artificial dimensions that narrate the journey of an entity through business processes. Like combination dimensions, their distinction from a typical junk dimension lies in semantics, not syntax. A storytelling dimension is created when the data engineer steps back from the raw data and envisions afresh what the business perspective looks like. The engineer then categorises all entities of interest into a finite list of journeys that reflect how those entities move through the business process. In the context of a self-service model, storytelling dimensions play a powerful role. They act as the first portal into the data, dividing all entities into manageable strata and initiating the process of drillthrough and closer examination. A close equivalent in traditional modelling is the "transaction profile dimension." Transaction dimensions are high-cardinality dimensions where each transaction row is a dimension value — that is, the dimension is the transaction itself. Their primary purpose is to allow drillthrough or cross-filtering of a single transaction across multiple business processes within a system. They are important because some high cardinality attributes are useful for comparison across multiple processes but do not easily normalise into standalone dimension due to its high cardinality. An important special case of a transaction dimension is the ID dimension. By design, a transaction dimension must include the primary key of the transaction to identify it. An ID dimension is one where the dimension contains only the primary key and almost nothing else, perhaps it includes a [Version number] column. Such a dimension allows a business user to quickly retrieve any information from the model using a known

business key. ID dimensions play a prominent role in Power BI because of its built-in interactivity. In traditional dimensional modelling, they would be the exception rather than the rule. In Power BI, this becomes the reverse. A more general view is to treat these as search dimensions. A search dimension is a high-cardinality dimension that supports searching business processes through a highcardinality value. For instance, the free-text description of mail packages may be used as a dimension that allows users to search business processes based on that text. In this case, the search dimension corresponds to the annotation fact. When the business objective is to search through a free-text field, it is best implemented as a search dimension. If the user is not expecting to search using the field, but simply wants to display supplementary information, then it is better implemented as an annotation fact. Transaction dimensions add significantly to model size and are not ideal for aggregation. This is why their primary purpose is searching and cross-filtering, not aggregation. Due to Power BI’s filtering behaviour, transaction dimensions need to be used in conjunction with a unit-record display measure. This is explained in the Filtering behaviour and Managing measures chapters. Degenerate dimensions occur when an attribute used for filtering or aggregation is retained within a fact table, rather than being elevated to a standalone dimension. This typically occurs for one of two reasons:

- The attribute lacks sufficient business weight to justify its own dimension.

- The attribute has a high cardinality, making it computationally expensive to be a

dimension. Despite these pressures, degenerate dimensions are best avoided because they violate the natural filtering paradigm of dimensional modelling in Power BI, where dimensions filter facts and not the reverse. Retaining such attributes in fact tables can complicate user interaction and introduce undesired filtering behaviour. It also signals a failure to properly articulate business meaning when the column actually deserves to be its own dimension but is not. If the attribute must be retained for display or cross-filtering, a transaction dimension may be preferable.

## Conclusion

One common theme of this chapter is to push information back from lower-grain than the entity, back to the entity level, and then further abstracted to the dimension. The combination, choice and Sankey dimensions all follow this pattern. They take detail-
