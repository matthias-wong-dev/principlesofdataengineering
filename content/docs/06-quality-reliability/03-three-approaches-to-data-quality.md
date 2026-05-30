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

Human curation is appropriate when business judgement is needed and the data engineer should not pretend the answer can be fully inferred by the system.

### Data annotation

The most common form of human curation is data annotation.

For example, a digital system may record sale locations as entered by store address. A business expert may later annotate these locations into sales regions or company sites. This annotation occurs in the data pipeline, not the source system, and is commonly known as reference data management.

Another example is harmonising employee identities across systems. In large organisations, the same employee may appear under different accounts for different business processes. A business expert who understands the enterprise view may annotate these accounts to map them to a canonical representation. This is known as master data management.

Human annotation extends beyond reference and master data. It applies wherever a human can interpret records outside the operational context.

There are two legitimate views of data: one fast-paced and operational, suited to digital systems; the other reflective and analytical, suited to business interpretation. Both may require human input. It is not reasonable to expect operational systems to carry the full load of analytical meaning.

Traditionally, data warehousing has treated human curation as an exception. But if human editing can be implemented transparently, with control and auditability, it should be treated as a standard business tool.

Whether the curation concerns reference data, master data, or other forms of annotation, the data engineer must monitor for incoming records that require curation. Examples include uncategorised store locations, unmapped employee accounts, or new values that do not yet belong to a known category.

### Applying assumptions

Another way for business experts to intervene in data quality issues is to apply assumptions and act when those assumptions are violated.

Consider the recording of dates. If users manually enter dates, they may accidentally type 2300 instead of 2030. If the digital system lacks validation, such errors can end up in the database. Even a single mistake can distort a line chart or skew time-based analysis.

One way to address this is to assume that future dates must be within 50 years. Dates outside this range are treated as invalid and converted to null. This assumption should be monitored. If it is violated, an alert should prompt a business expert to correct the source data.

Another example is assuming uniqueness. If data entries are almost always unique, but occasional duplicates occur, the pipeline can assume uniqueness, ignore duplicates, and monitor for violations. If duplicates appear, a business expert can intervene at the source.

This approach works best when violations are rare and the business expert can correct the issue before the next batch load. It is suitable for irregular data quality issues that do not require bulk remediation.

If data quality issues are frequent or systemic, a data quality report may be more appropriate.

### Data quality report

Data quality reports are suitable when issues are frequent, numerous, or easier to treat in bulk on a periodic basis.

An effective implementation is to create a combination or choice dimension. A combination dimension may include one column per issue and describe each transaction. For example, a dimension called `'Sales data quality'` might include `[Is missing sales amount]`, `[Is invalid sales date]`, `[Is unknown customer]`, and so on.

Coupled with the ID dimension, this makes it easy to build a Power BI report that surfaces transactions requiring remediation by a business expert.

A data quality dimension also supports systematic analysis by enabling statistics on the number and type of issues.

Reports are only effective if they embed in the user’s workflow. A decontextualised report becomes forgotten and unused. The same applies to data quality reports. The business should have a workflow trigger that prompts engagement with the report.

Human curation closes the quality gap by allowing business judgement to enter the data product. Its main monitoring need is to detect new records that require curation.

## Precise rules: when intent can be formalised

Translating business knowledge into precise rules allows it to be automated and reduces reliance on human intervention.

One way to look at these rules is to see them as “fixing issues” in the data. A more useful way is to see them as rules that bridge recorded data to business intent.

Precise rules are appropriate when the business can say what should happen clearly enough for the data engineer to implement it.

This chapter covers four recurring types of precise rule:

1. Defining analytical concepts
2. Defining primary keys
3. Defining the primary record
4. Defining relationships

### Defining analytical concepts

Since business insight is information analysed in light of business intent, a direct way of improving data quality is to define the analytical concept that the business needs.

This concept becomes a lens through which the data is interpreted. It allows users to see the data in a way that is more expressive of business intent.

#### Good and bad entities

A common example is defining “good” and “bad” entities.

A business process may collect detailed information such as audit results, inspection results, incidents, sentiment, or sales volume. However, these details may not yet be formalised into a systematic judgement.

Sometimes numeric values such as star ratings need to be translated into good and bad using thresholds. More commonly, a business process records information at a lower grain that needs to be rolled up to the entity of interest.

For example, a manufacturing batch may have multiple quality-control criteria. The business may decide that failing one critical criterion, or multiple non-critical criteria, defines failure at the batch level.

This closes the quality gap between detailed operational outcomes and the business’s need for a usable judgement.

