---
title: Tests and assumptions
url: /docs/quality-reliability/tests-and-assumptions/
description: Explains how tests and monitored assumptions make failure visible before errors undermine trust in a data product.
lede: Good engineering makes failure visible before it reaches the user.
weight: 4
# draft: true
---

## Anticipating errors

A data product is not trustworthy merely because it is correct today. It is trustworthy when users are not caught unawares by eventual failures.

This is the third principle of data engineering: 

> [!SHARE:instead-stopping-works]
> Instead of stopping with what works now, anticipate errors that may occur.

The principle follows from two facts.

First, the world changes. What is true today may not be true tomorrow. New data may arrive outside previously conceived parameters. Business processes may evolve. Source systems may change. Another developer may alter existing code.

Second, engineers make mistakes. Complex transformations create many opportunities for small errors to become consequential.

The danger is not only that errors occur—errors are inevitable.

The deeper danger is that errors occur silently.

A silent error allows a data product to remain polished and apparently authoritative while no longer being safe to use.

Therefore: 

> [!SHARE:data-engineering-not]
> Data engineering is not only building the transformation that works. It is building the means by which failure becomes visible.

This chapter covers two such mechanisms:

| Mechanism | Question | Output |
|---|---|---|
| Tests | Did two independent calculations produce the same result? | Pass or fail |
| Monitored assumptions | Has something appeared that requires human attention? | A list of violating records |

A test performs the same calculation in two different ways and checks whether the results agree.

A monitored assumption checks whether a condition presumed to hold has been violated, and returns the records requiring attention.

Tests protect the correctness of implemented logic. Monitored assumptions protect the safety of the conditions around that logic.

Both should run regularly, such as once per pipeline batch. Their purpose is not to eliminate failure entirely. Their purpose is to prevent avoidable failure from remaining hidden.

## Tests: checking the same result two ways

A data test is strongest when expected and actual results are calculated independently.

The premise of testing is this: when the same problem is solved in two different ways, and both methods arrive at the same result, confidence is justified.

In data engineering, a test has two parts:

| Test part | Meaning |
|---|---|
| Expected result | A calculation of what the result should be, preferably from a different source or logic path. |
| Actual result | The result produced by the pipeline, model, or measure being tested. |

The test passes if expected and actual results match.

In a data pipeline, the expected part of a test may be calculated from raw or partly transformed data. The actual part uses the transformed output.

In a Power BI semantic model, the expected part of a test may be calculated from the underlying data source, such as SQL or a data lake. The actual part may be calculated using DAX. This approach is effective for validating complex DAX measures, especially measures that rely on embedded grain or complex DAX.

Power BI tests are easy to create. The data engineer can drag and drop to build a table visual with dimensions and measures. The Performance Analyzer in Power BI Desktop reveals the DAX query behind the visual. This can serve as the actual portion of the test. The engineer then compares the DAX evaluation with a calculation from the underlying data source.

Tests lose effectiveness when the expected query is a copy of the pipeline code that produced the actual result. This entanglement reduces independence and narrows the surface of possible errors caught by the test.

A thoughtful test maximises the difference in logic between expected and actual results.

The way to write a good test is to ask:

> [!SHARE:complex-fragile-part]
> Where is the most complex or fragile part of the transformation, and how can this result be calculated in a different way?

The following examples are not exhaustive. They illustrate the mindset of checking weak points by calculating the same result through a different path.

### Row counts

Row count tests check whether records have appeared, disappeared, or duplicated unexpectedly.

The simplest test is to compare row counts before and after transformation. The expected query counts rows from the raw data with appropriate filters. The actual query counts rows from the transformed output.

**Example row count test**

| Test | Expected result | Actual result |
|---|---:|---:|
| Count sales records for April 2025 | 10,240 | 10,240 |

Even small variations can make row count tests more effective.

For example, instead of only counting all rows, the data engineer may group by a reference value.

**Example grouped row count test**

| Sales region | Expected sales rows | Actual sales rows |
|---|---:|---:|
| North | 2,450 | 2,450 |
| South | 3,100 | 3,100 |
| West | 1,920 | 1,918 |
| New store not annotated | 12 | 14 |

