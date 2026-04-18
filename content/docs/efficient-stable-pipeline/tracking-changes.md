---
title: Tracking changes
description: Covers the main techniques for detecting inserts, updates, and deletes so pipelines can respond precisely to real change.
lede: Incremental work begins with knowing what has genuinely changed.
weight: 5
draft: true
---

The aim of information efficiency is to process only what has changed. If there were no records changed after a table is processed, then ideal is have spent zero processing time it. In practice, even when there are no changes in input, a load still takes time to process. Every unnecessary scan consumes resources without adding value. Efficiency is achieved when downstream tables can reliably extract only the records that have changed and ignore the rest. Doing this well requires systematic change tracking. Without it, pipelines fall back bespoke methods for tracking changes. This leads to errors in incremental processing, periodic full reloads, and fragile recovery from disruptions. A robust pattern avoids these pitfalls. The following is a simple approach illustrate the concept of change tracking, before unpacking the details of a more robust approach.

## Simple approach

The most basic approach is to include an update datetime column from the source system and filter on it. This works when the source table deletes do not occur, and the target table mirrors the source one to one. Example scenario

- Source table Raw.Event with columns [PK1], [PK2], [Col1]…[Col15], [Update

datetime]

- Target table Curated.Event with [PK1], [PK2], [Col1], [Col2], [Update datetime]

Incremental extract logic would be as follows: While straightforward and intuitive, this approach suffers from a few problems.

First, it is not scalable to complexity. Additional source tables will break the logic because it is not practical to add the update datetime from each source onto the target table. It is possible to create a complex compound datetime, but it would be error prone. Second, it is not stable. If a system update shifts all values in [Update datetime], the pipeline will reprocess every row, causing a blow out in processing time for updates, and triggering similar issues downstream. Third, the approach is not scalable to continuous load. For example, if Curated.Event filters Raw.Event for rare events, then the maximum update datetime on Curated.Event will not represent latest processing time of Raw.Event. The simple approach will force a re-scan that goes too far back. For a continuous load scenario, this will be prohibitive. A more scalable and reusable pattern is to separate the time-tracking artefacts from the data content itself.

## Refresh bookmarks and polling tables

As explained in Load mechanics, as each table is processed, the pipeline logs the refresh bookmark of a load. That is, the starting datetime of the load of each table is logged if the load succeeded. The refresh bookmark for all tables in the pipeline can be stored in one table. Each row of this table is one table that was loaded, together with the starting datetime of that load.

This bookmark defines the cut off for what records in a source has fully made it to the processing of a target table. Any records that have come to the source table after this bookmark datetime would need to be considered in the next batch of processing. If the table load aborted because of a fault, then the bookmark should not be logged so that the next batch can resume from last success point. An advanced note. If the source is continuously loading, then some stray records may still come into the source table after the bookmark datetime, but before the processing has complete. However, there are no guarantees. Consequently, either the incoming source needs to be frozen, or the next batch should still resume from bookmark and reprocess these late records. The query to retrieve the latest bookmark for a table is simple: On the other hand, keeping track of source changes depends on whether the source table was created by the pipeline or whether it was raw data table from external source. In the former case, the tables created by the pipeline have reliable update datetimes created by the process in Load mechanics – [Row insert datetime], [Row update datetime] and [Row delete datetime]. Since these are created by the pipeline itself, they are comparable with the refresh bookmark and can be compared directly for understanding what records have come in after the latest bookmark. However, for tables that were not created by the pipeline, even though they may have a column called [Update datetime], there may be a substantial lag between that value versus when the row made it to the database. Hence, they cannot be used directly. To distinguish these two cases, we would say that the update datetimes in pipelines are in-sync while the update datetimes from source systems that are loaded in a separate process are out-of-sync with the data pipeline. If the datetimes are out-of-sync with the refresh bookmark, they cannot be directly compared. Instead, just as the target table’s state of processing can be tracked by a separate table, the source table’s state of processing can be tracked by a separate polling table.

A polling table is any table that can be consulted to know whether and what portion of data needs to be refreshed. For a polling table to be effective, it needs to be structured so that it can be queried rapidly – much more rapidly than the time to process the full data. Ideally, this query should be close to zero time to support continuous load. Following the example, direct comparison of Raw.Event[Update datetime] with the latest bookmark in Curated.Event is not possible. There can be an unknown lag between the update timestamp and its arrival in the database. The only safe assumption is that the datetime increases monotonically. A polling table provides a way to map the pipeline’s refresh time to the latest update datetime observed in Raw.Event. Suppose this table is called Raw.Bookmark, and is loaded using an append-only process. Each appended row records the maximum update datetime from Raw.Event at the time of the refresh. The columns of Raw.Bookmark are:

- [Refresh datetime] — the datetime of the check as the row is appended. This

datetime, since it is computed by the load, is part of the pipeline and thus insync with the refresh bookmarks.

