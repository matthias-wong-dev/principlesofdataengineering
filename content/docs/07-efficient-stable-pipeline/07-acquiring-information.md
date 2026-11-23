---
title: Acquiring information
url: /docs/efficient-stable-pipeline/acquiring-information/
description: Explains how to acquire information incrementally from databases, APIs, and files, how to keep what cannot be retrieved again, and how to record provenance without causing churn.
lede: Effectively acquiring information is the foundation for an efficient pipeline.
weight: 7
# draft: true
---

## The first contact

[Tracking changes](/docs/efficient-stable-pipeline/tracking-changes/) and [Responding to change](/docs/efficient-stable-pipeline/responding-to-change/) explained how incremental load works between tables in the warehouse. Both depend on how information first entered the warehouse.

Acquisition is the first contact between the business world and the data world. Whatever happens there is inherited by every incremental load downstream.

The source is not under the data engineer’s control. Its owners publish on their own schedule, revise on their own terms, and may not keep what they published yesterday.

Proportionate change is first won or lost at acquisition. If there is no way to tell what changed at the source, everything must be retrieved. If everything is retrieved, every downstream table must work out for itself what changed. Inefficiency at the edge is carried through the whole pipeline.

Information is also most easily lost at acquisition. A row that is transformed badly can be transformed again. A file that was overwritten after the publisher withdrew it cannot be retrieved again.

There are three common types of source:

| Source | Examples |
|---|---|
| Databases | A transactional system, such as the bakery’s order system, or a logging system. |
| APIs | A delivery platform that sells the bakery’s cakes and exposes its orders over the web. |
| Files | Excel workbooks, CSV files, and PDFs, in a file store or on a webpage. |

For each type, the same question arises in a different form: *What has changed since the last acquisition?* Whether information can be acquired incrementally, or must be acquired in full each time, depends on the answer.

## Databases

Databases are the most common source of large volumes of data, whether from transactional systems or from logging.

The approach depends on what is available from the source system. There are three things to look for.

### Replication and change data capture

The best case is that replication or change data capture (CDC) is available. With mirroring and similar technologies, inserts, updates, and deletes are copied from the source into the warehouse as they happen.

Here, capturing change is the platform’s responsibility. The data engineer’s responsibility is to monitor it: to detect failure and lag, and to recover when replication stops or re-synchronises.

In a re-synchronisation, whole tables are copied again. This is candidate change, not genuine change.

