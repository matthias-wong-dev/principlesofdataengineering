---
title: Anticipating questions
url: /docs/presenting-insights/anticipating-questions/
description: Shows how to design a Power BI dimensional model that preserves enough business structure to answer future questions, not only current requirements.
lede: A strong dimensional model preserves the structure needed to answer questions before they are formally asked.
weight: 2
# draft: true
---

## Designing for questions not yet asked

A good dimensional model does not merely answer the questions already written in requirements. It preserves enough business structure to answer all the questions users are likely to ask during the model’s lifetime.

This expectation can surprise data engineers who come from an application-development background. In application development, the work often begins by defining requirements with stakeholders and building accordingly. Even when development is iterative, it is still usually organised around delivering stated requirements.

That approach has its place, but analytics behaves differently.

In data work, answering one question often creates the next question. Users discover what they want to ask by interacting with the data. They may begin with a simple requirement, such as “show quality-control failures by month”, but once the data is visible, they will ask follow-up questions: Which products failed? Which batches? Which suppliers? Which customers were affected? Did shipping outcomes change afterward?

A data project focused only on stated requirements is therefore likely to frustrate everyone. If stakeholders have little interest, the stated requirements may be shallow. If stakeholders are engaged, the requirements will keep changing as the data reveals new possibilities.

The data engineer cannot predict every future question. But good design can preserve the structure from which future questions can be answered.

This is the purpose of anticipating questions.

Power BI dimensional models are well suited to this task because facts represent business processes, dimensions represent business information, and relationships determine which questions can be answered through filtering.

Instead of ticking off stated requirements, the data engineer should identify the business processes, the information known to those processes, and the information shared across processes. These become the facts, dimensions, and relationships of the dimensional model.

To develop a model that anticipates questions and captures the breadth of information, the data engineer can remember a simple three-step process:

1. All the facts—business processes
2. All the dimensions—business information
3. All the relationships—real-world relationships mirrored in the model

Each step has an artefact to help the data engineer and business stakeholders check the comprehensiveness of the model.

## All the facts

The first step to building a dimensional model that can anticipate all reasonable questions is to ensure it captures all the relevant business processes. For ease of memory, this is the step to capture “all the facts.”

This step can be non-trivial for two reasons.

First, in a complex business, many teams work together to complete a single goal. These teams often operate across different business processes. The data engineer and project team are usually working with a particular stakeholder group that focuses on specific processes rather than the full set. For example, some may focus on manufacturing, some on ordering, and others on quality control.

Second, different stakeholders often take different views of the same process. Operational staff may focus on detailed steps, while others take a broader, strategic view. Speaking with any one group always results in a skewed perspective.

In other words, the data engineer faces two challenges—how much to include, and how zoomed out the view should be.

Consider the following example of business processes:

1. Research and development
2. Sourcing materials
3. Manufacture
4. Quality control
5. Orders
6. Shipping
7. Customer feedback

For the question “what are the different business processes to include?”, the data engineer should be as comprehensive as possible during horizon scanning. This means being persistent in asking “where does this come from?” and “where is this going to?” until the end-to-end is covered.

A useful rule of thumb is to trace the process beyond the immediate team: where did the work come from, and where does it go next? For end-to-end process discovery, it can help to ask where the work first enters the organisation and where its effect eventually leaves.

Once all the processes are identified, it becomes easier for stakeholders to collectively decide which ones to include. Usually, there is a shared sense of what is core and what is peripheral. This is a different question from “what are your requirements?”

Requirements tend to narrow the perspective.

For example, a manager of quality control may focus narrowly on their part of the process. If the project is driven by this stakeholder—perhaps because quality control initiated the engagement—the requirements may be framed as “how much is spent on quality control?” or “how many products are failing?” Such a view is unhelpfully narrow.

Instead, the data engineer can help by identifying the full business process. The manager may then recognise that, even though reporting on the cost of manufacture is not a “must-have requirement” for quality control, it is still a core business process.

Research and development, by contrast, may be considered peripheral.

For the question “how zoomed out should the view be?”, the answer is to work at a level that makes sense for decision-making. It does not help to model the lowest-level details such as sending emails or looking up documents. On the other hand, it is also not helpful to see manufacturing and quality control as one large step.

