---
title: Meaningful fragments
url: /docs/creating-information/meaningful-fragments/
description: Explains fragment modelling as the discipline of building narrow, reusable information blocks instead of large all-purpose tables.
lede: Fragment modelling makes complex business meaning easier to build, test, reuse, and change.
weight: 9
---

## Fragment modelling

The earlier chapters introduced entity processing, entity tracking, reference data, conforming systems, and storytelling. Each depended on the same discipline: break complexity into individual fragments and connect them deliberately. 

This approach is **fragment modelling**.

This chapter closes the section on creating information by making fragment modelling explicit. It steps back from those specific patterns and names the broader practice. It then introduces additional fragment patterns that commonly appear in real business pipelines: milestones, current-version selectors, timelines, mappings, distribution weights, and hubs.

The key idea is summarised by the second principle of data engineering:

> Instead of building giant tables, create meaningful fragments.

## Why giant tables fail

New engineers often build giant tables to answer queries. This feels convenient because everything is in one place, and there are fewer artefacts to create and deploy.

However, the convenience is temporary.

Wide tables accumulate unrelated meanings. Business logic becomes buried and entangled. Change detection becomes harder because every column is treated as part of the same object. Being wide, they also become a magnet for dependencies for downstream use, creating additional risks.

The result is a pipeline that looks simple from far away and becomes fragile up close.

## Meaningful fragments

Fragment modelling takes the opposite approach.

A **meaningful fragment** is a narrow table that packages one reusable piece of business meaning. Each fragment should answer a clear question:

> What information does this table create?

The fragment then isolates the calculation of this information to its own table, and gives the table an expressive name. 

By packaging up complex calculation into a meaningful fragment, it becomes operable.

Consistent use of meaningful fragments makes the pipeline easier to understand, test, change, and reuse.

### Restaurant analogy

Fragment modelling is like *mise en place* in a restaurant kitchen.

The raw data are the whole potatoes and unwashed greens. Fragments are the prepared ingredients: chopped vegetables, cured sauces, and marinated proteins. They are not the final dish, but they make service possible.

A good pipeline works the same way. Once the fragments are well prepared, insights can be assembled quickly, consistently, and without repeating the same preparation work.

### The impact on legibility

A further benefit of meaningful fragments is legibility.

Creating a fragment and giving it a name elevates a concept into a first-class object within the warehouse. Users become aware that the concept exists and can discover it through the schema itself.

For example, milestone datetimes could be implemented as additional columns within `Cake.Sales`. While technically correct, users browsing the warehouse may not realise that milestone information has been prepared and curated. By creating a dedicated `Cake.SalesMilestone` fragment, the concept becomes visible. The table name itself communicates that milestones are important and available for use.

In this sense, fragments do more than package information for easy operability. They help communicate the structure of the business domain. A well-designed warehouse is not merely a collection of tables, but a map of the concepts that the organisation has chosen to recognise.

## Symptoms of poor fragmentation

When meaningful fragments are missing, the symptoms are usually visible:

- the same logic appears repeatedly in `where` clauses, joins, reports, or measures;
- tables become wider as constructed columns are bolted onto fact tables;
- reference data is duplicated into transaction tables;
- users need excessive joins, filters, and deduplication to answer basic questions;
- complex transformations are hidden inside one large table;
- small changes create large downstream effects.

These symptoms indicate that the pipeline has not been decomposed into its minimal informational components, and made easy for access.

## Common fragment patterns

The following examples illustrate common fragment patterns. They are not exhaustive. Any self-contained piece of reusable business meaning can become a fragment.

### Summaries of details and storytelling

Complex business processes generate detail rows that must be summarised to become useful. The computation for these summaries can be complex and should be placed in a separate fragment rather than compounded onto existing tables.

For example, a cake may undergo multiple inspections.

**`Cake.InspectionResult`**

| Inspection ID | Cake ID | Inspection result |
|---|---|---|
| I1001 | C1001 | Excellent cake |
| I1002 | C1001 | Good cake |
| I1003 | C1001 | Good cake |
| I1004 | C1002 | Good cake |
| I1005 | C1002 | Spoiled cake |

The business may only need to know whether the cake had a bad result.

**`Cake.CakeStory`**

| Cake ID | Is bad cake |
|---|---|
| C1001 | false |
| C1002 | true |

The fragment turns scattered detail into entity-level meaning.

This is a special case of the the storytelling dimension studied in the last chapter. 

Once computed, the storytelling dimension and the fragment often becomes the primary window through which the business sees the data.