The datetimes that come with replicated rows are not the pipeline’s own either. They may be the source’s commit time or the replication tool’s apply time. As explained in [The problem of time](/docs/efficient-stable-pipeline/tracking-changes/#the-problem-of-time), they are out-of-sync with the pipeline.

Replication is especially valuable for deletes, which are otherwise hard to track. The data engineer should keep them, not discard them at the first load.

### Audit columns

Where there is no replication, the source table may still have audit columns, such as `[Created datetime]` and `[Update datetime]`. With these, the data engineer can extract only the rows that changed since the last extract.

The data engineer’s task here is to understand how these columns are populated. This is a question about the business process, not the schema.

| How the column is maintained | Reliability |
|---|---|
| By the database, such as a trigger or default | Usually reliable, unless bulk fixes bypass it. |
| By application logic | Reliable only if every path that writes the row also sets the column. |
| By users | Unreliable for change tracking. |

Suppose the bakery’s order system sets `[Update datetime]` whenever an order is saved on screen. Each night, a correction script adjusts the prices of orders placed with an expired discount. The script writes directly to the table, and leaves `[Update datetime]` alone.

If orders are extracted on `[Update datetime]`, those corrections are never picked up. Nothing fails. The old prices simply remain in the warehouse.

Where the gaps are known and limited, a periodic full extract can catch what the incremental extract misses. The data engineer might extract all orders each Sunday, compare them with the warehouse, and apply only genuine change. The weekday extracts stay small, and no missed correction survives more than a week.

Where the gaps are unknown, the column cannot be relied on, and a full extract is needed each time.

Even a reliable column is set by the source’s clock, so each extract should start far enough back to allow for [the source time problem](/docs/efficient-stable-pipeline/tracking-changes/#the-source-time-problem).

### Deletes

Even where audit columns are reliable, deletes may not be visible. A deleted row has no `[Update datetime]`, because it is no longer there.

Deletes are visible in some sources, depending on how they are managed:

| Delete handling | What is available |
|---|---|
| Soft delete | Rows are flagged as deleted and keep their `[Update datetime]`. They are extracted like any other update. |
| Archive table | Deleted rows are moved to a separate table, which can be extracted incrementally. |
| Delete audit | A log records the keys of deleted rows, and when they were deleted. |
| None of these | Deletes cannot be seen directly. |

When deletes cannot be seen, the data engineer can extract the full list of primary keys from the source, and [anti-join](/docs/efficient-stable-pipeline/responding-to-change/#worked-example-3-anti-join) it with the warehouse. Keys in the warehouse that are no longer in the source have been deleted. Extracting keys alone is much cheaper than extracting full rows.

### Choosing the approach

The approach follows from what is available:

| Available from the source | Approach |
|---|---|
| Replication or CDC | Use it, and monitor it. |
| Reliable audit columns and visible deletes | Incremental extract. |
| Reliable audit columns, but no visible deletes | Incremental extract, with a full key extract and anti-join for deletes. |
| Audit columns with known, limited gaps | Incremental extract, with a periodic full extract to catch what it misses. |
| No reliable audit columns | Full extract each time. |

A full extract is not a full load. The extracted rows are still compared with what the warehouse holds, and only genuine change is written, as in [load mechanics](/docs/efficient-stable-pipeline/load-mechanics/#check-for-genuine-changes).

## APIs

Compared to a database, an API is a two-edged sword.

An API developer has usually thought about how others will use the data. The data is therefore more likely to be presented in a meaningful form, with the business rules already applied.

But the developer also controls access. If the API is incomplete or incorrect, there is usually no way around it. A database can be queried in ways its designers did not anticipate. An API can only be called in the ways its developer intended.

### Modified since

The equivalent of `[Update datetime]` is a *modified since* parameter. The data engineer supplies a datetime, and the API returns only the records changed after it.

In this case, the data engineer can call the API regularly, and save each response in a folder named for when it was retrieved. Each call resumes from the last successful retrieval.

```
orders/
    2025-11-13 06-00-00/
    2025-11-14 06-00-00/
    2025-11-15 06-00-00/
```

The folders are a record of what the API returned, and when. If a load fails, it can be rerun from the saved responses, without calling the API again.

Once saved, the responses are files. What follows about keeping, checking, and tracing acquired data applies to them as much as to files from a publisher.

The same caution applies as for audit columns. The modified datetime belongs to the source. The data engineer should understand which changes it reflects, and which it does not.

For example, the delivery platform’s orders API may return only the latest state of each order. An order that was placed, amended, and amended again between two calls appears once, in its final form. The intermediate amendments are never seen. If they matter, the data engineer must fetch each changed order again by its ID, to retrieve its full history.

This is where the developer’s control is felt again. Many APIs limit how many requests can be made in a period, and some charge for them. Fetching every changed order by its ID may take thousands of requests on the first run. A request budget, such as a thousand requests on the first run and a hundred on each run after, keeps the acquisition within those limits. Orders not reached in one run are fetched in the next.

### No reliable modified datetime

Without a reliable modified datetime, the data engineer must pull all records each time. Where that is too expensive, the alternative is to pull records as far back as practical against another date, such as the order date, to capture as much change as possible.

How far back is a judgement about how long records keep changing. Changes to older records will be missed, and this should be stated in the description.

### Deletes

Deletes are rarely available from an API. It is unusual for an API to offer a *deleted since* call.

The ideal case is that the source system does not allow deletes, and records a deletion as an update, such as a change of status to cancelled. A *modified since* call then returns deletions along with every other change.

Where records are genuinely deleted, the only option may be to fetch far enough back to see which records are missing. Even then, a record that is missing may have been deleted, or may simply have fallen outside the period requested. It is not always possible to tell which.

## Files

Files include Excel workbooks, CSV files, and PDFs, published in a file store or on a webpage. They often arrive periodically, such as a new price list each week.

Files are often less well managed than databases and APIs. Their structure is not enforced, and publishers rename and reorganise them freely. But because files are simple, they can be easier to deal with.

### Discovering new files

The first question is what the publisher currently provides.

A common approach is to predict where each file will be. If a flour supplier publishes one price list per week under a predictable name, the data engineer can work out the name for each week and request the file.

This works until the pattern changes. Publishers rename files, reorganise their pages, and change numbering schemes between years. If the names are worked out from a list of known years, the first price list of a new year is never requested. No error is raised. The data simply stops arriving.

A more reliable approach is to read the publisher’s own listing, such as the page that links to each file. New files are then discovered because they appear, not because their names were predicted.

The listing should be read from a **start period**. The start period is a deliberate decision about how much history the warehouse needs. Files before it are ignored, even if they are still listed.

Where there is no listing, predicted names may be unavoidable. In that case, the naming pattern is an assumption about the source, and it should be monitored like one.

### Immutable files

The next question is whether each file is immutable. Once a file is published, can it be changed?

If files are immutable, that is ideal. Acquisition can be done incrementally by name alone. On each run, it is enough to compare the names available with those already acquired, and fetch only the new ones. When nothing new has been published, there is no work to do.

Immutability is still an assumption. A publisher that corrects a file may publish the correction under a new name rather than the old one. A new file for a period that is already held should be treated as a new release of that period, not ignored.

### Mutable files

If files can be changed after release, the data engineer must decide how far back to fetch again.

Suppose the regional food authority publishes the results of each inspection round. The authority revises results after appeal, so the data engineer retrieves rounds from the previous twelve months again each day. Older rounds are treated as final.

Often there is no agreed date after which a file is final. The length of this **revision window** is a matter of practical judgement, and should be based on how the publisher has revised in the past, not on convenience. With a longer window, more revisions are caught, but more data is retrieved.

The window can be measured from the period a file describes, or from when the file was first retrieved. Measuring from first retrieval is safer when publication lags the period, because a late-published file still has its full window. The first retrieved datetime must then be kept through each revision. Otherwise the window restarts with every revision, and never closes.

Some files describe the current state of something, such as the authority’s register of licensed bakeries. They are republished under the same name whenever the state changes, so nothing about change can be learnt from the name. These files must be checked on every run. Where the web server reports a modified date or version marker, the data engineer can identify a candidate for change without downloading the file.

A file that is retrieved again has not necessarily changed. A workbook may be saved again with the same figures but a new creation date. If the data engineer keeps a hash of each file, and checks it before loading, a file that has not genuinely changed is not loaded again. For a workbook, the hash is best taken over the cell values rather than the file itself, so that a new creation date is not mistaken for new information.

### Files that overlap

A related question is whether each file contains only new data, or repeats data from earlier files.

Some publishers provide the whole history in every release. Suppose the bakery association publishes a monthly workbook of market sales, covering every month of the year to date.

**From the March workbook**

| Month | Market cake sales |
|---|---:|
| 2026-01 | 40,100 |
| 2026-02 | 39,800 |
| 2026-03 | 41,200 |

**From the April workbook**

| Month | Market cake sales |
|---|---:|
| 2026-01 | 40,100 |
| 2026-02 | 39,950 |
| 2026-03 | 41,200 |
| 2026-04 | 41,700 |

In the April workbook, one month is added and February is revised. January and March are repeated without change.

Other publishers show only a recent window. The flour supplier may offer only the last eighteen months of price lists. Such a window looks like a full extract, but it is not one. If it is loaded as a full extract, months that fall out of the window will be treated as deletes, and the warehouse will remove information that is still true.

This is a case where [source changes are not target actions](/docs/efficient-stable-pipeline/responding-to-change/#source-changes-are-not-target-actions). A month missing from the window means the publisher no longer shows it, not that it no longer exists.

### Load all rows, or only the changes

Once a file is acquired, the data engineer must decide what to load into the database.

| Approach | What happens | Consequence |
|---|---|---|
| Load all rows | The entire file is inserted each time. | Every repeated row is duplicated. Users must work out which copy is current. |
| Load only the changes | Incoming rows are compared with existing rows, and only genuine change is applied, as in [load mechanics](/docs/efficient-stable-pipeline/load-mechanics/#check-for-genuine-changes). | One current row per month. Overwritten values are kept in history. |

Loading all rows looks safer, because nothing is overwritten. But every user and every downstream table must then work out which copy is current. Loading only the changes is usually more helpful and more meaningful. One revised month means one changed row.

The real safety lies in keeping the acquired file. If every file is kept as it was retrieved, the information is preserved, and the rows in the database are free to be useful rather than also serving as the archive.

## Across all sources

The remaining sections apply whatever the source: a database extract, a saved API response, or a downloaded file.

### Syncing to data pipeline time

Every source keeps its own time. A replication commit time, an `[Update datetime]`, a *modified since* value, and a file’s modified date all belong to the source. As explained in [The problem of time](/docs/efficient-stable-pipeline/tracking-changes/#the-problem-of-time), they are out-of-sync with the pipeline.

The first task, once information arrives, is to map it into the data pipeline’s own time. Each acquired row is given pipeline-managed `[Row insert datetime]`, `[Row update datetime]`, and `[Row delete datetime]`, recording when the warehouse first held it, last saw it genuinely change, and saw it deleted. These are in-sync times.

This is the same translation described for [polling tables](/docs/efficient-stable-pipeline/tracking-changes/#polling-tables), from source time to pipeline time, applied at the point of entry. It is usually done in the [Filter step](/docs/creating-information/entity-processing/#first-pass-filter), where incoming rows are compared with what the warehouse already holds, and only genuine change is stamped.

Once information is in pipeline time, every downstream table can respond to it appropriately. Whether replication, audit columns, a *modified since* call, or none of these was available at the source, downstream tables see one consistent timeline. Each table can use its [refresh bookmark](/docs/efficient-stable-pipeline/tracking-changes/#refresh-bookmarks) to process only what genuinely changed, without knowing how the source behaved. When nothing changed at the source, nothing is stamped, and there is no work downstream.

This is where [efficiency and stability](/docs/efficient-stable-pipeline/efficiency-and-stability/) begin. A small change at the source becomes a small change in pipeline time, and the rest of the pipeline does only the work that change requires.

### Checking before accepting

Acquired data can arrive damaged. A download may be cut short. An API may return an error message in place of data. A publisher may replace a workbook with an error page that has the same name.

If such an item is accepted, a good copy is replaced with a bad one, and every row from the good copy appears to be deleted.

Each item should therefore be checked before it is accepted. Does it open, or parse? Does it have the expected sheets, columns, or fields? Is the row count plausible compared with the previous copy? An item that fails these checks is rejected, and the stored copy is kept. This is the same mindset as [Fault tolerance](/docs/quality-reliability/fault-tolerance/).

### When a source is missing

When an expected file or response is missing, the data engineer has to decide what the absence means.

Usually, the item has not been published yet. Next week’s price list is missing because next week has not happened. This is ordinary, and it should not fail the load.

The source may also be briefly unavailable. Nothing is learnt about the item, and the stored copy remains the best available.

In both cases, the stored copy is kept and the item is tried again on the next run. At most, the load for that source fails. The absence should not spread beyond it.

But absence should not pass unnoticed forever. A publisher that has stopped publishing looks the same, on any one run, as a publisher that has not published yet. Absence is ordinary only while it is expected. Once an item is overdue, it should be surfaced as a [monitored assumption](/docs/quality-reliability/tests-and-assumptions/#is-source-data-up-to-date).

| Absence | Meaning | Response |
|---|---|---|
| Item not yet due | Not yet published. | Try again next run. |
| Source briefly unavailable | Nothing is known about the item. | Keep the stored copy and try again next run. |
| Item overdue, or source unavailable for several runs | The source may have changed. | Surface for attention. |

### Keeping what was acquired

A transformed table can be rebuilt from its inputs. Acquired data cannot.

> Acquired data cannot be rebuilt. It can only be retrieved again, and the source may have moved on.

Acquired data should therefore be treated differently.

First, a replaced item should not be overwritten. When a revised version arrives, the previous version should be kept, for example under its hash. Otherwise there is no way to show what the source said before the revision.

Second, acquired data should be protected from rebuild. When a transformed table is rebuilt, the same result is restored. When acquired data is rebuilt, the source is retrieved as it is today. Once a publisher has withdrawn a file or moved its window, information would be lost in a rebuild.

## Provenance

When data is acquired by API or from files, a reasonable record of where it came from should be kept, and carried down to the rows loaded from it.

For each acquired file, this usually means its address, when it was first retrieved, when its content last changed, and its hash. The two datetimes are the file’s equivalent of `[Row insert datetime]` and `[Row update datetime]`. Like them, they should change only when the content genuinely changes. If they were updated on every run, every file would look changed, and every downstream table would respond. This is the [`[Today’s date]` problem](/docs/quality-reliability/fault-tolerance/#stability) in another form.

The rows loaded from a file should carry at least its address, in a column such as `[Source URL]`. A user can then trace each value back to the file it came from.

Provenance is harder to record for overlapping and mutable files. If the March workbook has three months and the April workbook has four, with one revised, which workbook is the source of each month? The latest, or the earliest?

Under the principle of proportionate change, the answer is the earliest workbook that delivered the current value. The provenance is updated only when the value changes.

**`Cake.MarketSales` after the April workbook**

| Month | Market cake sales | Source URL |
|---|---:|---|
| 2026-01 | 40,100 | …/market-sales-2026-03.xlsx |
| 2026-02 | 39,950 | …/market-sales-2026-04.xlsx |
| 2026-03 | 41,200 | …/market-sales-2026-03.xlsx |
| 2026-04 | 41,700 | …/market-sales-2026-04.xlsx |

January and March are unchanged, so they are still attributed to the workbook that first delivered their values. February was revised, so its value and its provenance change together. April is new.

The comparison described in [load mechanics](/docs/efficient-stable-pipeline/load-mechanics/#check-for-genuine-changes) is needed, with one difference. The provenance column must be *excluded from the comparison*. Otherwise every repeated row would look changed, because each workbook has a different address, and every row would be updated on every load.

Provenance is about the delivery, not the information. A repeated delivery of the same value is not a change in the business world, so it should not be a change in the data world.

There is a second design choice. `Cake.MarketSales` keeps only the current value for each month. Alternatively, `[Source URL]` can be included in the primary key, with every workbook’s value kept as a separate row. The full revision history is then preserved, at the cost of volume and a more complex model for users. Both are valid. The choice depends on whether users need to see how the figures were revised.

## Describing the acquisition

The interpretation of information depends materially on how it was acquired. This is especially so where a judgement was made, such as how far back to fetch. A revision older than the window will be missed, and users should know that.

As explained in [Quality metadata](/docs/quality-reliability/quality-metadata/#descriptions-answer-what-does-this-mean), the acquisition logic should be stated clearly and briefly in the table’s description. For example:

```md
Weekly flour price lists published by the supplier. Published price lists do not change, so only price lists not already held are fetched.
```

```md
Monthly market sales published by the bakery association, covering the year to date. Earlier months can be revised as late returns arrive. The latest six workbooks are fetched each day, and only genuine changes are loaded.
```

```md
Orders extracted incrementally from the order system using [Update datetime], which is set by the application when an order is saved. Prices corrected by the nightly discount script do not update this column, so a full extract is taken each Sunday. Deletes are detected by comparing the full list of order IDs each night.
```

In each description, the assumption behind the acquisition is stated. If the source starts to behave differently, the assumption can be checked, and users can see what may have been missed.

## Conclusion

Acquisition is the first load in the pipeline, and the one with the least control.

Different signals of change are available from databases, APIs, and files. With replication, audit columns, *modified since* calls, or immutable file names, incremental acquisition is possible. Where these are absent or unreliable, more must be fetched, and the data engineer must judge how far back change can reach.

Whatever the source, the outcome should be the same. Acquired content is kept as it was retrieved, rows are synced to pipeline time, provenance changes only when the information does, and the description states how the information was acquired. That is the foundation for every incremental load downstream.

> [!NOTE]
> **Key ideas**
>
> Acquisition is where proportionate change is first won or lost, and where information is most easily lost.
>
> The approach to acquiring from a database depends on what is available: replication, reliable audit columns, and visible deletes. Without them, more must be extracted and compared.
>
> An API is usually more deliberate than a database, but its gaps cannot be worked around. Deletes are rarely available from an API.
>
> Immutable files can be acquired by name alone. Mutable and overlapping files are fetched again within a revision window chosen by judgement.
>
> Acquired information is synced to pipeline time on arrival, so that every downstream table can respond to genuine change efficiently and stably.
>
> Acquired data cannot be rebuilt, so replaced versions are kept and protected from rebuild.
>
> Provenance is recorded from the earliest delivery of the current value, and excluded from the change comparison, so that repeated delivery does not cause churn.
>
> The acquisition logic belongs in the table’s description, so that users know what the table can miss.
