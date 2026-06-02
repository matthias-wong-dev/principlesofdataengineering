---
title: Working with stakeholders
url: /docs/judgement-under-ambiguity/working-with-stakeholders/
description: Explains how data engineers work with stakeholders by building trust, clarifying business intent, testing solution hypotheses, designing for workflows, and uncovering hidden complexity.
lede: Ambiguity is not a defect.
weight: 2
# draft: true
---

## Guiding stakeholders through ambiguity

Data projects often fail because teams treat requirements as something to collect rather than something to discover.

Stakeholders usually do not begin with a complete account of what should be built. They begin with business intent, operational pain, partial definitions, imagined solutions, and experience that is difficult to express. The delivery team begins in the same uncertainty.

When this ambiguity remains hidden, projects usually fall into one of two patterns.

The first is stalemate. The delivery team asks stakeholders for a list of “reporting requirements,” but the stakeholders struggle to provide one. From their perspective, the richness of their business cannot be reduced to a simple checklist. When the team insists on detailed requirements before exploration, the process stalls.

The second pattern appears more promising. Stakeholders provide a clear list of requirements upfront—sales aggregated by date or region, non-compliance by product type, even precise business definitions. The delivery team implements these, and all seems well. Yet during testing, the product does not meet its purpose. It lacks core features, breaks on edge cases, or proves too complex to use.

Both scenarios share the same flaw. The team waits for clarity instead of helping to create it.

This pattern persists because experts are often familiar with the intricacies of their own discipline but underestimate the challenges of others. They expect simplistic answers about everything outside their own craft to be given in clear-cut form so they can proceed with their part.

The world is not so straightforward. The most difficult part of a data project is not technical complexity alone, but thinking deeply about the business and its relationship with the data world. Asking stakeholders to enumerate requirements is convenient for delivery teams because it shifts the responsibility for this deep thinking to stakeholders, leaving developers with the easier task of implementing clear technical rules.

Instead, in a successful project, the delivery team guides stakeholders to express their intent, then works together to explore the data in light of that business intent. Through this process, stakeholders uncover what they need to see from the data to achieve business outcomes. These discovered needs—not an initial list—are the real requirements.

The fifth principle of data engineering is therefore: instead of waiting for clarity, **illuminate ambiguity**.

In stakeholder work, this means guiding stakeholders through ambiguity until unclear needs become shared understanding.

## Seven engagement principles

During development, the delivery team and stakeholders explore the data together in light of business intent. The delivery team contributes expertise by guiding stakeholders through ambiguity: helping them clarify intent, recognise workflows, test definitions, examine edge cases, and see how source data does or does not support the business purpose.

The seven engagement principles that follow provide a practical framework for guiding stakeholders:

1. Focus on trust
2. Lead by listening
3. Own the business intent
4. Anchor a vision
5. Gather around the solution
6. Design for workflows
7. Spot the 20%

