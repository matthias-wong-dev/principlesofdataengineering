---
title: Entity processing
url: /docs/creating-information/entity-processing/
description: Explains the entity processing pattern for immutable business entities, using filter, map, and reduce passes to create reusable information.
lede: Entity processing applies to business processes built around immutable transactional entities.
weight: 3
# draft: true
---

## Processing immutable entities

Entity processing is the main pattern for immutable business entities: entities that are treated as fixed once created.

Examples include a sales order, a bank transfer, or an import declaration. If such an entity changes, the change is treated as though it were a different entity. For immutable entities, the business objective is to process the entity according to defined business logic. Hence the term **entity processing**.


Immutable entities share common characteristics:

- **Versions**—each version can be considered a new entity, with the latest version replacing all others as the correct version.
- **Header and details structure**—the header represents the main entity, while the details represent its components. A sales order and its line items are a typical example.
- **Subprocesses**—multiple business processes are needed to complete the business activity on the entity.
- **Good or bad**—the entity is evaluated by outcome, such as profitable or unprofitable, compliant or non-compliant, fraudulent or legitimate.
- **Actors**—actors persist across multiple entities, such as a customer making multiple purchases over time.

These characteristics explain the goals of entity processing:

- Surface insight from the underlying business process.
- Identify macro-level trends, such as sales by region.
- Measure time between process milestones.
- Provide drill-through to specific events for troubleshooting and root-cause analysis.
- Provide a foundation for predictive analytics by engineering attributes that can be used to predict good or bad outcomes.
- Understand actors whose behaviour affects business outcomes.

The first task is to identify the **entity of interest**.

Usually this is clear. Sometimes it is not. A sales transaction may have multiple line items. Depending on the business question, the transaction may be the entity of interest, or each line item may be the entity of interest.

The correct lens is the one that supports business action.

Once the entity of interest is identified, the data engineer tells the high-level story of that entity while preserving the necessary detail. Fragment modelling is suited to this task because different aspects of the entity can be maintained in different fragments.

## Building the pipeline

A pipeline for entity processing follows three broad passes:

- **Filter**—remove irrelevant data and establish the minimum meaningful structure.
- **Map**—compute reusable blocks of business meaning.
- **Reduce**—aggregate to the grain required for analysis.

### First pass—Filter

The first pass works predominantly with incoming raw data. Its aim is to establish structure and meaning, beginning with keys.

It has three stages: identifying keys, defining reference tables, and extracting transactions.

#### Identifying keys

The first task is to identify the business keys that serve as primary keys to the raw data. These may be defined as database constraints in the source data, or inferred through exploratory analysis.

Defining primary and foreign keys is a simple but powerful way to bridge the data world and the business world.

In some cases, key columns need to be created. For immutable entities, the two common scenarios are versioning and sequence numbers.

In versioning, a typical application might use `[Sales ID]` and `[Previous sales ID]` to indicate that one record replaces another. A clearer approach is to introduce `[Original sales ID]` and `[Sales version number]`, using partitioning and ordering to establish lineage. The original `[Sales ID]` can still be retained for joins, but should be renamed `[Sales version ID]`.

In header-detail structures, detail rows are often stored as simple lists. For example, a `[Sales ID]` may be associated with multiple `[Sales item ID]` entries. Introducing `[Sales item sequence number]` can clarify the relationship between the order and its line items.

Keys do not need to be enforced as physical constraints. They can be stored in metadata tables. What matters is that they communicate meaning and can be looked up by consumers of the data.
#### Defining reference tables

Reference tables are small, slow-moving, descriptive tables that describe the content of larger, fast-moving transaction tables.

Examples include `RefProduct`, which describes the products being sold, and `RefLocation`, which describes the store where the sale occurred.

Reference tables are important for two reasons:

- **Expressiveness**—they provide a central place to describe the attributes of a business entity, rather than embedding all information in the transaction table.
- **Efficiency**—updates can be made to a small reference table rather than to large volumes of transaction data.

The data engineer can use source-system reference tables for inspiration, but should not be limited by them. Application reference tables are usually designed to support system functionality, not business insight.

The data engineer can make reference data more expressive by:

- Renaming incoming tables and columns to reflect business intent.
- Combining fragmented application reference tables when this clarifies the business concept.
- Creating new reference tables for analytical use.
- Adding default rows such as `Unknown product` where analytical use requires them.
- Using reference data to identify conformance across the warehouse.
- Adding metadata such as business definitions and descriptions.

#### Extracting transaction tables

Transaction tables are fast-moving tables that record business events. They are the primary source of informational value for the business.

When extracting transaction tables, use names that pair with the reference tables describing them. For example, `Sales` should be matched with `RefSales`, `Inspection` with `RefInspection`, and `AuditResult` with `RefAuditResult`.

Filter out noisy data, including unnecessary columns and, where justifiable and computationally simple, unnecessary rows. 

