---
title: Optimising Power BI load
weight: 7
draft: true
---

Loading a Power BI model is often one of the longest steps. This is particularly true for models with large fact tables. New technologies such as DirectLake promise to remove this step entirely, yet Import mode remains the most reliable way to deliver a fast and responsive experience. Consequently, it is important to establish efficiency for Power BI loads. Loading of Power BI should focus on assembling prepared fragments. It is not the stage to curate information. The restaurant analogy from Meaningful fragments makes the point. Mise en place is the long process before service time to customers. During mise en place, ingredients are washed, cut and portioned in advance. At service the kitchen completes the final assembly and plates dishes quickly, rather than peeling potatoes when the orders are made. Likewise, a Power BI load should be focusing on assembling finished fragments rather than transforming data. There are three main ways to optimise Power BI loads:

- Using DirectQuery to avoid loading

- Efficient underlying source tables

- Partitioning for parallel refresh, with two further enhancements of rolling

windows and incremental refresh This chapter assumes the model sources data from SQL, where purpose-built views or tables act as source tables that map one-to-one with the Power BI model tables.

## Using DirectQuery to avoid loading

DirectQuery for fact tables avoids the load entirely by sending DAX queries to the source at report time. To provide a responsive experience, the underlying source table often needs to be materialised as a columnstore table dedicated to this purpose. While materialising a large fact table is costly, it can also be incrementally loaded so that refresh remains minimal. By using DirectQuery over am incrementally loaded columnstore table, this achieves the highest possible efficiency in terms of information movement. However, there are serious drawbacks for user experience:

- DAX queries become noticeably slower.

- Some complex DAX expressions are not supported at all.

- Certain DAX functions behave differently in Import mode versus DirectQuery,

such as in how blanks are treated.

- Power BI limits how many rows can be retrieved in DirectQuery for certain

operations, which restricts what reports can be built.

- Dimension values can appear blank in filter lists even when the table does not

actually contain blanks. DirectQuery works best when:

- The table is far longer than it is wide, so queries touch fewer attributes.

- Queries against the table are simple - limited to sums, counts, minimums, and

maximums that work well against columnstore tables through their equivalent SQL query.

- Users are not expected to browse unit records and do not hit Power BI’s retrieval

limits. Where dimensions are shared by both Import and DirectQuery facts, dual mode must be implemented. Dual mode keeps a copy of the dimension for Import while still allowing the engine to query it in DirectQuery when needed. This ensures relationships remain fast for Import facts and correct for DirectQuery facts.

## Efficient underlying source tables

One of the biggest factors influencing Power BI load times is the efficiency of the underlying source tables, which are often implemented as views. A source view should be a straightforward join of ready-to-use tables that have been indexed appropriately to support high-performance execution. The views may have simple logic such as:

- Looking up surrogate keys to replace composite primary keys

- Backfilling null values with defaults

- Adding on-demand columns, for example [Days expired since creation] using

functions like GETDATE() However, heavy transformations such as windowing or nested logic should be avoided. These belong upstream in curated layers where they can be tested and reused. String aggregation for display should also be avoided, as this can be handled with appropriate DAX measures, as explained in Designing Measures. If a source table still requires elaborate logic to stitch pieces together, the issue is not SQL tuning. The solution is to reconsider whether upstream fragments have been adequately prepared. The ideal case is to create fragments that are both meaningful and effective for loading into the Power BI model. Materialisation is sometimes necessary to ensure the source table loads rapidly. This is especially true when data needs to be rearranged to support fast retrieval of load partitions against the partition key - a subject we turn to now.

## Partitions

Defining a table into partitions is the most effective way to reduce Power BI load times when fact tables grow large. Partitions are akin to having a large box of books from multiple publishing years. Batches of books arrive at regular intervals, and the box needs to be updated with the incoming batch. There can be new books, and old books can be updated. Updating the whole box can take a long time if the number of books is huge. Splitting them into boxes by publishing year allows a divide-and-conquer approach and vastly reduces total update time. The ability to load partitions in parallel is the first benefit of partitioning. If boxes of books that are too old become unnecessary, they do not need updating and the oldest set can be dropped. Over time, this reduces the number of boxes to update. This ability to apply a rolling window is the second possible benefit of partitions. Finally, if the incoming books can be sorted by year, and in each batch only a fraction of the years have new books, then only those boxes need updating. It may take additional effort to track changes from the incoming books, but this effort can dramatically reduce total update time. This ability to incrementally refresh is the third benefit of partitions. Thus, partitioning a table offers increasing levels of enhancement that can be adopted as the situation requires:

1. 2. 3. Load partitions in parallel, immediately reducing time to load

