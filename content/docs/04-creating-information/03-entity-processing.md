---
title: Entity processing
url: /docs/creating-information/entity-processing/
description: Shows how immutable business entities are processed through filter, map, and reduce passes to create reusable information.
lede: Immutable entities are processed into reusable information by clarifying keys, mapping business meaning, and reducing detail to insight.
weight: 3
draft: true
---

The most common pattern in data engineering work is that of entity processing. This applies to immutable business entities, those that do not change once created. Examples of immutable entities include a sales order, a bank transfer, or an import declaration. If they do change, it would be considered sufficiently different that it is a different entity. For immutable entities, the business objective is to process them according to defined business logic, hence the term entity processing.

Immutable entities often share certain characteristics:

- **Versions:** Each version can be considered a new entity and the latest one replaces all others as the “correct” version.
- **Header and details structure:** The header represents the main entity and the details represent its components. An example would be a sales order and the line items within the order.
- **Subprocesses:** Multiple business processes are often needed to fully complete the business activities on the entity.
- **Good or bad:** Immutable entities often come with a concept of “good” or “bad” entities, as in the case of customer sentiment, fraudulent transactions, or non-compliant import of goods.
- **Actors:** There may be actors who persist over time and over multiple immutable entities, such as a customer making multiple purchases over time.

The pattern of entity processing is suited to working with immutable entities. The usual goals of the entity processing pattern are to:

- Obtain insights about the entities from underlying processes.
- Identify macro-level trends on the business entities such as the level of sales per region.
- Measure the time to reach process milestones defined by the business.
- Provide drill-through to information about specific events that took place, usually to troubleshoot problems or identify the root cause of bad entities.
- Provide a foundation for predictive analytics by identifying attributes that may be indicative of bad entities.
- Provide a basis for understanding the actors and how their behaviour affects business outcomes.

The first task is to identify the entity of interest. Most often this entity is clear. Sometimes the entity of interest can be hard to identify. A sale transaction may have multiple line items. Depending on the nature of the business, the entire transaction may be the entity of interest, or the line items themselves would be the preferred entity of interest. The lens to adopt is determined by what makes sense for business action.

Once the entity of interest is identified, the data engineer’s aim is to tell the high-level story about that entity while maintaining all the necessary detail. Fragment modelling is especially suited to this task because information about different aspects can be maintained in different fragments.

## Building the pipeline

A data engineer building a pipeline for entity processing can follow three broad steps:

- Filter — remove irrelevant data and focus on the minimum blocks of information
- Map — compute reusable blocks of information
- Reduce — aggregate to the level required for analysis

### First pass — Filter

In this first pass, the data engineer works predominantly with incoming raw data. The aim is to establish structure and meaning, starting with the identification of keys. The first pass itself has three stages: identifying the key, defining reference tables, and extracting transactions.

#### Identifying keys

The first task is to identify the business keys that serve as primary keys to the raw data. These may be defined as database constraints in the source data, or they may need to be inferred through exploratory analysis. Defining primary and foreign keys is a simple but powerful way to bridge the gap between the data world and the business world.

In some cases, key columns may need to be created. For immutable entities, there are two common scenarios: versioning and sequence numbers.

In versioning, a typical application might use a column like `[Sales ID]` and another like `[Previous sales ID]` to indicate that one record replaces another. A clearer approach is to introduce `[Original sales ID]` and `[Sales version number]`, using partitioning and ordering to establish lineage. The original `[Sales ID]` can still be retained for joins but should be renamed to `[Sales version ID]`.

In header-detail structures, it is common for detail rows to be stored as simple lists. For example, a `[Sales ID]` may be associated with multiple `[Sales item ID]` entries. It may be appropriate to introduce a `[Sales item sequence number]` to clarify the relationship between the order and its line items.

Keys do not need to be enforced as physical constraints. It suffices to store them in separate metadata tables. What matters is that they communicate meaning and can be looked up by consumers of the data.

#### Define reference tables

Reference tables are small, slow-moving, descriptive tables that describe the content of larger, fast-moving transaction tables. Examples include `RefProduct`, which describes the products being sold, and `RefLocation`, which describes the store where the sale occurred.

Reference tables are important because they are:

- **Expressive** — they provide a central place to describe the attributes of a business entity, rather than embedding all information in the transaction table.
- **Efficient** — updates can be made to a small reference table rather than to large volumes of transaction data.

The data engineer can use reference tables from source systems for inspiration, but should not be limited by them. Application reference tables are often designed to support system functionality, not business insight. There are several ways to add value and make reference data more expressive:

- Rename incoming tables and columns to reflect business intent.
- Combine fragmented application reference tables when that better clarifies the business concept.
- Create new reference tables from scratch for analytical use.
- Add default rows such as “Unknown product” where analytical use requires them.
- Use reference data to identify conformance across the warehouse.
- Add metadata such as business definitions and descriptions.

#### Extract transaction tables

Transaction tables are fast-moving tables that record business events. They are the primary source of informational value for the business.

When extracting from transaction tables, use a name that pairs with a reference table that describes the transaction. For example, `Sales` should be matched with `RefSales`, `Inspection` with `RefInspection`, and `AuditResult` with `RefAuditResult`.

When extracting, filter out noisy data such as unnecessary columns and, where justifiable and computationally simple, unnecessary rows. The purpose of filtering is not just efficiency. It is also to remove noise and improve clarity for both the data engineer and the business.

