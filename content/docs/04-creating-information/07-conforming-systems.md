---
title: Conforming systems
url: /docs/creating-information/conforming-systems/
description: Explains how to integrate multiple systems through conformed reference data without losing clarity of grain or business meaning.
lede: Systems should be integrated only after the nature of their sameness is understood.
weight: 7
# draft: true
---

## Integration without distortion

Integration is common, tempting, and dangerous because it invites the data engineer to connect tables before clarifying what kind of sameness is involved.

Business often needs to see multiple systems together. A legacy system may be replaced by a new platform, but the business still needs to analyse across both systems. Different business processes may also need to be compared through common references. A company may want to compare production and sales by region and month. A government agency may want to compare applications, inspections, and enforcement actions by location or program.

New engineers often fall into two traps: forcing a union of tables that do not naturally fit, or performing large joins that create ambiguous grain and duplicated data. Both approaches can produce outputs that run but no longer mean what they appear to mean.

Conforming systems is the discipline of integrating information without distorting the business entities being represented. Fragment modelling handles this by refusing to collapse meaning into convenience.

There are two approaches:

- **Vertical integration**—the same kind of entity is recorded across multiple systems.
- **Horizontal integration**—different entities can be compared through shared references.

## Vertical integration

Vertical integration applies when the same kind of entity is recorded across multiple systems.

This commonly occurs when a legacy system is replaced by a new platform. The systems differ, but the business entity continues. The data engineer’s task is to preserve that continuity without pretending the two systems are identical.

Take a cake company using two systems, `CakeV1` and `CakeV2`, to record sales. The newer system adds fields and improves logic, but both systems record sales.

Integration proceeds in three steps:

- Model the systems individually.
- Build conformed reference tables.
- Integrate the transaction tables.

### Step 1—Model systems individually

A common mistake is to integrate too early.

Each system should first be modelled on its own terms. This preserves local meaning and makes the later integration safer.

Suppose both systems have sales and status, but `CakeV2` also has a marketing campaign.

The local tables might be:

- `CakeV1.Sales`
- `CakeV1.RefSales`
- `CakeV1.RefStatus`
- `CakeV2.Sales`
- `CakeV2.RefSales`
- `CakeV2.RefStatus`
- `CakeV2.RefCampaign`

At this stage, no union is required. The goal is to represent each incoming system clearly.

### Step 2—Build conformed references

The second step is to build references that express shared business meaning across both systems.

For example, suppose the two systems record sales status differently.

**`CakeV1.RefStatus`**

| V1 status code | V1 status name |
|---|---|
| O | Open |
| C | Completed |
| A | Abandoned |

**`CakeV2.RefStatus`**

| V2 status code | V2 status name |
|---|---|
| OP | Open |
| CO | Completed |
| WD | Withdrawn |
| RF | Refunded |

A proposed conformed reference might be:

**`Cake.RefStatus`**

| Status ID | Status name | Is finished sale |
|---:|---|---|
| 1 | Open | false |
| 2 | Completed | true |
| 3 | Withdrawn | true |
| 4 | Refunded | true |

The mapping table then connects each system-specific status to the conformed reference.

**`Cake.StatusMap`**

| System | Source status code | Status ID |
|---|---|---:|
| CakeV1 | O | 1 |
| CakeV1 | C | 2 |
| CakeV1 | A | 3 |
| CakeV2 | OP | 1 |
| CakeV2 | CO | 2 |
| CakeV2 | WD | 3 |
| CakeV2 | RF | 4 |

But this is only a hypothesis. It must be validated with the business. Even subtle differences in meaning can undermine the integration.

In addition to aligning codes, the golden reference tables should:

- Include default rows for unknown values
- Add analytical columns such as `[Is finished sale]` to support downstream use
- Be documented with metadata to support clarity and reuse

### Step 3—Integrate the transactions

Only after the local systems have been modelled and the references conformed should the transaction tables be integrated.

The integrated table might be:

- `Cake.Sales`

This table is created as a union of `CakeV1.Sales` and `CakeV2.Sales`.

If a column exists only in one system, the other system should be populated with an appropriate default value. This includes default foreign keys to reference tables where required.

During the union, the mapping tables translate system-specific codes to conformed references. This allows `Cake.Sales` to use shared meanings rather than system-specific values.

The final structure includes:

- `Cake.Sales`—the unified transaction table
- `Cake.RefSales`—the conformed reference for sales
- `Cake.RefStatus`—the conformed status reference
- `Cake.RefCampaign`—the conformed campaign reference

The separation into three steps—modelling, reference building, and integration—allows each system to be developed independently, supports incremental delivery, and makes it easier to refactor or extend the model later.
In practice, simplifications may be appropriate. The decision to simplify should be left to the data engineer, guided by expressiveness, fragment modelling, and the need to build a stable pipeline.

## Horizontal integration

Horizontal integration applies when the entities differ conceptually but share enough commonality to make comparison valuable. This pattern is closely related to Kimball's notion of conformed dimensions and the bus matrix. Different business processes remain separate while becoming comparable through shared references.

A cake company may both produce and sell cakes. The core tables are:

