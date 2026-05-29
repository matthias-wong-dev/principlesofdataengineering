---
title: A good dimensional model
url: /docs/presenting-insights/a-good-dimensional-model/
description: Learn what makes a good Power BI dimensional model, including business-friendly naming, intuitive dimensions, useful measures, clear relationships, and strong performance.
lede: A good dimensional model lets users ask real business questions without guessing.
weight: 3
# draft: true
---

## What makes a good dimensional model?

A dimensional model is successful when users can ask real business questions and obtain the expected answers without guessing how the model works.

This chapter describes a good dimensional model through two questions:

- What should a good model achieve?
- What are the signs of a good model?

## What should a good model achieve?

A good dimensional model in Power BI should:

- Resonate with the business view
- Be intuitive and unambiguous—it should "just work"
- Anticipate questions
- Support both summary and detail
- Perform quickly

### Resonate with the view from business intent

A dimensional model is where expressiveness is tested by use.

In earlier chapters, expressiveness meant creating information that corresponds to the business world in a recognisable way. In a dimensional model, this becomes even more important. Users must be able to recognise the business through the model.

In some cases, technically correct representations may need to give way to what better reflects how the business sees the world. For example, strict grain consistency can sometimes produce a proliferation of objects that are technically correct but difficult to understand. A simpler model may better match business understanding.

Resonance begins with naming. Models, tables, columns, and measures should use language that is immediately meaningful to the business.

This may also require creating perspectives the business has not yet articulated. Familiarity can cause business areas to miss insights in their own processes. The data engineer, working across domains, is often well placed to offer a fresh view.

Metadata also plays a key role. Descriptions should speak the business language, state the intent clearly, and, in complex cases, explain the logic in near-pseudocode using business terms.

### Be intuitive and unambiguous

As a self-service data model, a Power BI model should let users drag and drop fields to get answers. For this purpose, the model should just work.

If users must memorise complex filtering rules, understand the map of relationships, or second-guess which column to use, the model is not intuitive. An intuitive model behaves in a way that matches expectation without requiring a heavy manual.

A related issue is ambiguity. An ambiguous model gives users multiple apparent ways to get the same information, or presents the same information in ways open to interpretation.

For example, ambiguity can occur when a column has been denormalised into multiple fact tables, leaving the user unsure which version to use. It can also occur when a column name such as `[Calendar date]` is too generic, making it unclear which business date the column refers to.

An unambiguous model gives the user one obvious way to answer a question. The model should either answer the question accurately or make it apparent that it cannot.

### Anticipate questions

A good model does not merely satisfy the initial requirements. It anticipates the full range of reasonable business questions.

This requires the data engineer to think beyond the immediate request and consider what the model may need to answer over time. There is no escaping this reality. If a reasonable question is not answered now, a business area will eventually return and ask for it later.

In practice, this means a business process should either be outside the model, or, if included, represented in a form that supports its expected usage. All information captured by that process should be accessible in a way that allows users to ask sensible questions of it.

Achieving this is easier than it sounds, and is the subject of the chapter on anticipating questions.

### Support both summary and detail

One of the most powerful features of Power BI is the ability for users to move interactively through data by cross-filtering and drill-through.

Users often begin with a high-level view. If something catches their attention, they drill into the details to see exactly what happened. This is an important part of how users build trust in the model.

The opposite path is also common. Users who operate at the detailed level often begin with transactions for troubleshooting, but eventually want to zoom out in search of broader patterns. This movement from detail to pattern is a sign of trust and maturity.

A data engineer cannot ignore the need to support both high-level and detailed views. While individual reports may emphasise one or the other, the underlying model often needs to support both.

### Perform quickly

Most queries should return in under a second. Complex or infrequent queries should complete in under two seconds. Longer runtimes are acceptable only in rare cases.

Performance is not merely a user-experience consideration. It can also signal deeper issues in the articulation of information.

A slow model often indicates that key information has not been pre-computed through [meaningful fragments](/docs/creating-information/meaningful-fragments). The model is then forced to compensate with work at query time. In this sense, a slow model may be a concern of business expressiveness, not only technical performance.

## What are the signs of a good model?

The following signs do not guarantee that the above objectives are met, and some of the signs may occasionally be absent for good reasons. But a strong Power BI dimensional model will usually show many of them. Their absence or frequent violation would hint at a model that is difficult to use.

The signs can be grouped into four areas:

- Names and metadata
- Dimensions
- Facts and measures
- Relationships