It may become the default filter in reports and queries because it lets users stay at the grain of the entity of interest. They do not need to go lower into subprocess tables, joining across grain, and risk double-counting or inconsistent logic.

Thus, the storytelling fragment absorbs that complexity once, so ordinary queries can remain simple. Across a warehouse with many users, the option to skip over the detailed grain can vastly reduce errors and improve maintenance.

### Milestone datetimes

Business is always interested in measuring the time between milestones. This can be difficult if steps repeat or spread across multiple tables. The data engineer can add value by precomputing these milestones into a dedicated fragment.

A milestone datetimes fragment is simply a table at the grain of the entity of interest, with one datetime column per milestone.

A help desk may want to know when a case was received, escalated, and closed.

**`Helpdesk.CaseEvent`**

| Case ID | Event | Datetime |
|---|---|---|
| H1001 | Received | 2025-01-10 09:05 |
| H1001 | Escalated | 2025-01-11 11:20 |
| H1001 | Closed | 2025-01-12 15:40 |

This can be simplified into a milestone fragment.

**`Helpdesk.CaseMilestone`**

| Case ID | Received datetime | Escalated datetime | Closed datetime |
|---|---|---|---|
| H1001 | 2025-01-10 09:05 | 2025-01-11 11:20 | 2025-01-12 15:40 |

The fragment makes duration calculations straightforward and avoids repeated event-processing logic throughout the model.

Milestone tables are also known as accumulating snapshots in dimensional modelling.

### Current or primary version

Many entities have multiple versions. The full version history may be useful for audit or lineage, but the business often needs the current or primary version.

In many systems, this logic is handled in the application tier and is not obvious in the database. A fragment makes this explicit.

**`Sales.CustomerVersion`**

| Customer ID | Version | Customer name |
|---|---:|---|
| C1001 | 1 | John Smith |
| C1001 | 2 | John A. Smith |

A fragment can isolate the selection logic.

**`Sales.CurrentCustomerVersion`**

| Customer ID | Current version |
|---|---:|
| C1001 | 2 |

Users can then retrieve the current state without reconstructing the version-selection rule.

This is one case where fragment modelling can reduce immediate expressiveness if naming is poor. Most users do not expect to retrieve a row from one table and then consult another table to find whether it is current. The data engineer should compensate by naming the main table clearly, for example by using `version` in the table name or key columns.

### Timeline and end-of-period

When entities change over time, users often need consistent point-in-time views. This can be error-prone for users when the attributes are spread across multiple tables, because joins require careful handling of time conditions. The data engineer can make these results easily accessible through corresponding fragments.

The relevant fragments—timelines and end-of-period tables— are discussed in [Entity tracking](/docs/creating-information/entity-tracking/).

### Mapping

Business processes often do not record relationships at the grain required for analysis. 

Sometimes this granularity is impractical because processes do not operate in the neat way expected by the business.

Sometimes the recording is imperfect, such as through nearest temporal join. These relationships can be approximated using fuzzy logic.

These are often many-to-many relationships. Adding foreign key columns to the core tables would disturb their grain. 

Rather than including complex code in core tables, or disturbing their grain, the mapping can be stored in separate fragments. These are two-column tables with foreign keys pointing to each primary table. This is the mapping table.

For example, the business may want to relate sales to production batches, even though the source system does not record the link directly.

**`Cake.SalesProductionMap`**

| Sales ID | Production ID |
|---|---|
| S1001 | P5501 |
| S1002 | P5501 |
| S1003 | P5502 |

Rather than disturbing the grain of either table, the relationship is represented in its own fragment.

### Distribution weights

Sometimes a value is recorded only in aggregate form. However, the business wants to understand that value at the detail level and proposes a rule for distributing it. This logic can be complex and should be calculated in its own fragment. This is the distribution weights table.

Suppose a system records total effort for a work package.

**`Cake.WorkPackageEffort`**

| Work package ID | Total work hours |
|---|---:|
| WP1001 | 100 |
| WP1002 | 80 |

The same work package contains multiple tasks, but the system does not record actual effort per task.

**`Cake.Task`**

| Task ID | Work package ID | Task type | Worker | Task start datetime |
|---|---|---|---|---|
| T1001 | WP1001 | Design | Alex | 2025-01-10 09:00 |
| T1002 | WP1001 | Build | Priya | 2025-01-10 13:00 |
| T1003 | WP1001 | Test | Mei | 2025-01-11 10:00 |
| T2001 | WP1002 | Design | Alex | 2025-01-12 09:00 |
| T2002 | WP1002 | Build | Priya | 2025-01-12 14:00 |