Zooming out often involves grouping sub-processes into a single process, or denormalising detail rows into header-level structures that expose a broader grain.

For example, the quality control process may involve multiple testing steps for different criteria. Rather than creating one fact table for quality samples and another for quality sample tests, it may be more expressive to model the process as a single fact called `'Quality control'`, with the lower-level testing detail embedded where appropriate.

Power BI’s flexibility with its DAX engine supports this approach. In simple cases, a `distinctcount` can recover the embedded grain, such as counting headers by their ID. In more complex cases, DAX can still retrieve the embedded grain, as explained in [Designing measures](/docs/presenting-insights/designing-measures/).

This question often challenges engineers trained in traditional dimensional modelling who are learning Power BI for the first time. The classical approach tends to split facts by grain rather than by business process. This can obscure the business view.

The artefact for this step is the linear process diagram. A linear process diagram is a business process diagram using only linear steps with no branching, cycles, or decision trees. Readers find linear diagrams much easier to understand than diagrams with arrows pointing in all directions. The constraint of linearity forces the business analyst to abstract the process to a level that is useful for themselves and others. This is especially true for executive audiences.

It can also be helpful to categorise the business processes into higher-level categories.

Continuing with the example above:

- Design—Research and development
- Production—Sourcing, Manufacturing, Quality control
- Sales—Orders, Shipping, Customer feedback

{{< svg >}}
<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="360" viewBox="0 0 1080 360"
     style="background:transparent" role="img"
     aria-label="Linear process diagram showing design, production, and sales stages from research and development to customer feedback">

  <defs>
    <marker id="arrowhead-linear-process" markerWidth="10" markerHeight="8"
            refX="10" refY="4" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L10,4 L0,8 z" fill="#222222"/>
    </marker>
  </defs>

  <!-- Category bands -->
  <rect x="70" y="55" width="175" height="55" rx="14"
        fill="#ffffff" stroke="#222222" stroke-width="1.6"/>
  <text x="157.5" y="90" text-anchor="middle"
        font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
        font-size="21" font-weight="700" fill="#111111">Design</text>

  <rect x="305" y="55" width="430" height="55" rx="14"
        fill="#ffffff" stroke="#222222" stroke-width="1.6"/>
  <text x="520" y="90" text-anchor="middle"
        font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
        font-size="21" font-weight="700" fill="#111111">Production</text>

  <rect x="795" y="55" width="215" height="55" rx="14"
        fill="#ffffff" stroke="#222222" stroke-width="1.6"/>
  <text x="902.5" y="90" text-anchor="middle"
        font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
        font-size="21" font-weight="700" fill="#111111">Sales</text>

  <!-- Process nodes -->
  <rect x="70" y="175" width="175" height="70" rx="14"
        fill="#ffffff" stroke="#222222" stroke-width="1.6"/>
  <text x="157.5" y="204" text-anchor="middle"
        font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
        font-size="18" font-weight="700" fill="#111111">Research and</text>
  <text x="157.5" y="228" text-anchor="middle"
        font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
        font-size="18" font-weight="700" fill="#111111">development</text>

  <rect x="305" y="175" width="130" height="70" rx="14"
        fill="#ffffff" stroke="#222222" stroke-width="1.6"/>
  <text x="370" y="204" text-anchor="middle"
        font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
        font-size="18" font-weight="700" fill="#111111">Sourcing</text>
  <text x="370" y="228" text-anchor="middle"
        font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
        font-size="18" font-weight="700" fill="#111111">materials</text>

  <rect x="465" y="175" width="130" height="70" rx="14"
        fill="#ffffff" stroke="#222222" stroke-width="1.6"/>
  <text x="530" y="217" text-anchor="middle"
        font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
        font-size="18" font-weight="700" fill="#111111">Manufacture</text>

  <rect x="625" y="175" width="130" height="70" rx="14"
        fill="#ffffff" stroke="#222222" stroke-width="1.6"/>
  <text x="690" y="204" text-anchor="middle"
        font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
        font-size="18" font-weight="700" fill="#111111">Quality</text>
  <text x="690" y="228" text-anchor="middle"
        font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
        font-size="18" font-weight="700" fill="#111111">control</text>

  <rect x="795" y="175" width="95" height="70" rx="14"
        fill="#ffffff" stroke="#222222" stroke-width="1.6"/>
  <text x="842.5" y="217" text-anchor="middle"
        font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
        font-size="18" font-weight="700" fill="#111111">Orders</text>

  <rect x="920" y="175" width="95" height="70" rx="14"
        fill="#ffffff" stroke="#222222" stroke-width="1.6"/>
  <text x="967.5" y="217" text-anchor="middle"
        font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
        font-size="18" font-weight="700" fill="#111111">Shipping</text>

  <rect x="795" y="285" width="220" height="55" rx="14"
        fill="#ffffff" stroke="#222222" stroke-width="1.6"/>
  <text x="905" y="320" text-anchor="middle"
        font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
        font-size="18" font-weight="700" fill="#111111">Customer feedback</text>

  <!-- Arrows -->
  <line x1="245" y1="210" x2="305" y2="210"
        stroke="#222222" stroke-width="2"
        marker-end="url(#arrowhead-linear-process)"/>

  <line x1="435" y1="210" x2="465" y2="210"
        stroke="#222222" stroke-width="2"
        marker-end="url(#arrowhead-linear-process)"/>

  <line x1="595" y1="210" x2="625" y2="210"
        stroke="#222222" stroke-width="2"
        marker-end="url(#arrowhead-linear-process)"/>

  <line x1="755" y1="210" x2="795" y2="210"
        stroke="#222222" stroke-width="2"
        marker-end="url(#arrowhead-linear-process)"/>

  <line x1="890" y1="210" x2="920" y2="210"
        stroke="#222222" stroke-width="2"
        marker-end="url(#arrowhead-linear-process)"/>

  <path d="M967.5 245 L967.5 265 Q967.5 285 947.5 285 L905 285"
        fill="none" stroke="#222222" stroke-width="2"
        marker-end="url(#arrowhead-linear-process)"/>

