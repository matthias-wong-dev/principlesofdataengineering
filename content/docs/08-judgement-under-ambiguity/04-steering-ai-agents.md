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

As [The six principles of data engineering](/docs/judgement-under-ambiguity/the-six-principles-of-data-engineering/) explains, the data engineer’s greatest enemy is the willingness to provide easy substitutes. An agent has that willingness without limit.

It does not need to be told to "double-check its work" more. It needs to be steered: given the same judgement this book asks of the data engineer, and placed in a way of working where that judgement is applied and checked.

This chapter describes one way to do that: an **agent skill** published with this book.

## The tendencies of AI agents

AI agents learn from the code that already exists in its training data. Most of that code is not good data engineering. More importantly, most of the training is done locally — defensive reaction to local issues in the data, rather than from the perspective of the large information model. 

Four tendencies stand out.

| Tendency | What it looks like |
|---|---|
| Minimal transformation | Unless actively prompted or given specific rules, agents apply the absolute minimum transformation; thus preserving issues rather than re-arranging the data in a useful way.|
| Overengineering for needless caution | Agents go out of the way to add defensive mechanisms and conservative preservation of information. They treat imaginary edge-cases as equally important, and patch over problems rather than tackling the root cause. |
| A deluge of caveats | Agents bury every metadata description under caveats and qualifications — often saying what something *is not* rather than what it *is*. Agent-written metadata descriptions are barely readable for the business user. |
| Missing the bigger picture | Agents are unable to anchor local decisions against the business intent, thus creating a model that leaves the user to do all the work when querying. Agents-made pipelines are often fragile for the long horizon. |

Each tendency is a familiar substitute for judgement.

Minimal transformation is an escape from making design decisions. From the agent's point-of-view, there is no reason why it should push forward and re-imagine the data from the business perspective, as opposed to leaving the data as it found it. 