Removing rows requires judgement. In large tables, reversing such a decision later can be costly for the pipeline. A prudent approach is to remove only rows that are clearly irrelevant, such as stray test records, and handle more ambiguous filtering scenarios in later passes through mapping or classification tables.

Filtering is not only for efficiency. It removes noise and improves clarity for both the data engineer and the business. 


Transactional inconsistency is an important case. During batch extraction, inconsistency can arise within the batch. Depending on business use, early records may need to be filtered out until the next batch, provided the next extraction picks up the skipped records.

The transaction table should be as narrow as possible. Pass as much descriptive information as possible to reference tables.

When these steps are applied, the data engineer will have:

- Extracted the minimum information needed to remove noise and preserve clarity.
- Built a basic map of information through primary and foreign key relationships.
- Created expressive meaning through clear naming and reference tables.
- Applied change detection to incoming records to support downstream change tracking.
- Set up a foundation for future optimisation, including incremental extraction.

### Second pass—Map

The first pass extracts raw data, clarifies basic meaning, and establishes the foundation for deeper analytical work.

The second pass builds on this foundation. It creates useful information—derived, calculated, and shaped for business insight.

This pass should avoid working directly from raw data. It should use the outputs from the first pass.

The mindset here is storytelling. The data engineer should not be limited by source-system concepts, or even by the business terms initially provided by stakeholders. The work requires appropriate creativity: reshaping language and logic so the data makes sense for business decision-making.

The guiding question is:

> What valuable pieces of information would be useful for business insight?

Often, this information is latent in the data and must be explicitly calculated. For example, the concept of a non-compliant transaction may not be stated in the source data. It must be inferred.

The result should be stored in standalone tables rather than added as extra columns to extracted tables. This follows fragment modelling and provides a clean container for complex logic.

As in the first pass, information should be offloaded to reference tables and transaction tables kept narrow. This may require new reference tables because the concept does not exist in the source data.

For example, if the first pass creates `Sales`, `SalesItem`, `ItemSupplierCost`, and `SalesItemRefund`, the second pass may create `SalesItemMargin` to compute profitability on each sales item.

The full set of tables would look like this.

**First pass from the source data**

- `Sales`—header for the sales event.
- `SalesItem`—items sold in the sale and their prices.
- `ItemSupplierCost`—cost to supply each item, stored as a Type II table because supply cost can change.
- `SalesItemRefund`—refunds recorded against sales items.

**Second pass of derived computation**

- `SalesItemMargin`—profitability of each sales item after accounting for sale value, refunds, and costs.

### Third pass—Reduce

The third pass focuses on aggregation.

At this stage, the data engineer takes the detailed fragments from the first and second passes and rolls them up to the grain of the entity of interest. Source systems often contain fine-grained detail, while business attention is centred on the entity itself.

This stage is a major opportunity for the data engineer to add value. Aggregations can be technically complex, especially when they involve multiple sources or complex business rules. By building them into the pipeline, the data engineer delivers ready-made, trusted information blocks that can be used without repeated manual work.

Continuing the earlier example, suppose the first pass produced `Sales`, `SalesItem`, `ItemSupplierCost`, and `SalesItemRefund`, and the second pass created `SalesItemMargin`.

In the third pass, this information can be aggregated to the sales level to produce `SalesProfit`. This table combines the total margin from all items in the sale, applies any additional business rules, and arrives at a final profit figure for the sale. A reference table, `RefSalesProfit`, can include a binary flag indicating whether the sale was profitable.

This pass is also where the data engineer computes when an entity reaches specific milestones. A sales order may have milestones for placement, confirmation, shipment, and completion. These dates can be recorded in `SalesProcessMilestone`.

The outputs of this pass are valuable building blocks.

In business intelligence scenarios, they provide ready-to-use measures for dashboards and reports. In data science scenarios, they are equally important: much of feature engineering involves aggregating detailed attributes back to the correct grain.

### Summary of the three passes

When complete, the pipeline produces reusable information blocks: expressive of business intent, supported by metadata, and delivered through an efficient and robust process.

These blocks are ready for downstream use, including self-service dimensional models and feature engineering.

An overview of the three passes and examples is summarised in Figure 1.

