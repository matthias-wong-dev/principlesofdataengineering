---
title: Reference data
url: /docs/creating-information/reference-data/
description: Explains how reference data gives business meaning a stable form, and how mapping tables connect local system records to shared references.
lede: Reference data gives business meaning a stable place to live.
weight: 5
# draft: true
---

## A stable place for meaning

In the chapters [Entity processing](/docs/creating-information/entity-processing/) and [Entity tracking](/docs/creating-information/entity-tracking/), reference tables appeared as a way to make business meaning expressive. They gave names, descriptions, and analytical attributes a stable place to live.

This chapter takes the next step. The goal is to introduce reference data into the warehouse and connect individual systems to it. Local systems may continue using their own terminology, codes, and classifications, while the warehouse provides shared points of reference for business meaning.

Two constructs are important for this purpose: **reference tables** and **mapping tables**. Reference tables define the meanings the business wants to use. Mapping tables connect local system values to those shared meanings.

This chapter focuses on applying these ideas within a single system. The next chapter extends the same pattern across [multiple systems](/docs/creating-information/conforming-systems/).

## A point of reference

A reference table that applies to multiple business processes becomes a shared point of reference.

The calendar is a simple example. Most business processes can map directly to a calendar table through a date column. A country table is another common example. Product categories, organisational structures, geographic hierarchies, and customer classifications often play the same role.

