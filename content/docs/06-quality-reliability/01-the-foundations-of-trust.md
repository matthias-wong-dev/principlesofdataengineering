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

Because data is captured by process, it is never a perfect copy of the world. It is an imperfect projection of the business world into the data world.

Data quality issues arise from the gap between the business world and its projection into the data world.

For example, key information required for decisions may not be captured. It may be captured in free-text format. It may be stored inconsistently across systems. It may be captured at the wrong grain. It may exist in the business process but not in a form the data product can use.

When business users encounter these gaps, they experience a mismatch between the data product and the business world they already know. In many cases, this means they cannot trust the product for decision-making.

No amount of blaming the source system changes this reality. From the business’s point of view, the product simply cannot be used.

In this perspective, one of the data engineer’s jobs is to close the gap left by the projection, to the satisfaction of the decision-maker. This is how the data engineer adds to data quality.

Quality concerns the projection itself. Reliability concerns what happens to that projection as it moves through the pipeline.

Beyond the imperfections of the projection itself, the mechanical processes of a data pipeline may introduce further errors.

An example is schema change. Users may experience this when entire tables become empty or when inconsistencies arise between business processes.

On some occasions, this can be disastrous. For example, if the cost forecast has been updated to the latest month but the actual expenditure has not, the final reconciliation may show an unacceptable discrepancy.

The issue is not business meaning. The issue is mechanical reliability: the pipeline has produced a data product whose parts are no longer aligned.

The data engineer must build a pipeline that minimises the likelihood and impact of such errors.

Reliability is the discipline of making the data product stable against predictable forms of breakage.

## Trust requires both

Quality and reliability answer different questions.

| Foundation | Question | User failure mode |
|---|---|---|
| Quality | Does this data product represent the business reality well enough for the decision? | “This does not match the world I know.” |
| Reliability | Does the pipeline consistently produce the data product without hidden breakage? | “This number might be broken.” |

Either failure destroys trust.

A high-quality model that refreshes unpredictably cannot be trusted. A reliable pipeline that faithfully reproduces unusable source-system gaps cannot be trusted either.

Quality keeps users from guessing what the data means. Reliability keeps users from guessing whether the data worked.

Together, they are the foundations of trust.


## The third principle: anticipate errors

This section introduces the third principle of data engineering: anticipate errors.

This principle follows from the nature of quality and reliability. Data is an imperfect projection of complex reality, and pipelines are mechanical systems that operate in a changing world. 

A trustworthy data product therefore cannot depend on everything continuing as expected. The data engineer must anticipate errors.


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