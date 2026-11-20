---
title: Steering AI agents
url: /docs/judgement-under-ambiguity/steering-ai-agents/
description: Explains how an agent skill applies the principles of this book to steer AI agents through data engineering work, using an architect, independent authors and independent reviewers.
lede: An AI agent can build quickly. Judgement still decides whether it builds information.
weight: 4
# draft: true
---

## Speed without judgement

AI agents can now write pipelines, queries, tests, and semantic models in minutes. A task that once took a week may take an afternoon.

This changes the speed of implementation. It does not change the nature of the work.

As [The six principles of data engineering](/docs/judgement-under-ambiguity/the-six-principles-of-data-engineering/) explains, the data engineer’s greatest enemy is the willingness to provide easy substitutes. An agent has that willingness without limit. Asked for a report, it will map the source, apply the stated requirements, and load a few large tables. The result may look technically correct. It is shallow curation, produced faster.

An agent does not need to be told to work harder. It needs to be steered: given the same judgement this book asks of the data engineer, and placed in a way of working where that judgement is applied and checked.

This chapter describes one way to do that: an **agent skill** published with this book.

Nothing in the skill is a new rule. Each part applies a chapter of this book.

## The data engineering skill

A skill is a folder of instructions that an AI agent loads when a task matches its purpose. Many agents, such as Claude Code, support skills written as a `SKILL.md` file with supporting files alongside it.

The data engineering skill is at version 1.0.0.

