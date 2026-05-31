---
title: The foundations of trust
url: /docs/quality-reliability/the-foundations-of-trust/
description: Introduces quality and reliability as the conditions that make data products trustworthy for decision-making.
lede: Quality and reliability are the foundations of trust in a data product.
weight: 1
# draft: true
---

## Quality and reliability

Data is a fragment of reality captured by process.

Because of this, data is an [imperfect projection](/docs/foundations/what-is-data/) of the business world into the data world. Data quality issues arise from the gap between the business world and this projection.

For example, key information required for decisions may not be captured. It may be captured in free-text format. It may be captured at the wrong grain. 

When business users encounter these gaps, they experience a mismatch between the data product and the business world they already know. In many cases, this means they cannot trust the product for decision-making.

No amount of blaming the source system changes this reality. From the business’s point of view, the product simply cannot be used.

In this perspective, one of the data engineer’s jobs is to close the gap left by the projection, to the satisfaction of the decision-maker. This is how the data engineer adds to data **quality**.

Beyond the imperfections of the projection itself, the mechanical processes of a data pipeline may introduce further errors.

An example is schema change. Users may experience this when entire tables become empty or when inconsistencies arise between business processes.

On some occasions, this can be disastrous. For example, if the cost forecast has been updated to the latest month but the actual expenditure has not, the final reconciliation may contain an unacceptable discrepancy. However, there may be no obvious signs of such an error.

The issue is not with the source data, but with mechanical **reliability**: the pipeline has produced a data product whose parts are no longer aligned and has nothing to signal this divergence.

Reliability is the discipline of making the data product stable against predictable forms of breakage.

## Trust requires both

Quality keeps users from guessing what the data means. Reliability keeps users from guessing whether the output worked.

When both are available, users can use the product without second-guessing. Thus, quality and reliability are the foundations of trust.


| Foundation | Question | User failure mode |
|---|---|---|
| Quality | Does this data product represent the business reality well enough for the decision? | “This does not match the world I know.” |
| Reliability | Does the pipeline consistently produce the data product without hidden breakage? | “This number might be broken.” |


## The third principle: anticipate errors

This section introduces the third principle of data engineering: anticipate errors.

This principle follows from the nature of quality and reliability. Data is an imperfect projection of complex reality, and pipelines are mechanical systems that operate in a changing world. 

Because of these changes, a trustworthy data product cannot depend on everything continuing as expected. The data engineer does not stop with what works now, but anticipate errors that may occur.


## Key ideas

> [!NOTE]
> **Key ideas**
>
> Trust is produced when a data product is fit for decision.
>
> Quality means the data product represents business reality well enough for its intended use.
>
> Reliability means the pipeline consistently produces the data product without hidden failure.
>
> Quality keeps users from guessing what the data means.
>
> Reliability keeps users from guessing whether the data worked.
>
> The third principle of data engineering is to anticipate errors.