</svg>
{{< /svg >}}

<div style="max-width:42rem;margin:0.5rem;text-align:center;font-size:0.95rem;color:#666;">
Figure 1. Linear process diagram. Business processes are arranged in chronological order and grouped into Design, Production, and Sales.
</div>

Making linear process diagrams does not mean that business analysts cannot create more complex diagrams for other purposes. However, these are not linear process diagrams for model planning.

The identified business processes form the facts of the dimensional model. Hence this step can be remembered as “all the facts.” The processes selected for the model define its scope. For example, if the decision is to focus on manufacturing onwards, then questions about research and development or sourcing will fall outside the model’s scope.

Identifying the business processes is the hardest part of anticipating questions. It involves making business decisions and requires a high degree of judgement and practical experience. Once the processes are identified, the next step of identifying the business information follows more mechanically.

## All the dimensions

The second step, after identifying the business processes in scope, is to identify all the business information known to those processes. This ensures that all reasonable questions about the processes included in the model can be answered. For ease of memory, this is the step to capture “all the dimensions.”

The key distinction is between information a process captures and information a process knows.

This step is more straightforward than identifying the processes. Business stakeholders usually know what information is captured. While there may be debate about the relative importance of one attribute over another, the answer is often that they are all important. If they were not, they would not be captured in the first place.

The nuance for the data engineer is to distinguish between what is captured by a business process and what is known to it. The general rule is that downstream processes inherit information from upstream ones.

Consider the following example. Suppose each process captures the following information:

- Manufacturing—Product type, Manufacture details (date, batch number)
- Quality control—Testing details (manufacture sample, date, criteria, results)
- Orders—Product type, Customer, Order details (date, order units, sales amount, order number), Order status
- Shipping—Shipping order (order number, line items), Shipping logistics (shipping method, shipping company), Shipping status (date, status)
- Customer feedback—Customer, Product type, Feedback details (method, star rating, comments)

In this example, the order process captures product type, customer and order units.

The shipping process does not capture these directly but knows them through the order number. This is inheritance. However, not all downstream processes inherit everything.