- [Bookmark datetime] — the maximum of Raw.Event[Update datetime] as at that

time of refresh. This datetime, coming from the source and later loaded, is outof-sync. This table maps the [Update datetime] column, which is out-of-sync with the pipeline, to a column, [Refresh datetime], that is in-sync with the pipeline. This mapping makes it possible to compare changes to the incoming data tracked by the source’s [Update datetime] with processing events, which are tracked against the pipeline’s record of datetimes. In theory, refreshing this table infinitely often would allow the pipeline to translate its own time into the update datetime of Raw.Event at any point. In practice, the refresh frequency aligns with the pipeline cadence. There is no benefit in refreshing the table when Raw.Event has not changed. In addition, Raw.Bookmark can contain the bookmarks for multiple tables, such as Raw.Event, Raw.Event2, Raw.Event3 rather than creating one table for each. At the start of processing Curated.Event, the polling table Raw.Bookmark allows the pipeline to fetch the maximum bookmark of Raw.Event as of Curated.Event’s previous

batch start. Any row on Raw.Event whose [Update datetime] represents data that have come after the previous batch start and eligible for processing. In summary, tracking records that have changed in a source table since the last process depends on two components:

- Tracking the target. A bookmark table for the pipeline that records the

processing datetimes of each table whenever a load completes successfully.

- Tracking the source. If the source table has an [Update datetime] column that

is synchronised with the pipeline, this column can be used directly to retrieve updated rows. If not, a polling table is required to map the source table’s update datetime back to the pipeline’s datetime for comparison. With these components, it becomes possible to identify changes in the source relative to the target’s last processed state.

## Change detection columns

The previous example assumes that the source table Raw.Event has a reliable [Update datetime] column for change detection. This is not always the case. In the ideal scenario, the change detection column is an architectural column from the source system. Examples include server constructs, trigger-managed datetimes, or built-in datetimes from commercial products that can be trusted. This is also true for pipeline tables loaded as described in Load mechanics.

Less ideally, the change detection column is managed by the source application through application logic. These columns are generally reliable but can be prone to developer error or fail to capture direct database changes. Finally, there may be no change detection columns at all. In this case, it is not possible to determine whether a source row has been updated. However, it may still be possible to identify inserted records by performing an anti-join between the source and target tables. This approach is useful for append-only loads such as building of hub tables.

## Tracking deletes

Polling tables can be used for tracking updates and inserts. Tracking deletes is equally important. However, this can be far more difficult because, in the case of deletes, rows disappear completely from the table itself. In the ideal scenario, deletes are tracked in the source through architectural artefacts. Some database technologies implement default history tables or delta logs. These history tables allow reliable tracking of deletes, provided they include a change detection column to indicate when the delete occurred. Less ideally, some applications maintain dedicated business audit tables that track changes, including deletes. These tables can be highly reliable, though they are often difficult to query. In the worst case, there is no change tracking. Rows can disappear without a trace. The only option is to compare the source and target using an anti-join on the primary key.

## The role of the Filter step

Two themes recur, whether for tracking upserts or tracking deletes:

- Source update datetimes that are synchronised with the pipeline’s process

datetimes are trivial to query.

- Architectural artefacts, rather than business artefacts, are the most reliable way

to track inserts, updates, and deletes. When either of these is absent, tracking changes becomes complex or even impossible. This is one of the reasons why pipelines begin with a Filter step that keeps transformation minimal. The filter step is designed to be the first interaction with the source data. On first arrival of the data, the pipeline adds the architectural artefacts required for change tracking. Doing this once at the start allows the rest of the pipeline to apply transformations incrementally with reliable change tracking. The optimal case is if the incoming data can be incrementally extracted using polling tables and the filter step adds the architectural columns for change-tracking. This effectively converts the source change detection columns, which may be out-of-sync

with the pipeline, to change detection columns which are in-sync the datetimes tracked by the pipeline. The Filter step, which is a simple extract of the necessary rows and columns with minimal joins or aggregations, may look like a step with low value-add. However, this step is serving as a critical foundation for an efficient pipeline because proper load mechanics computes change-tracking artefacts to support efficient downstream response.

## Conclusion

An efficient pipeline requires knowing exactly what changed in the source so that it responds only to those records. These changes include inserts, updates, and deletes. A simple approach to tracking upserts is to include the source change detection column in the target table. However, this can be problematic for non-trivial extracts and is at risk of instability. Instead, bookmarks to track the target and polling tables to track the source are reliable patterns for tracking changes relative to each other. Deletes are much harder to track without additional artefacts or audit tables. If these artefacts are not available, a full comparison of each batch is necessary to identify changes for upserts, deletes, or both. Given the complexity of tracking sources and the fragility of relying on other systems to maintain reliable architectural columns, it is important that each pipeline begins with an uncomplicated extract from the source data. The Load mechanics process annotates this extract with reliable change detection artefacts for downstream processing.