The total row count may still match because one group is undercounted while another is overcounted. Grouped counts reveal the problem, helping catch update errors, join errors, and mapping issues.

The expected and actual calculations should use different logical paths. For example, the expected query may group raw records using source fields, while the actual query groups transformed records using curated dimensions.

Row count tests are especially important for incremental loads.

If the extract relies on an architectural column such as `[Row update datetime]`, the test should use a different datetime column, such as `[Staff update datetime]`, `[Submission datetime]`, or another business-centric column. This separation avoids self-confirmation.

Selecting a sample of recent records is also useful. A recent-record sample can check creation, update, and deletion behaviour across many columns, not only row counts.

### Checksums on key results

Checksum tests check whether an important summary result still balances.

They are useful when a transformation rolls detailed records up into a business concept.

Consider the example of manufacturing batch quality.

A business process may record individual quality-control criteria. The data engineer then rolls these up to define the overall quality outcome for each batch.

**Example structure of `'Batch quality criterion'`**

| Batch ID | Quality criterion | Quality result | Is critical criterion |
|---|---|---|---|
| B1001 | Temperature control | Pass | true |
| B1001 | Packaging integrity | Pass | false |
| B1001 | Labelling accuracy | Fail | false |
| B1002 | Temperature control | Fail | true |
| B1002 | Packaging integrity | Pass | false |

The transformed output may look like this.

**Example structure of `'Batch quality outcome'`**

| Batch ID | Critical criteria failed | Non-critical criteria failed | Batch quality outcome |
|---|---:|---:|---|
| B1001 | 0 | 1 | Pass |
| B1002 | 1 | 0 | Fail |

A checksum can test the core logic without copying the transformation.

For example, every batch should fall into one and only one of two groups: pass or fail.

**Example checksum test**

| Test | Expected result | Actual result |
|---|---:|---:|
| Count distinct batches from criterion table | 2 | 2 |
| Count batches marked pass or fail in outcome table | 2 | 2 |
| Count batches with any critical failure from criterion table | 1 | 1 |
| Count batches marked fail in outcome table | 1 | 1 |

This test is not a copy of the transformation. It checks whether the transformed result still balances against the source logic.

A more comprehensive version can group by values such as `[Product type]`, `[Manufacture site]`, or `[Inspection month]`. This increases the chance of catching errors that affect only a segment of the data.

### Bypassing mapping tables

Mapping tables are often introduced where the source system did not record an analytical relationship.

A good test for a mapping table is to compare results with and without the mapping table.

Consider the restaurant example from the previous chapter. The source system records table sittings, table customers, and food orders. It does not record which customer ordered which food item.

The data engineer introduces `Club.CustomerFoodOrderMap` to allocate food orders across members seated at the table.

**Example structure of `Club.TableCustomer`**

| Table sitting ID | Member ID |
|---|---|
| T001 | M001 |
| T001 | M002 |

**Example structure of `Club.TableFoodOrder`**

| Table sitting ID | Food order ID | Food item ID | Food item cost |
|---|---|---|---:|
| T001 | FO001 | F100 | 12.00 |
| T001 | FO002 | F200 | 18.00 |

**Example structure of `Club.CustomerFoodOrderMap`**

| Table sitting ID | Member ID | Food order ID | Allocation weight |
|---|---|---|---:|
| T001 | M001 | FO001 | 0.5 |
| T001 | M002 | FO001 | 0.5 |
| T001 | M001 | FO002 | 0.5 |
| T001 | M002 | FO002 | 0.5 |

Regardless of how complex the mapping logic becomes, some totals should remain the same. The total cost of food ordered at the table should not change after allocation.

**Example mapping checksum**

| Table sitting ID | Expected food cost from `Club.TableFoodOrder` | Actual allocated food cost from `Club.CustomerFoodOrderMap` |
|---|---:|---:|
| T001 | 30.00 | 30.00 |

