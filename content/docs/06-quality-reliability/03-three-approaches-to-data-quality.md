---
title: Three approaches to data quality
url: /docs/quality-reliability/three-approaches-to-data-quality/
description: "Explains how to close data quality gaps by choosing the right intervention: human curation, precise rules, or fuzzy logic."
lede: When recorded data does not meet business intent, choose the right kind of intervention.
weight: 3
# draft: true
---

## Quality means fitness for intent

Most people see data quality issues as failures of data capture to reflect reality.

That view is useful, but incomplete.

In practice, errors in the database are rarely neutral. They reflect the incentives and pressures of the process that produced the data. In general, errors tend to be biased toward the advantage of the person providing the information, or toward the path of least resistance in the business process.

Consider personal income.

Both government social services and the tax office may be concerned with underestimation of income, but the direction and consequence of error differ. For tax, a taxpayer is unlikely to complain if they accidentally report less income, because they may receive a higher tax return or pay less tax. For social services, the same person is more likely to notice an underestimate, because they may receive less support than expected.

A bank credit rater faces a different concern again. It may care more about overestimates of income, because overestimated income may lead to excessive lending risk.

The same data element—personal income—therefore has different quality implications depending on the business intent. Social services may actively manage underestimates to meet legislative requirements. Credit raters may actively manage overestimates to reduce risk. The tax office may design its controls around yet another risk profile.

All three may prefer perfect accuracy. But none takes the same approach when under constraint.

There is no accuracy without margin of error, no margin of error without a risk threshold, and no risk threshold without an articulation of business objective.

Consequently, data quality is not merely data versus reality. It is data versus business intent.

A dogmatic insistence on reflecting the real world perfectly is costly and often impractical. It may also conflict with privacy, timeliness, proportionality, or operational burden. The data engineer’s job is not to pursue perfect data in the abstract, but to help the business decide what quality means for the decision at hand.

With that in mind, common data quality issues arise because digital systems and business processes were not built to honour the full intent of the business. This may be due to poor design, such as missing data type constraints. It may be due to bias in the business process, such as different incentives for reporting income. It may also be due to a mismatch of purpose, such as import declarations captured for tax but analysed for biosecurity.

The data engineer therefore needs a practical set of interventions.

| Situation | Approach |
|---|---|
| Business judgement is needed | Human curation |
| Business intent can be formalised | Precise rules |
| Business intent can only be approximated | Fuzzy logic |

Each approach contains recurring methods.

**Human curation**

| Method | Use when... |
|---|---|
| Data annotation | Records need to be classified, mapped, enriched, or corrected by a business expert. |
| Applying assumptions | A practical assumption can handle most cases, but violations need expert review. |
| Data quality reports | Issues are frequent, numerous, or easier to remediate in bulk. |

**Precise rules**

| Method | Use when... |
|---|---|
| Defining analytical concepts | Operational details need to be turned into usable business concepts, such as good/bad, milestones, or conformed categories. |
| Defining primary keys | Rows need a clear identity that connects them to real-world entities. |
| Defining the primary record | Multiple records appear to refer to one underlying entity. |
| Defining relationships | Analytically important relationships were not recorded by the source system. |

**Fuzzy logic**

Fuzzy logic is handled through iterative approximation.

| Step | Question |
|---|---|
| Loose–tight iteration | Can the pattern be tuned to reduce both false matches and false rejects? |
| Random validation | Does the pattern hold up when checked against unbiased samples? |
| Monitoring for drift | Does the pattern continue to behave over time? |

One theme runs through all three approaches: assumptions must be monitored. If a data engineer closes a quality gap by applying judgement, rules, or approximation, the data product should also monitor whether that intervention continues to behave as intended.

This is covered in more detail in [Tests and assumptions](/docs/quality-reliability/tests-and-assumptions/).

## Human curation: when judgement is needed

If data quality issues arise from a gap between recorded data and business intent, one simple remedy is to allow business experts to intervene directly.

Human curation closes the quality gap by allowing business judgement to enter the data product. Its main monitoring need is to detect new records that require human attention.

It is appropriate when business judgement is needed and the data engineer should not pretend the answer can be fully inferred by the system.
### Data annotation

Data annotation is useful when records need to be classified, mapped, enriched, or corrected by a business expert.

For example, a digital system may record store locations as addresses. These addresses may be sufficient for operational use, but not enough for regional reporting. A business expert may later annotate each store with its sales region.

This annotation occurs in the data pipeline, not the source system, and is commonly known as reference data management.

**Example structure of `'Store'`**

| Store ID | Store address | Sales region (annotated) |
|---|---|---|
| S001 | 12 Smith St, Northvale | North |
| S002 | 88 Market Rd, Southport | South |
| S003 | 45 Central Ave, Westhaven | West |
| S004 | 9 Harbour Rd, Eastbank | New store not annotated |

The value `New store not annotated` flags the need for human attention.

Another example is harmonising employee identities across systems. In large organisations, the same employee may appear under different accounts for different business processes. A business expert who understands the enterprise view may annotate these accounts to map them to a canonical representation. This is known as master data management.

Human annotation extends beyond reference and master data. It applies wherever a human can interpret records outside the operational context.