For example, customer feedback may not record the order number and may only capture the product type. In that case, it does not know the order date, even though it is downstream.

Once the information is identified, it can be presented using a cumulative information diagram. This is a table with business information as rows and business processes as columns, both listed in chronological order. The diagram is cumulative because information typically accumulates downstream through inheritance.

Rows are business information. Columns are business processes. `C` means the process captures the information directly. `I` means the process inherits the information from an upstream process.

It is also helpful to annotate the diagram with where the information is physically stored—which database or table holds each attribute. This helps assess what can be reasonably answered and informs project planning.

The example below shows what information is known to each business process.

The linear process diagram describes the real-world business processes. The cumulative information diagram builds on the linear process diagram by showing how information flows through those processes and where it is stored in the database world.

| Business information | Manufacture | Quality control | Orders | Shipping | Customer feedback |
|---|---|---|---|---|---|
| Product type | C | I | C | I | C |
| Manufacturing details | C | I | | | |
| Testing details | | C | | | |
| Order status | | | C | I | |
| Order details | | | C | I | |
| Customer | | | C | I | C |
| Shipping order | | | | C | |
| Shipping logistics | | | | C | |
| Shipping status | | | | C | |
| Feedback details | | | | | C |
| Database storage | XYZ SQL database | ABC diagnostics database | XYZ SAP ERP | XYZ SAP ERP | Salesforce analytics |

In other words, the cumulative information diagram maps real-world processes to database storage.

Since business information becomes dimensions in a dimensional model, this step can be remembered as “all the dimensions.”

## All the relationships

The final step is to ensure that the business processes and their known information are reflected in the dimensional model through filtering relationships. If all relevant processes are captured, all relevant information is identified, and valid relationships are correctly implemented, then the model can anticipate all reasonable questions.

A relationship is not only a technical join. In a Power BI model, a relationship is a path by which a user’s question can reach a fact.

The rule of thumb is simple. If a business process knows a piece of information, whether by direct capture or by inheritance, then the corresponding dimension should filter that fact table.

Continuing with the earlier example, suppose `'Order ID'`, `'Order calendar'`, and `'Customer'` are dimensions, and `'Orders'` is the fact table. These dimensions should directly filter `'Orders'`. The `'Shipping'` fact table should also be filtered by `'Order ID'`, since shipping needs to know the order number. In this case, `'Order ID'` is a conformed ID dimension for both processes. The `'Order calendar'` and `'Customer'` dimensions should also filter `'Shipping'`, because this process inherits them through the order number.

New data engineers often forget about inheritance. This creates a frustrating experience for users who expect to retrieve all shipments for a customer but find the model does not support the question due to a missing relationship.

There are exceptions to inheritance. Sometimes an upstream process has a zero-to-many relationship with a downstream one. In these cases, including the upstream information as a filter may be problematic.

For example, suppose the quality control process usually tests manufactured batches, but sometimes tests other aspects not tied to a specific batch, such as testing factory equipment itself. In this case, `'Manufacture ID'` should filter `'Quality control'` so users can look up testing for a batch. However, it may be better not to implement a filtering relationship between `'Manufacture calendar'` and `'Quality control'`. In Power BI, if a user selects a manufacture date, this relationship will also filter `'Quality control'` and affect any measures, even when the test was unrelated to a batch.

It may be sufficient to use a role-playing `'Reporting calendar'` that filters `'Manufacture'` on manufacture date and `'Quality control'` on testing date. This avoids misleading results. If the relationship is implemented, the report design must be careful not to mislead users with incorrect numbers caused by unintended filters.

Usually, upstream processes tend not to know about downstream processes. This means that `'Customer'` should not filter `'Manufacture'` because this information does not exist at the time of manufacture. However, the data engineer has the benefit of hindsight, so some information can be brought back to the earlier process. For example, while the quality-control results of a manufactured batch are not known at the time of manufacture, the result can be associated to the batch number afterwards.

To express this at the batch-number grain, multiple quality control criteria may need to be rolled back to the batch for an overall pass or fail. A dimension for `'Batch quality outcome'` can be used to filter `'Manufacture'`. In general, storytelling dimensions summarise the journey of an entity through the whole business process and can be associated to all steps of the process in hindsight.