An important case for filtering is transactional inconsistency. During batch extraction, it is common for inconsistency to arise within the batch. Depending on business use, early records may need to be filtered out until the next batch, provided the next round of extraction picks up the skipped records.

The transaction table should be as narrow as possible, with a minimum number of columns. This can be achieved by passing as much information as possible to reference tables.

When these steps are applied, the data engineer will have:

- Extracted the minimum amount of information, not just for efficiency but to remove noise that impedes clarity.
- Built a basic map of information by implementing primary and foreign key relationships.
- Created expressive meaning through clear naming, especially by relying on reference tables.
- Applied change detection to incoming records to support downstream change tracking.
- Set up a foundation for future optimisation work, including incremental extract.

### Second pass — Map

The first pass focuses on extracting raw data, applying basic transformation to clarify meaning, and setting up the foundations for deeper analytical work. The second pass builds on these foundations. It focuses on creating useful information, derived, calculated, and shaped for business insight. This pass avoids working directly off the raw data and instead uses the outputs from the first level of processing.

The mindset here is that of storytelling. The chief consideration is not to be limited by the source system concepts, or even the business terms provided by stakeholders. The data engineer must be appropriately creative in reshaping the language in a way that makes sense for business decision-making.

In creating information, the guiding question is: “What are the valuable pieces of information that would be useful for business insight?” Often, this information is latent in the data and needs to be explicitly calculated. For example, the concept of a non-compliant transaction may not be stated in the source data and must be inferred.

When creating information, the result should be stored in standalone tables rather than as additional columns in the extracted tables. This is in line with the concept of fragment modelling and provides a clean container for complex logic.

As in the first pass, information should be offloaded to reference tables and the transactional tables kept narrow. This may require the creation of new reference tables from scratch because the concept does not exist in the source data.

As an example, if the first pass created `Sales`, `SalesItem`, `ItemSupplierCost`, and `SalesItemRefund` from the raw data, the second pass may use these to create a table called `SalesItemMargin` to compute profitability on each sales item.

The full set of tables in this example would look like:

**First pass from the source data**

- `Sales` — header for the sales event
- `SalesItem` — a list of items sold in the sale and for how much
- `ItemSupplierCost` — how much the item costs to supply, a Type II table since the supply cost can change
- `SalesItemRefund` — a separate table that records any refunds

**Second pass of derived computation**

- `SalesItemMargin` — computes the profitability on each sales item after calculating sale item value, refunds, and costs

### Third pass — Reduce

The third pass focuses on aggregation. At this stage, the data engineer takes the detailed fragments from the first and second passes and rolls them up to the grain that matches the entity of interest. Source systems often contain large volumes of fine-grained detail, yet business focus is centred on the entity itself.

This stage is also a major opportunity for a data engineer to add value. Aggregations can be technically complex, especially when they involve multiple sources or complex business rules. By building them into the pipeline, the data engineer delivers ready-made, trusted information blocks that can be used without repeated manual work.

Continuing the earlier example, suppose the first pass produced `Sales`, `SalesItem`, `ItemSupplierCost`, and `SalesItemRefund`, and the second pass created `SalesItemMargin` to calculate the profitability of each sales item. In the third pass, this information can be aggregated to the sales level to produce `SalesProfit`. This table would combine the total margin from all items in the sale, apply any additional business rules, and arrive at a final profit figure for the sale. A main reference table, `RefSalesProfit`, could include a binary flag indicating whether the sale was profitable.

This pass is also the place to compute the time where an entity reaches specific milestones. For example, a sales order may have a milestone for placement of the sale, confirmation, shipment, and completion. These dates can be recorded through columns of `SalesProcessMilestone`.

The outputs of this pass are valuable building blocks. In business intelligence scenarios, they provide ready-to-use measures for dashboards and reports. In data science scenarios, they are equally important. Much of feature engineering in machine learning involves aggregating detailed attributes back to the correct grain.

### Summary of the three passes

When complete, the pipeline should create a reusable block of valuable information, expressed in a way that reflects business intent, supported by good metadata, and delivered through an efficient and robust pipeline. These blocks of information are immediately ready for different purposes, including self-service dimensional models and feature engineering.

## Common problems

New data engineers benefit from being aware of common mistakes in entity processing.

**Starting with the details.** The order of work should follow the order of the business process itself. The starting point should be the main entity, for example `Sales`, before moving on to associated detail tables.

**Neglecting reference tables.** A common mistake is to store too much information in the transaction table rather than keeping it narrow and letting reference tables carry the descriptive load.

**“Garbage in, garbage out.”** Many application systems have poor or cryptic names for tables and columns because presentation is handled in the user interface and naming is not a primary concern. Renaming and reshaping to reflect business meaning is one of the most direct ways to make the model recognisable and useful.

**Skipping aggregation.** The third pass exists to aggregate information to the entity level. New engineers often stop at the first or second pass without completing this step.

**Compounded logic.** Placing too much computation into a single table makes it computationally unwieldy and difficult to maintain. Fragment modelling suggests breaking these computations into standalone tables.

More specifically, new engineers often mix the first and second passes into one. Combining extraction and complex transformation compounds computational complexity and undermines future possibilities for incremental extraction.

In general, there is a temptation to do all three passes at once in the beginning because of convenience. In practice, this creates a host of problems that fragment modelling avoids.

Avoiding these mistakes keeps the focus on the business outcome and ensures that the pipeline remains clear, adaptable, and valuable over time.
