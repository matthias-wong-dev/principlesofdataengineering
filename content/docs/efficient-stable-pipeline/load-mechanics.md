---
title: Load mechanics
weight: 2
draft: true
---

During a load, a table’s data needs to update with the most recent set. The simplest approach is to drop the original table and replace the data with a new set. This is how every data engineer starts. But it violates the key tenets of pipeline efficiency and stability. When a table’s content is replaced en masse, it is not possible to know which rows changed. Downstream processes cannot respond with precision because every row looks new and needs response. This breaks the goal of efficiency to ensure database changes are minimal. More importantly, when a table is dropped and replaced, any error that prevents a successful load becomes catastrophic. Reports may become empty for the user. It can also result in a domino effect of errors in downstream tables. In a production pipeline that transforms hundreds or thousands of tables, the cumulative probability and effect of these problems become untenably disruptive. Instead of drop and replace, updating the data of a table should occur through three steps:

1. 2. 3. Stage the incoming copy of the data into a temporary location

Check the incoming data against current data to pick up changes, anomalies and constraint violations Apply genuine changes to the target table, updating any timestamp columns. These are the same steps whether the incoming data is a full extract or a subset of increments.

## Loading

Suppose the current table is X. The goal is to update X with the latest batch of data. X has a primary key column [PK col1], [PK col2]. Step 1 – Stage The first step is to load the latest batch of data into a temporary table. In traditional warehousing terminology, this is the staging table. Suppose it is called X_staging. X_staging may be the full load of data to replace X. It may be less than the full set but still cover all the changed records in a recent batch. This is an incremental extract. An incremental extract reduces the number of records to stage, check, and apply from hundreds of millions to a couple of thousand. The ways to do this reliably are covered in [Tracking changes](/docs/efficient-stable-pipeline/tracking-changes/) and [Responding to change](/docs/efficient-stable-pipeline/responding-to-change/).

Step 2 – Check The next step is to check the content of X_staging against X for changes and validity before loading onto X. This is the most intensive step and is the one usually skipped in naive approaches to loading. The aspects to check are:

- Changes:

- Which rows to insert?

- Which rows to update?

- Which rows to delete?

- Instability:

- Violations:

- Are there a concerningly high number of rows to insert or update?

- Are there a concerningly high number of rows to delete?

- Are there rows of uniqueness violations to reject?

- Are there rows of existence (not null) violations to reject?

Checking for changes is essential. Checking for instability is highly desirable. Checking for each of the violations is not critical, but proactively rejecting a small number of bad rows and allowing correct rows to pass through can reduce disruption to users by allowing them to get access to most of their data. Checking for changes Not every row in X_staging is a genuine change in X. In fact, during a full load, only a few hundred out of millions may differ in the latest batch. The first step is to detect which rows are the ones that changed. This check is necessary even if X_staging is incrementally extracted with the intention of capturing only changed data. Despite the best effort of the data engineer, it is often difficult to extract only the changed rows, especially when there are multiple joins and transformations. While incremental extract may narrow the number of candidate rows from millions to thousands, some of them may still be identical to the rows in X, requiring a check to find those that are truly changed. In checking for changes, there are three possibilities:

- For a row in X_staging, is the primary key value new? If so, it is an insert.

- For a row in X_staging that has an existing primary key value in X, are any of the

column values different? If so, it is an update.

- For a row in X, should the primary key value still be retained? If not, the row

should be deleted. The first two are collectively known as an upsert. A computationally effective way of calculating inserts and updates simultaneously in SQL is to:

1. Start from X_staging and left join X on the primary key columns [PK col1], [PK

col2].

2. Keep only the rows from X_staging that do not identically exist in X. This can be

done using an EXCEPT comparison in the WHERE clause.

3. Add a computed column [Is new row] depending on whether the X primary key