- `Cake.Production`
- `Cake.Sales`

Production records manufacturing. Sales records transactions. However, they share common attributes such as region, time, cost, and staff, making comparison meaningful.

These should not be collapsed into a single abstract table such as `Cake.Event`. This creates a model that is difficult to understand and prone to error.

They can still be compared through shared references.

For example, both production and sales may use:

- `Cake.RefCalendar`
- `Cake.RefRegion`

This allows comparisons such as:

- production volume and sales volume by region and month
- production cost and sales value by region and month
- staff count and sales performance by site

An example SQL would be 

```SQL
select
      c.[Month start date]
    , r.[Region name]
    , sum(p.[Production volume])   as [Production volume]
    , sum(s.[Sales volume])        as [Sales volume]
    , sum(p.[Production cost])     as [Production cost]
    , sum(s.[Sales value])         as [Sales value]
    , count(distinct p.[Staff ID]) as [Production staff count]
    , count(distinct s.[Staff ID]) as [Sales staff count]
from       Cake.RefCalendar c
cross join Cake.RefRegion   r
left join  Cake.Production  p  on  p.[Production date] = c.[Calendar date]
                               and p.[Region ID]       = r.[Region ID]
left join  Cake.Sales       s  on  s.[Sales date]      = c.[Calendar date]
                               and s.[Region ID]       = r.[Region ID]
group by
      c.[Month start date]
    , r.[Region name];
```

The result is:

| Month start date | Region name | Production volume | Sales volume | Production cost | Sales value | Production staff count | Sales staff count |
|---|---|---:|---:|---:|---:|---:|---:|
| 2025-01-01 | North | 12,500 | 11,900 | 82,000 | 145,000 | 18 | 7 |
| 2025-01-01 | South | 9,800 | 10,200 | 63,000 | 126,000 | 15 | 6 |
| 2025-02-01 | North | 13,200 | 12,600 | 86,500 | 152,000 | 19 | 8 |
| 2025-02-01 | South | 10,400 | 10,100 | 66,000 | 128,500 | 15 | 6 |

The comparison occurs through the shared references of calendar and region. Neither `Cake.Production` nor `Cake.Sales` has been altered or merged into a common transaction table. This is integration without collapse of meaning.

### Horizontal integration through mapping fragments

Sometimes shared references are not enough.

The business may want to understand how specific production batches relate to specific sales. However, the source data may not record that relationship directly.

Suppose the business proposes a rule: Cakes produced in the same region and month are sold in that region and month, in production order.

This relationship is inferred. It is not native to either table.

New engineers may try to enforce the relationship by adding `[Production ID]` to `Cake.Sales`, or `[Sales ID]` to `Cake.Production`.

Both approaches damage the grain of the table.

A better approach is to create a mapping fragment.

**`Cake.SalesProductionMap`**

| Sales ID | Production ID | Sales month | Production batch |
|---|---|---|---|
| S1001 | P5501 | June | June, Batch 1 |
| S1002 | P5501 | June | June, Batch 1 |
| S1003 | P5502 | June | June, Batch 2 |
| S1004 | P5502 | June | June, Batch 2 |
| S1005 | P5601 | July | July, Batch 1 |
| S1006 | P5601 | July | July, Batch 1 |

Sales in the same region and month are allocated to production batches in production order. The relationship is stored as a fragment rather than forced into either `Cake.Sales` or `Cake.Production`.

`Cake.Sales` remains a sales table. `Cake.Production` remains a production table. The inferred relationship lives in its own fragment, where its logic can be tested, reviewed, and refined.

This is especially important when the relationship is fuzzy, inferred, many-to-many, or likely to change.


## Choosing between vertical and horizontal integration

The distinction between vertical and horizontal integration is not always obvious. A useful starting point is to ask two questions.

**First, would a union produce relatively few null columns?**

If the two systems record largely the same attributes, a union is often a good sign. If most columns would be null for large portions of the data, the systems may not represent the same business entity.

**Second, can the resulting union be given a meaningful name?**

For example, it is natural to combine `CakeV1.Sales` and `CakeV2.Sales` into `Cake.Sales`. Likewise, `LegacyCustomer` and `ModernCustomer` may become `Customer`.

In contrast, combining `Production` and `Sales` into a table called `Event` is technically possible but conceptually weak. The name exists to support the union rather than describe a genuine business entity.

When both questions can be answered positively, vertical integration is often the stronger option. It preserves continuity across systems and usually produces a simpler model for downstream use.

When the answer to either question is no, then vertical integration is likely to distort meaning. Horizontal integration would be more appropriate. 

## Key ideas

> [!NOTE]
> **Key ideas**
>
> Integration should begin by asking what kind of sameness is involved.
>
> Vertical integration applies when the same kind of entity is recorded across multiple systems.
>
> Horizontal integration applies when different entities can be compared through shared references.
>
> Mapping fragments preserve grain when relationships between entities are inferred, fuzzy, or many-to-many.
>
> A quick test for vertical integration: would the union produce few null columns, and can the resulting table be given a meaningful business name?
>
> The central danger of integration is collapsing meaning for technical convenience.