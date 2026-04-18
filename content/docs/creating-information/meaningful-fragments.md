---
title: Meaningful fragments
description: Shows why narrow, reusable fragments are more expressive and maintainable than large all-purpose tables.
lede: A good pipeline is built from fragments with clear informational purpose.
weight: 7
draft: true
---

New engineers often build giant tables to answer queries. This feels convenient and intuitive: everything in one place, easier to visualise. However, this approach has serious drawbacks, which continue to surface throughout the text.

Meaningful fragments are one of the most important concepts in data engineering. It is the idea that, instead of creating wide tables with many attributes, the developer creates narrow tables with specific, self-contained meanings. These fragments are designed to:

- Represent expressive content
- Package information in reusable blocks
- Isolate complex computation
- Enable change detection specific to those columns
- Reduce dependencies across the pipeline

The general approach is to extract data from the source as-is, keeping only the necessary columns and rows, and then compute everything else in meaningful fragments.

## Restaurant analogy

In a restaurant kitchen, meaningful fragments are like prepared plates of chopped vegetables, cured sauces, or marinated proteins. They are ready to be used as needed. The raw data are like whole potatoes or unwashed greens.

- The first part of processing is to peel off the skins and discard the junk.
- The second part is to prepare mini plates, which in kitchen terminology is the step of *mise en place*.
- The third part is the actual service, combining ingredients to cook and present the dishes on time.

The second part, *mise en place*, creates mini plates, which are the equivalent of meaningful fragments. As one notable chef said, “When the mise-en-place is done well, the service is easy.” In the same way, with the correct fragments, surfacing the insights for use is easy.

## Symptoms of anti-pattern

When meaningful fragments are not used effectively, several symptoms are obvious:

- The same logic recurs in `WHERE` clauses or join conditions across multiple queries, indicating that the logic could have been centralised earlier.
- Tables become wider and wider as constructed columns are bolted onto fact tables, making them hard to reuse and maintain.
- Information in the data model becomes duplicative of other tables, especially reference data, causing confusion for users.
- Users must write excessive joins and bespoke filters just to answer basic questions, rather than being able to plug-and-play.

These symptoms indicate a lack of fragment modelling.

## Examples of meaningful fragments

The following list provides illustrative examples of meaningful fragments. These are common patterns, but not exhaustive. Each serves a distinct scenario in modularising the pipeline.

**Summaries of details and storytelling.** Any reasonably complex business process will generate a significant number of detail rows that must be summarised to be useful. The computation for these summaries tends to be complex and should be placed in a separate fragment rather than compounded onto existing tables.

A special case is the storytelling dimension and its related fact. Once computed, the storytelling dimension becomes the primary window through which the business sees the data. It often becomes the default filter in queries. Because it is aggregated at the entity-of-interest level, it enables elegant queries and avoids the need for users to query subprocesses and then deduplicate results.

**Milestone datetimes.** Complex business processes often involve multiple milestones. A help desk may want to know when a case was received, first actioned, escalated, and completed. A manufacturing company may want to track when products were produced, shipped, and sold.

Entity processing is always interested in measuring the time between milestones. This can be difficult if steps repeat or are inconsistently recorded. The data engineer can add value by precomputing these milestones into a dedicated fragment. A milestone datetimes fragment is simply a table at the grain of the entity of interest, with one datetime column per milestone.

> [!NOTE]
> **TODO**
>
> The manuscript includes a screenshot of a table and histogram here.

Milestone tables are also known as accumulating snapshots in dimensional modelling.

**Current or primary version.** As discussed in the chapter on entity processing, immutable entities often have multiple versions. While the full version history may be useful for audit or lineage, the business is frequently interested in only the latest valid version that reflects the current state of the entity.

In many systems, this logic is handled in the application tier and is not obvious in the database. Rather than expecting users to reconstruct this logic repeatedly, the data engineer should precompute the latest version in a dedicated fragment.

In some cases, versions may not follow a strict chronological order. Multiple submissions of the same entity may exist, and the business may need to designate one as the primary version for reporting, counting, or representation. This selection may depend on business rules such as status flags, timestamps, or user roles.

Whether the requirement is for the current version or the primary version, if the logic is non-trivial, it should be implemented in its own fragment. This avoids compounding complexity in core tables and ensures that the logic is transparent and replaceable.

This is a case where fragment modelling can lead to a loss of expressiveness. Most users do not expect to retrieve a row from one table and then consult a separate fragment to find the current version of that row. The data engineer can compensate for this by ensuring that the main table is clearly named, for example including the word `version` in the table name and primary key columns.

**Timeline and end-of-period.** As discussed in entity tracking, when an entity has evolving attributes stored across multiple tables, it becomes difficult for users to retrieve consistent point-in-time views. This can be simplified through:

- Timeline tables: sets of keys pointing to Type II attributes for each validity period
- End-of-period tables: snapshots of those attributes at the end of each reporting period

These fragments make temporal analysis accessible and reliable.

**Mapping.** Business processes often do not record relationships at the grain needed for analysis. Sometimes this granularity is impractical. These relationships can be approximated using fuzzy logic in the analytical layer.

These are often many-to-many relationships. Rather than disturbing the grain of core tables, the mapping can be stored in separate fragments, typically two-column tables with foreign keys pointing to each primary table. This is the mapping table.

**Distribution weights.** In some cases, relationships lose information about how entities relate. A similar but distinct case is when measures are not clearly recorded against entities.

For example, a system may record the total time to complete multiple tasks, but not the time per task. The business may have rules to distribute the total time back to individual tasks as weights. This logic can be complex and should be calculated in its own fragment. This is the distribution weights table.

In many cases, mapping tables and distribution weights may be combined if their ambiguities stem from the same business phenomenon.

**Hubs.** A concept from the Data Vault method of data warehousing. A hub table creates a consistent surrogate key for the same entity appearing across multiple systems.

For example, a company may have multiple subsystems recording staff names, identified by first and last name. A data engineer may need to create a consistent surrogate key to represent this pair across all systems, either for anonymisation or for use as a relationship key in Power BI.

A hub table is a centralised fragment where this pairing and key assignment occurs. It belongs to no single subsystem and should be computed independently.

## Conclusion

These are examples of common patterns of fragments. In practice, anything can be a meaningful fragment. It does not need to fall under a predefined category. As long as the information is self-contained, and its creation can be justified by complex computation, dependency management, or business meaning, it qualifies.

The ability to create meaningful fragments also reflects the ability to see the data product in terms of its minimal informational components. This informational view is key to arriving at efficient, maintainable designs. It is one of the hallmarks of a mature data engineering mindset.