There are two legitimate views of data: one fast-paced and operational, suited to digital systems; the other reflective and analytical, suited to business interpretation. Both may require human input. It is not reasonable to expect operational systems to carry the full load of analytical meaning.

Traditionally, data warehousing has treated human curation as an exception. But if human editing can be implemented transparently, with control and auditability, it should be treated as a standard business tool.

Whether the curation concerns reference data, master data, or other forms of annotation, the data engineer must monitor for incoming records that require curation. Examples include uncategorised store locations, unmapped employee accounts, or new values that do not yet belong to a known category.

### Applying assumptions

Applying assumptions is useful when a practical assumption can handle most cases, but violations need expert review.

Consider the recording of dates. If users manually enter dates, they may accidentally type 2300 instead of 2030. If the digital system lacks validation, such errors can end up in the database. Even a single mistake can distort a line chart or skew time-based analysis.

One way to address this is to assume that future dates must be within 50 years. Dates outside this range are treated as invalid and converted to blank. The original issue should not simply disappear. The record should also be flagged so that a business expert can review and correct the source data.

Before applying the assumption, the data may look like this.

**Example structure before flagging**

| Record ID | Event date |
|---:|---|
| 1 | 2030-06-15 |
| 2 | 2300-06-15 |
| 3 | 2025-04-02 |

After applying the assumption, the invalid date is blanked out and the row is flagged.

**Example structure after flagging**

| Record ID | Event date | Is flagged for invalid date |
|---:|---|---|
| 1 | 2030-06-15 | false |
| 2 |  | true |
| 3 | 2025-04-02 | false |

This preserves analytical usefulness while making the intervention visible. The invalid date no longer distorts time-based analysis, but the issue remains available for remediation.

Another example is assuming uniqueness.

If records are almost always unique, but occasional duplicates occur, the pipeline can assume uniqueness for the main analytical table and separate the duplicates into a rejected-records table for review.

Before applying the assumption, the data may look like this.

**Example structure before deduplication**

| Submission ID | Customer ID | Submission date | Submission amount |
|---|---|---|---:|
| S1001 | C001 | 2025-04-01 | 120.00 |
| S1002 | C002 | 2025-04-01 | 95.00 |
| S1003 | C001 | 2025-04-01 | 120.00 |
| S1004 | C003 | 2025-04-02 | 80.00 |

In this example, the business expects one submission per customer per date. The duplicate record is removed from the main analytical table and written to a rejected-records table.

**Example structure of accepted records**

| Submission ID | Customer ID | Submission date | Submission amount |
|---|---|---|---:|
| S1001 | C001 | 2025-04-01 | 120.00 |
| S1002 | C002 | 2025-04-01 | 95.00 |
| S1004 | C003 | 2025-04-02 | 80.00 |

**Example structure of rejected records**

| Submission ID | Customer ID | Submission date | Submission amount | Rejection reason |
|---|---|---|---:|---|
| S1003 | C001 | 2025-04-01 | 120.00 | Duplicate customer submission for date |

This lets the main analytical table remain usable while preserving the rejected record for business attention. The duplicate is not silently lost. It is excluded from the analysis path and surfaced for remediation.

This approach works best when violations are rare and the business expert can correct the issue before the next batch load. It is suitable for irregular data quality issues that do not require bulk remediation. This can be done in bulk for the entire pipeline, and studied in [Fault tolerance]( /docs/quality-reliability/fault-tolerance/).

If data quality issues are frequent or systemic, a data quality report may be more appropriate.

### Data quality report

Data quality reports are suitable when issues are frequent, numerous, or easier to treat in bulk on a periodic basis.

An effective implementation is to create a [combination or choice dimension](/docs/presenting-insights/dimensional-modelling-for-ux/). A combination dimension may include one column per issue and describe each transaction. For example, a dimension called `'Sales data quality'` might include `[Is missing sales amount]`, `[Is invalid sales date]`, `[Is unknown customer]`, and so on.

**Example structure of `'Sales data quality'`**

| Sales data quality SK | Is missing sales amount | Is invalid sales date | Is unknown customer | Data quality category |
|---:|---|---|---|---|
| 1 | false | false | false | No known issue |
| 2 | true | false | false | Missing amount |
| 3 | false | true | false | Invalid date |
| 4 | false | false | true | Unknown customer |
| ... | ... | ... | ... | ... |
| 8 | true | true | true | Multiple issues |

The fact table can then refer to the data quality dimension.

**Example structure of `'Sales'`**

| Sales ID | Sales date | Customer ID | Sales amount | Sales data quality SK |
|---|---|---|---:|---:|
| S1001 | 2025-04-01 | C001 | 120.00 | 1 |
| S1002 | 2300-04-01 | C002 | 95.00 | 3 |
| S1003 | 2025-04-03 | C999 | 80.00 | 4 |
| S1004 | 2025-04-04 | C004 |  | 2 |

Coupled with the ID dimension, this makes it easy to build a Power BI report that surfaces transactions requiring remediation by a business expert.

A data quality dimension also supports systematic analysis by enabling statistics on the number and type of issues.

Reports are only effective if they embed in the user’s workflow. A decontextualised report becomes forgotten and unused. The same applies to data quality reports. The business should have a workflow trigger that prompts engagement with the report.

## Precise rules: when intent can be formalised

