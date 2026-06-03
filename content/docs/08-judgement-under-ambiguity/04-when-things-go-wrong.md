---
title: "When things go wrong"
url: /docs/judgement-under-ambiguity/when-things-go-wrong/
description: Explains why data engineering is always troubleshooting and how mature engineers diagnose symptoms, triggers, root causes, and final effects.
lede: All data engineering is troubleshooting.
weight: 4
# draft: true
---

## Things are already wrong

Other engineering disciplines, such as bridge-building, are primarily constructive. A crack in the bridge is an exception, not the rule.

Data engineering is fundamentally different.

The central premise of data engineering is that:

> Data is a fragment of reality captured by process.

The data world is an imperfect projection of the business world, which the data engineer reshapes in light of intent.

This means that the discipline, while it has elements of creativity and construction, is reconstructive from the very beginning.

In this sense, troubleshooting is not merely something that happens when the craft goes wrong. It is a concentrated form of the craft itself.

What follows is a framework for troubleshooting failures. This explicit framework is necessary because production failures are real, and data engineers need a structured approach to stay calm and systematically resolve them.

But a production failure is only the clearest instance of a wider discipline. It is a moment when the engineer’s judgement is tested under pressure. In practice, all data engineering involves the same movement: seeing where and how the recorded data became misaligned with business intent, and then deciding where to intervene.

The sixth and final principle of data engineering is this:

> Instead of stopping at the symptoms, diagnose the root cause.

This applies to the whole book. Troubleshooting a production failure is simply a crystallised instance of the discipline.

## The four steps to troubleshooting

When a data product fails, there is pressure to address it immediately using the quickest means possible.

This often creates greater trouble. Large data pipelines are typically so complex that the first solution that comes to mind is often the wrong one, and applying it can create compounding issues.

Instead, the data engineer must stay calm and understand the situation. A practical diagnosis moves through four steps:

1. Canvass the symptoms.
2. Identify the trigger.
3. Diagnose the root cause.
4. Check the final effect.

Each step is about sustaining judgement under ambiguity.