The artefact for this step is the chronological bus. A bus matrix is a table that lists dimensions as rows and facts as columns, showing which dimensions filter which facts. In Power BI, this should reflect the actual filtering relationships, including their cardinality. A chronological bus matrix is one where the facts and dimensions are sorted in chronological order of their occurrence in the business.

The chronological bus is the main planning artefact of the dimensional model. It shows, at a glance, which information can filter which business processes.

The diagram for our example is below. The symbol `1 -> *` is used to indicate one-to-many, while `* -> *`, which is used for product type and customer feedback, indicates a many-to-many relationship. The latter means one customer-feedback record may relate to several products at once.

| Dimension | Manufacture | Quality control | Orders | Shipping | Customer feedback |
|---|---|---|---|---|---|
| Reporting calendar | 1 -> * | 1 -> * | 1 -> * | 1 -> * | 1 -> * |
| Manufacture ID | 1 -> * | 1 -> * | 1 -> * | 1 -> * | |
| Manufacture calendar | 1 -> * | | 1 -> * | 1 -> * | |
| Batch number | 1 -> * | 1 -> * | 1 -> * | 1 -> * | |
| Batch quality outcome | 1 -> * | 1 -> * | 1 -> * | 1 -> * | |
| Product type | 1 -> * | 1 -> * | 1 -> * | 1 -> * | * -> * |
| Testing ID | | 1 -> * | | | |
| Testing date | | 1 -> * | | | |
| Quality criteria | | 1 -> * | | | |
| Testing result | | 1 -> * | | | |
| Order ID | | | 1 -> * | 1 -> * | |
| Order calendar | | | 1 -> * | 1 -> * | |
| Customer | | | 1 -> * | 1 -> * | 1 -> * |
| Order status | | | 1 -> * | 1 -> * | |
| Shipping calendar | | | | 1 -> * | |
| Shipping company | | | | 1 -> * | |
| Shipping status | | | | 1 -> * | |
| Arrival date | | | | 1 -> * | |
| Feedback calendar | | | | | 1 -> * |
| Feedback sentiment (star ratings) | | | | | 1 -> * |

The chronological bus can be used to evaluate what questions are answered by the model.

In the above example, because `'Customer'` is a conformed dimension for `'Orders'`, `'Shipping'`, and `'Customer feedback'`, it is possible to identify customers by the volume of orders, shipping delays, and feedback results.

Because `'Product type'` is a conformed dimension on all processes, it is the attribute that the model can answer most questions for, such as comparing quality-control results with customer feedback. Note, however, the many-to-many relationship between `'Product type'` and `'Customer feedback'` indicates that any assignment of feedback to product is approximate and may double-count.

Because `'Manufacture ID'` is a conformed ID dimension from `'Manufacture'` to `'Shipping'`, the model can support traceback of faulty products that have been shipped.

On the other hand, it is not possible to directly analyse the effect of shipping on customer feedback because shipping information does not filter the customer-feedback fact.

Such analysis may be possible indirectly through `'Reporting calendar'`, `'Product type'` and `'Customer'`, which together may narrow the transactions down to a segment that correlates shipping status and shipping company with feedback sentiment. If this can be done systematically, it can be introduced as precomputed information in the data pipeline.

Ensuring that the model’s relationships match the real-world flow of information means the model behaves in ways users intuitively expect. Downstream processes tend to inherit from upstream ones. By default, upstream processes do not know downstream outcomes. When downstream outcomes are brought back upstream, they should be deliberately modelled.

As a result, the chronological bus is typically dense in the upper right. This structure makes gaps easy to spot. These gaps may be accidental, reflect a limitation in the source system, or be a deliberate design choice.

In the example above, `'Manufacture calendar'` does not filter `'Quality control'`. This is a design decision. It does not filter `'Customer feedback'` either, which is a limitation because the information is not recorded. This example does not have any accidental gaps. If there were, they would stand out.

The chronological bus only works if the data engineer has modelled information as dimensions, processes as facts, and listed them in chronological order.

