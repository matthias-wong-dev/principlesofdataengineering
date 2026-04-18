---
title: Mapping the data world
description: Explains how primary keys, immutable entities, and mutable entities help connect database records to real-world business meaning.
lede: The data engineer's first task is to relate records back to the business entities behind them.
weight: 2
draft: true
---

Business is not interested in data for data’s sake. It is interested in the business reality behind the data. From this perspective, data is not an end in itself. Its function is to bridge the business processes that collect the data and the business interest that seeks insight.

Consequently, the data engineer sees each data record as an intermediary of the business entity that generated it. A business entity can be a concrete object, such as a customer or a product. It can also be an abstract event, such as a business transaction.

For a data engineer, the shift from focusing on data itself to focusing on the business entity behind the data is a prerequisite mental leap. Today, there are various pathways into the data engineering discipline. Some come from business areas and pick up data engineering to answer questions they have about the business. As data grows in social importance, more individuals enter through academia. The danger for the latter is that they are more prone to treating data and data techniques as ends in themselves and may lose valuable years before making the necessary shift in thinking, if they ever do so at all. Academic training can be an excellent starting point as it builds foundational technical expertise. All that is needed is to make the mental leap early in the journey as a data engineer.

For a data engineer who starts with the data and is reaching back to the business world, the tool of choice is the primary key.

## Primary key

Primary keys play a special role in establishing the correspondence between business entities in the real world and data records in the data world. A primary key is what business processes use to accurately retrieve a business entity’s data record from a data store.

For example, an order number identifies a sales transaction, and a customer number identifies a client record. These keys are visible to end users who use them to relate back to business processes, such as calling up the company to follow up on an order. On the other hand, systems often employ internal keys, invisible to users, to support subsidiary information retrieval. In every case, the function remains the same: reliable lookup of records.

The quality of a primary key is underpinned by its business process, which may be:

- **Rigorous:** A strict identity-proofing protocol, such as issuing social security numbers, ensures unique assignment of a key to a personal identity. Mistakes can occur. However, the overall system remains robust across the large population.
- **Fuzzy:** Smaller organisations may register customers by phone number or email. When the database is small, this may return accurate results. However, increased numbers of customers may lead to duplicate records or accidental access if contact details overlap.
- **Log-like:** Modern online shops often implement a guest checkout to cater to buyers’ preferences. Guest checkout creates a new record for every transaction. In this case, each row is effectively logged as a separate event.

The final example is a case of having no primary keys. This lack of primary key could be by design, as in the example of a guest checkout. The data engineer can treat each row as its own entity and assign a random, unique number for a primary key. If the business needs to know the underlying business entity driving each record, such as the identity of the guest shopper, then the data engineer or data scientist may apply entity resolution techniques to deduplicate the data.

The lack of primary keys can also be by accident. For example, it could be a business process where staff record information per day on a spreadsheet, without a clear key for each row on the spreadsheet to identify how they relate to a business entity.

Ultimately, the ability of a primary key to serve as a reliable link to the real world is directly proportional to the quality of its lookup process. Implementing and maintaining a strong primary-key process carries cost. Quite often the cost becomes a barrier to maintaining an accurate correspondence between data records and the business entity, resulting in duplication or loss of information:

- When record creation is easier than updates, duplicate entries proliferate.
- When creation or updates become burdensome, entities may go unrecorded or existing records may be overwritten or repurposed, resulting in information loss.

Any primary-key issue inevitably traces back to flaws in the underlying business process. If there are issues with the primary key, the data engineer must do more than accept the issue at face value. The engineer must work to find the root cause in the business process.

Given its foundational role, the primary key is the natural starting point for a data engineer examining a new system. Often the database does not come with keys implemented as constraints, for example if uniqueness of data is implemented in the application layer. In these cases, a data engineer investigating a new system would do well by inferring the primary keys for each table and, consequentially, asking how the primary keys are created, retrieved, and deleted in business processes.

A direct corollary of the primary key’s significance is that relational algebra becomes indispensable: experienced engineers think in keys and rely on algebraic operations to track and communicate data rather than memorise every detail of source processes. Discussion of relational algebra lies beyond this text’s scope.

## Immutable and mutable entities

It is helpful to divide business entities into two broad types: immutable and mutable.

Immutable entities are those that do not change. If they do change, the change is treated as the creation of a different entity, and the latest version is considered the “correct” one. In other words, neither the entity nor its attributes evolve over time. Examples include a completed bank transfer or an importer lodging an import declaration into a country. If the import declaration is altered, it is regarded as a new entity. Products can also be treated as immutable. A new model of phone is considered a different product from the previous version.

Mutable entities are those that may change over time while still being considered the same entity. A customer may change purchasing habits, or an employee in an HR system may update personal details or gain new qualifications. These changes are important but, according to business interest, still part of the same entity.

This distinction is helpful because most business processes are built with one of these perspectives in mind. A digital system may have sub-systems that manage both. For example, a sales system may record purchases as immutable entities, treat products themselves as immutable, but also register information about customers whose attributes and behaviour are mutable.

One way to distinguish mutable from immutable entities is the presence of a datetime component in the primary key to indicate the validity period of the record. In warehousing terminology, such a record is a Type II record. The datetime signals that it is important to track changes to the entity’s attributes over time. This tracking may be implemented in the source system and maintained by business processes, or it may be absent and later added by a data engineer to meet business interest.

The two major types of business entity, immutable and mutable, correspond to two major types of data engineering methods. These are entity processing and entity tracking.
