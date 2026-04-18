---
title: Filtering behaviour
description: Examines how filtering works in Power BI and how dimensions, measures, and relationships shape user interaction with a model.
lede: In Power BI, filtering behaviour is the heart of user interaction.
weight: 4
draft: true
---

Filtering is the driver for an interactive user experience in Power BI. Filtering occurs when a slice of the model’s data is selected for display or calculation based on a user action. Filtering can also be complex. If used inappropriately, the model can quickly become frustrating or error prone. Consequently, data engineers need to have a deep, almost second-nature understanding of how Power BI filtering works in practice, and the options available for different scenarios. Newcomers to Power BI often use bidirectional relationships incorrectly. An early and deep understanding of Power BI filtering behaviour will allow data engineers to use the right configuration instead of bidirectional relationships.

## Ways of filtering

There are five common ways of filtering in Power BI:

- Directly through a table relationship

- Indirectly through common filtered tables

- In a table by a non-blank measure value

- In a visual by a visual-level filter

- On-demand through a measure formula

Directly through a table relationship This is the standard case of filtering. When a table X filters another table Y, a user who selects a value from X will narrow down to the rows in Y based on the primary key and foreign key relationship. The most important case of table relationship is when dimension tables filter fact tables. Dimension tables are typically small in cardinality, and the resulting relationship is highest performing. New engineers often ask, "Why do we need dimensions at all? Why not leave all the information in the fact table? It is simpler." That is, why not rely solely on degenerate dimensions? There are three reasons for this. First, nonexistence is impossible to express with degenerate dimensions. For instance, if the full set of reference values are "Red", "Blue", and "Yellow", but the transaction table does not have "Yellow", then this absence cannot be communicated without a dimension that has the full list. Second, a proper dimension table is important for expressiveness. If the attributes are embedded in a fact table, the set of attributes, such as demographic details, become lost in the fact. Indeed, even the grain becomes unclear when attributes are

denormalised into a fact table. A user would have to read every single row to reverse engineer the entity and its grain. Third, cross filtering or drill through of multiple processes are impossible with degenerate dimensions. The simplest example is that of the calendar. Without a calendar dimension, each fact table would have its own business date for its business process, and these cannot be used to compare the measures between two processes. Similar applies to other attributes such as region or product. Indirectly through common denominators Filtering also propagates indirectly — through shared dimensions across multiple tables. This behaviour is often missed by new engineers but is just as essential. Consider two dimension tables Dim1 and Dim2, and a fact table Fact1. Suppose Dim1 filters Fact1. Now consider two cases:

- If Dim2 does not filter Fact1, dragging Dim1 [X] and Dim2 [Y] into the same visual

causes an error: "Can’t determine a relationship". In this case, Power BI does not produce a cross product of all results.

- If Dim2 does filter Fact1, Power BI returns only combinations of [X] and [Y] that

share a row in Fact1. This behaviour is visible in the DAX query via the Performance Analyzer. If multiple fact tables (Fact2, Fact3, Fact4, etc) are filtered by both Dim1 and Dim2, then a visual containing Dim1 [X] and Dim2 [Y] will show combinations where any fact table has a matching row. > [!NOTE]
> TODO: Insert manuscript screenshot or diagram from the source draft. This "upward" filtering from facts to dimensions enables the intuitive experience of a dimensional model. It is why dimensions alone can serve as the interface, even when facts are hidden. Mastering this behaviour is central to dimensional modelling. In a table by a non-blank measure value The previous method relies on implicit filtering via relationships. In simple models, this suffices. In complex models with five or more fact tables, it may not. Measures can be used to explicitly control filtering. Suppose Dim1 filters Fact1, and a measure [Measure1] counts rows in Fact1. Dragging Dim1 [X] into a table visual shows all values of [X]. But when [Measure1] is added, only values of [X] with a nonblank [Measure1] remain. If [Measure2], [Measure3], etc. are added, the visual retains only values of [X] where any measure returns a value.