Such tables are commonly called **conformed reference tables** because multiple business processes conform to the same definition. This makes reference data one of the main ways a warehouse gives stable form to [negotiated organisational meaning](/docs/foundations/data-and-organisations/#implications-for-data-engineering).

The term **golden record** is also used, particularly when a single reference table represents the authoritative version of a concept.

In simple cases, systems can map directly to the shared reference. In more complex cases, each system requires its own mapping table.

The goal is not to force every source system to use identical codes. The goal is to provide a common reference that allows information from different sources to be understood consistently.

## Building and applying shared references

It can be tempting to select a source-system table and declare it to be the golden reference, asking all other systems to conform to it.

This should be avoided.

The golden reference should be treated as physically and conceptually separate from any individual source system. This preserves flexibility and reduces coupling. If a source system changes, the warehouse reference remains stable.

A practical approach consists of three steps:

- Model the local system.
- Build shared references.
- Apply the references during presentation.

The following example uses a sales process from a fictional system called `Cake`.

### Step 1—Model the local system

Begin by modelling the source system in isolation. The objective at this stage is not integration. The objective is to understand and represent the system faithfully.

The resulting tables may look like:

- `Cake.Sales`
- `Cake.RefSales`
- `Cake.RefCountry`

**Example structure of `Cake.RefCountry`**

| Cake country code | Cake country name |
|---|---|
| AUS | Aus |
| NZ | Aotearoa |
| UK | Britain |

The local model should stand on its own before any reference-data work begins.

This separation allows the engineering work to progress while mapping decisions are still being refined.

### Step 2—Build shared references {#step-2-build-shared-references}

Next, construct the warehouse reference table and the mapping table.

The warehouse reference captures the business concept independently of any individual source system.

**Example structure of `Location.RefCountry`**

| Country ID | Country name | Region |
|---:|---|---|
| 1 | Australia | Oceania |
| 2 | New Zealand | Oceania |
| 3 | United Kingdom | Europe |

**Example structure of  `Cake.CountryMap`**

| Cake country code | Country ID |
|---|---:|
| AUS | 1 |
| NZ | 2 |
| UK | 3 |

The reference table can now hold information that may never have existed in the source system. Additional classifications, descriptions, metadata, and analytical attributes can be added without modifying operational systems.

If multiple systems require mapping to the same country list, the mappings may be stored separately:

- `Cake.CountryMap`
- `Finance.CountryMap`
- `Logistics.CountryMap`

An alternative is to combine them into a single table.

**Example structure of a consolidated mapping table**

| System | Source country code | Country ID |
|---|---|---:|
| Cake | AUS | 1 |
| Cake | NZ | 2 |
| Finance | AU | 1 |
| Finance | NZL | 2 |

While convenient, this introduces a polymorphic key. The meaning of the source code depends on the value of another column. Such designs are practical but no longer correspond cleanly to traditional entity-relationship semantics.

### Step 3—Apply during presentation

The final step is to apply the mapping during presentation.

This usually occurs through a dimensional model, reporting view, semantic model, or presentation layer.

The process is straightforward:

1. Retrieve the local system value.
2. Look up the mapping table.
3. Retrieve the shared reference.

The result is that reports and analytical models operate on shared business concepts rather than system-specific codes.

For example, a report consuming `Cake.Sales` no longer sees country code `AUS`. It sees the warehouse country reference and any associated classifications such as region.

**Example application**

Suppose `Cake.Sales` contains the local country code:

| Sales ID | Country code | Sales value |
|---|---|---:|
| 1001 | AUS | 125.00 |
| 1002 | UK | 320.00 |

The presentation layer can translate the local code into the warehouse reference by joining through the mapping table:

```sql
select
      s.[Sales ID]
    , s.[Sales value]
    , rc.[Country name]
    , rc.[Region]
from      Cake.Sales s
left join Cake.CountryMap     cm on cm.[Country code] = s.[Country code]
left join Location.RefCountry rc on rc.[Country ID]   = cm.[Country ID];
```

The result is:

| Sales ID | Sales value | Country name | Region |
|---|---:|---|---|
| 1001 | 125.00 | Australia | Oceania |
| 1002 | 320.00 | United Kingdom | Europe |

The report consumes the shared reference rather than the local system code. This allows multiple systems to present countries consistently even when their underlying codes differ.


In summary, the complete pattern introduces four tables, each table having a distinct responsibility:

| Table | Responsibility |
|---|---|
| `Cake.Sales` | Local business transaction |
| `Cake.RefCountry` | Local system country reference |
| `Cake.CountryMap` | Translation from local country code to shared country reference |
| `Location.RefCountry` | Shared warehouse country reference |

This structure provides flexibility, stability, and reuse while keeping responsibilities clear.

## Why these separations 

The pattern depends on several separations:

- the local system is separated from the warehouse reference;
- the reference table is separated from the mapping table;
- the building of reference data is separated from its application.

These separations guard against a common mistake: introducing shared reference data too early and too deeply into the local system model.

The local system should first be modelled on its own terms. `Cake.Sales` and `Cake.RefCountry` describe how the Cake system records sales and countries. `Location.RefCountry` describes the warehouse’s shared country reference. `Cake.CountryMap` connects the two.

Keeping these responsibilities separate has practical advantages.

First, the local system can be developed while reference mapping is still being reviewed. Mapping countries, product categories, and organisational structures often requires detailed business attention and cannot always be completed immediately. This matters in projects that require tight iteration loops.

Second, the design remains modular. Reference tables and mapping tables can be changed independently, which aligns with fragment modelling.

Third, reference data has an amplification effect. A change to a single reference row may affect large portions of the warehouse. If shared references are introduced too early into local transaction tables, changes to the warehouse reference can ripple through the local model. Delaying the dependency until presentation reduces unnecessary coupling.



## When to simplify

Smaller systems may not require the full pattern.

One option is to skip `Cake.RefCountry` if the mapping to the golden reference can be created directly. 

If a mapping can be expressed directly and maintained safely, `Cake.CountryMap` may be replaced by code. Where possible, this should be implemented through a temporary table or CTE rather than a large inline conditional, so that the pattern is still visible in code.

The full pattern exists because it scales well. Simpler systems can often adopt lighter variations without losing the underlying principle.

## The discipline of separation

The pattern is simple, but easy to damage in practice.

Most mistakes come from collapsing distinctions that should remain separate: treating a source-system table as the warehouse reference, hard-coding mappings into reports, applying shared references too early, or merging mapping logic into the reference table itself.

The pattern in this chapter has been tested in complex settings. It is the path of least regret.

Above all, it is a discipline of separation, not a mechanical implementation recipe.


> [!NOTE]
> **Key ideas**
>
> Reference data gives business meaning a stable place to live.
>
> Reference tables define shared business concepts.
>
> Mapping tables connect local system values to those shared concepts.
>
> Build the local system first, then construct shared references, then apply them during presentation.
>
> Shared references allow a warehouse to remain coherent even when source systems use different codes and classifications.
>
> Changes to shared references can amplify across the warehouse; delay the dependency until presentation when possible.