Apply rolling window to drop off older partitions that are not necessary Incrementally refresh only the partitions that changed Parallel partitions A partition key is a business date or datetime column that divides the data into intervals such as daily, monthly, or yearly. Power BI can load these partitions in parallel. Depending on the degree of parallelism, this can lead to massive improvements in load time with little effort. To make partitions effective, the source must return a single partition quickly. If the underlying view is complex, the solution is not to push SQL harder but to move complexity upstream and materialise the result with an index on the partition key. This ensures that Power BI can request "give me this month" and receive the data immediately. Continuing the analogy, the incoming batches of books must be readily accessible by publishing year. If not, it may take longer to fetch each year’s books than the time gained from divide-and-conquer. The optimal solution is to organise the incoming batches by publishing year. In SQL terms, this means storing the source data sorted by the partition key used to define the Power BI partition. There is a trade-off between load time and query time. Splitting one big box of books into multiple boxes by publishing year increases the total space used for storage

because each box has a minimum size that can lead to wasted space. It can also take longer to fetch books because there are now more boxes to work through. The choice of interval size between publishing year, first of month, or publish date depends on the actual volume of books in the processing. When partitioning, new developers often confuse which date to use. The partition key must be a business date rather than a change-tracking column like [Row update datetime]. Using the same column for partitioning and change detection will push rows toward the end of the range and break the logic. Following the analogy, the date should be the publishing year rather than the year the book arrived in a batch. The latter will always be in the last batch and does not correctly update older books. Rolling windows When partitions are in place, rolling windows provide the next level of efficiency. Power BI allows a data engineer to define the number of partitions to keep, and older partitions are dropped from the model. This keeps the model size under control and prevents refresh times from growing indefinitely. Boundary points in the window are error-prone. Two details deserve attention. First, if the SQL source table itself rolls history, its window must be kept in sync with the Power BI table’s rolling window to avoid mismatches. Second, the boundaries of fact tables must match related dimensions and other facts. This is particularly true of ID dimensions. If dimensions are not kept in sync, they will contain primary key values that no longer exist in the fact tables. Incremental refresh Incremental refresh adds change detection on top of partitions so only partitions with changes are refreshed. The native Power BI interface allows the user to choose a datetime column in the table for change detection. During refresh, Power BI evaluates the maximum value per partition. This is the polling query. The maximum value is stored against each partition as its refresh bookmark. If the next polling query returns a different value than the bookmark, that partition is refreshed. There is a substantial benefit to load time if only a fraction of the polling queries differs from the bookmarks, and thus only that fraction of partitions are refreshed. > [!NOTE]
> TODO: Insert manuscript screenshot or diagram from the source draft. Following the analogy, each box of books by publishing year may have a label showing the last time it was updated. This is the bookmark. When batches of books arrive, they can be scanned for each publishing year to see if the update date on any book is greater than the label on the box. This is the polling query. This is only effective if incoming batches are organised so that it is easy to find the maximum update datetime for each publishing year.

The native approach offered by Power BI can be limited if the source table is a view that joins multiple tables, and thus there is no single column representing change detection. It is also not applicable if partitions have deletes because the change detection column cannot reflect delete datetimes. When the native approach is not sufficient, the user can specify a custom polling query with arbitrary M code. Polling tables can facilitate rapid evaluation of a polling query for complex cases. A polling table is simply a list of partition dates and the datetime the partition was last updated. During refresh, the polling query looks up this update datetime for a partition date. Following the analogy, the incoming batches of books may have a companion spreadsheet that tracks publishing years and the last update datetime of books for that year. During updates, this spreadsheet is consulted to decide whether that year’s box needs updating. Power BI does not support custom polling queries in its interface. XMLA-based configuration is required. If Power BI can rapidly evaluate whether a partition needs refreshing and retrieve the data for that partition quickly from the source table, this can lead to substantial improvements in load times. Supporting these requires the data engineer to prepare the data to facilitate these queries through indexing, sorting, or even constructing dedicated polling tables. This preparation itself takes time, and any base tables or polling tables should themselves be incrementally refreshed. Consequently, optimising Power BI loads means trading Power BI load times with data source load times. If not done well, implementing these artefacts can lead to even longer time than saved through defining incremental partition refreshes.

## Conclusion

Loading a Power BI model is time intensive. Using DirectQuery over a columnstore table avoids the load entirely, but DirectQuery imposes serious limits on the queries that can be made. Consequently, the most common factor for a fast Power BI load is the efficiency of the underlying source tables. These should be simple assemblies of welldefined fragments that join easily and avoid complex transformations. When fact tables become substantial, partitions can deliver a major speed boost by enabling parallel loads. This often requires rearranging data or implementing dedicated indexes to support retrieval by partition date. When partitions are in place, rolling windows provide further benefit by dropping older partitions and keeping load times consistent. This introduces room for error and requires attention to detail at boundary points.