{{< svg >}}
<svg xmlns="http://www.w3.org/2000/svg"
     width="980" height="340"
     viewBox="0 0 980 340"
     style="display:block;width:100%;max-width:44rem;height:auto;background:transparent"
     role="img"
     aria-label="Four-step troubleshooting framework moving from symptoms to trigger to root cause to final effect">

  <defs>
    <marker id="arrowhead-troubleshooting-v2" markerWidth="10" markerHeight="8"
            refX="10" refY="4" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L10,4 L0,8 z" fill="#222222"/>
    </marker>

    <style>
      .troubleshooting-title-v2 {
        font-family: Inter, Segoe UI, Roboto, Arial, sans-serif;
        font-size: 21px;
        font-weight: 700;
        fill: #111111;
      }

      .troubleshooting-label-v2 {
        font-family: Inter, Segoe UI, Roboto, Arial, sans-serif;
        font-size: 15px;
        font-weight: 700;
        fill: #111111;
      }

      .troubleshooting-small-v2 {
        font-family: Inter, Segoe UI, Roboto, Arial, sans-serif;
        font-size: 13px;
        fill: #333333;
      }

      .troubleshooting-box-v2 {
        fill: #ffffff;
        stroke: #222222;
        stroke-width: 2;
      }

      .troubleshooting-lightbox-v2 {
        fill: #ffffff;
        stroke: #999999;
        stroke-width: 1.5;
      }

      .troubleshooting-arrow-v2 {
        stroke: #222222;
        stroke-width: 2;
        fill: none;
        marker-end: url(#arrowhead-troubleshooting-v2);
      }
    </style>
  </defs>

  <!-- Title -->
  <text x="70" y="52" class="troubleshooting-title-v2">The four steps of diagnosis</text>
  <text x="70" y="78" class="troubleshooting-small-v2">Move from what is visible to the level where the problem is produced.</text>

  <!-- Boxes -->
  <rect x="45" y="145" width="185" height="120" rx="18" class="troubleshooting-lightbox-v2"/>
  <text x="75" y="183" class="troubleshooting-label-v2">Canvass symptoms</text>
  <text x="75" y="213" class="troubleshooting-small-v2">What is observably</text>
  <text x="75" y="235" class="troubleshooting-small-v2">wrong?</text>

  <rect x="265" y="145" width="185" height="120" rx="18" class="troubleshooting-lightbox-v2"/>
  <text x="295" y="183" class="troubleshooting-label-v2">Identify trigger</text>
  <text x="295" y="213" class="troubleshooting-small-v2">What exposed the</text>
  <text x="295" y="235" class="troubleshooting-small-v2">problem now?</text>

  <rect x="485" y="145" width="230" height="120" rx="18" class="troubleshooting-box-v2"/>
  <text x="515" y="183" class="troubleshooting-label-v2">Diagnose root cause</text>
  <text x="515" y="213" class="troubleshooting-small-v2">Why was this</text>
  <text x="515" y="235" class="troubleshooting-small-v2">possible?</text>

  <rect x="750" y="145" width="185" height="120" rx="18" class="troubleshooting-lightbox-v2"/>
  <text x="780" y="183" class="troubleshooting-label-v2">Check final effect</text>
  <text x="780" y="213" class="troubleshooting-small-v2">What must hold</text>
  <text x="780" y="235" class="troubleshooting-small-v2">when fixed?</text>

  <!-- Arrows -->
  <path d="M230 205 L265 205" class="troubleshooting-arrow-v2"/>
  <path d="M450 205 L485 205" class="troubleshooting-arrow-v2"/>
  <path d="M715 205 L750 205" class="troubleshooting-arrow-v2"/>

</svg>
{{< /svg >}}

<div style="max-width:44rem;text-align:center;font-size:0.95rem;color:#666;margin-top:0.5rem;">
Figure 1. Diagnosis moves from the visible symptom to the trigger, then to the root cause, and finally to the intended effect.
</div>

### Step 1—Canvass the symptoms

The first symptom, such as a stakeholder complaining about an unexpected number in a report, is a sign that something has gone wrong. However, this symptom cannot be taken at face value.

When a patient reports chest pain, the doctor’s first response is not to accept the patient’s diagnosis. The doctor asks about other symptoms, such as shortness of breath, dizziness, fever, recent injury, medication, and medical history. The aim is to build a wider picture before deciding what the symptom means.

The same applies to data engineering.

The data engineer should canvass the issues that look like something has gone wrong, using experience to judge what may be relevant and what is probably unrelated.

Examples may be:

- If one report is broken, are others broken?
- If one metric is wrong, are related metrics wrong?
- Did the pipeline produce an abnormal number of deletes?
- Were any records rejected during validation?
- Did a table load time increase drastically?
- Did any unit tests fail?
- Did any assumption checks fail?
- Are there anomalies upstream or downstream of the table with the reported error?

This is one reason why systematic logging in the warehouse and established tools for querying the logs are essential to a mature operation. Practised observability allows fast and accurate canvassing of symptoms.

### Step 2—Identify the trigger

A patient reporting a symptom often implies a diagnosis by associating it with a recent event: “I started feeling chest pain after lifting heavy boxes,” or “I developed a fever after eating seafood.” The doctor does not ignore this history, but also does not accept it as the diagnosis. The recent event may be relevant, but it may only be the trigger that exposed an underlying condition.

In the same way, the data engineer’s next step, after canvassing the symptoms, is to identify the trigger.

The trigger is the event that allowed the symptom to surface.

Common triggers in data engineering include:

- changes upstream, such as schema changes in source systems;
- new or unexpected source values;
- unusual records entering the pipeline;
- recent code releases;
- infrastructure or platform changes;
- permission or security changes;
- changes in load ordering or scheduling;
- changes in business process or operational behaviour;
- delayed, missing, or partial source loads.

If the symptom is reported by a stakeholder, identifying the trigger may involve asking questions. Useful questions include: “Why do you think the number is wrong?”, “What would you expect it to be?”, and “Do you have another source to compare with?”

Identifying the trigger is useful for two reasons.

First, the trigger often provides a hint for an urgent patch. If the trigger is a code release, rolling back the code may be the temporary fix.

Second, and more importantly, the trigger is a clue to finding the root cause. But just like a patient’s self-report, the important discipline is not to confuse the trigger with the root cause itself.

### Step 3—Diagnose the root cause {#step-3-diagnose-the-root-cause}

Once the patient has reported symptoms and given an account of recent history, the doctor often starts taking measurements: blood pressure, temperature, oxygen saturation, or a physical examination. Some cases may need blood tests, an X-ray, or other investigations.

With these measurements, the doctor is diagnosing the root cause—what actually caused the symptoms to occur.

Root cause diagnosis is often difficult, especially under time pressure. The two main approaches are:

- Theoretical: reading the system, such as scripts, metadata, logs, and table dependencies, and identifying what must be true for the failure to occur. For example, if the row count became unexpectedly high and the load time increased significantly, the engineer may inspect the code and discover a table had been accidentally joined onto its own column.

- Experimental: isolating variables through controlled tests, such as making changes in a test environment and observing the result. For example, if the data engineer suspects a code release caused the issue, without being able to see which code, then reverting in a development environment and re-running may confirm the diagnosis.

Their application is situational. While experimental diagnosis can be safer, it is not always possible to conduct the experiment. It requires a scientific approach. Theoretical diagnosis is often faster, but it can be easy to misread complex code. Both require deep skill.

The difficulty of diagnosing root cause, however, is not merely technical. It is also a matter of judgement.

One engineer may think one event or condition is the root cause, while another engineer thinks it is only a trigger.

One way to distinguish root cause from trigger is that:

> Root cause issues are those that violate design principles.

For example, a table load failed when a column received an unexpected value from the source system. At first glance, it may seem that the root cause is the system changing its list of defined values. But if that table is a list of port codes and the violation is an unexpected port code, then the root cause is not the system’s addition at all, but a violation of reference data design principles and a failure to implement [assumption monitoring](/docs/quality-reliability/tests-and-assumptions/#monitored-assumptions-surfacing-records-that-require-attention).

In this view, the disagreement between engineers reflects a different understanding of the design principle that has been violated.

This also affects the final step.

### Step 4—Check the final effect

The doctor finishes, not when the symptoms have disappeared, but when the patient is well.

The final effect is the only confirmation of the diagnosis. Importantly, the final effect is not the absence of the symptom.

The equivalent is much harder for data engineers.

Inexperienced data engineers sometimes silence the error. This is not addressing the root cause.

Another common mistake is to create the code fix in development, deploy it to production, assume the code is fixed, and move to the next task without checking the outcome post-deployment.

Instead, checking the final effect includes:

- visual validation: not “does the code run?”, but “are the outputs correct?”;
- environment validation: checking behaviour across development, pre-production, and production;
- end-to-end validation: whether the information now supports the intended decision;
- stakeholder validation: closing the loop with the stakeholder who raised the issue.

Ultimately, the final effect that needs to be checked is always:

> The business receives the information it needs to make the decision.

### Example: false deletions after a partial source extract

Suppose an operational report suddenly shows that thousands of active records have disappeared.

The immediate pressure is intense. The business thinks the report is wrong. The delivery team thinks the source system may have deleted records. Someone suggests restoring yesterday’s data. Someone else suggests disabling deletion logic. Another person asks whether the report can simply exclude today’s load.

A hasty response may make the report look better while making the warehouse less trustworthy.

Using the four-step framework, the engineer systematically tackles the issue.

**Symptom.** The reported symptom is that the operational report shows far fewer active records than expected. But this is only the first visible issue. The engineer canvasses nearby symptoms and finds that the downloaded files are shorter than usual, and that several downstream tables have lost records. Significantly, the data extract step did not fail and reported successful completion, but took much longer than normal.

**Trigger.** After investigation, the source is found to be extracted through an API. Since the API is rate-limited, the extract is downloaded in batches. The team had been warned of a planned network change through email, and the timing coincided with the extraction.

It turns out the network change is the trigger. The change resulted in extended API calls, and some calls timed out. However, the timeout exit was not logged as an error, so the extraction still appeared successful.

**Root cause.** One team member suggests that timeout exits need to be reported as errors to prevent future occurrences. Another team member suggests better coordination with the change management team, and that the team leader regularly attend the organisation’s change committee meeting to represent the team’s pipeline interests.

These may be relevant, but in this case they do not address the root cause.

The deeper issue is the design of deletion detection. The source system allows records to be deleted, but the API does not provide a reliable delete log. The warehouse therefore relies on a full source scan to infer deletes: if a record exists in the warehouse but is absent from the latest full scan, it is treated as deleted.

This design is only safe if a completed scan means a complete population has been received. In this case, that assumption was false. The pipeline treated an incomplete extraction as a complete scan, then interpreted the missing records as deletes.

**Final effect.** The final effect is not simply reporting timeout errors or improving attendance at the change committee meeting, because other issues may still produce incomplete extraction. Those actions may help with containment, but they do not make the design safe.

The business needs the warehouse to preserve the correct population of active records, even when remote extraction fails silently.

A better fix is to protect the deletion-detection step. The full scan should be staged first. The pipeline should check the expected batch count or source row count before applying deletion logic. Only when the extract is fully accounted for should the warehouse compare populations and mark deletes. If the scan is incomplete, the run should be quarantined, the prior population preserved, and the team alerted.

This is a contrived and simplified example. Real failures are rarely so simple. However, it shows why troubleshooting must move beyond the visible symptom. The report was where the problem appeared. The network change was the trigger. The root cause was unsafe deletion logic built on an unmonitored assumption. The final effect was a warehouse that could distinguish genuine deletion from incomplete capture.

## Conclusion

This chapter explained a simple four-step framework for troubleshooting:

1. Canvass the symptoms.
2. Identify the trigger.
3. Diagnose the root cause.
4. Check the final effect.

While the framework looks simple, it is distilled from countless scars, from small errors to costly failures, where premature conclusion and hasty fixes only made things worse.

Ultimately, troubleshooting complex errors in production, under time pressure, is a skill that can only be learned through personal experience. However, for new engineers, the framework provides a mental model to help accelerate attaining the necessary clarity and judgement.

Most importantly, the framework is not only for time-sensitive production failures. It applies to the entire discipline of data engineering. It is captured in the final principle of data engineering: instead of stopping at the symptoms, diagnose the root cause.

> [!NOTE]
> **Key ideas**
>
> The sixth principle of data engineering is diagnose the root cause.
>
> Data engineering is reconstructive because data begins as a fragment of reality captured by process.
>
> Troubleshooting a production failure is a crystallised instance of the whole discipline.
>
> The four steps of troubleshooting are: canvass the symptoms, identify the trigger, diagnose the root cause, and check the final effect.
>
> A symptom is what has visibly gone wrong. A trigger is the event that exposed it.
> 
> A root cause issue is the condition that violates a design principle.
>
> The final effect is not merely the disappearance of the symptom. The work is complete when the business receives the information it needs to make the decision.