This mirrors fact table filtering, but with greater control. The data engineer defines which values are retained, rather than relying on implicit row existence. > [!NOTE]
> TODO: Insert manuscript screenshot or diagram from the source draft. In a visual by a visual-level filter Sometimes the measure cannot be placed directly in the visual, as with slicers, or doing so would interfere with layout. In these cases, the report developer can apply a visual level filter using the measure value. This allows filtering without altering the visual’s structure. > [!NOTE]
> TODO: Insert manuscript screenshot or diagram from the source draft. If possible, this method should be avoided. The evaluation cost can be significant on a visual with a large number of rows for which to calculate the measure value. On-demand through a measure formula The previous methods allow the report developer to control which dimensional values are displayed in a visual. The prototypical context is the columns in a table visual, but also the columns and rows in a matrix visual. > [!NOTE]
> TODO: Insert manuscript screenshot or diagram from the source draft. There are occasions when the data engineer needs to apply filters directly on the data that feeds a measure. A measure, unlike dimension values, is not a fixed value in the data. It is defined by a formula and returns only one value at a time. The prime example is a visual card. > [!NOTE]
> TODO: Insert manuscript screenshot or diagram from the source draft. Usually, the need to apply a specific measure level filter arises because the standard model relationships do not support the intended outcome. In this circumstance, the filtering context must be created inside the measure definition. Power BI supports this through DAX expressions such as USERELATIONSHIP and CROSSFILTER. These expressions allow the data engineer to activate a relationship between tables on demand, even if that relationship is not defined in the model schema.

## Filtering scenarios

The five filtering patterns above can be combined to support a wide range of interactivity goals, all within the standard dimensional model framework of dimensions filtering facts using single directional relationships. Displaying unit records (single business process) A common requirement is for business users to view all the details of a business process. Suppose we have a business process represented by the 'Sales' fact table. In

the ideal setup, the 'Sales' fact table is hidden and represented through its dimensions and a single measure. The set up is as follows:

- A fact table ‘Sales’

- The ID dimension 'Sales ID' with business key [Sales order number]

- The calendar dimension 'Sales calendar'

- The business dimension 'Sales product'

- The measure [Total sales amount] which sums up the sales amount in Sales

When you place dimension fields together with 'Sales ID'[Sales order number], Power BI returns only combinations of dimension values that correspond to existing rows in the fact. Since 'Sales ID'[Sales order number] is the business key for a sales transaction, it uniquely identifies the row in 'Sales'. Adding 'Sales ID'[Sales order number], 'Sales calendar'[Sales date], and 'Sales product'[Product name] returns the complete transaction context for each sale. Sales also have an amount recorded in 'Sales'[Sales amount] on the fact table. A simplistic approach is to place this column on the canvas, treating it like a degenerate dimension. A better approach is to use the measure [Total sales amount]. Because 'Sales ID'[Sales order number] uniquely identifies a single row, [Total sales amount] returns the correct result as the sum of that one row in the current context, which is the same numeric value as 'Sales'[Sales amount] for that transaction. While this sounds complex in the backend, it is seamless for the user. In the ideal setup, the fact table and thus 'Sales'[Sales amount] is hidden. The user only sees the measure [Total sales amount] and does not see both the measure and the raw 'Sales'[Sales amount] column, which removes ambiguity. This is far superior to exposing both the measure and the raw column. In this instance, both would show the same number for each transaction, which encourages users to treat them as interchangeable. In other contexts such as charts, aggregations, and time intelligence, only the measure behaves correctly. That inconsistency is confusing when something appears to work in one visual but not in another. With this setup, [Total sales amount] behaves intuitively across all situations, so users get consistent results without needing to remember special cases. It is important to consider how the user experience changes depending on the order in which fields are selected:

- First 'Sales ID'[Sales order number], then 'Sales calendar'[Sales date]

This immediately gives the valid combination of sales order numbers and sales date because the combination of dimension values is filtered by their common

facts (second method of filtering). This gives desired unit-level transaction record because the business key selects the correct grain.

- First 'Sales ID'[Sales order number], then [Total sales amount]

This also immediately gives the unit-level transaction record. However, this time it is not because of the common fact (second method of filtering), but because [Total sales amount] returns a non-blank measure value for the [Sales order number] (third method of filtering). If there are sales order numbers without a sales amount (for example, unconfirmed sales), those order numbers will not appear. This is, for most use cases, the desired outcome.

- First [Total sales amount], then 'Sales product'[Product name]