The same information becomes much less useful when sorted alphabetically:

| Dimension | Customer feedback | Manufacture | Orders | Quality control | Shipping |
|---|---|---|---|---|---|
| Arrival date | | | | | 1 -> * |
| Batch number | | 1 -> * | 1 -> * | 1 -> * | 1 -> * |
| Batch quality outcome | | 1 -> * | 1 -> * | 1 -> * | 1 -> * |
| Customer | 1 -> * | | 1 -> * | | 1 -> * |
| Feedback calendar | 1 -> * | | | | |
| Feedback sentiment (star ratings) | 1 -> * | | | | |
| Manufacture calendar | | 1 -> * | 1 -> * | | 1 -> * |
| Manufacture ID | | 1 -> * | 1 -> * | 1 -> * | 1 -> * |
| Order calendar | | | 1 -> * | | |
| Order ID | | | 1 -> * | | 1 -> * |
| Order status | | | 1 -> * | | 1 -> * |
| Product type | * -> * | 1 -> * | 1 -> * | 1 -> * | 1 -> * |
| Quality criteria | | | | 1 -> * | |
| Reporting calendar | 1 -> * | 1 -> * | 1 -> * | 1 -> * | 1 -> * |
| Shipping calendar | | | | | 1 -> * |
| Shipping company | | | | | 1 -> * |
| Shipping status | | | | | 1 -> * |
| Testing date | | | | 1 -> * | |
| Testing ID | | | | 1 -> * | |
| Testing result | | | | 1 -> * | |

In comparison, this matrix is difficult to read. This remains true even though the dimension names have been deliberately prefixed to group similar attributes together, and “Manufacture”, “Order” and “Shipping” happen to sort roughly chronologically. In any other instance, the bus matrix would be incomprehensible.

Consequently, the three-step process of linear process diagram, cumulative information diagram, and chronological bus is not an accident. It is designed to make it simple for the data engineer to keep track of information, visualise what questions can be answered, and thus accomplish the goal of anticipating questions.

The bus matrix is also a chance to check naming. Dimensions should be nouns because they represent business attributes or information. Fact names should usually be process-oriented because facts represent business processes.

The relationship between business information and business processes is mirrored in the relationship between dimensions and facts. Hence this step can be remembered as “all the relationships.”

## Conclusion

The three-step approach guides the data engineer to work on the information captured in business processes, rather than the stated requirements of “I would like to see X by Y”. The focus is on preserving information, not on answering specific questions.

The three steps and their artefacts can be summarised in a table like this:

| Step | Content | Artefact |
|---|---|---|
| All the facts | Identify all the business processes. | Linear process diagram. Shows all the major steps in a business, set at a level that makes sense to decision-making. |
| All the dimensions | Identify all the information captured or inherited by the processes. | Cumulative information diagram. Shows all the information relevant to the business, how it flows, and where it is physically stored. Used to inform what can be reasonably answered. |
| All the relationships | Relate information to its processes in the dimensional model. | Chronological bus. Shows the dimensional model that is implemented. Used to identify which possible questions can or cannot be answered, particularly any gaps. |

Following these three steps ensures the full range of information is preserved, and questions relating to this information can be answered because the relationships exist in the model.

This breadth of information requires a variety of modelling techniques. The later chapters in this section explain how filtering, measures, measure families, and security patterns make the preserved structure usable.

In future, when a user asks a different question, the model can answer it if the relevant information has already been articulated in the dimensional model.

This is how the data engineer anticipates questions.



> [!NOTE]
> **Key ideas**
>
> A strong dimensional model preserves enough business structure to answer all reasonable future questions.
>
> Requirements tend to narrow attention; analytical modelling must preserve the structure from which follow-up questions can be answered.
>
> “All the facts” means identifying the business processes that should become fact tables.
>
> “All the dimensions” means identifying the information captured or inherited by those processes.
>
> “All the relationships” means implementing the filtering paths that mirror what each process knows.
>
> The three planning artefacts are the linear process diagram, the cumulative information diagram, and the chronological bus.
>
> The chronological bus shows which questions the model can and cannot answer.