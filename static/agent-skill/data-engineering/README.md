# Data engineering skill

One agent skill that runs an architect–author–reviewer loop for data-engineering work. It is grounded in *Principles of Data Engineering* (https://principlesofdataengineering.org/).

The main agent loads the skill and acts as the architect. It sends the author and reviewer roles out to subagents, giving each one its role file:

| File | Role | Runs as |
|---|---|---|
| `SKILL.md` | Architect: holds the business intent, commissions the author and reviewers, synthesises findings, and decides what is done | Main agent |
| `roles/author.md` | Author: designs and implements pipelines and information models | Two independent subagents (preferred), or one |
| `roles/reviewer.md` | Reviewer: independently reviews one book chapter against four MUSTs: keys, names, proportionate change, tests and assumptions | One fresh subagent per chapter |

## Flow

1. The architect clarifies the intent, scope and stopping condition.
2. The architect commissions two author subagents to build the model independently (preferred), or one. Two independent builds are a test: two ways of doing the same thing.
3. For each candidate, the architect fixes a version and commissions one fresh reviewer per chapter of the **ER** group (business information model). Reviewers don't see each other's findings, the author's self-assessment or the other candidate.
4. The architect synthesises each candidate from its own reviews, briefs its author on material changes, and has fresh reviewers recheck only the affected findings.
5. The architect and the user select one candidate.
6. The selected candidate is reviewed on the **DAG** group (pipeline) and, where there is a dimensional model or Power BI consumer, the **BUS** group, then synthesised, repaired and rechecked.
7. The architect verifies the result against the real execution path and reports.

Section introductions are not reviewed. `SKILL.md` lists the chapters in each group and the default MUST assignments.

The architect does not implement or review the work itself. If the environment has no subagents, it says so rather than presenting a self-review as independent.

## Install

Copy the `data-engineering` folder, including `roles/`, into your agent's skills directory:

- **Claude Code:** `~/.claude/skills/` for all projects, or `<repo>/.claude/skills/` for one repository.
- **Hermes:** your Hermes skills directory.
- **Others:** any agent that supports the `SKILL.md` format.

Subagents are commissioned through whatever the platform provides: the Agent tool in Claude Code, `delegate_task` in Hermes. Each subagent is pointed at its role file. If it can't read files, the architect pastes the role file into its brief.

## Licence

MIT