### Names and metadata

Names should be business-centric rather than system-centric. It is a common mistake for data engineers to use acronyms or terms from the source system rather than names that reflect the business content itself. This should be avoided unless the model is intentionally about the system.

Names should also avoid technical implementation terms. Words such as `dim`, `fact`, or `bridge` should not appear in visible names. These are implementation details, not business concepts.

Names should be explicit. For example, `[Sales date]` is better than `[Date]`. It may even be useful to repeat the table meaning in the column name, such as changing `Sales[Date]` to `Sales[Sales date]`. This is because the column name, and not the table name, is what appears in report visuals.

Visible names should not repeat across the model. When a user searches for a name in the field list, it should return one result. If a column appears more than once, it presents an immediate ambiguity.

If the repeated columns are genuinely the same, but all are visible, the model may need to be reworked to remove duplication. If the columns are different but share the same name by accident, they should be renamed rather than relying on table context to resolve the ambiguity.

Dimensions represent information or attributes, while facts represent business processes. As such, dimensions should be nouns, while business process facts should be verbal nouns or carry a sense of action.

For example, in a business system with three processes—manufacture, order, and shipping—the facts may be called `Manufacture`, `Order`, and `Shipping`. The dimensions may be called `Product`, `Region`, `Manufacture date`, `Order date`, and `Shipping date`. The facts name the business processes; the dimensions name the attributes those processes capture.

Naming facts after business processes is harder than it sounds. It requires a clear focus on business intent and enough familiarity with Power BI to design the model with simplicity.

A common case is the transaction and reference table pair, such as `Sales` and `RefSales`. One approach is to use `Sales` as the fact name and `Sales description` as the dimension name.

Finally, a strong indicator of a good dimensional model is the presence of rich, business-centric descriptions in the hover text of tables, columns, and measures.

<!-- These are studied in its wider context in [Quality metadata](/docs/quality-reliability/quality-metadata/). -->

### Dimensions

In Power BI, dimensions are the window through which users interact with the model. A good dimensional model consciously treats dimensions as the user's point of access. They are the biggest influence on the model's look and feel.

On the surface, dimension table names should be nouns that convey the type of information available to the user.

Dimensions should also have a reasonable number of columns, often around five to ten. There can be more if some columns are simple derivations of others, such as text versions of binary flags.

Too few columns in a dimension may mean that it carries too narrow a business meaning. For example, a dimension called `Gender` with a single column `[Gender]` is likely too thin. A large number of dimensions with very few columns indicates a fragmented rather than consolidated view of the business. It may be more useful to combine `Gender` with related attributes into a broader `Demographic` dimension.

Too few columns may also indicate missing helpful attributes. For example, a `Gender` table should include `[Gender display order]` so the values can be sorted usefully.

On the other hand, too many columns in a dimension may suggest that the grouping of attributes is too complicated and may overwhelm users. It also reflects a view of the business that is insufficiently nuanced. In that case, the dimension may need to be broken into several more manageable dimensions.

A dimensional model often includes two special types of dimensions that indicate thoughtful design.

The first is the ID dimension. This is a table of the primary keys of a business process. It allows users to retrieve detailed transactions for a business entity by looking up a familiar business key.

The second is the storytelling dimension. It sits at the opposite end of the spectrum. As explained in the Storytelling chapter, a storytelling dimension categorises business entities into a digestible number of journeys. It is often the front door of the model: the first high-level lens through which users enter the data.

The presence of both ID dimensions and storytelling dimensions suggests that the data engineer has considered a broad range of user needs. It is not a guarantee of quality, but it is a useful sign.

The full set of useful dimensions is covered in the next chapter on the [components of a dimensional model](/docs/presenting-insights/dimensional-modelling-for-ux/).

### Facts and measures

Power BI is designed so that users primarily interact with dimensions and measures rather than facts. This is explained in greater depth in the chapter on [filtering behaviour](/docs/presenting-insights/filtering-behaviour/).

For now, it is enough to note that a good Power BI dimensional model usually reduces the prominence of fact tables. In the ideal case, fact tables are hidden from the user.

A related sign is the absence, or at least limited use, of degenerate dimensions (attributes stored directly in the fact table rather than in a separate dimension) in fact tables. A proliferation of degenerate dimensions suggests that the model is working against the natural filtering behaviour of Power BI. It also indicates that business information has been left as miscellaneous attributes of business processes rather than articulated as standalone properties that deserve dimension tables.

