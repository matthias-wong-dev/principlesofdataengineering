---
title: Sound judgement
weight: 4
draft: true
---

Sound judgement is the defining capability of a mature data engineer. It is tempting to think of data engineering as a sequence of technical tasks: building pipelines, fixing errors, optimising performance, and integrating systems. In practice, these tasks are secondary. What distinguishes effective engineers is not how quickly they act, but where they act. Sound judgement is the ability to recognise at what level a problem should be addressed — whether a situation calls for surface correction, structural repair, or a reconsideration of what "good" even means. It is exercised continuously, not only when something is visibly broken. For this reason, troubleshooting is not a special activity reserved for failures. It is the most explicit expression of a posture that pervades the entire discipline. The same judgement used to diagnose a broken pipeline is used when deciding how to model an entity, where to aggregate information, or whether a system should be conformed at all. This chapter presents a simple diagnostic framework that makes sound judgement explicit. This framework defines the final principle of data engineering—instead of treating symptoms, diagnose root cause.

## A diagnostic framework for sound judgement

Sound judgement can be practised deliberately by distinguishing four stages that are often confused: Stage Diagnostic question Symptom What is observably wrong? Trigger What event caused the symptom to surface? Root cause What structural violation allows this to recur? Final effect What outcome must hold for the system to be genuinely fixed? This framework does not prescribe solutions. Its purpose is to discipline attention. It prevents engineers from reacting to what is loud instead of addressing what is consequential. A simple example Consider someone learning piano.

- Symptom: the playing sounds offbeat.

- Trigger: the finger is lifted too late before the next note.

- Root cause: the learner relies on playing by ear rather than learning the

mechanics of timing and articulation.

- Final effect: the piece is played according to the intended rhythm, not merely

"close enough" to how it should sound. Two observations matter. First, the trigger is not the root cause. The trigger explains how the symptom occurs, not why it persists. Second, the final effect is not the absence of mistakes. It is the presence of the intended outcome. Sound judgement lies in acting at the level that prevents recurrence, not merely silences error. Step 1: Symptoms — seeing clearly before acting The first act of sound judgement is to systematically canvas the symptoms, rather than reacting to the first issue reported. Stakeholders describe what they see. They do not describe the full boundary of failure. Beginning work from a single reported symptom allows the reporting channel to define the problem — and that definition is almost always incomplete. At this stage, interpretation is a liability. The task is mechanical observation. In medicine, uncertainty is met with vital checks. In data systems, the equivalent is to examine surface health before forming explanations. Typical symptom canvassing includes:

- If one report is broken, are others broken?

- If one metric is wrong, are related metrics wrong?

- If a domain disappears, did the underlying rows disappear or only their

classification?

- Did row counts change? Did distributions shift? Did null rates spike?

- Did upstream pipelines succeed? Did downstream consumers fail?

Jumping ahead at this stage is a failure of judgement. Engineers tend to do so for two reasons:

- pattern-matching based on past experience

- taking the reported symptom as a complete description

Both lead to work that is precise but misdirected. Sound judgement at this stage consists in restraint. Seeing clearly comes before acting decisively.

Step 2: Triggers — locating the point of exposure The second act of sound judgement is to identify the trigger — the event that caused the symptom to surface. Triggers are time-bound and concrete. They narrow the search space and provide orientation. Common triggers in data engineering include:

- schema changes in source systems

- new or invalid records entering a load

- code changes or refactors

- infrastructure or platform migrations

- permission or security changes

- changes in load ordering or scheduling

Triggers are useful because they are often discoverable, and because they sometimes allow temporary containment: rollbacks, bypasses, or delayed execution. However, sound judgement requires a strict distinction: A trigger explains when a symptom appeared. A root cause explains why it can reappear. Treating the trigger as the cause leads to fragile systems that fail again under different conditions. Step 3: Root causes — acting at the level that matters The third act of sound judgement is to diagnose the root cause. Root causes explain recurrence. They are structural violations that allow different triggers to produce the same class of symptom. Root cause diagnosis may be:

- Theoretical: reading the system and identifying what must be true for the failure

to occur

- Experimental: isolating variables through controlled tests

Both require skill. Theoretical diagnosis depends on structural understanding. Experimental diagnosis depends on technical competence and disciplined inquiry. A useful rule is:

Root causes violate core principles that define the ideal system. Triggers merely activate those violations. In data engineering, recurring root causes include:

- incorrect or ambiguous grain

- missing, unstable, or misused keys

- semantic mismatches hidden behind identical column names

- wide tables that collapse unrelated concepts

- implicit dependencies on ordering, timing, or existence

- weak business processes that produce unreliable identity

- compounded logic that mixes extraction, transformation, and aggregation

Two engineers may observe the same symptom and trigger. One applies a patch. The other reshapes the system. The difference is not effort, but judgement. Sound judgement is the willingness to act where the system is wrong, not merely where it is noisy. Step 4: Final effect — knowing when you are done Between diagnosing root cause and completing work lies the act of applying a fix. Fixes vary: containment, refactoring, redesign, or process change. Regardless of the fix, the final act of sound judgement is to check the final effect. This includes:

- visual validation: not "does the code run", but "are the outputs correct"

- environment validation: behaviour across development, pre-production, and

production

- end-to-end validation: whether the information now supports the intended

decision A critical rule applies: The final effect is not the absence of the symptom. Error suppression creates silence, not correctness. Silence is often mistaken for success, until the failure reappears elsewhere. Knowing the final effect is difficult because it requires seeing what "good" should be. Engineers often fail to recognise slow systems because they do not know what fast

systems look like. They fail to recognise weak models because they do not know what expressive models look like. In data engineering, the final effect is always the same: The business receives the information it needs to make the decision. Pipeline success, test success, and error absence are necessary — but they are not the end.

## Sound judgement throughout data engineering

Sound judgement is not exercised only when something breaks. It is present throughout the discipline of a data engineer:

- Expressiveness:

o Symptom-level response: rename columns or add documentation when reports confuse users. o Root-cause response: reshape the model so business meaning is explicit in its structure.

- Fragment modelling:

o Symptom-level response: patch special cases into existing tables as complexity grows. o Root-cause response: extract independent fragments and isolate responsibilities.

- Reference data and conformance:

o Symptom-level response: reconcile mismatched numbers in reports. o Root-cause response: introduce shared reference data and apply it consistently.

- Aggregation and grain:

o Symptom-level response: simplify visuals or add filters when reports are slow or inconsistent. o Root-cause response: aggregate correctly in the pipeline at a grain aligned with decisions. In each case, nothing is "broken" in an obvious sense. Yet judgement is still required. Mature engineers recognise these situations early and act at the level that prevents future failure.

## Conclusion

Sound judgement is the ability to act at the right level of abstraction, at the right time, for the right reason. The diagnostic framework introduced here makes that judgement explicit:

1. Canvas the symptoms

2. Identify the trigger

3. Diagnose the root cause

4. Check the final effect

Common failures arise from:

- acting on symptoms without understanding scope

- mistaking triggers for causes

- equating silence with success

The goal is not to avoid problems. It is to address them at the level where they stop recurring. Thus, instead of treating the symptom, diagnose the root cause. Sound judgement is not a talent. It is a discipline — and it is the thread that runs through all effective data engineering work.