It is not reasonable to expect operational systems to always define these concepts. Their primary job is to execute workflows while preserving records. The data engineer plays a role by adding the analytical lens.

#### Milestones

Milestones are another important analytical definition.

A business process may have many detailed steps, some of which loop back. This mass of steps can bury insight in operational detail. A useful analytical view is to define major milestones that can be used to measure performance.

To be useful, milestones should be limited in number. More importantly, each milestone should be associated with a specific control point or responsible owner who can act on the timeliness of reaching that milestone.

To deal with loops, the data engineer can define the earliest and latest time each event occurs.

Milestones close the quality gap between messy workflow events and meaningful process control. This pattern is studied in [Meaningful fragments](/docs/creating-information/meaningful-fragments/).

#### Conformed dimensions

Another analytical concept is the conformed dimension.

A large organisation may have many processes, and many of them share similar concepts under different names. A conformed dimension reconciles these local concepts into a shared view.

When done appropriately, a conformed view can empower decision-makers at the most senior levels of the organisation.

Conformed dimensions close the quality gap between local system categories and enterprise intent.

Defining analytical concepts takes [leadership and negotiation skill](/docs/foundations/data-and-organisations/). The data engineer is often well placed to broker between stakeholder groups by experimenting with the data and visually communicating possible outcomes.

### Defining primary keys

Primary keys serve as the link between data records and their counterparts in the real world. Unfortunately, some business processes do not rigorously define primary keys.

This can lead to slippery definitions in the database. In other cases, the primary key is defined at the application layer but remains invisible at the data layer, leaving the business user without a clear way to interpret the data.

The data engineer should establish the primary key where it is not meaningfully defined.

The primary key articulates the data engineer’s view of how the data row should be interpreted as a business entity.

Most primary keys can be traced by examining how a business process creates, retrieves, and updates a data record. Three common patterns are sequence numbers, version numbers, and temporality.

#### Sequence numbers

Sequence numbers are useful when a header has multiple detail rows and the detail table lacks a meaningful primary key.

For example, a sales order may have multiple items. The order is stored in `Sales`, with `[Order number]` as the primary key. The items are stored in `SalesItems`, which may be a miscellaneous list without a meaningful key.

If each product can appear only once, then `[Order number]` and `[Product ID]` may suffice as a primary key. But if a product can appear more than once, this fails.

A simple solution is to treat the list of items as a sequence and create an artificial column `[Sales item sequence number]`, forming the key `[Order number]`, `[Sales item sequence number]`.

Sometimes a system will implement a meaningless key such as `[Sales item ID]`, a simple integer used for UI or database constraints. Even in these cases, the data engineer may still define a sequence number and use `[Order number]`, `[Sales item sequence number]` as the business-facing primary key. `[Sales item ID]` can be retained for joins.

In general, sequence numbers are effective wherever there is a miscellaneous list of line items within a header. Care must be taken to ensure the sequence is deterministic by breaking ties—using a surrogate key like [Sale items ID] as a sort order is a reliable approach.

#### Version numbers

Version numbers are useful for entities whose changes should be preserved as new versions.

For example, a customer order may be submitted, revised, and resubmitted before it is fulfilled. The business may still regard this as the same order, but each revision changes the content that was true at a particular point in time.

The data engineer may model this using `[Order ID]`, `[Order version number]`.

Digital systems are not always consistent in how they manage versions. A common but problematic approach is to allow the entity ID to change each time the record is revised and record the relationship using `[Previous order ID]` or `[Superseded order ID]`. This may work for rendering a web UI but can cause confusion in analysis.

Where versioning is lost or muddled, the data engineer can restore clarity using a consistent pattern such as `[Entity ID]`, `[Version number]`.

Version numbers close the quality gap where the source system records change, but does not make the continuity of the entity clear.

#### Temporality

Temporality refers to tracking changes over time. In data warehousing, this is commonly handled through type II tracking.

Some business processes are designed to handle only the current event, without tracking history. But when the business is interested in change over time, the entity is mutable.

Mutable entities should usually be expressed through a primary key that includes a time component. The data engineer may define the key as `[Entity ID]`, `[Start datetime]`, with `[End datetime]` marking the end of the validity period.

This is especially important if an entity can be deleted and recreated, because the start of one row is not necessarily the end of the previous row.

Recovering temporality depends on how history is stored. Sometimes it is available in audit tables. Sometimes it must be reconstructed with help from business experts.

Temporality closes the quality gap where the business needs historical interpretation but the source system only presents the current state.

### Defining the primary record

