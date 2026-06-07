---
title: Meaningful fragments
url: /docs/creating-information/meaningful-fragments/
description: Explains fragment modelling as the discipline of building narrow, reusable information blocks instead of large all-purpose tables.
lede: Fragment modelling makes complex business meaning easier to build, test, reuse, and change.
weight: 8
---

## Fragment modelling

The earlier chapters introduced [entity processing](/docs/creating-information/entity-processing/), [entity tracking](/docs/creating-information/entity-tracking/), [reference data](/docs/creating-information/reference-data/), [conforming systems](/docs/creating-information/conforming-systems/), and [storytelling](/docs/creating-information/storytelling/). Each depended on the same discipline: break complexity into individual fragments and connect them deliberately. 

This approach is **fragment modelling**.

This chapter closes the section on creating information by making fragment modelling explicit. It steps back from those specific patterns and names the broader practice. It then introduces additional fragment patterns that commonly appear in real business pipelines: milestones, current-version selectors, timelines, mappings, distribution weights, and hubs.

The key idea is summarised by the [second principle of data engineering](/docs/creating-information/expressiveness-and-fragment-modelling/#fragment-modelling):

> [!SHARE:instead-building-giant]
> Instead of building giant tables, create meaningful fragments.

## Why giant tables fail

New engineers often build giant tables to answer queries. This feels convenient because everything is in one place, and there are fewer artefacts to create and deploy.

However, the convenience is temporary.

Wide tables accumulate unrelated meanings. Business logic becomes buried and entangled. Change detection becomes harder because every column is treated as part of the same object. Being wide, they also become a magnet for dependencies for downstream use, creating additional risks.

The result is a pipeline that looks simple from far away and becomes fragile up close.

## Meaningful fragments

Fragment modelling takes the opposite approach.

A **meaningful fragment** is a narrow table that packages one reusable piece of business meaning. Each fragment should answer a clear question:

> [!SHARE:information-table-create]
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

{{< svg >}}
<svg xmlns="http://www.w3.org/2000/svg"
     width="980" height="700"
     viewBox="0 0 980 700"
     style="display:block;width:100%;max-width:44rem;height:auto;background:transparent"
     role="img"
     aria-label="Figure 1 comparing one giant Sales.Everything table and meaningful analytical fragments around Sales">

  <defs>
    <marker id="arrowhead-meaningful-fragments-sales-v4" markerWidth="10" markerHeight="8"
            refX="10" refY="4" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L10,4 L0,8 z" fill="#222222"/>
    </marker>

    <style>
      .mf-title-sales-v4 {
        font-family: Inter, Segoe UI, Roboto, Arial, sans-serif;
        font-size: 21px;
        font-weight: 700;
        fill: #111111;
      }

      .mf-label-sales-v4 {
        font-family: Inter, Segoe UI, Roboto, Arial, sans-serif;
        font-size: 15px;
        font-weight: 700;
        fill: #111111;
      }

      .mf-small-sales-v4 {
        font-family: Inter, Segoe UI, Roboto, Arial, sans-serif;
        font-size: 13px;
        fill: #333333;
      }

      .mf-mono-sales-v4 {
        font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
        font-size: 11px;
        fill: #333333;
      }

      .mf-box-sales-v4 {
        fill: #ffffff;
        stroke: #222222;
        stroke-width: 2;
      }

      .mf-lightbox-sales-v4 {
        fill: #ffffff;
        stroke: #999999;
        stroke-width: 1.5;
      }

      .mf-line-sales-v4 {
        stroke: #999999;
        stroke-width: 1.1;
      }

      .mf-link-sales-v4 {
        stroke: #222222;
        stroke-width: 1.7;
        fill: none;
        marker-end: url(#arrowhead-meaningful-fragments-sales-v4);
      }

      .mf-arrow-sales-v4 {
        stroke: #222222;
        stroke-width: 2;
        fill: none;
        marker-end: url(#arrowhead-meaningful-fragments-sales-v4);
      }
    </style>
  </defs>

  <!-- Title -->
  <text x="70" y="48" class="mf-title-sales-v4">From one giant table to meaningful fragments</text>
  <text x="70" y="74" class="mf-small-sales-v4">A meaningful fragment isolates one informational purpose around an entity of interest.</text>

  <!-- Left heading -->
  <text x="90" y="122" class="mf-label-sales-v4">Shallow curation</text>
  <text x="90" y="145" class="mf-small-sales-v4">Many purposes are collapsed into one wide table.</text>

  <!-- Left big table -->
  <rect x="90" y="175" width="330" height="360" rx="16" class="mf-box-sales-v4"/>
  <text x="120" y="210" class="mf-label-sales-v4">Sales.Everything</text>
  <line x1="120" y1="226" x2="390" y2="226" class="mf-line-sales-v4"/>

  <text x="120" y="255" class="mf-mono-sales-v4">Sales ID</text>
  <text x="120" y="276" class="mf-mono-sales-v4">Item ID</text>
  <text x="120" y="297" class="mf-mono-sales-v4">Quantity</text>
  <text x="120" y="318" class="mf-mono-sales-v4">Sale value</text>
  <text x="120" y="339" class="mf-mono-sales-v4">Supplier cost</text>
  <text x="120" y="360" class="mf-mono-sales-v4">Refund amount</text>
  <text x="120" y="381" class="mf-mono-sales-v4">Margin</text>
  <text x="120" y="402" class="mf-mono-sales-v4">Total margin</text>
  <text x="120" y="423" class="mf-mono-sales-v4">Is profitable</text>
  <text x="120" y="444" class="mf-mono-sales-v4">Placed date</text>
  <text x="120" y="465" class="mf-mono-sales-v4">Shipped date</text>
  <text x="120" y="486" class="mf-mono-sales-v4">Is meeting SLA</text>

  <text x="120" y="525" class="mf-small-sales-v4">Mixed purpose · hidden rules · hard to reuse</text>

  <!-- Middle arrow -->
  <path d="M445 350 L530 350" class="mf-arrow-sales-v4"/>
  <text x="452" y="330" class="mf-small-sales-v4">separate</text>
  <text x="452" y="374" class="mf-small-sales-v4">meaningful</text>
  <text x="452" y="394" class="mf-small-sales-v4">purposes</text>

  <!-- Right heading -->
  <text x="575" y="122" class="mf-label-sales-v4">Meaningful fragments</text>
  <text x="575" y="145" class="mf-small-sales-v4">Fragments describe reusable analytical meanings.</text>

  <!-- Top row: reference + entity of interest -->
  <rect x="545" y="185" width="195" height="92" rx="14" class="mf-lightbox-sales-v4"/>
  <text x="567" y="216" class="mf-label-sales-v4">ItemSupplierCost</text>
  <text x="567" y="238" class="mf-small-sales-v4">reference data</text>
  <line x1="567" y1="251" x2="715" y2="251" class="mf-line-sales-v4"/>
  <text x="567" y="270" class="mf-mono-sales-v4">Item ID · Supplier cost</text>

  <rect x="775" y="185" width="170" height="92" rx="16" class="mf-box-sales-v4"/>
  <text x="800" y="216" class="mf-label-sales-v4">Sales</text>
  <text x="800" y="238" class="mf-small-sales-v4">entity of interest</text>
  <line x1="800" y1="251" x2="920" y2="251" class="mf-line-sales-v4"/>
  <text x="800" y="270" class="mf-mono-sales-v4">Sales ID · date</text>

  <!-- Detail fragment -->
  <rect x="655" y="325" width="210" height="90" rx="14" class="mf-lightbox-sales-v4"/>
  <text x="680" y="356" class="mf-label-sales-v4">SalesItem</text>
  <line x1="680" y1="370" x2="835" y2="370" class="mf-line-sales-v4"/>
  <text x="680" y="393" class="mf-mono-sales-v4">Item · quantity · value</text>

  <!-- Parallel derived fragments -->
  <rect x="520" y="470" width="185" height="82" rx="14" class="mf-lightbox-sales-v4"/>
  <text x="542" y="500" class="mf-label-sales-v4">SalesItemMargin</text>
  <line x1="542" y1="514" x2="680" y2="514" class="mf-line-sales-v4"/>
  <text x="542" y="537" class="mf-mono-sales-v4">Value − cost</text>

  <rect x="795" y="470" width="185" height="82" rx="14" class="mf-lightbox-sales-v4"/>
  <text x="817" y="500" class="mf-label-sales-v4">SalesItemRefund</text>
  <line x1="817" y1="514" x2="955" y2="514" class="mf-line-sales-v4"/>
  <text x="817" y="537" class="mf-mono-sales-v4">Refunds against items</text>

  <!-- Final aggregate -->
  <rect x="665" y="595" width="250" height="82" rx="14" class="mf-box-sales-v4"/>
  <text x="690" y="625" class="mf-label-sales-v4">SalesProfit</text>
  <line x1="690" y1="639" x2="885" y2="639" class="mf-line-sales-v4"/>
  <text x="690" y="662" class="mf-mono-sales-v4">Margin − refunds · profitable?</text>

  <!-- Links -->
  <!-- Reference and Sales feed SalesItem -->
  <path d="M642 277 C650 305, 685 318, 720 325" class="mf-link-sales-v4"/>
  <path d="M860 277 C850 305, 825 318, 800 325" class="mf-link-sales-v4"/>

  <!-- SalesItem and ItemSupplierCost feed SalesItemMargin -->
  <path d="M700 415 C675 438, 640 455, 612 470" class="mf-link-sales-v4"/>
  <path d="M610 277 C590 348, 590 420, 612 470" class="mf-link-sales-v4"/>

  <!-- Sales and SalesItem feed SalesItemRefund -->
  <path d="M885 277 C925 350, 930 420, 888 470" class="mf-link-sales-v4"/>
  <path d="M820 415 C845 438, 870 455, 888 470" class="mf-link-sales-v4"/>

  <!-- Margin and refund feed SalesProfit -->
  <path d="M612 552 C635 575, 690 588, 735 595" class="mf-link-sales-v4"/>
  <path d="M888 552 C860 575, 825 588, 805 595" class="mf-link-sales-v4"/>

</svg>
{{< /svg >}}

<div style="max-width:44rem;text-align:center;font-size:0.95rem;color:#666;margin-top:0.5rem;">
Figure 1. A giant table hides the entity of interest, mixes grains, and makes change detection harder. Meaningful fragments separate information into clear grains around the entity, so each fragment can be built, tested, reused, and updated deliberately.
</div>


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

The relevant fragments—timelines and end-of-period tables— are discussed in [Entity tracking](/docs/creating-information/entity-tracking/#second-pass-build-the-timeline).

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