Translating business knowledge into precise rules allows it to be automated and reduces reliance on human intervention.

One way to look at these rules is to see them as “fixing issues” in the data. A more useful way is to see them as rules that bridge recorded data to business intent.

Precise rules close data quality gaps by formalising business intent into repeatable logic. Their main monitoring need is to detect rule violations, edge cases, and changes in the business process that make the rule unsafe.



Precise rules are appropriate when the business can say what should happen clearly enough for the data engineer to implement it.

This section covers four recurring types of precise rule:

1. Defining analytical concepts
2. Defining primary keys
3. Defining the primary record
4. Defining relationships

### Defining analytical concepts

Defining analytical concepts closes the quality gap between operational detail and business interpretation.

Since business insight is information analysed in light of business intent, a direct way of improving data quality is to define the analytical concept that the business needs.

Defining analytical concepts takes [leadership and negotiation skill](/docs/foundations/data-and-organisations/). The data engineer is often well placed to broker between stakeholder groups by experimenting with the data and visually communicating possible outcomes.

#### Good and bad entities

Good and bad entity definitions close the quality gap between detailed operational outcomes and the business’s need for a usable judgement.

A business process may collect detailed information such as audit results, inspection results, incidents, sentiment, or sales volume. However, these details may not yet be formalised into a systematic judgement.

Sometimes numeric values such as star ratings need to be translated into good and bad using thresholds. More commonly, a business process records information at a lower grain that needs to be rolled up to the entity of interest.

For example, a manufacturing batch may have multiple quality-control criteria. The business may decide that failing one critical criterion, or multiple non-critical criteria, defines failure at the batch level.

**Example structure of `'Batch quality criterion'`**

| Batch ID | Quality criterion | Quality result | Is critical criterion |
|---|---|---|---|
| B1001 | Temperature control | Pass | true |
| B1001 | Packaging integrity | Pass | false |
| B1001 | Labelling accuracy | Fail | false |
| B1002 | Temperature control | Fail | true |
| B1002 | Packaging integrity | Pass | false |

The analytical concept can then be expressed at the batch level.

**Example structure of `'Batch quality outcome'`**

| Batch ID | Critical criteria failed | Non-critical criteria failed | Batch quality outcome |
|---|---:|---:|---|
| B1001 | 0 | 1 | Pass |
| B1002 | 1 | 0 | Fail |

This gives the user immediate view of the business at the level of intent.

It is not reasonable to expect operational systems to always define these concepts. Their primary job is to execute workflows while preserving records. The data engineer plays a role by adding the analytical lens.

This implementation is studied in greater depth in [entity processing](/docs/creating-information/entity-processing/).

#### Milestones

Milestones close the quality gap between messy workflow events and meaningful process control.

A business process may have many detailed steps. Some may loop back. Some may start and stop multiple times. Some may occur repeatedly for the same business entity. This mass of events can bury insight in operational detail.

A useful analytical view is to define a small number of major checkpoints that can be used to measure performance. These checkpoints are milestones.

The difficulty is choosing the right level of abstraction. A milestone can be too narrow, in which case it merely reproduces operational noise. It can also be too broad, in which case it merges several different responsibilities into one measure.

A practical rule is that each milestone should have one main control point or responsible owner. If a milestone mixes responsibilities, then a delay becomes difficult to interpret. The business can see that something is late, but not who is able to act on it.

For example, an HR recruitment process may contain dozens of operational steps: position approved, advertisement drafted, advertisement cleared, advertisement published, applications received, applications closed, eligibility checked, longlist completed, shortlist completed, interviews scheduled, interviews completed, referee checks completed, delegate approval received, offer issued, offer accepted, and commencement recorded.

In practice, such an operational process may contain more than forty recorded steps. That level of detail is necessary for workflow execution, but too noisy for business decision-making.

The solution is to define key milestones.

**Example structure of `'Recruitment event'`**

| Recruitment ID | Event datetime | Event type |
|---|---|---|
| R1001 | 2025-04-01 09:00 | Advertisement drafted |
| R1001 | 2025-04-03 11:30 | Advertisement cleared |
| R1001 | 2025-04-04 09:00 | Advertisement published |
| R1001 | 2025-04-18 17:00 | Applications closed |
| R1001 | 2025-04-21 10:00 | Eligibility checked |
| R1001 | 2025-04-23 16:00 | Shortlist completed |
| R1001 | 2025-04-29 09:00 | Interviews scheduled |
| R1001 | 2025-05-02 16:30 | Interviews completed |
| R1001 | 2025-05-07 10:00 | Delegate approved |
| R1001 | 2025-05-09 14:00 | Offer accepted |
| R1002 | 2025-04-03 09:00 | Advertisement drafted |
| R1002 | 2025-04-05 10:00 | Advertisement returned for changes |
| R1002 | 2025-04-08 13:00 | Advertisement cleared |
| R1002 | 2025-04-09 09:00 | Advertisement published |
| R1002 | 2025-04-23 17:00 | Applications closed |
| R1002 | 2025-04-29 15:00 | Eligibility checked |
| R1002 | 2025-05-05 15:00 | Shortlist completed |
| R1002 | 2025-05-14 16:00 | Interviews completed |

The data engineer can turn the event history into a milestone fragment.