Overengineering for needless caution look like diligence. But they mistake activity for quality. A monitor that fires every day becomes [background noise](/docs/quality-reliability/fault-tolerance/#containing-failure), and machinery built for an imagined case is code that must still be understood, tested, and maintained.

A deluge of caveats looks like honesty. But a limitation that matters is lost among the ones that do not. As [Quality metadata](/docs/quality-reliability/quality-metadata/) explains, an important limitation should be stated in the context of how the information is used.

Missing the bigger picture is innate to the way agents are trained. Agents are trained on local code-edits, and in this context, the reviewer's global criterion are not often supplied. And when vast amount of the training data is repairing local issues, then this, rather than the business intent, becomes the driver of design.

The net outcome of all four is exactly source-in-source-out. The source is copied, then wrapped in machinery, defensive checks, and qualifications. It looks like more work. It is no more information.

None of these should be a surprise and blame the tool. That's not what they are designed for. Nor should we expect the situation to improve with default frontier models. There is no reason to believe that commercial models will teach AI agents to take initiative on design decisions anchored to business intent.

However, out of the box, these tendencies make an agent close to unusable for serious data engineering. The work looks complete, and much of the user’s time goes into stripping out what is not needed and asking for what is missing.

The tendencies are not corrected by instruction alone. They are corrected by giving the agent the principles that tell good work from its substitutes, and by checking its work against them independently. This combines the strengths of a data engineer's judgement with the strengths of an AI agent to write code, metadata, and diligent checks that would otherwise be too tedious to be practical.

The data engineering skill is one way to steer an agent.

## The data engineering skill

A skill is a folder of instructions that an AI agent loads when a task matches its purpose. Many agents, such as Claude Code, support skills written as a `SKILL.md` file with supporting files alongside it.

The data engineering skill is at version 1.1.0.

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


## Architect, authors and reviewers

The **architect** [holds the business intent](/docs/judgement-under-ambiguity/working-with-stakeholders/#own-the-business-intent). Its role is to work with the user to exercise judgement. It clarifies what the business is trying to understand, achieve or decide, what is in and out of scope, and what “done for now” means. It commissions the work and judges the result.

The architect does not implement the work, nor does it actively review it. 

By separating the architect from the author and reviewer, it is able to hold the user's intent in its memory, and can work with the user on making design decisions, rather than letting vast amount of code crowd out the token context.

The **author** owns the implementation. Its aim is to create a useful model of the business, not a cleaned copy of the source data. Its skills instructions state the standard upfront: an implementation is not justified because it works. It is justified because, in light of the business intent, the author cannot identify a better way to achieve the same purpose.

The author works by the six principles. With an index in the skills file for relevant chapter for specific problems and patterns.

By default, the author would still write source-in-source-out, defensive code. The review is where this is corrected. 

The **reviewer** examines one chapter of this book against the implementation. It is read-only. An independent subagent is started for each relevant chapter of the book, so the code is reviewed against that particular concern, whether it is metadata, or fault tolerance. The architect collects these reviews for synthesis.

## Three operational phases

The skill arranges the chapters of this book into three groups. Each group is a phase of the work, reviewed against the chapters written for that phase.

| Phase | Core artefact | Covers | Chapters drawn from |
|---|---|---|---|
| **ER** | Business information model | Entities, keys, relationships, reference data, names, and the quality of the information itself. | Creating information and Quality & reliability, except Fault tolerance |
| **DAG** | Pipeline | Acquisition, loading, dependencies, failure, and change over time. | Efficient & stable pipeline, except Optimising Power BI load, with Fault tolerance |
| **BUS** | Dimensional model and Power BI | Facts, dimensions, measures, and the semantic layer. | Presenting insights, with Optimising Power BI load |

ER and DAG always apply. It is preferable to settle the information model first, because the pipeline follows from overall design and not the other way around. BUS applies only when there is a dimensional model or a Power BI consumer.

## Independent review

Each chapter is reviewed by its own **fresh** reviewer. One reviewer never covers several chapters.

Each reviewer is given the business intent, the source evidence, its one chapter in full, one fixed version of the implementation, and the MUSTs it is responsible for. No reviewer is given the author’s self-assessment, earlier verdicts, other reviewers’ findings, or anything from another candidate.

The review chapter is a guide for the agent as to "what to look for" — metadata, efficiency, and so on.This is why each chapter needs an independent agent. An agent using multiple chapters will struggle to hold everything in context. Over time, important review criteria will be missed.

Moreover, independent reviews supply redundancies, as explained in [Tests and assumptions](/docs/quality-reliability/tests-and-assumptions/#tests-checking-the-same-result-two-ways). The same issue may be caught by multiple reviewers.


## Synthesis before acting

On the other hand, the reviewer will focus locally on its issues, treating them as the most paramount. 

Some are material. Some share a cause. Some propose machinery for cases that are merely imaginable. 

The architect therefore synthesises before acting:

- decide which concerns are substantiated and material to the intent;
- combine findings that share a cause into one improvement;
- separate necessary corrections from optional or unsupported proposals;
- discard overengineering, overdefensiveness, and premature optimisation;
- judge whether a remedy is worth its cost, separately from whether the finding is valid.

Combining findings that share a cause is [diagnosing the root cause](/docs/judgement-under-ambiguity/when-things-go-wrong/#step-3-diagnose-the-root-cause). Several findings about awkward joins, repeated conditions, and slow loads may all point to one poorly chosen grain.

The architect then briefs the author on the intended changes and how each will be verified. After material changes, fresh reviewers recheck only the affected findings. The review does not start again.

## Independent authors

By preference, the architect commissions **two** authors to build the same thing independently, from the same intent and source evidence.

The two authors are kept apart. Each has its own branch and its own environment. Neither sees the other’s design, reviews or findings until the user has chosen.

This applies the spirit of a test: two independent ways of doing the same thing.

Where the two authors agree, confidence rises. Where they differ, the difference marks a judgement worth making deliberately, rather than by default.

For example, suppose both authors model `Cake.InspectionResult`. One keys it by cake. The other keys it by cake and inspection criterion, since one cake is inspected against several criteria. Neither is wrong on its face. The difference exposes a question of grain that a single author would have settled silently.

Each candidate is reviewed on the ER phase separately. The architect then works with the user to select one, giving a short, readable comparison and a recommendation. The user selects with the architect’s advice. They should not need to read the code.

Only the selected candidate goes on to the DAG and BUS phases.

This also applies the same principle of doing the same work twice, independently, as a way of testing.

## The hygiene gate

Before any work reaches the user, and before review begins, the architect runs a **hygiene gate**. It is a mechanical count across every object the work adds or changes.

| Check | What it asks |
|---|---|
| Names | Are business-facing names free of implementation-style names and abbreviations? |
| Relationships | Does every object relate to the business entities and reference data it describes? |
| Keys | Does every object have a primary key that expresses identity and grain, with foreign keys that resolve? |
| Ceremony | Are there hash or evidence columns the load does not actually need? |
| Acquisition | Does every acquisition state how it discovers new items, detects change, and how far back it retrieves again? Does a second run with no change write nothing? |

The counts are taken from what actually exists, not from what has been documented.

The gate exists so that the user never has to send work back for basic hygiene, and so that reviewers spend their attention on judgement rather than on counting names. These may change from site to site.

## Tools for agents

To work this way, agents need control of the platform they are building on.

An author must be able to build what it designed, load it, and inspect the result. A reviewer must be able to query the actual data, run the tests, and provoke a monitor to see whether it fires. To verify proportionate change, an agent must run the load twice and observe that the second run writes nothing. Reading the code is not enough.

How much of this is possible depends on the platform.

Many data platforms are fragmented. One tool handles SQL transformation. Another runs Python in browser notebooks. A third deploys the semantic model. Each gives an agent a view of one part of the work, and none lets it run the whole pipeline and see what a user would see. An agent in this position must guess at the behaviour of the parts it cannot run.

It helps when agents have a desktop command-line interface that gives them feedback the way a user gets it: build, run, test, and query, with results the agent can read. Independent authors also need environments of their own, so that one candidate’s runs do not disturb the other’s.

Weaver is one platform designed this way. See [Using Weaver with AI agents](https://docs.weaverstack.dev/reference/ai-agents/).

## Data engineering in the world of AI

In the world of AI, the data engineer may seem redundant. An agent writes code faster than any person.

But the data engineer is redundant only if data engineering is writing code to move data from A to B.

It is not. As [What is data engineering?](/docs/foundations/what-is-data-engineering/) set out at the start of this book, data engineering is an activity in which business intent is applied to data to create first information, then insight. Code is how that work is expressed. It was never the work itself. 

This is why the book has focused on principles rather than tools. **Expressive entities**, **meaningful fragments**, **anticipate errors**, **proportionate change**, **illuminate ambiguity**, and **root cause** were true before AI agents, and they remain true now. 

Instead, coupled with AI agents, a modern data engineer can do far more than before. One engineer can explore several designs, build them in parallel, and have each checked independently, in the time it once took to build one.

But only if the engineer inhabits the principles.

Steered by an engineer who knows what good information looks like, an agent can build it quickly. Steered by an engineer who does not, it produces shallow curation at a scale no team could produce by hand. 

> [!NOTE]
> **Key ideas**
>
> An AI agent can build quickly. Judgement still decides whether it builds information.
>
> Out of the box, AI agents tend toward minimal transformation, overengineering, needless caution, a deluge of caveats, and misses the bigger picture.
>
> The data engineering skill applies the principles of this book to steer agents. 
>
> The skill divides into three roles — architect, author, reviewer. 
>
> The architect holds the business intent and works with the user to exercise judgement. It does not implement or review. 
>
> The author implements the code, with index to relevant chapters of patterns. Dual authors are recommended.
>
> The reviewer takes a relevant chapter of the book and reviews the author's code accordingly. A fresh agent is started for each chapter. These are given to the architect to synthesise before implementaiton.
>
> In the world of AI, sound judgement by mature data engineers are more important than ever before.