column value is null. Storing the result of this query into X_upsert gives only the rows that changed, with a column [Is new row] to indicate whether it is an insert or update. `[Example SQL from manuscript image pending transcription.]` Checking for deletes depends on whether X_staging is fully extracted or incrementally extracted. If X_staging is fully extracted, then it represents all the records that should be in the final table. Rows from X that should be deleted are those whose primary key values are not in X_staging. An implementation in SQL would be a left anti-join of X on X_staging. The primary keys to delete should be stored in a table X_delete. `[Example SQL from manuscript image pending transcription.]` If X_staging is incrementally extracted, the idea would not work because it only has a fraction of the primary keys in the desired final output. Rather, X_delete needs to be tailored to the incremental extract logic for X. This is explored in greater depth in Responding to change. Checking for instability With the tables X_upsert and X_delete, it is easy to check whether there are an abnormally high number of rows to be upserted or deleted in a batch. If there are an abnormally high number of rows, then the load should abort. The thresholds for abnormality can be a combination of the number of rows in the base table and the percentage of rows. These are stability thresholds. For example, if the table X has a hundred thousand rows, and more than 10% are upserted, then this can be a sign of abnormality for aborting the load. The threshold for deletes should be different from the threshold for upserts. There are usually far fewer deletes than upserts. For example, less than 5% of a large table should be deleted on a given day. In practice, a simple stability threshold can apply as a default across the entire pipeline to catch most abnormalities, such as having half the rows disappear. Specific tables may have their stability thresholds tailored to their case. Examining a table’s history of

changes can be useful in determining the threshold. This can be done if these statistics are logged. This logging is discussed in a subsequent subsection. The SQL for aborting on the upsert threshold can be done by checking the number of rows in X_upsert versus that of X: `[Example SQL from manuscript image pending transcription.]` Checking the delete threshold is only possible on a full extract. The SQL is as follows: `[Example SQL from manuscript image pending transcription.]` These checks are an important part of monitoring and improving a pipeline’s stability. It is very unlikely that every record of a business process’s entire history, or even more than 5% of them, changes their content. If the upsert rows in X_staging do exceed this number, it is more likely to be an unintended side-effect of a system change rather than a change in informational content. Stability thresholds prevent these unintended changes from propagating. If the load is frequently aborted for a table, then the extraction logic needs to be improved for stability, or the thresholds need to be adjusted. Checking for violations When there are too many rows to upsert or delete, the entire table aborts its load. This means the user does not get any of the latest data. This can be too drastic when only one row out of thousands is problematic. Instead, if the table has uniqueness constraints and existence constraints (not null property on a column), only the rows which violate these constraints need to be discarded, and the rest can proceed. These are the reject rows and can be stored in X_reject. The algorithm for rejecting existence violations is simply to discard rows in X_staging which have a null value on a column with a not null property, and send them to X_reject. Suppose X has a column [Col not null] with a not null property, the SQL is as follows: `[Example SQL from manuscript image pending transcription.]` The algorithm for detecting uniqueness violations has two scenarios. Suppose X_staging has a column [Col unique]. The possibilities are:

1. The duplicates exist in X_staging when two rows have the same value on [Col

unique].

2. The duplicate happens when X_staging applies an upsert that creates a value in

[Col unique] that already exists in X, but not if that same row swaps its value to another one to avoid a duplicate.

In these cases, all but one of the rows should be sent to X_reject. Example SQL follows. `[Example SQL from manuscript image pending transcription.]` The two criteria can also be extended to other criteria such as data type violations. In theory, any tailored criteria can be applied to abort a load or reject some rows on a particular table. These two cover many of the problems that a large pipeline encounters. They can be applied by default to every load through automation rather than manual tailoring. Step 3 - Apply Once the changes are determined in X_upsert and X_delete, and invalid rows are sent to X_reject, the changes can be applied to X. The first step is to delete the rows in X using the keys in X_delete. Rather than completely losing the rows, it is important to send the deletes to a history table so that downstream processes know which rows have been deleted. In some platforms, this can be done automatically. In this example, the table to hold the old records is X_history. The SQL is as follows: `[Example SQL from manuscript image pending transcription.]` Then the upserts should be applied. The rows to be inserted from X_upsert into X are identified by loading X_upsert where [Is new row] = 1. The rows in X to be updated using values from X_upsert are identified by [Is new row] = 0. As with deletes, the old values in X that are to be updated should be sent to X_history rather than being overridden and lost. Keeping these rows is important for incremental processing downstream. This step of applying changes should also add architectural columns for change datetimes. They are:

- [Row insert datetime] — when was the row, defined by the primary key value,

first inserted into the table.

- [Row update datetime] — when was the row, defined by the primary key value,