This initially returns the total sales amount for the entire model as a single number, then breaks it down by product. When the user adds 'Sales ID'[Sales order number], the table expands to the unit record. In other words, the user experience is "correct" at every step. What we see is that, regardless of the sequence of field selection, the model produces sensible business results at every step. This is the power of a properly designed dimensional model focused on dimensions and measures, with single-direction filters on facts. This seamless experience would not occur if the user had selected the degenerate 'Sales'[Sales amount] instead of [Total sales amount] in the last scenario. The user would first see a distinct list of sales amount values, then an incomprehensible combination of sales amount and product, and only after adding 'Sales ID'[Sales order number] would the table make sense. The experience would be jarring rather than seamless. This is another reason to hide 'Sales' altogether and avoid exposing any degenerate numeric values. There is also an additional consideration of what happens when there are existing filters on the canvas, such as a filter on product name or date. While all the previous sequences still work, the most seamless outcome occurs when the user starts with the measure [Total sales amount], as in the last sequence. We do not expand on this here and leave it as an exercise for the reader. Even though this is a simple use case of presenting transaction records for a single business process, there is careful modelling work behind the scenes to create a seamless experience that caters to a staggering number of possibilities. All these possibilities are elegantly handled if the data engineer uses the best practice of focusing on dimensions and hiding facts. In this example, ‘Sales ID’[Sales order number] is a single column business key. If the business key were multi-columns, then all columns need to be used.

Displaying unit records (two business processes) Continuing with the previous example, consider the situation where sales can be refunded, modelled as follows:

- A fact table 'Refund'

- The calendar dimension 'Refund calendar'

- Refunds can be tracked to the original sales order number and are filtered by all

dimensions that filter 'Sales'

- There is no business key for a refund, and hence no 'Refund ID'

- A measure [Total refund amount] which sums the refund amount. Because there

can be partial refunds, this does not equal [Total sales amount] even for the same sales order [Screenshot] In this model, the user may want to see the transactions for sales, for refund, and sometimes for both simultaneously. Displaying sales When displaying records for sales, everything works as if there were only the 'Sales' fact table. This is because Power BI shows combinations of dimension values if there are valid rows in any of the fact tables they share. Since every refund comes from a sale, the 'Sales' fact table is a superset of 'Refund', so adding the refund fact table does not cause an issue. The fact that 'Sales' is a superset of 'Refund' is essential. If there were [Sales order number] values in 'Refund' that do not exist in 'Sales', then selecting 'Reporting calendar'[Reporting date] and 'Sales ID'[Sales order number] would not correctly identify the list of sales transactions. Furthermore, because filters are single-direction, even if the report canvas has a filter on 'Refund calendar', this filter does not interfere with the presentation of sales transactions. This would not be the case if there were bidirectional filters, which would return unexpected results. Displaying refunds When displaying records for refunds, the user is interested in [Total refund amount], but it is also necessary to display the sales context of 'Sales ID'[Sales order number] and 'Sales product'[Product name]. If the user selects the [Total refund amount] column first, this would return the total measure value for the entire dataset and then adding the sales attribute dimensions would break this number down until the ID dimension is selected to return the unit-record transaction. If the user selects sales attributes first, Power BI displays the full list of sales orders and their products, regardless of whether they were refunded. When the user adds either

'Refund calendar'[Refund date] or the [Total refund amount] measure, the table filters down to refund transactions. This happens because these attributes are linked only to the 'Refund' table, not 'Sales'. Whether the user selects the sales attribute first, and then the unique refund attributes or in the reverse order, a dimensional model gives a seamless and intuitive experience for the user. Nevertheless, the situation is not so simple as it appears. Consider a case where a sales order of $100 is refunded in two partial refunds of $50 on the same day. Because there is no primary key for refunds, the refund for that sales order appears as a single transaction with [Total refund amount] = $100, rather than two rows of $50. For most scenarios, this may be sufficient, but in some cases, it is not. When it is necessary to see each transaction row as in the business process, the solution is to create a key that distinguishes each refund transaction. One option is to create a surrogate key [Refund SK], a unique integer for each refund, and expose this as 'Refund ID'[Refund SK]. However, this is not preferable for two reasons:

- [Refund SK] is high cardinality, increasing model size due to the 'Refund ID'

dimension and relationship columns.

- [Refund SK] has no natural business meaning and would require additional

learning curve. A better approach is to create a [Refund number], which is a sequence number for each refund action for a sales order, to form a composite primary key of [Sales order number] and [Refund number]. This effectively identifies each refund. The [Refund number] should be exposed 'Refund ID'[Refund number], which is a distinct list of integers with the maximum number equal to the highest number of refunds in a sale. This is a partial ID dimension because it has one part of the full key to identify a refund. This dimension is low cardinality, has minimal resource impact, and is natural for users. From the user’s perspective:

- Using [Total refund amount] gives the refund value for the transaction.

- Adding 'Refund ID'[Refund number] breaks this down into separate refund

transactions. This is perfectly natural for the user where every step returns a meaningful result. The use of the measure [Total refund amount], rather than the degenerate ‘Refund’[Refund amount], is essential for correct result. Suppose the user selects the raw value 'Refund'[Refund amount] instead. In the absence of a refund primary key, Power BI would display the previous case as one single row of $50 for the sales order—

an incorrect result. This is yet another example of why exposing degenerate numeric columns is problematic and why the fact tables are better hidden. Displaying both sales and refund The user may want to see details of the sales and refund business processes simultaneously. There are three possibilities:

- The processes displayed side by side

- The sales transaction with supplementary details about refund

- The refund transaction with the original sales amount

Displaying the refund and sales processes side by side on the same report page is straightforward. Suppose there is a table visual for sales with the columns:

- 'Sales ID'[Sales order number]

- 'Sales product'[Product name]

- 'Sales calendar'[Sales date]

- The measure [Total sales amount]

And a table visual for refund with the columns:

- 'Sales ID'[Sales order number]

- 'Sales product'[Product name]

- 'Refund calendar'[Refund date]

- The measure [Total refund amount]

These two tables work well because of the dimensional model design. If there is a slicer on 'Sales product'[Product name], and the user selects a particular product name, then both visuals filter down to that product. Similarly, if there is a slicer on 'Sales ID'[Sales order number], the user can look up a specific sales order number and retrieve details of both the sale and any refund. In addition, a user can click on a row in the sales table and cross-filter to any refund. This works because 'Sales ID' is a conformed dimension for both Sales and Refund facts. For the business user, this is exceedingly convenient navigating unit-records. This is why the ID dimension is one of the most powerful dimensions and an indicator of a good model. The same cannot be achieved if [Sales order number] were used as a degenerate dimension. If degenerate dimensions were used, the experience would be highly frustrating for the user because none of the filtering would work as expected.

The user experience is perfect when operating on the conformed dimensions 'Sales ID' and 'Sales product'. However, it becomes complicated with the two calendar dimensions: 'Sales calendar' and 'Refund calendar'. Users expect to slice by time. Neither calendar works perfectly:

- A slicer on 'Refund calendar' has no effect on the sales table because it does not

filter the Sales fact.

- A slicer on 'Sales calendar' correctly filters the sales table, but for the refund

table, it returns refunds for products sold on that date—not refunds that occurred on that date. In simple examples, users may interpret this correctly. In real-world scenarios with multiple dates, this nuance is often difficult to understand. In the worst case, it would silently mislead users. The solution is to create a role-playing 'Reporting calendar' that links [Reporting date] to both 'Sales'[Sales date] and 'Refund'[Refund date]. When used as a slicer, both tables return rows for that date. This works because the selection filters the Sales and Refund facts directly (first method of filtering), and then the visuals filter out combinations without matching fact rows (second method of filtering). This chain of filtering behind the scenes is responsible for creating a seamless experience for the user. If, instead of having two tables side-by-side, the user wants a single table of sales transactions with refund amount, it suffices to use the sales table columns above and add [Total refund amount] as an additional column. The table visual then has two measures [Total sales amount] and [Total refund amount]. The result is that:

- All sales transactions display as normal, with the [Total sales amount]

- Rows with refunds show a value in [Total refund amount]; others remain blank.

The outcome works because Power BI displays rows where any measure is non-blank (third method of filtering). In addition, if a refund exists without a sales amount, the row stands out with a blank [Total sales amount] and a non-blank [Total refund amount]. However, the user cannot add 'Refund calendar'[Refund date] to this visual. Technically, this dimension relates only to Refund, not Sales. The business interpretation for this is because one sale can have multiple refunds on different days, and therefore it is not logically correct to add the refund date when the intent is to display one row per sales. If displaying refund dates is necessary, the data engineer can create a measure [Sales refund dates] that returns the unique refund date if there is one, or concatenates distinct dates if there are multiple.

The scenario with displaying sales does not mirror to refunds. Adding [Total sales amount] to the refund table causes Power BI to return incorrect results by cross-joining sales and refunds. This happens because 'Refund calendar'[Refund date] relates only to Refund and does not filter the Sales fact. There is no valid relationship path for [Total sales amount] to work. Thus, users expect to drag [Total sales amount] into the refund table and see the original sales amount but instead get cross-join of rows. This is one of the situations where the default dimensional model is not intuitive out of the box and requires additional tuning. There are multiple solutions while staying within the parameters of dimensional modelling:

- Define [Total sales amount] to behave differently depending on context using

DAX functions like TREATAS.

- Denormalise 'Sales'[Sales amount] into the Refund table as [Sales amount

before refund]. This remains intuitive because a keyword search for "sales amount" shows both measures. Clear naming and display folders grouped by business process help disambiguate. Since the Refund fact may have multiple rows per sale, [Sales amount before refund] is not a simple sum. The DAX is more complex and is explained in the Designing measures chapter. The first option of adjusting [Total sales amount] gives the most seamless experience for the user at a complexity and performance penalty for the measure itself. It is not advisable to complicate such a core business measure to satisfy a narrow use case. The second option adds a more narrowly defined [Sales amount before refund] measure to the model. The measure is unlikely to be useful in other scenarios. However, it is more explicit, remains intuitive for the business, and maintains lower DAX complexity overall. Displaying unit records (three or more business processes) The techniques for displaying sales and refunds rely on conformed dimensions and the existence of fact rows to filter. In this, the ID dimension plays a special role. This does not scale neatly. With three or more facts it becomes hard to know which combinations of dimension values still have at least one row in any fact. Managing multiple ID dimensions is also complicated because some are conformed against some facts but not others. Many processes will not have a ready business key. A practical solution is to control the display with measures. The data engineer can create one display measure per business process that returns a value for that fact:

- [Display sales transaction]

- [Display refund transaction]

- [Display … transaction]

Each measure returns 1 when there is at least one row in its fact under the current filter context. These should be placed collectively in a display folder named "Display unit records". A refinement is to return a value only when 'Sales ID'[Sales order number] is filtered so that unit records appear only after an order is selected. This can be done by checking the calculation for 'Sales ID'[Sales order number] context using ISINSCOPE. > [!NOTE]
> TODO: Insert manuscript screenshot or diagram from the source draft. Adding one of these measures to a table visual filters dimension values to those that have a matching fact row (third method of filtering). The user can hide the helper column by renaming it and shrinking its width to zero. > [!NOTE]
> TODO: Insert manuscript screenshot or diagram from the source draft. An alternative is to use the measure as a visual level filter the fourth method of filtering (fourth method of filtering). This is convenient but has noticeable performance penalty on large facts. > [!NOTE]
> TODO: Insert manuscript screenshot or diagram from the source draft. While this has a learning curve for the user that involves a Power BI trick, it is a helpful clarification. A model that has more than four or five business processes are likely to be complicated to understand. An explicit selection of business processes through the "menu" of display unit-records measures can aid mental clarity. Cascading filters Cascading filters refer to the behaviour where selecting a value in one filter narrows the choices in another so that only valid options remain. For example, if a report page has a slicer for 'Sales product'[Product name] and another for 'Sales calendar'[Sales date], then choosing a product limits the dates to those where that product was sold, and choosing a date limits the products to those sold on that date. > [!NOTE]
> TODO: Insert manuscript screenshot or diagram from the source draft. The first method of filtering requires tables to have a chain of relationships that flow in from one to the other. In this case, no such path exists between the two dimensions. The second and third methods require two elements in a single visual—a dimension value and either another dimension or a measure—so they do not apply either. The solution is to use a visual level filter, which is the fourth method of filtering. In this case, the measure [Total sales amount] can be used as a visual level filter. A more explicit option is to create a measure such as [Has sales] which returns 1 if the count of