**Example structure of `'Recruitment milestone'`**

| Recruitment ID | Advertisement published datetime | Interview completed datetime | Offer accepted datetime | Days from advertisement to interview | Days from interview to offer |
|---|---|---|---|---:|---:|
| R1001 | 2025-04-04 09:00 | 2025-05-02 16:30 | 2025-05-09 14:00 | 28.3 | 6.9 |
| R1002 | 2025-04-09 09:00 | 2025-05-14 16:00 |  | 35.3 |  |

The milestone fragment does not replace the event history. It gives the business a stable analytical view of the process.

In this example, the three milestones correspond to different control points. Advertisement publication depends on the area preparing and clearing the advertisement. Shortlist completion depends on the assessment process after applications close. Offer acceptance depends on post-interview approval and candidate response. If these were collapsed into one broad measure such as `[Days to recruit]`, the business would know the process was slow but not where the delay occurred.

To deal with loops and repeated events, the data engineer can define the earliest or latest relevant occurrence. For example, `[Advertisement published datetime]` may use the first publication event, while `[Offer accepted datetime]` may use the final accepted offer event.

This pattern is studied in [Meaningful fragments](/docs/creating-information/meaningful-fragments/).

#### Conformed dimensions

Conformed dimensions close the quality gap between local system categories and enterprise intent.

A large organisation may have many processes, and many of them share similar concepts under different names or codes. A conformed dimension reconciles these local concepts into a shared view.

For example, one system may store country using two-letter country codes, while another system may store country using its own operational codes.

**Example structure of `Sales.Customer`**

| Customer ID | Customer country code |
|---|---|
| C001 | AU |
| C002 | NZ |
| C003 | US |

**Example structure of `Shipping.Delivery`**

| Delivery ID | Delivery country code |
|---|---|
| D001 | AUS |
| D002 | NZL |
| D003 | USA |

Both systems refer to the same business concept: country. However, the codes are not the same. If the data engineer leaves them as separate local values, enterprise reporting becomes harder than it needs to be.

The data engineer can create a standard country reference table.

**Example structure of `'Country'`**

| Country SK | Country name | ISO alpha-2 code | ISO alpha-3 code |
|---:|---|---|---|
| 1 | Australia | AU | AUS |
| 2 | New Zealand | NZ | NZL |
| 3 | United States | US | USA |

The local system codes can then be mapped to the conformed dimension.

**Example structure of `'Country code map'`**

| Source system | Source country code | Country SK |
|---|---|---:|
| Sales | AU | 1 |
| Sales | NZ | 2 |
| Sales | US | 3 |
| Shipping | AUS | 1 |
| Shipping | NZL | 2 |
| Shipping | USA | 3 |

This allows sales and shipping data to be analysed through the same country dimension, even though the source systems use different local codes.

When done appropriately, a conformed view can empower decision-makers at the most senior levels of the organisation.

Conformed dimensions are studied in [Reference data](/docs/creating-information/reference-data/).


### Defining primary keys

Defining primary keys closes the quality gap between database rows and real-world entities.

Primary keys serve as the [link between data records and their counterparts in the real world](/docs/creating-information/mapping-the-data-world/). Unfortunately, some business processes do not rigorously define primary keys.

This can lead to slippery definitions in the database. In other cases, the primary key is defined at the application layer but remains invisible at the data layer, leaving the business user without a clear way to interpret the data.

The data engineer should establish the primary key where it is not meaningfully defined.

The primary key articulates the data engineer’s view of how the data row should be interpreted as a business entity.

Most primary keys can be traced by examining how a business process creates, retrieves, and updates a data record. Three common patterns are sequence numbers, version numbers, and temporality.

#### Sequence numbers

Sequence numbers close the quality gap where the source system stores a list, but the data product needs stable business identity for each row.

Sequence numbers are useful when a header has multiple detail rows and the detail table lacks a meaningful primary key.

For example, a sales order may have multiple items. The order is stored in `Sales`, with `[Order number]` as the primary key. The items are stored in `SalesItems`, which may be a miscellaneous list without a meaningful key.

If each product can appear only once, then `[Order number]` and `[Product ID]` may suffice as a primary key. But if a product can appear more than once, this fails.

**Example structure of `SalesItems` before sequence numbering**

| Order number | Product ID | Sales item ID | Quantity |
|---|---|---:|---:|
| O1001 | P100 | 501 | 1 |
| O1001 | P100 | 502 | 2 |
| O1001 | P200 | 503 | 1 |

`[Order number]`, `[Product ID]` cannot identify a row because `P100` appears twice for the same order.

A simple solution is to treat the list of items as a sequence and create an artificial column `[Sales item sequence number]`, forming the key `[Order number]`, `[Sales item sequence number]`.

**Example structure of `SalesItems` after sequence numbering**

| Order number | Sales item sequence number | Product ID | Sales item ID | Quantity |
|---|---:|---|---:|---:|
| O1001 | 1 | P100 | 501 | 1 |
| O1001 | 2 | P100 | 502 | 2 |
| O1001 | 3 | P200 | 503 | 1 |

Sometimes a system will implement a meaningless key such as `[Sales item ID]`, a simple integer used for UI or database constraints. Even in these cases, the data engineer may still define a sequence number and use `[Order number]`, `[Sales item sequence number]` as the business-facing primary key. `[Sales item ID]` can be retained for joins.