most recently updated with a new value. Because of the Check step, these are always genuine changes.

- [Row delete datetime] — when was the row, now in X_history, deleted from X.

This could be because of a full delete by its primary key or because it was overridden by an update. Some platforms calculate one or more of these automatically. `[Example SQL from manuscript image pending transcription.]`

By the end of this step, and if there were no other errors, the changes would be applied to X. The additional artefacts – X_history, [Row insert datetime], [Row update datetime], and [Row delete datetime] – provide information for downstream tables that rely on X to incrementally extract from it.

## After loading

Cleaning-up and logging are important part of the load mechanics. Cleaning-up If there are no errors, the tables X_staging, X_upsert, and X_delete do not need to be retained. The rows in X_history can also be purged after a while, once they have informed incremental processing downstream. In Delta table context, the history rows are the tombstoned rows, and their purge is known as vacuuming. If there are errors, then the intermediary tables and X_reject need to be retained for troubleshooting. It is important to ensure they are secured in the same way as X, and do not accidentally cause unintended data leakage. Logging In addition, it is essential to log the table’s bookmark, and highly valuable to log the change statistics. The table’s refresh bookmark is the datetime of the start of the load, if the load successfully completed. Suppose the table X draws data from A, B, and C. The refresh bookmark of a load defines when X started reading from its source data, and any records that appear in A, B, and C after that datetime have come afterwards. When X is incrementally extracted in the next batch, the updated records in the source tables are easily identified. This is explained in greater depth in [Tracking changes](/docs/efficient-stable-pipeline/tracking-changes/). > [!NOTE]
> TODO: Insert manuscript screenshot or diagram from the source draft. The Check step calculates the number of rows to be inserted, updated, and deleted. It is only a small additional effort to log these numbers. While not essential, they form a rich history to understand a table’s evolution and can be valuable for troubleshooting. Since they are already calculated as part of the load, it is easily worthwhile to log them. > [!NOTE]
> TODO: Insert manuscript screenshot or diagram from the source draft. The success, or failure and associated failure messages, should be logged. > [!NOTE]
> TODO: Insert manuscript screenshot or diagram from the source draft.

## Analysis

The full three steps create five extra tables in addition to X — X_staging, X_upsert, X_delete, X_reject, and X_history. It also creates three extra columns — [Row insert

datetime], [Row update datetime], and [Row delete datetime]. The logic is also much more complex than simply dropping and replacing the table X. In a simple environment with five or even fifty tables, all the additional work may be unjustified overhead. In a moderately sized pipeline, the benefits offered by the extra work outweigh the cost. Past a certain point where errors and resource become costly, they are non-negotiable. From the view of efficiency, the row-by-row check for genuine change seems exorbitant. But in a table with millions of rows and only a small fraction changing in a load, it is much faster to check for changes and apply them than to load all rows and perform any re-indexing. More importantly, checking each row and updating [Row update datetime] only for rows with a genuine change informs downstream tables how to respond. Without such a check, all downstream tables will need to reload all rows in every batch. Seen in a different way, the data warehouse has responsibility to keep track of every single change that happens within it. The row check is the foundation for this tracking. From the view of stability, the row-by-row check plays an important role in stabilising a pipeline of incremental extract by eliminating noisy changes. Incremental extract typically works by selecting candidate change rows through a change detection column. If an external factor causes the change detection column to shift all its value but none of the other column values changed in the row, this process of row-by-row checking eliminates these nil changes and informs downstream tables not to incorrectly react. To rephrase, a pipeline of incremental extract relies on change detection columns, but when one such column goes wrong, the effect can be disastrous. Instead of relying solely on the change detection column, it should be used as a first pass, while allowing the Check step to do a second pass to eliminate any noise if things go wrong. Finally, the Check step improves stability and fault tolerance by limiting the impact of abnormalities or errors. To take advantage of the fault tolerance, tables must not have unstable columns that change frequently for no informational reason, or may suddenly change on many rows, such as on a switch to new year. Examples of these are discussed in the Fault tolerance chapter. On a specific table, the additional work may seem excessive. But doing the work consistently as a pattern is the backbone of a sophisticated pipeline by monitoring and controlling row changes. Investment in automation or appropriate technology ensures that the additional logic is applied by default, with no development cost to the engineer.