rows in the 'Sales' fact table is greater than zero. Therefore, the solution is to rely on a common fact table and a measure that can pass information back to the dimension against the default filter direction. > [!NOTE]
> TODO: Insert manuscript screenshot or diagram from the source draft. Aggregating dimension values Cascading filters aim to filter one dimension by another. Sometimes the goal is to aggregate a dimension by another dimension. Following the example of sales and refunds, suppose the user wants to display a concatenated list of distinct products refunded on each day. If [Product name] were already included in the 'Refund' fact table as a raw value, the measure would take the distinct values in 'Refund'[Product name], and apply CONCATENATEX on those values. > [!NOTE]
> TODO: Insert manuscript screenshot or diagram from the source draft. However, this approach is often not possible. For example, if 'Sales product'[Product name] is linked to 'Refund' via [Product ID] rather than the product name, or if the user wants to aggregate another column from 'Sales product' such as [Product type]. It is not practical to include all such columns in the fact table. An inexperienced data engineer might denormalise the required column into the fact table or even precompute string concatenation in the data layer so that the column can be used as a degenerate dimension. Sometimes it is pragmatic to include a frequently aggregated column in the fact table. In general, this is not desirable because it is heavy work to modify a large fact table for every column the user might want to aggregate. Preaggregation is also not ideal because it cannot respond to user filter context. Instead, the solution is to notice that the information is already in the model, and it is just a matter of retrieving it. The fifth method of filtering—on-demand filtering in a measure—provides the answer. The DAX is to concatenate 'Sales product'[Product name] and wrap it in a CALCULATE context where CROSSFILTER is set to both directions. This temporarily changes the single direction relationship to bidirectional and allows 'Refund calendar' to filter 'Sales product'. [TEST , SCREENSHOT] Filter by having follows: Consider the case of an organisation’s HR system. The dimensional model is set up as

- A dimension 'Employee' that stores details such as name, email, and date of

birth. This table is type II to reflect changes in employee attributes. The key columns are [Employee ID] and [Start datetime]. An [End datetime] signals the

end of the validity period of a row. [Employee SK] is used as a surrogate key for Power BI relationships.

- A dimension 'Organisation unit' that stores the hierarchy of teams in columns

[Department name], [Group name], [Branch name], and [Section name]. This table is also type II because names and hierarchy can change. The key columns are [Team unit ID] and [Start datetime]. An [End datetime] signals the end of the validity period of a row. [Team unit SK] is used as a surrogate key for Power BI relationships.

- An end-of-month fact table 'Employee end of month' that stores the employee’s

attributes and organisation unit at the end of each month. > [!NOTE]
> TODO: Insert manuscript screenshot or diagram from the source draft. The user wants to search an employee’s and organisation unit history by personal attributes such as name or role. Since 'Employee' is type II, a direct search returns only the end-of-period states that match the point-in-time attribute values. This is not the desired outcome. The user wants the full history of the employee using any historical attribute. This is an example of filtering dimensions by whether they have an attribute, rather than filtering on the attribute value itself. We call this filter by having. It applies to any scenario where a user would like to look up a header on a detail attribute and return all other details for that header. New data engineers often try to solve this by restructuring the fact table. This leads to complex code and artefacts that confuse other contexts. A simpler solution is to add a search dimension to the model, 'Employee search'. This can be a duplicate of 'Employee' and relates to 'Employee' on [Employee ID] in a snowflake configuration. The relationship is many-to-many and single direction. > [!NOTE]
> TODO: Insert manuscript screenshot or diagram from the source draft. Using 'Employee search', the user can look up any attribute of the employee at any point in time, retrieve the [Employee ID], and return all rows in 'Employee' that match this ID. Under this view, 'Employee search' and 'Employee' work together as one logical "dimension" that acts as an interface for searching the model. This pattern generalises. The data engineer can add 'Compliance search' or any other derived attribute of [Employee ID] as additional search dimensions as more branches of the snowflake. From the user’s perspective, these are simply "search" tables that allow searching employees by their history. Unlike tampering with fact tables, this solution is nondestructive. It adds a few tables as an interface without modifying the rest of the model.

Dynamic type I Type II dimensions show an entity at its point-in-time attribute. Type I shows the latest attribute value. Dynamic type I shows the latest attribute value as at a user-selected time. This is the natural expectation in entity tracking. Consider employees and their organisation unit. The fact 'Employee end of month' returns employee attributes and organisation unit at the end of each month. Suppose the user wants employee metrics for a group over a period, such as the total number of commencements and separations in the last 12 months. This is not the count as at the month end. It is all commencements and separations that happened in the 12 months prior. The 'Organisation unit' dimension is type II, so the fact reflects the hierarchy as at each period. When units reshuffle often, teams that moved between groups do not bring their counts with them. A measure of commencements broken by [Group name] gives the wrong result. It only shows the hierarchy as at now and ignores teams that were in the group during the last 12 months. If the requirement were fixed to the latest view only, a type I version of 'Organisation unit' would suffice. However, the goal is to report against the hierarchy as it stood at the end of every 12 months period. This requires using the view of the organisation unit to change dynamically as selected by the user, and hence dynamic type I is needed. The problem is notoriously complex to solve through amending the fact table. It requires associating all the organisation unit’s history to each fact row. Rewriting facts to carry the full hierarchy history is complex and fragile. The model already has the history in 'Organisation unit'. The solution is to surface it at query time. Two steps implement this approach

