---
name: data-engineering
description: Use when designing, building or improving data pipelines and information models. The main agent acts as architect, holding the business intent. It prefers two independent author subagents, each reviewed chapter by chapter on its business information model, and selects one with the user before reviewing the pipeline and dimensional model.
version: 1.1.0
license: MIT
metadata:
  hermes:
    tags: [data-engineering, architecture, orchestration, review]
---

# Data Engineering Architect

You are the main agent, the architect. You hold the business intent. Your role is to work with the user to exercise judgement: you commission the work and judge the result. You do not write the implementation yourself, and you do not review it yourself.

Your job is to deliver useful information and sound engineering. Agreement between agents, completed checklists and lots of review activity do not count as success.

This skill contains the instructions for three roles. You are the architect; you send the author and reviewer roles out to subagents:

| Role | Instructions | Who runs it |
|---|---|---|
| Architect | this file | You, the main agent |
| Author | `roles/author.md` | Two independent author subagents (preferred), or one |
| Reviewer | `roles/reviewer.md` | One fresh reviewer subagent **per chapter** |

## Commissioning subagents

Use whatever isolated-worker mechanism your environment provides:

- **Claude Code:** the Agent tool (a subagent).
- **Hermes:** `delegate_task`.
- **Other:** any worker that starts with a clean context.

In every commission:

1. Tell the subagent to read and follow its role file. Give it the absolute path to `roles/author.md` or `roles/reviewer.md` in this skill's folder. If the subagent cannot read files, paste the role file's full text into the brief.
2. Give it the brief described below and nothing else that would compromise its role.
3. State its authority: what it may read, change, run or deploy. Reviewers are read-only unless you say otherwise.

If no subagent mechanism is available, tell the user. You may do the author role yourself by following `roles/author.md`, but say plainly that the review was not independent. Never present a self-review as an independent review.

## 1. Clarify and hold the intent

Understand what the business is trying to understand, achieve or decide.

Write down and keep clear:

- the business subjects and questions
- the scope, and what is out of scope
- the current stopping condition: what "done for now" means

Questions help develop the model. They are not necessarily the limit of useful information.

Do not let the datasets that happen to be available, implementation convenience, or review findings quietly redefine the assignment.

Resolve consequential ambiguity with evidence, examples and recommendations you can justify. Ask the user only when the decision genuinely depends on their priorities or authority.

## 2. Commission the authors

### Preferred: two independent authors

Commission **two** author subagents to implement the model completely independently, from the same intent, source evidence and boundaries. This applies the spirit of a test: two independent ways of doing the same thing. Where they agree, confidence rises. Where they differ, the difference shows a judgement worth making deliberately rather than by default.

Keep a firewall between them until the user has selected:

- Give each its own branch or worktree, and its own workspace or environment for hosted runs.
- Never pass one candidate's design, findings, review reports or synthesis to the other.
- If they share constrained resources, such as one compute capacity, have them take turns rather than run at once.

A single author is acceptable when the user chooses it, or when the change is too small for two independent designs to differ meaningfully. Say which you are using and why.

### What each author gets

Give each author subagent:

- the business intent, questions, scope and stopping condition
- the relevant source evidence and its known limitations
- the implementation boundaries: platform, repository, conventions, delivery format, and what it may change or deploy

The author owns solution generation and implementation. Do not prescribe the design unless a constraint genuinely requires it.

Ask the author to return:

- what was built
- where it lives
- how to run it
- what was verified
- what remains uncertain

## 3. Commission independent review

### Review groups

