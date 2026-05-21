---
title: Mapping the data world
url: /docs/creating-information/mapping-the-data-world/
description: Explains how primary keys, immutable entities, and mutable entities help connect database records to real-world business meaning.
lede: The data engineer's first task is to relate records back to the business entities behind them.
weight: 2
---

## From records to entities

Business is not interested in data for data’s sake. It is interested in the business reality behind the data.

From this perspective, data is not an end in itself. Its function is to bridge the business processes that collect the data and the business intent that seeks insight.

Consequently, the data engineer sees each data record as an intermediary of the business entity that generated it.

A business entity can be a concrete object, such as a customer or a product. It can also be an abstract event, such as a business transaction.

This shift from data record to business entity is the first practical step in expressiveness. For many data engineers, it is also the first threshold: learning to see not the record itself, but the entity behind it.

For a data engineer who starts with the data and reaches back to the business world, the tool of choice is the primary key.

## Primary key

Primary keys play a special role in establishing the correspondence between business entities in the real world and data records in the data world.

A primary key is the handle by which business processes use to accurately retrieve a business entity’s data record from a data store.

For example, an order number identifies a sales transaction, and a customer number identifies a client record. These keys are visible to end users who use them to relate back to business processes, such as calling a company to follow up on an order.

Systems may also employ internal keys, invisible to users, to support subsidiary information retrieval. In every case, the function remains the same: reliable lookup of records.

The quality of a primary key is underpinned by its business process. This process may be:

- **Rigorous:** A strict identity-proofing protocol, such as issuing social security numbers, ensures unique assignment of a key to a personal identity. Mistakes can occur. However, the overall system remains robust across a large population.
- **Fuzzy:** Smaller organisations may register customers by phone number or email. When the database is small, this may return accurate results. However, increased numbers of customers may lead to duplicate records or accidental access if contact details overlap.
- **Log-like:** Modern online shops often implement guest checkout to cater to buyer preference. Guest checkout creates a new record for every transaction. In this case, each row is effectively logged as a separate event.

The final example is a case of having no true primary key.

This absence may be by design, as in the case of guest checkout. The data engineer can treat each row as its own entity and assign a random, unique number for a primary key. If the business needs to know the underlying business entity driving each record, such as the identity of the guest shopper, the data engineer or data scientist may apply entity resolution techniques to deduplicate the data.

The absence of a primary key can also be accidental. For example, staff may record information each day on a spreadsheet without a clear key for each row, leaving the data engineer to infer how those rows relate to business entities.

This way of looking at the primary key departs from treating it only as a technical constraint, or even as a pure link between a record and a real-world entity.

The emphasis on lookup is significant. The ability of a primary key to serve as a reliable link to the real world is directly proportional to the quality of the lookup process that supports it. It helps the data engineer see not only that primary keys can fail, but where the failure is likely to sit within the business process.

Implementing and maintaining a strong primary-key process carries cost. Quite often, this cost becomes a barrier to maintaining accurate correspondence between data records and business entities. The result is duplication or loss of information:

- When record creation is easier than updates, duplicate entries proliferate.
- When creation or updates become burdensome, entities may go unrecorded, overwritten, or repurposed.

Any primary-key issue inevitably traces back to the underlying business process.

If there are issues with the primary key, the data engineer must do more than accept the issue at face value. The engineer must work to find the root cause in the business process.

Given its foundational role, the primary key is the natural starting point for a data engineer examining a new system.

Often the database does not come with keys implemented as constraints, for example when uniqueness is enforced in the application layer. In these cases, a data engineer investigating a new system would do well to infer the primary keys for each table and then ask how those keys are created, retrieved, and deleted in business processes.

A direct corollary of the primary key’s significance is that relational algebra becomes indispensable.

Experienced engineers think in keys. They rely on algebraic operations to track and communicate data rather than memorise every detail of source processes. Discussion of relational algebra lies beyond this text’s scope.

## Immutable and mutable entities

It is helpful to divide business entities into two broad types: immutable and mutable.

Immutable entities are those that do not change. If they do change, the change is treated as the creation of a different entity, and the latest version is considered the correct one. In other words, neither the entity nor its attributes evolve over time.

Examples include a completed bank transfer or an importer lodging an import declaration into a country. If the import declaration is altered, it is regarded as a new entity. Products can also be treated as immutable. A new model of phone is considered a different product from the previous version.

Mutable entities are those that may change over time while still being considered the same entity.

A customer may change purchasing habits. An employee in an HR system may update personal details or gain new qualifications. These changes are important but, according to business intent, still part of the same entity.

This distinction is helpful because most business processes are built with one of these perspectives in mind.

A digital system may have sub-systems that manage both. For example, a sales system may record purchases as immutable entities, treat products themselves as immutable, but also register information about customers whose attributes and behaviour are mutable.

One way to distinguish mutable from immutable entities is the presence of a datetime component in the primary key to indicate the validity period of the record.

In warehousing terminology, such a record is a Type II record. The datetime signals that it is important to track changes to the entity’s attributes over time. This tracking may be implemented in the source system and maintained by business processes, or it may be absent and later added by a data engineer to meet business intent.

The two major types of business entity, immutable and mutable, correspond to two major types of data engineering methods: **entity processing** and **entity tracking**.

> [!NOTE]
> **Key ideas**
>
> A data record is an intermediary of the business entity behind it.
>
> Primary keys establish correspondence between data records and business entities through reliable lookup.
>
> The quality of a primary key depends on the quality of the business process that creates, retrieves, and maintains it.
>
> Immutable entities lead to entity processing.
>
> Mutable entities lead to entity tracking.