1. Broaden the relationship for evaluation

Relate each fact row not to a single point-in-time row in 'Organisation unit', but to all rows for that [Team unit ID]. Use a many-to-many, single-direction relationship on [Team unit ID]. Each fact row now has the full history of its team available during calculation.

2. Select the valid row at query time

In the measure, take the latest date in the current context and filter 'Organisation unit' to the row whose validity covers that date: [Start datetime] ≤ selected_date < [End datetime]. For a given [Team unit ID] this is unique because the primary key is [Team unit ID] and [Start datetime]. Under this filter the table behaves like a one-to-many join for that evaluation and the measure returns values only for

the valid row. Other rows go blank and drop out by the third method of filtering on non-blank measure values. This alters how 'Organisation unit' behaves. There are two options that preserves the behaviour of the dimension. Option A. Add a new dimension

- Duplicate 'Organisation unit' as 'End of period organisation unit'.

- Add [Team unit ID] to 'Employee end of month'. The fact now carries [Team unit

SK] for the normal join to 'Organisation unit', and [Team unit ID] for the many-tomany join to 'End of period organisation unit'. > [!NOTE]
> TODO: Insert manuscript screenshot or diagram from the source draft.

- Wrap measures when dynamic type I is needed. For example, rename

[Employee commencements] to [_Employee commencements]. Define [Employee commencements] that evaluates [_Employee commencements] inside CALCULATE, filtering 'End of period organisation unit' to the valid row as at the latest date in context. > [!NOTE]
> TODO: Insert manuscript screenshot or diagram from the source draft. In this option, the user chooses perspective by choosing the dimension.'Organisation unit' gives type II. 'End of period organisation unit' gives dynamic type I. Option B. Keep one dimension and switch in measures

- Keep the normal one to many single direction relationship on [Team unit SK].

- Add a many to many single direction relationship on [Team unit ID]. It remains

dormant.

- In measures that need dynamic type I, deactivate the SK path and let the [Team

unit ID] path apply for the calculation. Then filter to the valid row as above. > [!NOTE]
> TODO: Insert manuscript screenshot or diagram from the source draft.

In this implementation the dimension works as type II by default, and the user can choose the dynamic type I perspective on certain measures. Under both options the original dimension 'Organisation unit' keeps its normal behaviour. All existing measures work as before. Both options are non-destructive. The distinction between them is whether the user chooses type II or dynamic type I through using different dimensions, or through using different measures.

## Buttons and effects

These scenarios are not intended to be an exhaustive list of filtering techniques or scenarios – this would be a book itself. Instead, their purpose is to illustrate a philosophy of seeing Power BI as an interface that users click to achieve an effect. In this philosophy every table has one of two roles:

- Tables that define the interface as buttons to click, usually the dimension tables

- Tables that define the content which drives the effect, usually the fact tables

A good model keeps these roles separate. Every table serves a single purpose and not a mix. This is why an indicator of quality is that all fact tables are hidden. The first three examples show how dimensions present information from facts using the more difficult case of displaying transaction records. They illustrate that the fact tables, which are the natural focus for new data engineers, are not the artefacts to expose to the users. In fact, trying to expose the fact tables and degenerate dimensions will only cause issues. Instead, the dimensions act as the entry point to the data. The same philosophy explains why degenerate dimensions and bidirectional relationships frustrate users. They blur the line between tables that act as buttons and tables that create the effect. The examples of cascading filters and aggregating dimension values show that the data engineer can handle occasions where a dimension is on the receiving end of the button and effect relationship without compromising the model with degenerate dimensions or creating bidirectional relationships. The final two examples generalise the idea of a dimension to a set of tables. For this purpose, a dimension is not simply a lookup table. If the user sees it as intuitive, and get the desired outcome unambiguously and rapidly, that is what matters. In this view, a dimension’s chief purpose is to be the user’s interface to the model. The final two examples also demonstrate Power BI’s flexibility of using many-to-many relationships that would otherwise require substantial modification to the model. This is the philosophy of separation of concerns from software design. It maintains a clear distinction between the interface layer and the content layer. Power BI supports this through the five filtering mechanisms described at the start of the chapter. This

perspective pushes the data engineer to see a data model as software and to design a clean interface that is business-centric and intuitive for the user.