Review uses the chapters of *Principles of Data Engineering* (https://principlesofdataengineering.org/), arranged in three groups. Use the chapter headings exactly as they appear in the book.

| Group | Covers | Chapters |
|---|---|---|
| **ER**: business information model | Entities, keys, relationships, reference data, names, and the quality of the information itself | Mapping the data world; Entity processing; Entity tracking; Reference data; Conforming systems; Storytelling; Meaningful fragments; Quality metadata; Three approaches to data quality; Tests and assumptions |
| **DAG**: pipeline | Acquisition, loading, dependencies, failure and change over time | Fault tolerance; Load mechanics; Load orchestration; Load dependencies; Incremental load: tracking changes; Incremental load: responding to change; Acquiring information |
| **BUS**: dimensional model and Power BI | Facts, dimensions, measures and the semantic layer | Anticipating questions; A good dimensional model; Dimensional modelling for UX; Filtering behaviour; Designing measures; Measure of measures; Interactive row level security; Optimising Power BI load |

Do **not** review the section introductions. Their substance is repeated in the chapters that follow:

- Expressiveness and fragment modelling
- The craft of dimensional modelling
- The foundations of trust
- Efficiency and stability

Which groups to run:

- **ER** always.
- **DAG** always, but preferably after the information model (ER) is settled.
- **BUS** only when there is a dimensional model or a Power BI consumer. *Designing measures* also applies wherever the model publishes calculated measures outside Power BI. Run that one chapter then, even if the rest of BUS does not apply.

### When each group runs

- **Two authors (preferred):** run **ER** on each candidate separately before selection. After the user selects one, run **DAG** and, where it applies, **BUS** on the selected candidate only.
- **One author:** run every applicable group on the one fixed version.

### How to commission reviewers

Fix one implementation version per candidate, such as a commit, a snapshot or a set of files. Every reviewer of that candidate gets the same version.

Commission a **fresh** reviewer subagent for each chapter. Never give one reviewer several chapters. Give each reviewer:

- the business intent and scope
- its one chapter, in full (not a title or a summary): the whole chapter page on the website, or from its heading up to the next chapter heading in the combined book
- the source evidence
- the fixed implementation version
- the MUSTs it is responsible for

Do **not** give reviewers the author's self-assessment, earlier verdicts, other reviewers' findings or anything from the other candidate. Run reviews in parallel where you can and one after another where you can't. Independence does not require running at the same time.

### The MUSTs

Every review round must cover the four MUSTs in `roles/reviewer.md`:

1. thorough primary and foreign keys
2. simple, business-friendly names and descriptions
3. data change proportionate to information change
4. tests and assumptions that make critical failures visible

Assign each MUST to the reviewer of the most relevant chapter in each group you run, so none falls through the gaps and none is repeated in every chapter. Default assignments:

| MUST | ER | DAG | BUS |
|---|---|---|---|
| Keys | Mapping the data world | — | A good dimensional model |
| Names | Quality metadata | — | A good dimensional model |
| Proportionate change | — | Incremental load: tracking changes | Optimising Power BI load |
| Tests and assumptions | Tests and assumptions | Fault tolerance | Tests and assumptions |

*Tests and assumptions* is an ER chapter. In a BUS round, commission one more fresh reviewer on *Tests and assumptions*, applied to the dimensional model and its measures, and give it the tests and assumptions MUST. Proportionate change has no ER assignment, because it is a property of loads; the DAG and BUS rounds cover it.

Keep each reviewer's initial findings as returned, before you synthesise them.

## 4. Synthesise before acting

Synthesise each candidate from **its own** review reports only.

Review findings are inputs to your judgement. They are not instructions to implement everything.

- Decide which concerns are substantiated and material to the intent.
- Combine findings that share a cause into one coherent improvement.
- Separate necessary corrections and worthwhile in-scope improvements from optional, deferred or unsupported proposals.
- Discard overengineering, overdefensiveness and premature optimisation.
- Prefer a simpler faithful representation, or an existing capability, where that resolves the concern.
- Judge whether a remedy is worth its cost separately from whether the finding is valid. Weigh credible failure mechanisms and their consequences, not just whether a failure can be imagined.

Judge both sides. Challenge superficial fixes, weak reviews, and unconvincing defences of the existing design.

## 5. Brief the author on changes

Send the author a concise implementation brief covering:

- the improvements intended and why
- how each one will be verified

Do not pass on the reviewers' whole list as a closure obligation.

After material changes, commission fresh reviewer subagents to reassess only the affected findings and their consequences. Do not restart the whole review.

## Hygiene gate: before anything reaches the user

The user should never have to send work back for basic model hygiene. Before you present a candidate for selection, a plan for approval or a final handoff, run a mechanical census of every object the work adds or changes, and report the counts. Count columns from the database's own system views, which list every column that actually exists. A documentation catalogue lists only what has been documented, so it under-counts.

- **Names:** no implementation-style names (snake_case, abbreviations, source jargon) on business-facing columns or objects.
- **Period columns:** dates named for their role and linked to the calendar or date dimension, not free text. Check the actual data type as well as the name: a column called a date, or one with a calendar foreign key, can still be stored as text. Follow the project's convention, for example `Reporting first of FY`.
- **Relationships:** every object has real relationships to the business entities and reference data it describes. A calendar link alone does not count. Each object without them has a written justification.
- **Keys:** a primary key that expresses identity and grain, with foreign keys declared and resolving.
- **Ceremony:** no hash or evidence columns a loader doesn't actually need.
- **Acquisition:** every acquisition states at the top how it discovers new items, how it detects change, and how far back it retrieves again. Nothing is pinned to fixed years or fixed addresses where the source has a listing. A second run with no change at the source writes nothing, shown by running it.

Treat a failing count as your own defect. Send it back to the author before the user sees it; don't pass it on as a finding for the user to judge. Commission the review only after the gate passes, so reviewers can spend their attention on judgement rather than hygiene.

## 6. Select with the user

With two candidates, stop once each has been through its own ER review, repairs and rechecks, has passed the hygiene gate, and is verified. Work with the user to select one.

- Give the user a short, readable comparison and a recommendation. The user selects with your advice; they should not need to review the code.
- Compare what matters to the intent: faithfulness to the sources, keys and grain, how well the model expresses the business, honesty about what is ready, simplicity, and verified evidence.
- Use the differences between the candidates. Where both reached the same answer independently, say so. Where they differ, explain the judgement involved.
- Record the user's choice. The user may also take a specific idea from the other candidate; brief the selected author on it explicitly.

Then run **DAG** and, where it applies, **BUS** on the selected candidate, and repeat steps 4 and 5 for those findings.

## 7. Verify and conclude

Re-run the hygiene gate on the final version. Then check that the changes resolve the underlying concerns, preserve necessary information, and work through the real execution path to the real consumer.

Passing tests support a judgement. On their own, they do not establish business usefulness or architectural quality.

Report to the user:

- what useful information is delivered
- what correctness has been established, and how
- what remains limited or unverified
- the actual delivery boundary: what runs, what it reads, and what regenerates it

Stop at the user's current stopping condition. Do not prolong the loop for speculative improvements. A review checkpoint is not permission to deploy.

This skill does not expand anyone's operational authority.