In general, sequence numbers are effective wherever there is a miscellaneous list of line items within a header. Care must be taken to ensure the sequence is deterministic by breaking ties—using a surrogate key like `[Sales item ID]` as a sort order is a reliable approach.

#### Version numbers

Version numbers close the quality gap where the source system records change, but does not make the continuity of the entity clear.

Version numbers are useful for [entities whose changes should be preserved as new versions](/docs/creating-information/entity-processing/).

For example, a customer order may be submitted, revised, and resubmitted before it is fulfilled. The business may still regard this as the same order, but each revision changes the content that was true at a particular point in time.

Digital systems are not always consistent in how they manage versions. A common but problematic approach is to allow the entity ID to change each time the record is revised and record the relationship using `[Previous order ID]` or `[Superseded order ID]`. This may work for rendering a web UI but can cause confusion in analysis.

Where versioning is lost or muddled, the data engineer can restore clarity using a consistent pattern such as `[Entity ID]`, `[Version number]`.

The order can be represented with a stable `[Order ID]` and a changing `[Order version number]`.

**Example structure of `Sales.Order`**

| Order ID | Customer ID | Current order version number | Order status |
|---|---|---:|---|
| O1001 | C042 | 3 | Submitted |
| O1002 | C087 | 1 | Fulfilled |

**Example structure of `Sales.OrderVersion`**

| Order ID | Order version number | Version datetime | Product ID | Quantity | Order value |
|---|---:|---|---|---:|---:|
| O1001 | 1 | 2025-04-01 09:15 | P100 | 10 | 250.00 |
| O1001 | 2 | 2025-04-01 11:40 | P100 | 12 | 300.00 |
| O1001 | 3 | 2025-04-02 08:30 | P200 | 12 | 420.00 |
| O1002 | 1 | 2025-04-03 14:10 | P300 | 5 | 175.00 |

The primary key for `Sales.OrderVersion` is `[Order ID]`, `[Order version number]`.


#### Temporality

Temporality closes the quality gap where the business needs historical interpretation but the source system only presents the current state.

Temporality refers to tracking changes over time. In data warehousing, this is commonly handled through Type II tracking.

Some business processes are designed to handle only the current event, without tracking history. But when the business is interested in change over time, the [entity is mutable](/docs/creating-information/entity-tracking/).

Mutable entities should usually include a time component in their business key. The data engineer may define the business key as `[Employee ID]`, `[Start datetime]`, with `[End datetime]` marking the end of the validity period.

In implementation, it is necessary to add a surrogate key as well.

**Example structure of `Employee.TeamAssignment`**

| Team assignment SK | Employee ID | Start datetime | End datetime | Team name |
|---:|---|---|---|---|
| 1 | E1001 | 2024-01-01 00:00 | 2025-03-15 09:30 | Finance |
| 2 | E1001 | 2025-03-15 09:30 | 9999-12-31 00:00 | Analytics |
| 3 | E1002 | 2024-07-01 00:00 | 9999-12-31 00:00 | Operations |

The business key is `[Employee ID]`, `[Start datetime]`. `[End datetime]` marks the end of the validity period. `[Team assignment SK]` provides a simple surrogate key for joins, relationships, and downstream modelling.

Recovering temporality depends on how history is stored. Sometimes it is available in audit tables. Sometimes it must be reconstructed with help from business experts.

### Defining the primary record

Defining the primary record closes the quality gap between multiple records and one underlying entity.

This occurs when the database has primary keys, but different primary keys relate to the same underlying entity. It is common in business processes that gather decentralised observations.

Consider the example of whale sightings. A database may collect observations from citizen scientists, stored in `Whale.Observation`, with `[User ID]`, `[Observation number]` identifying each user’s submissions. A surrogate key such as `[Observation ID]` may also exist for system retrieval.

Multiple citizens may report sightings of the same whale. As a result, multiple `[Observation ID]` values relate to the same real-world entity.

**Example structure of `Whale.Observation`**

| Observation ID | User ID | Observation number | Species | GPS area | Observation date |
|---:|---|---:|---|---|---|
| 101 | U01 | 1 | Blue whale | A17 | 2025-05-01 |
| 102 | U02 | 1 | Blue whale | A17 | 2025-05-01 |
| 103 | U03 | 1 | Humpback whale | B04 | 2025-05-01 |

Suppose the business has a rule such as:

> A whale species at one GPS proximity should only appear once within a day.

This rule can be used to group observations and identify a representative record.

The data engineer can express this by identifying the primary observation. For example, the pipeline may select the first observation of the day at a location and store it as `[Primary observation ID]` in a table called `Whale.PrimaryObservation`.

**Example structure of `Whale.PrimaryObservation`**

| Observation ID | Primary observation ID |
|---:|---:|
| 101 | 101 |
| 102 | 101 |
| 103 | 103 |

`[Observation ID]` is the key for the original record. `[Primary observation ID]` identifies the chosen representative.

Subsequent transformation can focus on the `[Primary observation ID]` grain. The same key can also be used in Power BI to return the true count of whale sightings.