{{< svg >}}
<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="360" viewBox="0 0 1080 360"
     style="background:#ffffff" role="img"
     aria-label="Three passes of entity processing with purpose and example artefacts">

  <defs>
    <marker id="arrowhead-entity-processing" markerWidth="10" markerHeight="8"
            refX="10" refY="4" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L10,4 L0,8 z" fill="#222222"/>
    </marker>
  </defs>

  <!-- Filter -->
  <rect x="45" y="45" width="290" height="235" rx="16"
        fill="#ffffff" stroke="#222222" stroke-width="1.8"/>

  <text x="190" y="83" text-anchor="middle"
        font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
        font-size="24" font-weight="700" fill="#111111">Filter</text>

  <text x="190" y="116" text-anchor="middle"
        font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
        font-size="14" fill="#555555">establish keys</text>
  <text x="190" y="137" text-anchor="middle"
        font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
        font-size="14" fill="#555555">define reference tables</text>
  <text x="190" y="158" text-anchor="middle"
        font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
        font-size="14" fill="#555555">remove noise</text>

  <line x1="75" y1="180" x2="305" y2="180"
        stroke="#dddddd" stroke-width="1.4"/>

  <text x="190" y="207" text-anchor="middle"
        font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
        font-size="13" fill="#333333">Sales</text>
  <text x="190" y="228" text-anchor="middle"
        font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
        font-size="13" fill="#333333">SalesItem</text>
  <text x="190" y="249" text-anchor="middle"
        font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
        font-size="13" fill="#333333">ItemSupplierCost · RefProduct</text>

  <!-- Map -->
  <rect x="395" y="45" width="290" height="235" rx="16"
        fill="#ffffff" stroke="#222222" stroke-width="1.8"/>

  <text x="540" y="83" text-anchor="middle"
        font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
        font-size="24" font-weight="700" fill="#111111">Map</text>

  <text x="540" y="116" text-anchor="middle"
        font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
        font-size="14" fill="#555555">compute reusable</text>
  <text x="540" y="137" text-anchor="middle"
        font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
        font-size="14" fill="#555555">business meaning</text>
  <text x="540" y="158" text-anchor="middle"
        font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
        font-size="14" fill="#555555">isolate complex logic</text>

  <line x1="425" y1="180" x2="655" y2="180"
        stroke="#dddddd" stroke-width="1.4"/>

  <text x="540" y="217" text-anchor="middle"
        font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
        font-size="13" fill="#333333">SalesItemMargin</text>
  <text x="540" y="239" text-anchor="middle"
        font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
        font-size="13" fill="#333333">RefSalesItemMargin</text>

  <!-- Reduce -->
  <rect x="745" y="45" width="290" height="235" rx="16"
        fill="#ffffff" stroke="#222222" stroke-width="1.8"/>

  <text x="890" y="83" text-anchor="middle"
        font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
        font-size="24" font-weight="700" fill="#111111">Reduce</text>

  <text x="890" y="116" text-anchor="middle"
        font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
        font-size="14" fill="#555555">aggregate detail</text>
  <text x="890" y="137" text-anchor="middle"
        font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
        font-size="14" fill="#555555">to entity grain</text>
  <text x="890" y="158" text-anchor="middle"
        font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
        font-size="14" fill="#555555">produce usable outputs</text>

  <line x1="775" y1="180" x2="1005" y2="180"
        stroke="#dddddd" stroke-width="1.4"/>

  <text x="890" y="207" text-anchor="middle"
        font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
        font-size="13" fill="#333333">SalesProfit</text>
  <text x="890" y="228" text-anchor="middle"
        font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
        font-size="13" fill="#333333">RefSalesProfit</text>
  <text x="890" y="249" text-anchor="middle"
        font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
        font-size="13" fill="#333333">SalesProcessMilestone</text>

  <!-- Arrows -->
  <line x1="350" y1="162" x2="375" y2="162"
        stroke="#222222" stroke-width="2.2"
        marker-end="url(#arrowhead-entity-processing)"/>

  <line x1="700" y1="162" x2="725" y2="162"
        stroke="#222222" stroke-width="2.2"
        marker-end="url(#arrowhead-entity-processing)"/>

</svg>
{{< /svg >}}

<div style="text-align: center; font-size: 0.95rem; color: #666; margin-top: 0.5rem;">
Figure 1. The three passes of entity processing, showing both the purpose of each pass and example artefacts produced in a sales pipeline.
</div>

## Common problems

New data engineers should watch for common mistakes in entity processing.

**Starting with the details.** Work should follow the shape of the business process. Start with the main entity, such as `Sales`, before moving to associated detail tables.

**Neglecting reference tables.** A common mistake is to store too much information in the transaction table instead of keeping it narrow and letting reference tables carry the descriptive load.

**Accepting “garbage in, garbage out.”** Source systems often have poor or cryptic names because presentation is handled in the user interface. Renaming and reshaping data to reflect business meaning is one of the most direct ways to make the model recognisable and useful.

**Skipping aggregation.** The third pass aggregates information to the entity level. New engineers often stop at the first or second pass without completing this step.

**Compounding logic.** Placing too much computation into a single table makes the pipeline difficult to understand and maintain. Fragment modelling suggests breaking these computations into standalone tables.

New engineers often mix the first and second passes: extracting raw data while performing complex transformation. This compounds computational complexity and weakens future options for incremental extraction.

The same temptation applies to all three passes. Convenience at the beginning creates fragility later.

> [!NOTE]
> **Key ideas**
>
> Entity processing applies to immutable business entities.
>
> The first task is to identify the entity of interest.
>
> The three passes are filter, map, and reduce.
>
> The reduce pass returns detailed fragments to the grain required by business intent.
