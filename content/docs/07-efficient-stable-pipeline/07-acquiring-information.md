---
title: Acquiring information
url: /docs/efficient-stable-pipeline/acquiring-information/
description: Explains how to acquire external data efficiently and stably by discovering new items, detecting change before retrieval, and retaining what cannot be retrieved again.
lede: Efficient acquisition retrieves only what may have changed, and keeps what cannot be retrieved again.
weight: 7
# draft: true
---

## The first contact

[Tracking changes](/docs/efficient-stable-pipeline/tracking-changes/) and [Responding to change](/docs/efficient-stable-pipeline/responding-to-change/) explained how incremental load works between tables. Both depend on a foundation laid at the start of the pipeline, when information is first acquired.

Acquisition is the first contact between the business world and the data world. Every incremental load downstream inherits what happened there. This is why acquisition deserves a special study.

The source may be an operational database, a publisher’s website, a file share, or an API. Whatever its form, the source is not under the pipeline’s control. It publishes on its own schedule, revises on its own terms, and may not keep what it published yesterday.

Acquisition is where proportionate change is first won or lost. If the pipeline cannot tell what changed at the source, it must retrieve everything. If it retrieves everything, every downstream table must work out for itself what changed. The inefficiency at the edge spreads through the whole pipeline.

Acquisition is also where information is most easily lost. A row that is transformed badly can be transformed again. A file that was overwritten, after the publisher withdrew it, cannot be retrieved again.

Acquiring information well means answering three questions:

| Question | Concern |
|---|---|
| Discovery | What does the source publish, and what is new? |
| Change detection | Which known items may have changed, and how far back can they change? |
| Retention | What must be kept, because it cannot be retrieved again? |

This chapter uses published files as the main example, because they make each question visible. The same questions apply to tables and APIs.

## Discovering new items

The first question is what the source currently publishes.

A common approach is to predict where each item will be. If a flour supplier publishes one price list per week under a predictable name, the pipeline can work out each week’s name and try to retrieve it.

This works until the pattern changes. Publishers rename files, reorganise what they publish, and change numbering schemes between years. A pipeline that works out names from a list of known years will quietly stop discovering new price lists when the first list of a new year is published. Nothing fails. The data simply stops arriving.

A more reliable approach is to read the source’s own listing.

Most sources maintain a list of what is available. Reading the listing lets the source say what exists, rather than the pipeline guessing. New items are discovered because they appear, not because the pipeline predicted their names.

The listing should be read from a **start period**. The start period is a deliberate decision about how much history the warehouse needs. Items before it are ignored, even if the listing still shows them.

| Discovery approach | Strength | Risk |
|---|---|---|
| Predicted names | Works when no listing exists. | Silently stops when the naming pattern changes. |
| Listing from a start period | Discovers what the source actually publishes. | Depends on the listing being complete. |

Where no listing exists, predicted names may be unavoidable. In that case, the naming pattern is an assumption about the source, and it should be monitored like one.

### Absence is not failure

When an expected item is missing, the pipeline has to decide what the absence means.

Usually, the item has not been published yet. Next week’s price list is missing because next week has not happened. This is ordinary, and it should not fail the load.

The source may also be briefly unavailable. This says nothing about the item, and the stored copy remains the best available.

In both cases, the stored copy is kept and the item is tried again on the next run. At most, the load for that source fails. The absence should not spread beyond it. This is the same mindset as [Fault tolerance](/docs/quality-reliability/fault-tolerance/).

