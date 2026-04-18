---
title: Reference data
weight: 4
draft: true
---

In the chapters *Entity processing* and *Entity tracking*, reference data emerged as an effective tool for expressiveness. Reference tables describe business processes succinctly, provide a place to add descriptive or analytical columns, and can be annotated with metadata to support business meaning.

Beyond expressiveness, reference data is also the cornerstone of integration. This chapter outlines the fundamentals of reference data when applied to a single system. These foundations support the integration of information across multiple systems, which is the focus of the next chapter, [Conforming systems](/docs/creating-information/conforming-systems/).

## A point of reference

A reference table that applies to multiple business processes becomes a shared point of reference. In dimensional modelling, this is called a conformed reference table. The calendar is a basic example. The list of countries is another. The conformed reference table is also known as the golden record.

In rare cases, the mapping of system-specific records to the golden record is straightforward. For example, most processes can map directly to the calendar table using a date column. In more complex cases, systems may maintain their own codes. A business system may have its own country codes. These require the use of mapping tables.

Mapping tables are narrow tables that translate system-specific codes to the golden reference. These are often materialised in advance and stored as standalone tables. In simpler cases, they can be calculated at runtime.

## Applying reference tables

It can be tempting to select a source system table and treat it as the golden reference, asking all other systems to conform to it. This should be avoided. The golden record is treated as physically and conceptually distinct from any source system. This preserves flexibility and supports future changes.

When applying reference tables, the data engineer should proceed in three distinct steps:

- Model the individual system in isolation without reference data
- Build reference tables
- Apply the reference tables for presentation

The manuscript illustrates these steps using the example of applying a country reference table to the `Cake.Sales` business process.

### Step 1 — Model the individual system

Begin with system-specific tables and build the pipeline as described in earlier chapters. This produces tables such as `Cake.Sales` and `Cake.RefSales`. If the source system includes its own country reference, this would be `Cake.RefCountry`.

> [!NOTE]
> **TODO**
>
> The manuscript includes an ER diagram / screenshot example here.

### Step 2 — Build reference tables

Next, construct the golden reference table `Location.RefCountry` and the mapping table `Cake.CountryMap`. The mapping table translates country codes from `Cake.RefCountry` to `Location.RefCountry`.

If multiple systems need to map to the golden country list, a single `Location.CountryMap` can be created by taking a union of all records. However, this introduces polymorphic keys. A polymorphic column is one whose meaning depends on the value of another column. A polymorphic key is one whose primary table reference switches depending on the value of another column. While easy to engineer, it is syntactically incorrect from an entity-relationship diagram perspective.

> [!NOTE]
> **TODO**
>
> The manuscript includes screenshots and ER diagrams here to illustrate the reference table and mapping table patterns.

### Step 3 — Apply during presentation

During presentation, typically through a view or dimensional model, a lookup from `Cake.Sales` to `Cake.CountryMap` converts system-specific codes to the golden reference.

> [!NOTE]
> **TODO**
>
> The manuscript includes a SQL screenshot here. Reconstruct this as a fenced `sql` block during review if the original draft becomes available in text form.

This process maintains a clear separation between modelling the local system and building reference tables. First, this separation allows the pipeline to proceed while the mapping work catches up. Mapping country codes often requires attention to detail and cannot be rushed early in a project. Second, the separation aligns with fragment modelling. Components such as `CountryMap` and `RefCountry` can be swapped out later if needed.

Separating the build and application of reference tables also provides flexibility in when reference data is introduced as a dependency. Deferring this step is often preferable. Reference data has an amplification effect: changes to a single row can cause widespread downstream updates.

The full process creates a minimum total of four tables:

- `Sales`
- `RefSalesCountry`
- `SalesCountryMap`
- `RefCountry`

> [!NOTE]
> **TODO**
>
> The manuscript includes ER diagrams here for the four-table and simplified variants.

These three steps and the resulting table structure support agility in development, flexibility in components, and stability in the pipeline. In smaller systems, a more lightweight approach may be appropriate.

One option is to skip `RefSalesCountry` if the mapping to the golden reference can be created directly. Another option is to skip `SalesCountryMap` if the mapping can be expressed in code. Ideally, this is done using a temporary table rather than an inline conditional.

Applying reference data in this way sets the foundation for integrating information across multiple systems in the warehouse.