This is a powerful way to validate mapping logic. The test does not need to repeat every detail of the mapping. It checks whether the mapping preserves an invariant.

More specific tests can then check the business rule itself.

For example, if the business rule assumes food cost is evenly distributed among seated members, the test can check that allocation weights sum to `1` per food order.

**Example allocation-weight test**

| Food order ID | Expected allocation weight total | Actual allocation weight total |
|---|---:|---:|
| FO001 | 1.0 | 1.0 |
| FO002 | 1.0 | 1.0 |

Grouping by reference columns such as `[Food item ID]`, `[Food item type]`, or `[Table sitting ID]` can make the test more sensitive.

### Checking boundary cases

Boundary cases are common sources of error.

A typical example is a rolling-window measure. Any implementation of a rolling window should be tested at boundary points.

Suppose there is a Power BI measure `[Total sales volume]`, and a derived rolling 12-month version `[Total sales volume past 12 months]`.

The rolling measure is easy to get subtly wrong. It may include the wrong start date, exclude the current date, mishandle leap years, or behave incorrectly at the beginning of the available history.

One useful test is to compare the rolling result against known calendar boundaries.

For example, if `[Total sales volume past 12 months]` is evaluated at 31 December 2025, it should match total sales volume for the 2025 calendar year.

**Example boundary test**

| Evaluation date | Expected result | Actual rolling 12-month result |
|---|---|---|
| 2025-12-31 | Total sales from 2025-01-01 to 2025-12-31 | Total sales volume past 12 months at 2025-12-31 |
| 2026-06-30 | Total sales from 2025-07-01 to 2026-06-30 | Total sales volume past 12 months at 2026-06-30 |

This checks that the measure behaves properly at calendar-year and financial-year boundaries.

However, this test would still pass if `[Total sales volume past 12 months]` were mistakenly implemented as a copy of `[Total sales volume]` in a model that is already filtered to one year.

To guard against this, the data engineer should also test turning points, such as the first and last day of a month.

**Example turning-point test**

| Evaluation date | Boundary being tested |
|---|---|
| 2025-02-28 | End of February |
| 2025-03-01 | Start of March |
| 2025-06-30 | End of financial year |
| 2025-07-01 | Start of financial year |

A rolling-window measure that passes at calendar-year boundaries, financial-year boundaries, and interim month turning points provides much stronger assurance than one tested only at convenient dates.

### Using subject matter knowledge

Subject matter knowledge can introduce independence into a test.

Normally, the data engineer should avoid building unverified assumptions into the pipeline. This prevents blind spots and reduces the risk of silent errors.

However, tests are one place where business knowledge can be safely used to strengthen robustness. If the business knowledge is wrong, the test will reveal that. If the business knowledge was once right but stops being right, the test will reveal a change in the process.

For example, a business expert may know that every table sitting must have at least one customer. The data engineer should not blindly assume this in the pipeline, because load errors may still occur. But the knowledge can be used in a test.

**Example subject-matter test**

| Business knowledge | Expected calculation | Actual calculation |
|---|---|---|
| Every table sitting has at least one customer | Count table sittings using an inner join to `Club.TableCustomer` | Count all rows in `Club.TableSitting` |

If the results differ, either the data has an error, the pipeline has an error, or the business knowledge was incomplete.

Business knowledge can also validate roll-up logic.

Consider a help desk system where cases escalate from Tier 1 to Tier 4. Escalations are recorded in `Helpdesk.Escalation`, keyed by `[Case ID]`, with `[Tier]` indicating escalation level. The table `Helpdesk.CaseEscalation` rolls this information up to case grain. A reference table `Helpdesk.RefCaseEscalation` includes `[Highest escalation]` to summarise each case.

Tests can use business knowledge to validate the roll-up.

| Business knowledge | Expected | Actual |
|---|---|---|
| Every case starts at Tier 1 | Count distinct `[Case ID]` in `Helpdesk.Escalation` where `[Tier] = "Tier 1"` | Count rows in `Helpdesk.CaseEscalation` |
| Tier 4 is the maximum escalation | Count distinct `[Case ID]` in `Helpdesk.Escalation` where `[Tier] = "Tier 4"` | Count rows in `Helpdesk.CaseEscalation` where `[Highest escalation] = "Tier 4"` |
| Cases do not skip the existence of earlier tiers | Count Tier 4 cases with no Tier 1 record | Should be zero |