But absence should not pass silently forever. A source that has stopped publishing looks the same, on any one run, as a source that has not published yet. Absence is ordinary only for as long as it is expected. Once an item is overdue, it should be surfaced as a [monitored assumption](/docs/quality-reliability/tests-and-assumptions/#is-source-data-up-to-date).

| Absence | Meaning | Response |
|---|---|---|
| Item not yet due | Not yet published. | Try again next run. |
| Source briefly unavailable | Nothing is known about the item. | Keep the stored copy and try again next run. |
| Item overdue, or source unavailable for several runs | The source may have changed. | Surface for attention. |

## Detecting change before retrieval

Once an item is known, the next question is whether it may have changed.

As explained in [Tracking changes](/docs/efficient-stable-pipeline/tracking-changes/#detecting-change-at-the-source), change tracking at an external source should begin before anything is retrieved. The right approach depends on how the source behaves.

| Source behaviour | Approach |
|---|---|
| Immutable items | Retrieve once by name, then never again. |
| Revisable items | Retrieve again within a revision window. |
| Current-state items | Check on every run, then compare content. |
| Rolling publication windows | Keep one copy per edition, so older periods are not lost. |

Each approach is an assumption about the source. It should be stated in the table’s [description](/docs/quality-reliability/quality-metadata/#descriptions-answer-what-does-this-mean), so that users know what the table can miss.

### Immutable items

Some sources never change what they have published. A weekly price list labelled with its week, or a monthly statement labelled with its month, is published once and left alone.

For immutable items, the name is enough. If the warehouse already holds an item with that name, there is nothing to do. The pipeline reads the listing, finds no new names, and finishes without retrieving anything.

This is the cheapest possible acquisition. When nothing new has been published, the run does no work.

Immutability is still an assumption. A publisher that corrects an item may publish the correction under a new name rather than the old one. A new name for an existing period should therefore be treated as a new release of that period, not ignored.

### Revision windows

Other sources revise recent items. A bakery association may amend its monthly market sales figures for some months after they are first published, as late returns arrive.

For these sources, the pipeline retrieves recent items again within a **revision window**. Items older than the window are treated as final.

For example, each monthly market sales file may be retrieved again each day for six months, then left alone. As at June 2026:

| Period | Within revision window | Action |
|---|---|---|
| 2026-05 | Yes | Retrieve again and compare. |
| 2026-01 | Yes | Retrieve again and compare. |
| 2025-09 | No | Treat as final. |

The window is a trade-off. A longer window catches more revisions but retrieves more data. A shorter window is cheaper but misses late revisions. The length should be based on how the source has actually revised in the past, not on convenience.

The window can be measured from the period an item describes, or from when the item was first retrieved. Measuring from first retrieval is safer when publication lags the period, because a late-published item still receives its full window. The first retrieved datetime must then survive each revision. Otherwise every revision restarts the window, and it never closes.

A retrieved item is not necessarily a changed item. A file may be republished with the same figures but a new creation date. Comparing the whole file would report a change. Comparing the figures would not. The comparison should be on the information, not on the packaging.

### Current-state items

Some items describe the current state of something, such as a register of approved suppliers, and are republished under the same name whenever the state changes.

For current-state items, the name says nothing about change. The pipeline must check on every run.

Some sources provide change metadata, such as a modified date or version marker, that says whether an item may have changed since the stored copy was retrieved. This identifies a candidate. Genuine change is still confirmed by comparing content. Where there is no such metadata, the pipeline retrieves the item on every run and compares it with the stored copy.

### Rolling publication windows

Some sources show only a recent window. A supplier may offer only the last eighteen months of weekly price lists. A quarterly market report may carry only the last eight quarters.

A rolling window looks like a full extract, but it is not one. If it is loaded as a full extract, periods that fall out of the window will be treated as deletes, and the warehouse will remove information that is still true.

This is a case where [source changes are not target actions](/docs/efficient-stable-pipeline/responding-to-change/#source-changes-are-not-target-actions). Absence from the window means the publisher no longer shows the period, not that the period no longer exists.

The answer is to keep one copy per edition. Each new edition is added to what the warehouse already holds. Nothing is removed because it has dropped out of the publisher’s window.

Each edition repeats the periods still in the window, so the same period is delivered several times. Whether users see one current value per period or every edition’s value is a design choice, covered in [Files that repeat older data](/docs/efficient-stable-pipeline/acquiring-information/#files-that-repeat-older-data).

## Retaining what was retrieved

The third question is what to keep. The answer is to keep what was retrieved, as it was retrieved, alongside a record of how it was acquired.

**Example structure of an acquisition record**

| Field | Meaning |
|---|---|
| Source location | Where the item was retrieved from, and the listing it was discovered on. |
| First retrieved datetime | When the warehouse first held this item. |
| Retrieved datetime | When the current content was retrieved. |
| Checksum | A fingerprint of the content, used to detect genuine change. |
| Source version | The edition, release, or version the source assigns, if any. |
| Source change metadata | The source’s own modified date, size, or version marker, if provided. |

The record serves three purposes. It lets the next run decide whether anything changed. It gives downstream tables the provenance they need. It lets the data engineer answer what the source said, and when, long after the source has moved on.

### Write only on genuine change

If the retrieved content is identical to the stored copy, nothing should be written.

This applies to the record as well as the content. Updating the retrieved datetime on every run would make every item look changed, and every downstream table would respond. This is the [`[Today’s date]` problem](/docs/quality-reliability/fault-tolerance/#stability) in another form.

When content genuinely changes, the record should change with it, in the same way that [load mechanics](/docs/efficient-stable-pipeline/load-mechanics/#step-3-apply-the-changes) updates `[Row update datetime]` only for genuine change. Because the record changes only with content, its first retrieved datetime and retrieved datetime serve as the stored file’s pipeline-managed change datetimes, equivalent to `[Row insert datetime]` and `[Row update datetime]`.

### Never discard what cannot be retrieved again

A transformed table can be rebuilt from its inputs. Acquired data cannot.

This changes how acquired data should be treated.

First, a replaced item should not be overwritten. When a revised version arrives, the previous version should be kept, for example under its checksum. Otherwise the warehouse loses the ability to show what the source said before the revision.

Second, acquired data should be protected from rebuild. Rebuilding a transformed table restores the same result. Rebuilding acquired data retrieves the source as it is today, which may be different. Once the source has withdrawn an item or moved its rolling window, a rebuild would delete information.

> Acquired data cannot be rebuilt. It can only be retrieved again, and the source may have moved on.

## Reading only what changed

Once acquisition writes only on genuine change, downstream tables can read only what changed.

The pattern is the same as for tables. Each acquisition run records which items were added or changed. A downstream table looks up its [refresh bookmark](/docs/efficient-stable-pipeline/tracking-changes/#refresh-bookmarks) and reads only the items that changed after it.

If nothing changed, nothing was recorded. The downstream table finds no items to read, and finishes without doing any work.

| Acquisition run | Items changed | Downstream work |
|---|---|---|
| New weekly price list published | 1 insert | Read one file. |
| Recent market sales file revised | 1 update | Read one file and apply genuine changes. |
| No new or changed items | None | None. |

Disappearance deserves the same caution as deletes in [load mechanics](/docs/efficient-stable-pipeline/load-mechanics/#check-for-instability). An item that disappears from the source, or a revised item that drops keys it used to contain, is a large change at the source. It may be a genuine withdrawal, or it may be a publishing error. Either way, it should be checked before it is allowed to spread.

## Files that repeat older data

Some sources repeat older data in every file. A quarterly market report may carry a time series for the last eight quarters. An annual release may restate every previous year.

The same value therefore arrives many times. This creates a tension between two needs.

The first is provenance. The user should be able to see which file a value came from.

The second is stability. If a value has not changed, receiving it again should not change the warehouse.

Suppose `Cake.MarketSales` is loaded from quarterly editions of the market report, keyed by `[Quarter]`, with `[Source edition]` recording the edition each value came from.

**Current `Cake.MarketSales`**

| Quarter | Market cake sales | Source edition |
|---|---:|---|
| 2025-Q3 | 120,400 | 2025-Q4 |
| 2025-Q4 | 121,100 | 2025-Q4 |

The next edition repeats both quarters and adds a new one. 2025-Q4 has been revised.

**Incoming from edition 2026-Q1**

| Quarter | Market cake sales | Source edition |
|---|---:|---|
| 2025-Q3 | 120,400 | 2026-Q1 |
| 2025-Q4 | 121,300 | 2026-Q1 |
| 2026-Q1 | 121,900 | 2026-Q1 |

If `[Source edition]` is included when [load mechanics checks for genuine change](/docs/efficient-stable-pipeline/load-mechanics/#check-for-genuine-changes), every repeated row becomes an update. 2025-Q3 is updated even though its value is unchanged. With eight quarters per file, every edition updates eight rows to add one. Downstream tables respond to changes that did not happen.

Provenance columns should therefore be **excluded from the comparison**.

The comparison asks whether the information changed. `[Source edition]` does not describe the information. It describes the delivery. A repeated delivery of the same value is not a change in the business world, so it should not be a change in the data world.

**Updated `Cake.MarketSales`**

| Quarter | Market cake sales | Source edition |
|---|---:|---|
| 2025-Q3 | 120,400 | 2025-Q4 |
| 2025-Q4 | 121,300 | 2026-Q1 |
| 2026-Q1 | 121,900 | 2026-Q1 |

2025-Q3 is unchanged, and still shows the edition that first delivered its value. 2025-Q4 was genuinely revised, so its value and its provenance change together. 2026-Q1 is new.

Excluding provenance from the comparison does not lose provenance. Each row shows the edition that delivered its current value. When the value is revised, the provenance moves with it. When the value is merely repeated, the row keeps pointing to its original source.

There is a second design choice. The table above keeps only the current value for each quarter. An alternative is to include `[Source edition]` in the primary key, keeping every edition’s value as a separate row. This preserves the full revision history, at the cost of volume and a more complex model for users. Both are valid. The choice depends on whether users need to see how the figures were revised, and it should be stated in the description.

## Database replication

When the source is an operational database, acquisition is usually configured rather than built. Change data capture, mirroring, and other replication technologies copy inserts, updates, and deletes into the warehouse.

This removes much of the work of discovery and retrieval. It does not remove the problem of time.

Replicated change datetimes may be the source’s commit time or the replication tool’s apply time, and replication may lag or re-synchronise whole tables. Unless the replication itself stamps changes in pipeline time, those datetimes are out-of-sync. The principles of [Tracking changes](/docs/efficient-stable-pipeline/tracking-changes/#the-problem-of-time) therefore apply unchanged. A re-synchronisation is candidate change, not genuine change, and a [Filter step](/docs/creating-information/entity-processing/#first-pass-filter) assigns pipeline-managed row change datetimes.

Replication is valuable because it captures deletes, which are otherwise hard to track. The pipeline should preserve them rather than discard them at the first load.

## Conclusion

Acquisition is the first load in the pipeline, and the one with the least control.

The source decides what to publish, when to revise it, and when to withdraw it. The pipeline cannot change this. It can only observe the source carefully, retrieve no more than necessary, and keep what it cannot retrieve again.

Done well, acquisition gives the rest of the pipeline what it needs: stored content with pipeline-managed change datetimes, provenance for every item, and a record of what changed in each run. Every incremental load downstream builds on that foundation.

> [!NOTE]
> **Key ideas**
>
> Efficient acquisition retrieves only what may have changed, and keeps what cannot be retrieved again.
>
> Discover new items from the source’s own listing, from a deliberate start period, rather than predicting their names.
>
> A missing item is usually not yet published. Contain its absence, but surface it once it is overdue.
>
> Immutable items are retrieved once. Revisable items are retrieved again within a revision window. Rolling publication windows are kept one edition at a time.
>
> Compare content, not packaging, and write only on genuine change.
>
> Acquired data cannot be rebuilt. Replaced versions should be kept, and acquired data protected from rebuild.
>
> Database replication still needs the principles of tracking changes, because the source’s time is not the pipeline’s time.
>
> When files repeat older data, provenance columns should be excluded from the comparison, so repeated delivery does not cause churn.