{{< svg >}}
<svg xmlns="http://www.w3.org/2000/svg"
     width="980" height="760"
     viewBox="0 0 980 760"
     style="display:block;width:100%;max-width:44rem;height:auto;background:transparent"
     role="img"
     aria-label="Seven engagement principles grouped into movements from ambiguity to shared clarity">

  <defs>
    <marker id="arrowhead-engagement-path-v4" markerWidth="10" markerHeight="8"
            refX="10" refY="4" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L10,4 L0,8 z" fill="#222222"/>
    </marker>

    <style>
      .engagement-path-title-v4 {
        font-family: Inter, Segoe UI, Roboto, Arial, sans-serif;
        font-size: 21px;
        font-weight: 700;
        fill: #111111;
      }

      .engagement-path-label-v4 {
        font-family: Inter, Segoe UI, Roboto, Arial, sans-serif;
        font-size: 16px;
        font-weight: 700;
        fill: #111111;
      }

      .engagement-path-small-v4 {
        font-family: Inter, Segoe UI, Roboto, Arial, sans-serif;
        font-size: 13px;
        fill: #333333;
      }

      .engagement-path-box-v4 {
        fill: #ffffff;
        stroke: #222222;
        stroke-width: 2;
      }

      .engagement-path-lightbox-v4 {
        fill: #ffffff;
        stroke: #999999;
        stroke-width: 1.5;
      }

      .engagement-path-arrow-v4 {
        stroke: #222222;
        stroke-width: 2;
        fill: none;
        marker-end: url(#arrowhead-engagement-path-v4);
      }

      .engagement-path-line-v4 {
        stroke: #999999;
        stroke-width: 1.4;
        fill: none;
      }
    </style>
  </defs>

  <!-- Title -->
  <text x="70" y="52" class="engagement-path-title-v4">Guiding stakeholders through ambiguity</text>
  <text x="70" y="78" class="engagement-path-small-v4">The engagement principles turn unclear need into shared clarity.</text>

  <!-- Ambiguity -->
  <rect x="245" y="112" width="490" height="80" rx="18" class="engagement-path-lightbox-v4"/>
  <text x="490" y="145" text-anchor="middle" class="engagement-path-label-v4">Ambiguity</text>
  <text x="490" y="170" text-anchor="middle" class="engagement-path-small-v4">partial intent · imagined solutions · uncertain definitions · hidden edge cases</text>

  <path d="M490 192 L490 224" class="engagement-path-arrow-v4"/>

  <!-- Movement 1 -->
  <rect x="180" y="224" width="620" height="84" rx="16" class="engagement-path-box-v4"/>
  <text x="215" y="258" class="engagement-path-label-v4">1. Focus on trust</text>
  <text x="215" y="282" class="engagement-path-small-v4">Make honest dialogue possible.</text>
  <text x="505" y="258" class="engagement-path-label-v4">2. Lead by listening</text>
  <text x="505" y="282" class="engagement-path-small-v4">Guide from what stakeholders have said.</text>

  <path d="M490 308 L490 340" class="engagement-path-arrow-v4"/>

  <!-- Movement 2 -->
  <rect x="180" y="340" width="620" height="84" rx="16" class="engagement-path-box-v4"/>
  <text x="215" y="374" class="engagement-path-label-v4">3. Own business intent</text>
  <text x="215" y="398" class="engagement-path-small-v4">See the problem first-hand.</text>
  <text x="505" y="374" class="engagement-path-label-v4">4. Anchor a vision</text>
  <text x="505" y="398" class="engagement-path-small-v4">Give the work a centre.</text>

  <path d="M490 424 L490 456" class="engagement-path-arrow-v4"/>

  <!-- Movement 3 -->
  <rect x="180" y="456" width="620" height="84" rx="16" class="engagement-path-box-v4"/>
  <text x="215" y="490" class="engagement-path-label-v4">5. Gather around the solution</text>
  <text x="215" y="514" class="engagement-path-small-v4">Make understanding visible.</text>
  <text x="505" y="490" class="engagement-path-label-v4">6. Design for workflows</text>
  <text x="505" y="514" class="engagement-path-small-v4">Connect the product to real use.</text>

  <path d="M490 540 L490 572" class="engagement-path-arrow-v4"/>

  <!-- Movement 4 -->
  <rect x="245" y="572" width="490" height="76" rx="16" class="engagement-path-box-v4"/>
  <text x="280" y="604" class="engagement-path-label-v4">7. Spot the 20%</text>
  <text x="280" y="628" class="engagement-path-small-v4">Find hidden foundations, assumptions, and edge cases.</text>

  <path d="M490 648 L490 678" class="engagement-path-arrow-v4"/>

  <!-- Shared clarity -->
  <rect x="245" y="678" width="490" height="62" rx="18" class="engagement-path-lightbox-v4"/>
  <text x="490" y="705" text-anchor="middle" class="engagement-path-label-v4">Shared clarity</text>
  <text x="490" y="727" text-anchor="middle" class="engagement-path-small-v4">statement of intent · workflow · wireframe · definitions · construction plan</text>

  <!-- Side movement label -->
  <path d="M830 150 C885 250, 885 585, 830 710" class="engagement-path-line-v4"/>
  <rect x="846" y="332" width="28" height="162" rx="10" fill="#ffffff"/>
  <text x="864" y="413"
        transform="rotate(90 864 413)"
        text-anchor="middle"
        class="engagement-path-small-v4">listen · sketch · test · refine</text>

</svg>
{{< /svg >}}

<div style="max-width:44rem;text-align:center;font-size:0.95rem;color:#666;margin-top:0.5rem;">
Figure 1. Guiding stakeholders through ambiguity is a disciplined movement from unclear need to shared clarity. Trust and listening make dialogue possible; intent and vision give it direction; solution sketches and workflows make it concrete; spotting the 20% protects the project from hidden complexity.
</div>

### Focus on trust

Many assume that the primary mode of stakeholder engagement is extracting information. In this view, the question becomes: “How effectively and accurately can I get information from stakeholders to build a product?”

This is the wrong focus.

The first responsibility of a delivery team is to gain the stakeholder’s trust.

There are several reasons for this.

1. Trust is the context for information. Clearly articulating and refining requirements is arduous. Stakeholders will not be able to give the right information before they have first established strong trust in the people asking for it.

2. Relationship with others is the biggest factor for meaningful and enjoyable work. Strong relationships with stakeholders are more likely to lead to enjoyable collaboration during development and, subsequently, the success of the team.

3. The focus on extracting information sees stakeholders instrumentally as vehicles for information. The focus on growing trust sees stakeholders as human beings with whom we work.

4. Delivery teams have recurring partnerships with stakeholders that extend beyond a particular project. The focus on building trust takes the long-term view.

Without trust, no data project can succeed. After each engagement, the question should not be “Do we know more about the requirements?” but:

> Do our stakeholders trust us more?

The best ways to grow trust are transparency and active listening.

- Transparency means clear communication of the [construction plan](/docs/judgement-under-ambiguity/construction-planning/) and regular demonstrations of progress—weekly or twice-weekly. This is akin to a home buyer seeing the building take shape.

- Active listening means thoughtful paraphrasing and summarising stakeholder input. When stakeholders hear their own language reflected, they feel understood and affirmed. This also happens when they are invited to check metadata, which gives them a tangible way to contribute.

A common habit is for delivery teams to assume that the purpose of speaking is to transfer information. If they already know what stakeholders are about to say, they think they can skip to the next part.

This is a mistake.

Beneath the surface, the stakeholder is:

1. developing a feeling of being heard;
2. clarifying their own thinking through articulation;
3. growing in data literacy through dialogue with technical experts.

All these build trust. By remembering that the first responsibility of the team is to gain trust, we resist the temptation to cut people off or jump in to correct them. Patience is paramount.

### Lead by listening

In some types of partner dancing, there are two designated roles: Lead and Follow. The Lead initiates movements and the Follow completes the sequence with an elegant response.

An analogous dynamic is needed with stakeholders. The delivery team should formulate its own statements as responses to previous statements from stakeholders. These responses typically take one of the following forms:

- Clarifying question: “You said X. Can you clarify whether X means...?” or “You said your team needs X—can you help us understand how this fits into your goal?”

- Playback: “There’s a lot in what you just said—can I paraphrase to check I’m on the right track?” or “I’ve summarised your explanation into workflows—can I share them for confirmation?”

- Proposal: “Based on what you said about your workflows, here are wireframes of our solution hypothesis—does this align?”

- Amendment: “You gave feedback on our hypothesis—here’s a refinement. What do you think?”

By responding to stakeholder initiatives, the delivery team is, in reality, leading. This is achieved by listening closely to what has been said and naturally guiding stakeholders through the problem. This approach ensures:

- stakeholders are heard, feel heard, and are seen to be heard;
- the conversation remains structured, logical, and focused on business objectives.

There will be times when the team needs to correct an error, redirect focus, or counter unconscious bias. This principle still applies. A common scenario is when stakeholders describe solutions before the problem is fully explored—for example, asking for a detailed data dump dashboard when analysis suggests a summarised view would better serve the intent.

Saying “Let’s focus on requirements instead of jumping to the solution” sounds natural but often feels dismissive. For stakeholders, the solution is the requirement.

Regardless of content, stakeholders are trying to communicate something important.

This should always be affirmed. Even if the content is incorrect, the underlying intent is valuable. Respond by continuing with their initiative rather than breaking off. For example:

- Explore the intent: “You said your goal is to detect potential non-compliance. How does the data dump help?”

- Explore the utility: “You want a detailed data dump. Can you give an example of a workflow where this is used?”

- Re-orient: “Thanks for raising the data dump idea. You previously said your goal is detecting non-compliance. Can we explore scenarios where that happens, then revisit the data dump in that context?”

These approaches respect intent and apply the first engagement principle: **focus on trust**. They also apply the fifth engagement principle: **gather around the solution**.

This principle should never be used as a shield for blame—"I just did what you told me to do."

### Own the business intent

The task of data engineering is to align data to business intent. It is an experimental process that demands the data engineer see the stakeholder’s perspective first-hand. Without this, the team will never truly see what the stakeholder sees, and the potential of the solution will remain unrealised.

This act of viewing the data through the stakeholder’s lens is owning the business intent.

The data engineer who owns the business intent must be committed to in-depth business analysis.

This chapter is not a guide to business analysis, except to note that business processes often conform to recurring patterns. Mastering these patterns helps the team achieve high-quality analysis quickly, even for complex scenarios. The team can do this by consistently asking stakeholders five key questions:

- Intent: What is the business intent?
- Measure: How does the business measure the achievement of this intent, either directly or indirectly?
- Sensor: What instruments does the business have for knowing whether things are going well or not?
- Controls: What levers does the business have to influence this measure?
- Drivers: What external events outside the business’s control may influence this measure?

Business analysis needs to permeate the project from start to finish. For example, concepts such as “good vs bad” entities or milestones for measuring processes are rarely defined in source systems. It is unrealistic to expect stakeholders to define these upfront before seeing the data. Instead, these definitions evolve through exploration and require input from technical expertise and experience with similar problems. This, once again, demands that the team see the business problem first-hand.

Owning the business intent is an extension of the first engagement principle: **focus on trust**. Nothing gains trust with stakeholders as quickly as a team that can speak the details of the business fluently. From this perspective, business analysis is a delivery team’s way of active listening.

Whether a team owns the business intent will define its passion, drive, business knowledge, and creativity. These qualities will determine whether its output is a mediocre reflection of the current state or a solution that pushes the business forward.

### Anchor a vision

The natural extension of owning the business intent is a vision for the business. A vision is a view of the value the team aspires to achieve. It is both ambitious and concrete.

While having a vision is important for any project, it is particularly critical in exploratory data projects for the following reasons:

- Improves the probability of arrival. Complex data projects are often ambiguous and uncertain. Teams that articulate and revisit a vision are more likely to reach the intended outcome.
- Sustains engagement. Long projects involve hard work, such as resolving edge cases. A clear vision inspires a sense of meaning that helps maintain engagement.
- Keeps debates in perspective. Under constraints, debates are inevitable and can become flashpoints of tension. A vision keeps these debates in perspective. Teams often relax around specific problems when they see those problems as only one part of the whole.

- Structures discussion. Data projects are open-ended and can easily drift. Anchoring the project in a vision, and deriving each step from that vision, keeps the team on track.

Using the vision to structure discussions begins with agreement on the overall intent of the business. The project objective is situated within the business objective, which is itself part of the broader organisation’s objectives. The discussion on each delivery feature should be anchored to this hierarchy, with constant reference back to the higher-level intent. When the conversation becomes lost, the team moves up one level and reorients.

Example dialogue:

> **Stakeholder:** “We need a dashboard.”
> 
> **Team:** “Can you start by telling us the purpose of your business, your role, and what success means to you?”
> 
> **Stakeholder:** “Our goal is to improve customer experience. My team monitors service quality.”
> 
> **Team:** “So your organisation’s goal is to improve customer experience, and your team supports this by monitoring service quality?”
> 
> **Stakeholder:** “Yes, but also recurring issues.”
> 
> **Team:** “Okay, so you track service quality, but you also need to identify recurring issues to prevent them. Is that right?”
> 
> **Stakeholder:** “Yes.”
> 
> **Team:** “At the start you mentioned a dashboard. What is its purpose in this context? Is it for your team’s internal use, or to share insights with other areas?”

This pattern—bringing stakeholders up to the highest level and then unpacking details step by step—requires fast thinking and familiarity with the organisation’s goals. It is harder than it appears, but essential for clarity.

When priorities conflict, reference to the higher-level intent provides common ground. Agreement is easier at higher levels and can be used to resolve issues. This approach works only when the conversation has been structured from the vision downward.

Unlike a building project, which relies on well-defined specifications of the target building and strict timelines to track progress, data projects are exploratory and open-ended. In this setting, a clear vision, rather than detailed specifications, plays the role of guiding the team. It serves as a north star and compass that sustains quality and momentum across a long project. For this reason, team leaders should insist on vision, quality, and momentum rather than rigid deadlines.

### Gather around the solution

Data projects often waste time through too much talking and not enough doing.

The best way to collaborate is to gather around a solution—start with a pen-and-paper solution hypothesis and refine it through discussion and experimentation.

The project should develop hypotheses as early as possible, even by the second engagement. Early development matters because:

- A convincing solution is the only proof the team has understood the requirements.
- Hypotheses provide a concrete point for clarifying stakeholder thinking.
- Refinement creates excitement as all parties see an early vision come to life.

A solution hypothesis is the most important artefact in discovery because it is the clearest proof that the team has understood the need.

In an analogy of commissioning a building, it is futile if the builder only has a list of requirements: four rooms, lots of sunlight, and enough storage. The builder wins confidence by providing an architectural sketch—nothing less will do. No buyer would pay a mortgage deposit for a building without a sketch.

Why expect stakeholders to work with a team without showing a solution hypothesis?

When projects meander, it is often because direction is unclear. The best advice for such situations is simple:

> When the project is stuck, draw a picture of the solution.

The best way to refine the solution hypothesis is through an open workbench format. In an open workbench, the delivery team and stakeholders meet regularly to explore the data model, experiment with new features, test definitions, and provide feedback for the next iteration. Stakeholders may come from different business areas, making the data model a centre for converging perspectives.

{{< svg >}}
<svg xmlns="http://www.w3.org/2000/svg"
     width="980" height="620"
     viewBox="0 0 980 620"
     style="display:block;width:100%;max-width:44rem;height:auto;background:transparent"
     role="img"
     aria-label="Open workbench showing vision above, trust below, and stakeholder intent, source data, workflows, and solution sketches brought into the same conversation">

  <defs>
    <marker id="arrowhead-open-workbench-v2" markerWidth="10" markerHeight="8"
            refX="10" refY="4" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L10,4 L0,8 z" fill="#222222"/>
    </marker>

    <style>
      .open-workbench-title-v2 {
        font-family: Inter, Segoe UI, Roboto, Arial, sans-serif;
        font-size: 21px;
        font-weight: 700;
        fill: #111111;
      }

      .open-workbench-label-v2 {
        font-family: Inter, Segoe UI, Roboto, Arial, sans-serif;
        font-size: 16px;
        font-weight: 700;
        fill: #111111;
      }

      .open-workbench-small-v2 {
        font-family: Inter, Segoe UI, Roboto, Arial, sans-serif;
        font-size: 13px;
        fill: #333333;
      }

      .open-workbench-box-v2 {
        fill: #ffffff;
        stroke: #222222;
        stroke-width: 2;
      }

      .open-workbench-lightbox-v2 {
        fill: #ffffff;
        stroke: #999999;
        stroke-width: 1.5;
      }

      .open-workbench-arrow-v2 {
        stroke: #222222;
        stroke-width: 2;
        fill: none;
        marker-end: url(#arrowhead-open-workbench-v2);
      }

      .open-workbench-line-v2 {
        stroke: #222222;
        stroke-width: 2;
        fill: none;
      }

      .open-workbench-muted-line-v2 {
        stroke: #999999;
        stroke-width: 1.5;
        fill: none;
      }
    </style>
  </defs>

  <!-- Title -->
  <text x="70" y="48" class="open-workbench-title-v2">The open workbench</text>
  <text x="70" y="74" class="open-workbench-small-v2">Bring intent, workflows, data, and solution sketches into the same conversation.</text>

  <!-- Vision line -->
  <line x1="110" y1="112" x2="870" y2="112" class="open-workbench-line-v2"/>
  <rect x="405" y="93" width="170" height="38" rx="18" fill="#ffffff"/>
  <text x="490" y="118" text-anchor="middle" class="open-workbench-label-v2">Vision</text>

  <!-- Centre workbench -->
  <rect x="345" y="235" width="290" height="145" rx="22" class="open-workbench-box-v2"/>
  <text x="415" y="285" class="open-workbench-title-v2">Open workbench</text>
  <text x="395" y="315" class="open-workbench-small-v2">listen · sketch · test · refine</text>
  <text x="390" y="343" class="open-workbench-small-v2">shared understanding grows here</text>

  <!-- Inputs -->
  <rect x="80" y="165" width="230" height="92" rx="18" class="open-workbench-lightbox-v2"/>
  <text x="110" y="199" class="open-workbench-label-v2">Stakeholder intent</text>
  <text x="110" y="225" class="open-workbench-small-v2">goals, pain, imagined solution</text>

  <rect x="670" y="165" width="230" height="92" rx="18" class="open-workbench-lightbox-v2"/>
  <text x="700" y="199" class="open-workbench-label-v2">Source data</text>
  <text x="700" y="225" class="open-workbench-small-v2">records, gaps, edge cases</text>

  <rect x="80" y="405" width="230" height="92" rx="18" class="open-workbench-lightbox-v2"/>
  <text x="110" y="439" class="open-workbench-label-v2">Business workflows</text>
  <text x="110" y="465" class="open-workbench-small-v2">triggers, actions, decisions</text>

  <rect x="670" y="405" width="230" height="92" rx="18" class="open-workbench-lightbox-v2"/>
  <text x="700" y="439" class="open-workbench-label-v2">Solution sketch</text>
  <text x="700" y="465" class="open-workbench-small-v2">wireframes, model, prototype</text>

    <!-- Arrows into workbench -->
    <path d="M310 220 C328 226, 334 238, 338 250" class="open-workbench-arrow-v2"/>
    <path d="M670 220 C652 226, 646 238, 642 250" class="open-workbench-arrow-v2"/>
    <path d="M310 450 C328 436, 334 400, 338 368" class="open-workbench-arrow-v2"/>
    <path d="M670 450 C652 436, 646 400, 642 368" class="open-workbench-arrow-v2"/>

  <!-- Trust line -->
  <line x1="110" y1="548" x2="870" y2="548" class="open-workbench-line-v2"/>
  <rect x="405" y="529" width="170" height="38" rx="18" fill="#ffffff"/>
  <text x="490" y="554" text-anchor="middle" class="open-workbench-label-v2">Trust</text>


</svg>
{{< /svg >}}

<div style="max-width:44rem;text-align:center;font-size:0.95rem;color:#666;margin-top:0.5rem;">
Figure 2. The open workbench brings stakeholder intent, business workflows, source data, and solution sketches into the same conversation. Vision anchors the work from above; trust supports it from below. Between them, the team listens, sketches, tests, and refines until the solution becomes recognisable to the business.
</div>

This format requires developers to be confident hosting discussions and responding to impromptu questions from stakeholders. The entire team should support them in doing so. When done well, the open workbench has a transformative effect: it builds trust through transparency and enables genuine dialogue.

Teams sometimes say, “Let’s not jump into solution mode.” This statement is not acceptable with stakeholders. For them, the solution is the requirement. When asked to describe requirements, most stakeholders are painting a mental picture of the solution. Even if it is a bad solution, it still describes what they imagine they are working toward. The team should play back the intent or seek clarification.

The error is to draw a hard line between requirements and solution. This is a distinction developers make, not stakeholders. The real distinction is between the why, which is intent, and the what, which is solution. Stakeholders will often mix both. It is the team’s job to discern one from the other.

This cannot be stressed enough: to stakeholders, the solution is the requirement—not something separate from it. In a data project, it is never too early to gather around the solution.

Gathering around the solution is the ultimate way the delivery team guides stakeholders toward clarity. It helps them see how reshaped data interacts with business intent, turning abstract requirements into something tangible. Through iterative refinement—testing, visualising, and adjusting—the solution evolves until it displays fidelity with business reality.

### Design for workflows

It is common for data projects to deliver reports that are rarely used. Stakeholders may specify many requirements—“I want to see count of X per country”—and show excitement during development and testing. Yet after deployment, usage often drops quickly.

This happens when solutions are not anchored in real workflows. Anchoring a solution in workflows ensures that it has a place in real use.

Every workflow has at least two elements: an intent and a trigger.

For example, a helpdesk workflow might look like this.

{{< svg >}}
<svg xmlns="http://www.w3.org/2000/svg"
     width="980" height="520"
     viewBox="0 0 980 520"
     style="display:block;width:100%;max-width:44rem;height:auto;background:none"
     role="img"
     aria-label="Example workflow showing a helpdesk worker receiving a trigger, using an operations dashboard, and acting toward an intent">

  <defs>
    <marker id="arrowhead-workflow-example-v2" markerWidth="10" markerHeight="8"
            refX="10" refY="4" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L10,4 L0,8 z" fill="#2f6fce"/>
    </marker>

    <style>
      .workflow-example-label-v2 {
        font-family: Inter, Segoe UI, Roboto, Arial, sans-serif;
        font-size: 17px;
        font-weight: 700;
        fill: #111111;
      }

      .workflow-example-text-v2 {
        font-family: Inter, Segoe UI, Roboto, Arial, sans-serif;
        font-size: 16px;
        fill: #111111;
      }

      .workflow-example-blue-v2 {
        font-family: Inter, Segoe UI, Roboto, Arial, sans-serif;
        font-size: 18px;
        font-style: italic;
        fill: #2f6fce;
      }

      .workflow-example-icon-v2 {
        fill: none;
        stroke: #111111;
        stroke-width: 3;
        stroke-linecap: round;
        stroke-linejoin: round;
      }

      .workflow-example-solid-v2 {
        fill: #111111;
      }

      .workflow-example-arrow-v2 {
        stroke: #2f6fce;
        stroke-width: 2;
        fill: none;
        marker-end: url(#arrowhead-workflow-example-v2);
      }
    </style>
  </defs>

  <!-- Row 1: person -->
  <g transform="translate(90 72)">
    <circle cx="26" cy="15" r="10" class="workflow-example-solid-v2"/>
    <path d="M8 49 C10 32, 42 32, 44 49 Z" class="workflow-example-solid-v2"/>
    <path d="M15 10 C22 18, 31 18, 38 10"
          fill="none" stroke="#ffffff" stroke-width="3" stroke-linecap="round"/>
  </g>

  <text x="170" y="107" class="workflow-example-label-v2">Alex works at the product helpdesk.</text>

  <!-- Row 2: email / trigger -->
  <g transform="translate(90 158)">
    <rect x="2" y="4" width="54" height="38" class="workflow-example-icon-v2"/>
    <path d="M4 7 L29 28 L56 7" class="workflow-example-icon-v2"/>
    <path d="M5 42 L23 25" class="workflow-example-icon-v2"/>
    <path d="M55 42 L36 25" class="workflow-example-icon-v2"/>
  </g>

  <text x="170" y="185" class="workflow-example-text-v2">
    <tspan font-weight="700">Alex receives an email notification</tspan>
    <tspan dx="4">that a recent order needs attention.</tspan>
  </text>

  <line x1="820" y1="178" x2="720" y2="178" class="workflow-example-arrow-v2"/>
  <text x="845" y="184" class="workflow-example-blue-v2">trigger</text>

  <!-- Row 3: dashboard -->
  <g transform="translate(90 250)">
    <line x1="4" y1="54" x2="58" y2="54" class="workflow-example-icon-v2"/>
    <rect x="8" y="38" width="8" height="16" class="workflow-example-solid-v2"/>
    <rect x="24" y="25" width="8" height="29" class="workflow-example-solid-v2"/>
    <rect x="40" y="10" width="8" height="44" class="workflow-example-solid-v2"/>
    <line x1="8" y1="38" x2="8" y2="26" class="workflow-example-icon-v2"/>
    <line x1="24" y1="25" x2="24" y2="12" class="workflow-example-icon-v2"/>
    <line x1="40" y1="10" x2="40" y2="2" class="workflow-example-icon-v2"/>
  </g>

  <text x="170" y="274" class="workflow-example-text-v2">
    <tspan>Alex logs into the</tspan>
    <tspan dx="4" font-weight="700">operations dashboard</tspan>
    <tspan dx="4">and searches for the</tspan>
    <tspan dx="4" font-weight="700">Order ID</tspan>
    <tspan>.</tspan>
  </text>

  <text x="170" y="301" class="workflow-example-text-v2">
    <tspan>On the details page, Alex can see</tspan>
    <tspan dx="4" font-weight="700">all checks applied to the order</tspan>
  </text>

  <text x="170" y="328" class="workflow-example-text-v2">and notices one has failed.</text>

  <!-- Row 4: resolution / intent -->
  <g transform="translate(90 386)">
    <rect x="4" y="8" width="54" height="38" class="workflow-example-icon-v2"/>
    <rect x="10" y="14" width="42" height="26"
          fill="none" stroke="#111111" stroke-width="1.7"/>
    <path d="M18 27 L28 35 L45 18" class="workflow-example-icon-v2"/>
  </g>

  <text x="170" y="410" class="workflow-example-text-v2">
    <tspan>With this information, Alex contacts the client, explains the options,</tspan>
  </text>

  <text x="170" y="437" class="workflow-example-text-v2">
    <tspan>and</tspan>
    <tspan dx="4" font-weight="700">agrees on the resolution.</tspan>
  </text>

  <line x1="820" y1="418" x2="720" y2="418" class="workflow-example-arrow-v2"/>
  <text x="845" y="424" class="workflow-example-blue-v2">intent</text>

</svg>
{{< /svg >}}

<div style="max-width:44rem;text-align:center;font-size:0.95rem;color:#666;margin-top:0.5rem;">
Figure 3. A workflow begins with a trigger and is organised around an intent. The data product is useful because it supports the action between them.
</div>

A trigger can be a specific event, such as receiving an email from a customer, or a schedule, such as publishing a quarterly report.

Contextualising requirements in workflows offers key advantages:

1. Ensures the product delivers value because it meets the intent of an established workflow.
2. Ensures the product will be used because real-world triggers exist for its use.
3. Integrates the product into the user’s daily role.
4. Helps stakeholders recognise when a requirement is not important and can be dropped.
5. Provides a natural way to rationalise requirements—for example, one report page per workflow.

Designing for workflows is a simple tool to ensure that project teams are grounded in real-world problems.

### Spot the 20%

The 80/20 rule says 80% of results come from 20% of effort. Its flip side is that the remaining 20% consumes 80% of the effort. This creates an illusion that most work is done when the hardest part remains—the hidden, complex 20%.

The 20/80 trap is dangerous because:

1. foundational elements are missed until production;
2. expectations are mismanaged when stakeholders think the work is complete;
3. technical debt piles up when essentials are discovered late.

Teams avoid the trap by:

1. grounding requirements in thorough business analysis to uncover hidden assumptions;
2. focusing equally on what works and what does not—the parts that work are often forgotten;
3. asking not only “What should this do?” but “What could go wrong?”;
4. balancing common cases and edge cases without bias;
5. developing in sound engineering order, not simply in the order stakeholders want to see.

As an analogy, home buyers focus on visible features—“How many rooms?” or “Is there good ventilation?”—based on obvious needs and past pain. A good builder starts with the foundation. Likewise, a good data team begins with the start of the business process and systematically works through the business processes in order, rather than jumping to flashy features.

Because of this, the team will often run counter to stakeholder instincts. This is healthy.

In effect, the team acts as:

- a counterweight to natural biases that overlook fundamentals;
- a safeguard against missed edge cases that matter.

Foreseeing hidden elements is hard. It takes strong business knowledge, technical experience, and high engagement skills to counter bias. Only the best teams do it well.

## Conclusion

The hardest part of any data project is thinking deeply about the business and how it relates to data. This can only be achieved when stakeholders and the delivery team explore the data together—thinking together through a dialogue focused on the solution.

In this dialogue, the relationship is not symmetrical. Stakeholders understand the business, but they are often new to data and do not know what to look for. This is why the experienced delivery team plays an important role in guiding stakeholders through ambiguity.

The seven engagement principles capture hard-earned wisdom for facilitating these dialogues. They run counter to ingrained habits that focus on visible details while ignoring complexity.

> [!NOTE]
> **Key ideas**
>
> Ambiguity is not a defect in stakeholder work.
>
> Requirements are discovered through dialogue, not merely collected upfront.
>
> The delivery team should guide stakeholders through ambiguity until unclear needs become shared understanding.
>
>> The fifth principle of data engineering is **illuminate ambiguity**.
>
> The seven engagement principles are:
>
> 1. **Focus on trust**
> 2. **Lead by listening**
> 3. **Own the business intent**
> 4. **Anchor a vision**
> 5. **Gather around the solution**
> 6. **Design for workflows**
> 7. **Spot the 20%**
>
> These principles move the team beyond reacting to requirements and toward a solution that truly meets business intent.