Defining the primary record is related to defining primary keys, but it solves a different problem.

This occurs when the database has primary keys, but different primary keys relate to the same underlying entity. It is common in business processes that gather decentralised observations.

Consider the example of whale sightings. A database may collect observations from citizen scientists, stored in `Whale.Observation`, with `[User ID]`, `[Observation number]` identifying each user’s submissions. A surrogate key such as `[Observation ID]` may also exist for system retrieval.

Multiple citizens may report sightings of the same whale. As a result, multiple `[Observation ID]` values relate to the same real-world entity.

Suppose the business has a rule such as: "A whale species at one GPS proximity should only appear once within a day."

This rule can be used to group observations and identify a representative record.

The data engineer can express this by identifying the primary observation. For example, the pipeline may select the first observation of the day at a location and store it as `[Primary observation ID]` in a table called `Whale.PrimaryObservation`.

This table might contain `[Observation ID]` and `[Primary observation ID]`, where `[Observation ID]` is the key for the original record and `[Primary observation ID]` identifies the chosen representative.

Subsequent transformation can focus on the `[Primary observation ID]` grain. The same key can also be used in Power BI to return the true count of whale sightings.

Care must be taken to resolve race conditions. If two users submit observations at the same time, only one record should be selected as primary. This can be resolved deterministically using a surrogate key such as `[Observation ID]`.

Defining the primary record closes the quality gap between multiple observations and one underlying entity.

### Defining relationships

Digital systems are usually good at recording relationships needed by operational workflows. They are less reliable at recording relationships that are useful for analysis.

This is especially common when the system is designed for operational efficiency rather than analytical understanding.

The data engineer can sometimes close this quality gap by defining relationships that the source system did not record.

Two useful techniques are:

- nearest temporal joins;
- mapping tables.

#### Nearest temporal join

Sometimes two sets of events are related, but the relationship is not recorded as a database key.

If business knowledge suggests that one set of events is expected to precede another, the relationship can sometimes be recovered by identifying the nearest preceding event. This technique is known as a nearest temporal join.

Consider a lounge where members check in and may then make purchases at the bar.

The check-in is recorded by the door scanner with `[Member ID]`, `[Check-in datetime]`, and `[Membership level]`. This is stored in `Club.Checkin`. There is a surrogate key `[Check-in event SK]`.

Purchases are recorded separately at the register. These are stored in `Club.Purchase`, with `[Member ID]`, `[Purchase datetime]`, and `[Purchase item]`. There is a surrogate key `[Purchase event SK]`.

Although both tables contain `[Member ID]`, there is no direct relationship between a specific check-in and the purchases made during that visit. The system does not record which check-in a purchase belongs to. This makes it difficult to identify the membership level associated with the purchase.

To support analysis, the data engineer can create a link using a nearest temporal join.

For example, the rule might be: "A purchase belongs to the most recent check-in by the same member that occurred before the purchase."

The result can be stored in `Club.PurchaseCheckin` as a two-column table of `[Purchase event SK]` and `[Check-in event SK]`.

One implementation is to identify the latest check-in for each purchase using a `max()` aggregation, then join back to retrieve the check-in event.

Another approach is to consider each check-in as a window from one check-in to the next, and for each purchase, find the corresponding check-in window.

This table re-establishes the relationship between the purchase event and the check-in event.

Nearest temporal joins are especially valuable at the macro level, where business processes operate in bulk and lack unit-level linkage.

For example, seed suppliers may distribute large batches to farms, and harvest yields may later be reported in aggregate. Individual bags of seed are not tracked, but the business may still need to understand how seed characteristics such as supplier or variety affect outcomes. In such cases, the data engineer can define keys for seed batches and yield events, then use nearest temporal joins to associate each yield with the most recent relevant seed delivery.

Similar patterns arise in regulatory compliance. Businesses may submit periodic declarations or claims, while auditors conduct inspections or reviews later. These audits are not tied to specific submissions but are temporally related. Nearest temporal joins allow the business to associate each audit with the most recent relevant declaration, enabling analysis of compliance patterns over time.

Nearest temporal joins close the quality gap between related events whose relationship was not explicitly recorded.

#### Mapping tables

Mapping tables are introduced when the original system does not record relationships needed for analysis.

A common scenario is a header table with two separate detail tables at different grains. Both detail tables relate to the header, but not to each other.

The data engineer may introduce a mapping table between them based on a business rule.

Consider a club restaurant with data captured in three tables:

- `Club.TableSitting`—records of customers seated at the restaurant, one per sitting, keyed by `[Table sitting ID]`
- `Club.TableCustomer`—club members identified by `[Member ID]`, linked to `[Table sitting ID]`
- `Club.TableFoodOrder`—menu items ordered per `[Table sitting ID]`, with food items identified by `[Food item ID]`

The system does not record which member ordered which item. For analysis, the business may wish to associate members with food items. However, this relationship is not captured in the source system.

To support analysis, the data engineer may introduce a mapping table called `Club.CustomerFoodOrderMap`, with `[Table sitting ID]`, `[Member ID]`, and `[Food item ID]`.

The logic may be based on a business rule such as: "Every member at the table shares the cost of all items ordered."

For implementation, the data engineer can join `Club.TableCustomer` and `Club.TableFoodOrder` on `[Table sitting ID]`.

Because a food item can be ordered multiple times, `[Table sitting ID]`, `[Member ID]`, and `[Food item ID]` do not yet form a primary key. Additional grouping is needed. The pipeline may calculate `[Food item occurrences]`, the number of times the food item was ordered at the table, and `[Number of members]`, the number of members seated at the table.

The ratio of these values can be used as distribution weights in subsequent calculations.

Because the relationship is inferred rather than recorded, it should be tested. Techniques for validating mapping logic are described in [Tests and assumptions](/docs/quality-reliability/tests-and-assumptions/).

Mapping tables close the quality gap between entities that must be related analytically but are not related operationally.

Precise rules close data quality gaps by turning business intent into repeatable logic. Their main monitoring need is to detect rule violations, edge cases, and changes in the business process that make the rule unsafe.

## Fuzzy logic: when intent can only be approximated

There are cases where precise rules do not apply.

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

A useful way to think about fuzzy logic is through loose–tight iteration.

Every pattern has matches and rejects. The matches are records that meet the criteria. The rejects are records that do not.

The data engineer tunes the pattern by adjusting the criteria:

- tightening to reduce over-matching;
- loosening to recover missed records.

The goal is not to maximise matches. The goal is to reduce mistakes on both sides.

Consider the example of extracting phone numbers from a free-text field. Phone numbers may appear in formats such as `(02) 1234 5678`, `0412345678`, `12345678`, or `02-1234-5678`.

The challenge is that the field may also contain other numbers, such as invoice numbers or dates.

Finding the best pattern is an iterative process:

1. Define a rough pattern.
2. Inspect the match set for false matches.
3. Inspect the reject set for false rejects.
4. Adjust and repeat.

Start with a simple pattern that captures the most obvious cases. This produces a match set and a reject set.

The match set should be inspected for false matches. For example, the pattern may pick up numeric strings that are not phone numbers. If so, tighten the pattern.

The reject set should be inspected for false rejects. For example, valid mobile numbers or hyphenated formats may have been excluded. If so, loosen the pattern.

Each adjustment changes the match set and reject set. It is usually better to tighten or loosen one thing at a time, then inspect the result.

The key idea is that focusing only on matches creates a blind spot. The rejected records are equally significant. A useful pattern is found by examining both incorrect matches and incorrect rejects.


### Step 2—Random validation

Once the pattern has been tuned, it should be validated by a business expert.

This is done by randomly sampling records from both the match set and the reject set.

The sample must be unbiased. It should not focus only on records where the engineer has low confidence, nor only on records that seem easy to validate. The point is to test the pattern across its full range of behaviour.

This process should be repeated periodically. Even if the pattern was correct at the time of implementation, changes in business processes or user behaviour may cause it to degrade.

Regular validation helps ensure the pattern continues to serve its intended purpose.

### Step 3—Monitoring for drift

In practice, random validation cannot be performed continuously. Drift monitoring provides a lightweight alternative.

The idea is to identify a statistic that should remain relatively stable over time. If the statistic changes significantly, the pattern may no longer be behaving as expected.

For example, suppose a free-text field is used to extract phone numbers. Not all extracted numbers will match the customer database, but a certain percentage—say 85%—typically do. This percentage reflects the stability of the pattern.

If it drops to 60%, users may have started entering phone numbers in a new format, or the pattern may be picking up irrelevant content.

This is a form of assumption monitoring. The assumption is that the extracted values will continue to resemble the known population. If the assumption fails, the pattern may need to be revisited.

Drift monitoring is especially useful when the business has a relatively static reference point, such as a customer table, a list of known codes, or a set of standard formats. However, any stable statistic can be used.

Fuzzy logic closes data quality gaps by approximating business intent where exact rules are not available. Its main monitoring need is to detect drift in match rates, validation results, or alignment with a known reference.

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