Care must be taken to resolve race conditions. If two users submit observations at the same time, only one record should be selected as primary. This can be resolved deterministically using a surrogate key such as `[Observation ID]`.

### Defining relationships

Defining relationships closes the quality gap where analytically important relationships were not recorded by the source system.

Digital systems are usually good at recording relationships needed by operational workflows. They are less reliable at recording relationships that are useful for analysis.

This is especially common when the system is designed for operational efficiency rather than analytical understanding.

The data engineer can sometimes close this quality gap by defining relationships that the source system did not record.

Two useful techniques are:

- nearest temporal joins;
- mapping tables.

#### Nearest temporal join

Nearest temporal joins close the quality gap between related events whose relationship was not explicitly recorded.

Sometimes two sets of events are related, but the relationship is not recorded as a database key.

If business knowledge suggests that one set of events is expected to precede another, the relationship can sometimes be recovered by identifying the nearest preceding event. This technique is known as a nearest temporal join.

Consider a building fire-safety process.

Building owners submit fire-safety certificates periodically, or when the building’s fire-safety arrangements change. Fire-safety officers conduct inspections separately. Some inspections may be scheduled. Others may be triggered by complaints, incidents, risk reviews, or follow-up action.

The two processes are related, but they are not one-to-one. One certificate may be followed by several inspections. Several certificates may be submitted before the next inspection. Some inspections may have no recent certificate at all.

The inspection system records the building and inspection date, but it does not record which certificate was in force at the time of inspection. This makes the relationship analytically important but structurally missing.

The fire-safety certificates are stored in `FireSafety.Certificate`.

**Example structure of `FireSafety.Certificate`**

| Fire safety certificate SK | Building ID | Certificate submitted datetime | Certificate type | Declared risk level |
|---:|---|---|---|---|
| 1 | B001 | 2025-04-01 09:00 | Annual certificate | Low |
| 2 | B001 | 2025-05-01 09:00 | Revised certificate | Medium |
| 3 | B002 | 2025-04-10 14:30 | High-risk occupancy | High |
| 4 | B002 | 2025-04-18 16:00 | Remediation certificate | Medium |

The inspections are stored separately in `FireSafety.Inspection`.

**Example structure of `FireSafety.Inspection`**

| Inspection SK | Building ID | Inspection datetime | Inspection trigger | Inspection outcome |
|---:|---|---|---|---|
| 101 | B001 | 2025-04-18 10:00 | Scheduled | Pass |
| 102 | B001 | 2025-05-20 11:30 | Complaint | Fail |
| 103 | B002 | 2025-04-15 09:00 | Risk review | Fail |
| 104 | B002 | 2025-04-30 13:15 | Follow-up | Pass |

Although both tables contain `[Building ID]`, there is no direct relationship between a specific inspection and a specific fire-safety certificate. The source system does not say which certificate the inspection should be read against.

To support analysis, the data engineer can create a nearest temporal join.

For example, the rule might be:

> An inspection relates to the most recent fire-safety certificate submitted for the same building before the inspection.

The result can be stored in `FireSafety.InspectionCertificate`.

**Example structure of `FireSafety.InspectionCertificate`**

| Inspection SK | Fire safety certificate SK | Days from certificate to inspection |
|---:|---:|---:|
| 101 | 1 | 17 |
| 102 | 2 | 19 |
| 103 | 3 | 5 |
| 104 | 4 | 12 |

This table re-establishes an analytical relationship between the inspection and the fire-safety certificate that preceded it.

The relationship is not “true” in the same way as a source-system foreign key. It is an inferred relationship created from business logic. For that reason, it should be documented and tested.

The data engineer should monitor cases where the assumption may be unsafe, such as:

- inspections with no preceding fire-safety certificate;
- inspections where the most recent certificate is too old;
- buildings with multiple certificates close together;
- certificate types that should not be associated with inspections;
- changes in the inspection process that alter the expected timing.

For example, the business may decide that an inspection should only be linked to a fire-safety certificate if it occurred within 60 days. If the most recent certificate is older than that, the inspection should be flagged for review rather than automatically linked.

Nearest temporal joins are especially valuable at the macro level.

At unit level, the problem is often that two records should be related but no foreign key was recorded. At macro level, the problem is broader: two business processes are related, but they operate in bulk, at different grains, and without unit-level traceability.

In the fire-safety example, certificate submission and inspection are not the same business process. They are separate processes that become analytically meaningful only when the data engineer defines a relationship between them.

This is the discipline of the pattern: use time to restore a relationship only where business knowledge says the relationship is meaningful, then monitor the assumptions that make it safe.

#### Mapping tables

Mapping tables close the quality gap between entities that must be related analytically but are not related operationally.

Mapping tables are introduced when the original system does not record relationships needed for analysis.

A common scenario is a header table with two separate detail tables at different grains. Both detail tables relate to the header, but not to each other.

The data engineer may introduce a mapping table between them based on a business rule.

Consider a club restaurant with data captured in three tables:

- `Club.TableSitting`—records of customers seated at the restaurant, one per sitting, keyed by `[Table sitting ID]`
- `Club.TableCustomer`—club members identified by `[Member ID]`, linked to `[Table sitting ID]`
- `Club.TableFoodOrder`—menu items ordered per `[Table sitting ID]`, with food items identified by `[Food item ID]`