In general, existence and uniqueness conditions known to business experts can be used to bypass or vary the original pipeline logic.

This is one of the strongest ways to write tests because it introduces a source of independence outside the code itself.

## Monitored assumptions: surfacing records that require attention

Data engineers must make assumptions.

However, assumptions may fail over time. Sometimes the failure is unanticipated. At other times, the failure is anticipated but still needs to be detected.

A monitored assumption is a query that returns records if and only if human attention is required.

If no rows are returned, the assumption remains valid. If rows are returned, each row is a violation that needs attention.

The key to monitoring assumptions is recognising that an assumption exists.

The following are common cases.

| Assumption | Returns rows when... |
|---|---|
| Source data is up to date | The latest expected batch has not arrived. |
| Reference data is complete | New values need mapping. |
| Known values remain stable | A new hard-coded or unhandled value appears. |
| Data quality rules still hold | Invalid dates, duplicate keys, or out-of-range values appear. |
| Fuzzy logic has not drifted | Match rates or validation results move outside tolerance. |

### Is source data up to date?

Source data cannot always be assumed to arrive on time.

Any number of failures may delay the arrival of new data: an upstream system may be unavailable, an extract may fail, a file may not arrive, or a source team may change a schedule without warning.

A monitored assumption can check whether the latest expected data has arrived.

**Example source freshness assumption**

| Source table | Expected latest date | Actual latest date | Requires attention |
|---|---|---|---|
| `Sales.Order` | 2025-05-01 | 2025-05-01 | false |
| `Sales.Payment` | 2025-05-01 | 2025-04-28 | true |

If the query returns `Sales.Payment`, the issue needs attention. The data product may be incomplete even though the pipeline has technically run.

This assumption is especially important when multiple source systems are combined. A report may look normal while one process has updated and another has not.

### Is reference data complete?

Reference data is vital to a quality warehouse.

It enables different systems to map local values to conformed values. But reference mappings require maintenance as new source values arrive.

For example, one system may start sending a new country code that is not yet mapped.

**Example structure of `'Country code map'`**

| Source system | Source country code | Country SK |
|---|---|---:|
| Sales | AU | 1 |
| Sales | NZ | 2 |
| Sales | US | 3 |
| Shipping | AUS | 1 |
| Shipping | NZL | 2 |
| Shipping | USA | 3 |

A monitored assumption can check whether any source country codes have arrived without a mapping.

**Example assumption output**

| Source system | Source country code | Records affected |
|---|---|---:|
| Shipping | SGP | 14 |

The query should return only the values that require human attention. In this case, someone needs to decide whether `SGP` maps to an existing country record or whether the country reference data need to be extended.

### Are there unanticipated values?

Hard-coded values are sometimes unavoidable.

This is acceptable when a source column contains a small number of stable values. For example, a status column may have contained `Open`, `Closed`, and `Cancelled` for many years.

However, if a new value appears, the transformation logic may no longer be safe.

**Example status assumption**

| Source status | Records affected |
|---|---:|
| Pending review | 37 |

This assumption does not necessarily mean the pipeline is broken. It means the business process has produced a value not anticipated by the transformation. The data engineer or business owner must decide how it should be handled.

This is especially important when a transformation uses `case` logic, hard-coded mappings, or manually curated categories.

### Are there data quality issues?

Source data may contain issues from unvalidated collection.

These can include duplicate keys, dates outside expected ranges, negative values where only positive values make sense, or records that violate business rules.

In some cases, the pipeline may treat the issue to preserve analytical usefulness. For example, a future date outside the allowed range may be converted to blank and flagged.

**Example assumption output for invalid dates**

| Record ID | Source date | Issue |
|---:|---|---|
| 2 | 2300-06-15 | Date exceeds allowed future range |