- [Download the skill](https://principlesofdataengineering.org/downloads/data-engineering-skill.zip)
- [Browse its files](https://principlesofdataengineering.org/agent-skill/data-engineering/SKILL.md)

To install it, copy the `data-engineering` folder, including `roles/`, into the agent’s skills directory. The skill’s `README.md` lists the locations for common agents.

The skill divides the work into three roles.

| Role | Instructions | Runs as |
|---|---|---|
| Architect | `SKILL.md` | The main agent. |
| Author | `roles/author.md` | Two independent subagents, or one. |
| Reviewer | `roles/reviewer.md` | One fresh subagent for each chapter of this book. |

A subagent is a separate worker that starts with a clean context. It knows only what it is given. This is what makes independent authoring and review possible.

Where no subagents are available, the skill says so plainly, rather than presenting a self-review as independent.

## Architect, authors and reviewers

The **architect** holds the business intent. It clarifies what the business is trying to understand, achieve or decide, what is in and out of scope, and what “done for now” means. It commissions the work and judges the result.

The architect does not implement the work, and it does not review it.

This is [owning the business intent](/docs/judgement-under-ambiguity/working-with-stakeholders/#own-the-business-intent), given a role of its own. An agent that both builds and judges its own work is inclined to confirm it. An agent that holds only the intent can judge the work against that intent, not against the effort that went into it.

The **author** owns the implementation. Its aim is to create a useful model of the business, not a cleaned copy of the source data. Its instructions state the standard plainly: an implementation is not justified because it works. It is justified because, in light of the business intent, the author cannot identify a better way to achieve the same purpose.

The author works by the six principles. They are written into its instructions as disciplines of judgement, not as categories of machinery to build.

The **reviewer** examines one chapter of this book against the implementation. It is read-only. It reports what it finds, and the architect decides what to do.

## Three operational phases

The skill arranges the chapters of this book into three groups. Each group is a phase of the work, reviewed against the chapters written for that phase.

| Phase | Covers | Chapters drawn from |
|---|---|---|
| **ER**: business information model | Entities, keys, relationships, reference data, names, and the quality of the information itself. | Creating information and Quality & reliability, except Fault tolerance |
| **DAG**: pipeline | Acquisition, loading, dependencies, failure, and change over time. | Efficient & stable pipeline, except Optimising Power BI load, with Fault tolerance |
| **BUS**: dimensional model and Power BI | Facts, dimensions, measures, and the semantic layer. | Presenting insights, with Optimising Power BI load |

ER always applies, because every piece of work creates information. DAG applies whenever the work acquires or loads data. BUS applies only when there is a dimensional model or a Power BI consumer.

The phases follow the order of the work: what the business world is, how information moves, and how it is presented.

The section introductions are not reviewed. Their substance is repeated in the chapters that follow.

## Independent review

Each chapter is reviewed by its own **fresh** reviewer. One reviewer never covers several chapters.

Each reviewer is given the business intent, the source evidence, its one chapter in full, one fixed version of the implementation, and the MUSTs it is responsible for. Every reviewer of that implementation receives the same version.

No reviewer is given the author’s self-assessment, earlier verdicts, other reviewers’ findings, or anything from another candidate.

These restrictions matter.

A reviewer given several chapters will skim them. A reviewer given a chapter’s title will apply what it already believes the title means. A reviewer who has read the author’s explanation will tend to judge the explanation rather than the work. A reviewer who has seen another reviewer’s findings will tend to agree with them.

Independence is what gives a review its value. This is the same idea as [checking the same result two ways](/docs/quality-reliability/tests-and-assumptions/#tests-checking-the-same-result-two-ways). A second check is only useful if it can disagree with the first.

The reviewer is also told that a chapter is a way of investigating, not a list of requirements. It may reveal a problem, suggest an improvement, support the existing design, or call for no change. All are legitimate outcomes. A reviewer that must always find something will manufacture findings.

## Dual authors

By preference, the architect commissions **two** authors to build the same thing independently, from the same intent and source evidence.

The two authors are kept apart. Each has its own branch and its own environment. Neither sees the other’s design, reviews or findings until the user has chosen.

This applies the spirit of a test: two independent ways of doing the same thing.

Where the two authors agree, confidence rises. Where they differ, the difference marks a judgement worth making deliberately, rather than by default.

For example, suppose both authors model `Cake.InspectionResult`. One keys it by cake. The other keys it by cake and inspection criterion, since one cake is inspected against several criteria. Neither is wrong on its face. The difference exposes a question of grain that a single author would have settled silently.

Each candidate is reviewed on the ER phase separately. The architect then works with the user to select one, giving a short, readable comparison and a recommendation. The user selects with the architect’s advice. They should not need to read the code.

This is [gathering around the solution](/docs/judgement-under-ambiguity/working-with-stakeholders/#gather-around-the-solution). Two concrete candidates give the user something real to react to. The user may also take a specific idea from the candidate that was not chosen.

Only the selected candidate goes on to the DAG and BUS phases.

A single author is acceptable when the user chooses it, or when the change is too small for two designs to differ meaningfully.

## Synthesis before acting

Review findings are inputs to the architect’s judgement. They are not a checklist to be completed.

A thorough review of a substantial piece of work will always produce findings. Some are material. Some share a cause. Some propose machinery for cases that are merely imaginable. Implementing all of them is a wholesale response where the principle asks for a proportionate one.

The architect therefore synthesises before acting:

- decide which concerns are substantiated and material to the intent;
- combine findings that share a cause into one improvement;
- separate necessary corrections from optional or unsupported proposals;
- discard overengineering, overdefensiveness, and premature optimisation;
- judge whether a remedy is worth its cost, separately from whether the finding is valid.

Combining findings that share a cause is [diagnosing the root cause](/docs/judgement-under-ambiguity/when-things-go-wrong/#step-3-diagnose-the-root-cause). Several findings about awkward joins, repeated conditions, and slow loads may all point to one poorly chosen grain.

The architect then briefs the author on the intended changes and how each will be verified. After material changes, fresh reviewers recheck only the affected findings. The review does not start again.

This is judgement under ambiguity, which is the subject of this section. Agents can multiply findings without limit. Only judgement decides which of them matter.

## The hygiene gate

Before any work reaches the user, and before review begins, the architect runs a **hygiene gate**. It is a mechanical count across every object the work adds or changes.

| Check | What it asks |
|---|---|
| Names | Are business-facing names free of implementation-style names and abbreviations? |
| Period columns | Are dates named for their role, linked to the calendar, and stored as dates? |
| Relationships | Does every object relate to the business entities and reference data it describes? |
| Keys | Does every object have a primary key that expresses identity and grain, with foreign keys that resolve? |
| Ceremony | Are there hash or evidence columns the load does not actually need? |
| Acquisition | Does every acquisition state how it discovers new items, detects change, and how far back it retrieves again? Does a second run with no change write nothing? |

The counts are taken from what actually exists, not from what has been documented.

The gate exists so that the user never has to send work back for basic hygiene, and so that reviewers spend their attention on judgement rather than on counting names. A failing count is the architect’s own defect. It is returned to the author before the user sees it.

Each check applies a chapter: names from [Quality metadata](/docs/quality-reliability/quality-metadata/), keys from [Mapping the data world](/docs/creating-information/mapping-the-data-world/#primary-key), and acquisition from [Acquiring information](/docs/efficient-stable-pipeline/acquiring-information/).

## The MUSTs

Every round of review covers four **MUSTs**. They are the disciplines most easily skipped and most costly to miss.

| MUST | What the reviewer examines |
|---|---|
| Keys | Primary and foreign keys, checked against the data, not the declarations. |
| Names and descriptions | Simple, business-friendly names and descriptions on the actual objects. |
| Proportionate change | Stored changes that correspond to genuine information change, verified by running. |
| Tests and assumptions | Critical failures made visible, with monitors that can actually fire. |

Each MUST is assigned to the reviewer of the most relevant chapter in each phase where it applies. By default, these are:

| MUST | ER | DAG | BUS |
|---|---|---|---|
| Keys | Mapping the data world | — | A good dimensional model |
| Names and descriptions | Storytelling | — | Dimensional modelling for UX |
| Proportionate change | Entity processing | Incremental load: responding to change | Optimising Power BI load |
| Tests and assumptions | Tests and assumptions | Fault tolerance | Designing measures |

None falls through the gaps, and none is repeated in every review.

## Tools for agents

To work this way, agents need control of the platform they are building on.

An author must be able to build what it designed, load it, and inspect the result. A reviewer must be able to query the actual data, run the tests, and provoke a monitor to see whether it fires. To verify proportionate change, an agent must run the load twice and observe that the second run writes nothing. Reading the code is not enough.

How much of this is possible depends on the platform.

Many data platforms are fragmented. One tool handles SQL transformation. Another runs Python in browser notebooks. A third deploys the semantic model. Each gives an agent a view of one part of the work, and none lets it run the whole pipeline and see what a user would see. An agent in this position must guess at the behaviour of the parts it cannot run.

It helps when agents have a desktop command-line interface that gives them feedback the way a user gets it: build, run, test, and query, with results the agent can read. Independent authors also need environments of their own, so that one candidate’s runs do not disturb the other’s.

Weaver is one platform designed this way. See [Using Weaver with AI agents](https://docs.weaverstack.dev/reference/ai-agents/).

## Conclusion

AI agents make implementation fast. As [Construction planning](/docs/judgement-under-ambiguity/construction-planning/#conclusion) observes, success depends less on development as development becomes routine. With agents, this is more true, not less.

What remains is judgement: holding the business intent, choosing between candidate designs, deciding which findings matter, and knowing when the work is done for now.

The data engineering skill does not replace that judgement. It gives the agent a way of working in which the principles of this book are applied, checked independently, and weighed before anything changes.

> [!NOTE]
> **Key ideas**
>
> An AI agent can build quickly. Judgement still decides whether it builds information.
>
> The data engineering skill applies the principles of this book to steer agents. Nothing in it is a new rule.
>
> The architect holds the business intent, commissions the work, and judges it. It does not implement or review.
>
> The work is reviewed in three phases: the business information model, the pipeline, and the dimensional model.
>
> Each chapter is reviewed by a fresh, independent reviewer, working on the same fixed version.
>
> Two independent authors are a test: two ways of doing the same thing.
>
> Review findings are inputs to judgement, not a checklist.
>
> A hygiene gate checks the basics mechanically, so review can focus on judgement.
>
> Agents need control of the platform to build, run, test, and query, and to see the work as a user would.