**Example structure of `Club.TableCustomer`**

| Table sitting ID | Member ID |
|---|---|
| T001 | M001 |
| T001 | M002 |

**Example structure of `Club.TableFoodOrder`**

| Table sitting ID | Food order ID | Food item ID | Food item cost |
|---|---|---|---:|
| T001 | FO001 | F100 | 12.00 |
| T001 | FO002 | F200 | 18.00 |

The system does not record which member ordered which item. For analysis, the business may wish to associate members with food items. However, this relationship is not captured in the source system.

To support analysis, the data engineer may introduce a mapping table called `Club.CustomerFoodOrderMap`.

The logic may be based on a business rule such as:

> Every member at the table shares the cost of all items ordered.

**Example structure of `Club.CustomerFoodOrderMap`**

| Table sitting ID | Member ID | Food order ID | Allocation weight |
|---|---|---|---:|
| T001 | M001 | FO001 | 0.5 |
| T001 | M002 | FO001 | 0.5 |
| T001 | M001 | FO002 | 0.5 |
| T001 | M002 | FO002 | 0.5 |

Variants of this are studied in [Meaningful fragments](/docs/creating-information/meaningful-fragments/).

Because the relationship is inferred rather than recorded, it should be tested. Techniques for validating mapping logic are described in [Tests and assumptions](/docs/quality-reliability/tests-and-assumptions/).

## Fuzzy logic: when intent can only be approximated

There are cases where precise rules do not apply. 

Fuzzy logic closes data quality gaps by approximating business intent where exact rules are not available. Its main monitoring need is to detect drift in match rates, validation results, or alignment with a known reference.

A common example is natural language processing. When working with free text, it is often impossible to define exact rules that meet business intent.

Fuzzy logic is appropriate when the business intent is real but cannot be captured precisely. In many scenarios, something is better than nothing, and a perfect match with reality does not justify the cost.

This aligns with the view that data quality is not data versus reality, but data versus business intent.

Examples of fuzzy logic include:

- optical character recognition to extract information from images;
- large language models to infer sentiment from user text;
- entity resolution techniques to identify the underlying entity behind multiple records;
- pattern extraction from free text, such as phone numbers, invoice numbers, or addresses.

Fuzzy logic often pushes into the domain of data science, where statistical and mathematical disciplines bring rigour to its application. However, there are cases where a data engineer can apply a simple and practical approach.

The following is a three-step process, a kind of “poor man’s data science”:

1. Find the pattern through loose–tight iteration.
2. Check the pattern with random validation.
3. Monitor the pattern by watching for drift.

This approach can be highly effective in common scenarios that require extracting information from free text. A data engineer should be comfortable considering this approach and ready to pivot to a more sophisticated data science method when necessary.

### Step 1—Loose–tight iteration

Loose–tight iteration closes the quality gap where a pattern is real enough to use, but too messy to define perfectly at the start.

Every pattern has matches and rejects. The matches are records that meet the criteria. The rejects are records that do not.

The data engineer tunes the pattern by adjusting the criteria:

- tightening to reduce over-matching;
- loosening to recover missed records.

The goal is not to maximise matches. The goal is to reduce mistakes on both sides.

Consider the example of extracting phone numbers from a free-text field. Phone numbers may appear in formats such as `(02) 1234 5678`, `0412345678`, `12345678`, or `02-1234-5678`.

The challenge is that the field may also contain other numbers, such as invoice numbers, dates, quantities, account numbers, or address numbers.

**Example structure of `'Customer note'`**

| Customer note ID | Customer note |
|---:|---|
| 1 | Please call me on (02) 1234 5678 after 3pm. |
| 2 | Mobile is 0412345678. Invoice 889912 is unrelated. |
| 3 | Address is 12 Hill Street. No phone provided. |
| 4 | Try 02-9876-5432 or office 98765432. |
| 5 | Order 12345678 was delayed. |
| 6 | Phone number changed to 0412 345 678 on 2025-04-01. |

A rough first pattern might look for any eight-digit number.

This will produce matches, but it will also over-match.

**Example match set after rough pattern**

| Customer note ID | Extracted value | Correct extraction? | Comment |
|---:|---|---|---|
| 2 | 0412345678 | true | Mobile number |
| 4 | 98765432 | true | Local phone number |
| 5 | 12345678 | false | Order number, not phone number |

The pattern found real phone numbers, but also picked up an order number. This is a false match. The pattern is too loose.

The data engineer may tighten the pattern by looking for phone-like context, such as nearby words like `phone`, `mobile`, `call`, or `office`, or by excluding known phrases such as `order` and `invoice`.

After tightening, the match set may improve, but some genuine phone numbers may now be missed.

**Example reject set after tightened pattern**

| Customer note ID | Customer note | Should have matched? | Comment |
|---:|---|---|---|
| 1 | Please call me on (02) 1234 5678 after 3pm. | true | Landline with area code |
| 3 | Address is 12 Hill Street. No phone provided. | false | No phone number |
| 6 | Phone number changed to 0412 345 678 on 2025-04-01. | true | Mobile with spaces |

The rejected records reveal false rejects. The pattern is now too tight, or it does not recognise enough valid phone-number formats.