Measures become more prominent as fact tables become less visible. A good dimensional model invests heavily in measures.

As a rough rule of thumb, each fact table representing a business process should usually have at least ten measures. This reflects the reality that there are often many metrics needed to understand a business process. For example, a sales process may require measures for sales volume, turnaround time, profit, cost, and related percentages.

If the model has implemented the concept of "good" and "bad", this often leads to sub-measures for each category. Percentages and other derivatives quickly add more.

If users can grab ready-made measures and arrive at useful answers with minimal effort, this is a strong sign of a good model. It shows that the data engineer has thought carefully about the business process and placed important information at the user's fingertips.

Conversely, a lack of ready-to-use measures means that the data engineer has not sufficiently engaged with the business intent of the user.

When a model contains many measures, measure management becomes important. A good pattern is to place all measures into a single table at the top of the field list. A suitable name for this table is simply `Measure`.

Power BI supports this behaviour. If all columns in a table are hidden and the table contains at least one measure, Power BI places the table at the top of the field list. This indicates a model that elevates measures to first-class status.

Measures should be organised by display folders. By default, these folders should be grouped by business process. For example, a model with the processes `Manufacture`, `Order`, and `Shipping` could have folders called `"Manufacture"`, `"Order"`, and `"Shipping"`.

<!-- > [!NOTE]
> TODO: Insert manuscript screenshot or diagram from the source draft. -->

The prominence of measures, their business-centricity, and their organisation through business processes are strong contributors to the look and feel of a good data model.

Measures are also easier to define when the pipeline has already created meaningful fragments at the right grain. A good model should not rely on complex measures to compensate for missing upstream structure.

### Relationships

Relationships in a Power BI model define user interactivity.

Following the theme of using dimensions as the main point of interaction, dimensions should filter facts and not the other way around.

A good sign is that, if a piece of information is known to a business process, the dimension representing that information should filter the corresponding fact.

For example, consider a model with two processes: `Manufacture` and `Shipping`.

The `Product` dimension should filter both facts if both processes know the product. `Manufacture` captures the product directly. `Shipping` inherits the product because shipped items trace back to what was manufactured.

By contrast, the `Shipping date` dimension should filter only the `Shipping` fact. It should not filter `Manufacture`, because shipping occurs at the shipping grain. One manufactured batch may be shipped across multiple dates, so there is no single shipping date that naturally belongs to the manufacture process.

This does not mean that each business process is filtered only by its own attributes. For example, all fact tables may be filtered by `Manufacture date` if the shipment tracks back to a manufacture batch.

The criterion is whether the dimension belongs naturally to the grain of the fact being filtered.

| Dimension | Manufacture | Shipping |
|---|---|---|
| Product | 1 → * | 1 → * |
| Manufacture date | 1 → * | 1 → * |
| Shipping date |  | 1 → * |

Relationships are explored in greater depth in the chapter on [anticipating questions](/docs/presenting-insights/anticipating-questions/).

Since dimensions are the user's access point to the model, the column on the filtered side of the relationship, usually in the fact table, should be hidden to avoid ambiguity. The user should use the column on the filtering side, usually in the dimension.

## Conclusion

This chapter sketched what a good dimensional model looks like.

The purpose is not to provide a definitive checklist that guarantees quality. It is to attune the data engineer to the look and feel of a good model in Power BI by taking the perspective of the user.

A list of signs is helpful, but the best test is for the data engineer to use the model personally and ask a range of real business questions. This is part of conducting visual checks.

This task requires deep familiarity with the business and strong curiosity about the subject matter. It cannot be reduced to ticking off formal requirements.

The common theme is business centricity and intuitive use. A good model implements answers explicitly so that they appear naturally. It does not require the user to interpret technical structure or apply guesswork.

The Zen of Python is a useful guide to designing a dimensional model. Its emphasis on explicit over implicit, and on having one—and preferably only one—obvious way of doing something, applies directly to Power BI model design.

> [!NOTE]
> **Key ideas**
>
> A good dimensional model lets users ask real business questions without guessing.
>
> A dimensional model is judged by the experience it creates for users, not only by whether has the technically correct information.
>
> It should resonate with the business view, feel intuitive and unambiguous, anticipate reasonable questions, support both summary and detail, and perform quickly.
>
> The signs of a good model are business-friendly names and metadata, useful dimensions, ready-to-use measures, and relationships that support natural filtering.
>
> A strong model makes answers appear naturally because the data engineer has already made the hard design decisions.