The business may define a rule for distributing the total effort across tasks. The result should be stored as a fragment.

**`Cake.TaskWeight`**

| Task ID | Estimated work hours |
|---|---:|
| T1001 | 50 |
| T1002 | 30 |
| T1003 | 20 |
| T2001 | 35 |
| T2002 | 45 |

The fragment does not claim that the source system directly recorded these task-level hours. By placing the allocation in its own table, and naming the column appropriately, the data engineer keeps the assumption visible, testable, and replaceable.

In many cases, mapping tables and distribution weights may be combined if their ambiguities stem from the same business phenomenon.

A common variation occurs when the detailed records contain repeated item types, while the measure is recorded only at the header level.

Suppose a restaurant records the bill amount by table.

**`Restaurant.TableBill`**

| Table ID | Bill month | Bill amount |
|---|---|---:|
| T1001 | 2025-01 | 120.00 |
| T1002 | 2025-01 | 80.00 |

The table also records drink orders.

**`Restaurant.DrinkOrder`**

| Table ID | Drink item |
|---|---|
| T1001 | Beer |
| T1001 | Wine |
| T1001 | Wine |
| T1001 | Spirits |
| T1002 | Wine |
| T1002 | Wine |

If the business assumes each drink order has equal value, the data engineer can create a distribution-weight fragment.

**`Restaurant.DrinkOrderWeight`**

| Table ID | Drink item | Item order count | Total order count |
|---|---|---:|---:|
| T1001 | Beer | 1 | 4 |
| T1001 | Wine | 2 | 4 |
| T1001 | Spirits | 1 | 4 |
| T1002 | Wine | 2 | 2 |

The final two columns can be used as a fractional weight. For example, `T1001` has a bill amount of `120.00`, and wine accounts for `2 / 4` drink orders, so the estimated wine value is `60.00`. This also simplifies whole-of-month measures at the item level. A monthly estimate of wine sales can be calculated without repeatedly scanning and counting the raw order rows.

### Hubs

A hub creates a consistent surrogate key for the same entity appearing across multiple systems.

This is a concept from the Data Vault method of data warehousing, but it is also useful as a fragment pattern. The hub centralises identity logic that should not belong to any one subsystem.

For example, multiple systems may record staff by first name and last name.

**`Payroll.Staff`**

| Payroll staff ID | First name | Last name |
|---|---|---|
| P1001 | Jane | Smith |
| P1002 | John | Wong |
| P1003 | Alex | Spelic |

**`Training.Staff`**

| Training staff ID | First name | Last name |
|---|---|---|
| T884 | Jane | Smith |
| T921 | John | Wong |
| T312 | Mary | Zimm |

A hub table assigns a consistent surrogate key to the shared identity.

**`Workforce.HubId`**

| Staff SK | First name | Last name |
|---:|---|---|
| 1001 | Jane | Smith |
| 1002 | John | Wong |
| 1003 | Alex | Spelic |
| 1004 | Mary | Zimm |

This key can then be used for light anonymisation, relationship modelling, or downstream tools such as Power BI.

The hub belongs to no single subsystem. It is a central fragment where pairing and key assignment occur.

## The discipline of meaningful fragments

Fragment modelling is a discipline of decomposition.

The data engineer looks at a data product and asks:

- What are the entities?
- What meanings are being created?
- Which computations are complex enough to isolate?
- Which relationships should not be forced into core tables?
- Which pieces of information need to be reused?
- Which dependencies should be delayed or reduced?

A meaningful fragment is justified when it creates business meaning, isolates complexity, reduces dependency, supports reuse, or makes change easier to manage.

In practice, anything can become a meaningful fragment. It does not need to fall under a predefined category. If the information is self-contained and its creation is justified by business meaning, complex computation, or dependency management, it belongs in its own place.

This is one of the hallmarks of mature data engineering: the ability to see a data product not as a pile of tables, but as a set of minimal informational components.

## Key ideas

> [!NOTE]
> **Key ideas**
>
> The second principle of data engineering—Instead of building giant tables, create meaningful fragments.
>
> A meaningful fragment is a narrow table with a specific informational purpose.
>
> Fragments isolate complex computation, reduce dependencies, support reuse, and make change easier to manage.
>
> Common fragment patterns include storytelling summaries, milestones, current-version selectors, timelines, mappings, distribution weights, and hubs.
>
> Mature data engineering depends on seeing the data product as a set of minimal informational components.