The data engineer then loosens the pattern to recognise area codes, mobile numbers with spaces, and hyphenated numbers while still avoiding obvious order numbers, invoice numbers, dates, and addresses.

A later iteration may produce a more useful extraction.

**Example extraction after loose–tight iteration**

| Customer note ID | Extracted phone number | Extraction status |
|---:|---|---|
| 1 | 0212345678 | Matched |
| 2 | 0412345678 | Matched |
| 3 |  | No phone detected |
| 4 | 0298765432; 98765432 | Matched |
| 5 |  | Rejected as likely order number |
| 6 | 0412345678 | Matched |

The important point is not the exact pattern. The important point is the discipline of iteration.

Finding the best pattern is an iterative process:

1. Define a rough pattern.
2. Inspect the match set for false matches.
3. Inspect the reject set for false rejects.
4. Adjust and repeat.

Each adjustment changes the match set and reject set. It is usually better to tighten or loosen one thing at a time, then inspect the result.

The key idea is that focusing only on matches creates a blind spot. The rejected records are equally significant. A useful pattern is found by examining both incorrect matches and incorrect rejects.

### Step 2—Random validation

Random validation closes the quality gap where approximate logic looks plausible, but has not been checked against independent judgement.

Once the pattern has been tuned, it should be validated by a business expert.

This is done by randomly sampling records from both the match set and the reject set.

The sample must be unbiased. It should not focus only on records where the engineer has low confidence, nor only on records that seem easy to validate. The point is to test the pattern across its full range of behaviour.

For example, the data engineer may extract phone numbers from 50,000 customer notes. The pattern may return 18,000 notes with phone numbers and 32,000 notes without phone numbers. The validation sample should include records from both groups.

**Example validation sample**

| Sample ID | Source set | Customer note | Pattern result | Expert judgement | Validation outcome |
|---:|---|---|---|---|---|
| 1 | Match set | Mobile is 0412345678. | Phone found | Phone present | Correct match |
| 2 | Match set | Order 12345678. Please follow up. | Phone found | No phone present | False match |
| 3 | Reject set | Call through reception on 98765432. | No phone found | Phone present | False reject |
| 4 | Reject set | Address is 12 Hill Street. | No phone found | No phone present | Correct reject |

The validation result can then be summarised.

**Example validation summary**

| Validation outcome | Count |
|---|---:|
| Correct match | 86 |
| False match | 6 |
| Correct reject | 92 |
| False reject | 16 |

This tells the data engineer how the approximation behaves. It may be good enough for some purposes and not good enough for others.

If the business only needs a rough indication of whether contact details are likely to be present, this may be acceptable. If the extracted phone number will be used for direct customer contact, the tolerance for false matches and false rejects will be much lower.

This is why fuzzy logic still depends on business intent. The question is not whether the pattern is perfect. The question is whether the pattern is good enough for the decision or action it supports.

This validation process should be repeated periodically. Even if the pattern was correct at the time of implementation, changes in business processes or user behaviour may cause it to degrade.

Regular validation helps ensure the pattern continues to serve its intended purpose.

### Step 3—Monitoring for drift

Monitoring for drift closes the quality gap where an approximation was once good enough, but may stop behaving as intended over time.

In practice, random validation cannot be performed continuously. Drift monitoring provides a lightweight alternative.

The idea is to identify a statistic that should remain relatively stable over time. If the statistic changes significantly, the pattern may no longer be behaving as expected.

For example, suppose a free-text field is used to extract phone numbers. Not all extracted numbers will match the customer database, but a certain percentage—say 85%—typically do. This percentage reflects the stability of the pattern.

The data engineer can monitor this statistic over time.

**Example drift monitoring**

| Month | Notes processed | Notes with extracted phone number | Extracted phone match rate |
|---|---:|---:|---:|
| 2025-01 | 12,400 | 4,820 | 86% |
| 2025-02 | 13,100 | 5,040 | 85% |
| 2025-03 | 12,850 | 4,910 | 84% |
| 2025-04 | 13,300 | 5,110 | 85% |
| 2025-05 | 13,050 | 7,900 | 61% |

A sudden drop from the usual range may indicate that the pattern is no longer behaving as expected.

Users may have started entering phone numbers in a new format. The source system may have changed its note template. Another number, such as a case number or ticket number, may have started appearing near phone-like words. The customer database may also have changed, reducing the apparent match rate.

This is a form of assumption monitoring. The assumption is that the extracted values will continue to resemble the known population. If the assumption fails, the pattern may need to be revisited.

Drift monitoring is especially useful when the business has a relatively static reference point, such as a customer table, a list of known codes, or a set of standard formats. However, any stable statistic can be used.

Useful drift statistics may include:

- percentage of records matched;
- percentage of extracted values that match a known reference table;
- number of distinct extracted values;
- proportion of records with multiple extracted values;
- proportion of records requiring manual review;
- proportion of null or rejected records.

## Key ideas

> [!NOTE]
> **Key ideas**
>
> Data quality is fitness for business intent, not perfect correspondence with reality.
>
> Different intents create different quality requirements.
>
> Human curation is appropriate when business judgement is needed.
>
> Precise rules are appropriate when business intent can be formalised.
>
> Fuzzy logic is appropriate when business intent can only be approximated.
>
> All three approaches depend on monitoring assumptions.