Similarly, duplicate records may be removed from the main analytical table and written to a rejected-records table.

**Example assumption output for duplicate submissions**

| Submission ID | Customer ID | Submission date | Rejection reason |
|---|---|---|---|
| S1003 | C001 | 2025-04-01 | Duplicate customer submission for date |

These are monitored assumptions because the business needs to know that the issue occurred. The pipeline may be able to continue, but the underlying source issue still requires attention.

### Is there data drift?

Statistical and fuzzy logic often rely on assumptions about the distribution or pattern of input data.

These assumptions can change over time. This is commonly known as data drift.

Data engineers may encounter this when applying fuzzy patterns to extract information from free-text fields. A pattern may work well when users write notes in one style, then fail when a source form changes or users begin entering data differently.

For example, suppose a pattern extracts phone numbers from customer notes. The data engineer may monitor the proportion of extracted numbers that match known customer phone records.

**Example drift monitoring**

| Month | Notes processed | Notes with extracted phone number | Extracted numbers matching customer records |
|---|---:|---:|---:|
| 2025-01 | 12,400 | 4,820 | 86% |
| 2025-02 | 13,100 | 5,040 | 85% |
| 2025-03 | 12,850 | 4,910 | 84% |
| 2025-04 | 13,300 | 5,110 | 85% |
| 2025-05 | 13,050 | 7,900 | 61% |

The May result may indicate drift. Users may have started entering phone numbers in a new format. Another number may have started appearing near phone-like words. The customer reference table may also have changed.

A monitored assumption should return rows, periods, or segments where the statistic moves outside tolerance.

The important point is that fuzzy logic should not be treated as set-and-forget. Its assumptions must be monitored.

## Tests and assumptions together

Tests and monitored assumptions are closely related, but they protect different things.

Tests detect whether implemented logic has failed. Monitored assumptions detect whether the world has changed in a way that makes the logic unsafe.

A condition can often be expressed either as a test or as a monitored assumption by rephrasing.

For example, row counts before and after transformation should usually be expressed as tests. A discrepancy may indicate a serious error in the pipeline.

New country codes requiring annotation are better expressed as monitored assumptions. Their appearance does not necessarily mean the pipeline has failed. It means the world has produced something that requires human attention.

A useful rule of thumb is:

| Condition | Prefer | Reason |
|---|---|---|
| Critical correctness condition | Test | Failure suggests the product may be wrong. |
| Slow-moving business condition | Monitored assumption | Failure suggests human attention is needed. |
| New values or mappings | Monitored assumption | The product needs curation, not necessarily shutdown. |
| Core reconciliation or row preservation | Test | Failure suggests the transformation may have broken. |
| Statistical or fuzzy pattern stability | Monitored assumption | Failure suggests logic may need review. |

## Conclusion

Tests and assumptions accelerate delivery rather than slow it down. They reduce the cost of change. They allow data engineers to modify complex transformations with confidence. They make it safer to refactor code, adjust business logic, optimise performance, and release improvements without relying on hope.

If something is easy to test, it should be tested because the cost is low. If something is hard to test, it definitely should be tested because the logic is complex. Either way, it should be tested.

Thoughtful tests are best, but even simple tests are valuable. Many errors in data products are not profound misunderstandings. They are careless mistakes made during rapid development. Simple tests and assumptions can catch these before they reach the user.

New engineers naturally spend more time choosing patterns and building their implementation. With experience, design becomes more mechanical and rapid. Mature engineers dealing with greater complexity spend proportionately more time anticipating failure: defining tests, monitoring assumptions, and making sure that the data product will reveal when it is no longer safe.



> [!NOTE]
> **Key ideas**
>
> Data engineering is not only building the transformation that works. It is building the means by which failure becomes visible.
>
> The third principle of data engineering is to **anticipate errors**.
>
> Tests check the same result in two independent ways.
>
> Tests are strongest when expected and actual calculations are not entangled.
>
> Monitored assumptions return records that require human attention.
>
> Tests detect failures in implemented logic.
>
> Monitored assumptions detect changes that make the logic unsafe.