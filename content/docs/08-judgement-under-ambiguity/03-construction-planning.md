---
title: Construction planning
url: /docs/judgement-under-ambiguity/construction-planning/
description: Shows how data engineers create flexible construction plans that sequence delivery, build momentum, and adapt as discovery continues.
lede: A strong construction plan gives ambiguous work a flexible order.
weight: 3
# draft: true
---

## Shaping movement

Complex data projects are rarely clear at the beginning. The business intent may still be forming. The source data may not behave as expected. Dependencies may be unclear. Stakeholders may discover new priorities as soon as they see the first useful output.

A weak team responds to this uncertainty in one of two ways. It either meanders, waiting for clarity before moving, or it overcorrects by imposing a rigid plan that cannot survive discovery.

However: 

> [!SHARE:ambiguity-and-order]
> Ambiguity does not justify meandering. Order does not require rigidity.

A data engineer is responsible for shaping movement through uncertain work. This is the purpose of the **construction plan**. A construction plan gives uncertain work enough order to proceed and enough flexibility to adapt.

A strong construction plan avoids both failures of meandering and paralysis. It gives the team a sequenced path of delivery without pretending the whole project is known in advance.

In complex projects, this plan is expected from an experienced engineer because:

1. No project waits in silence. The engineer cannot disappear for a month to apply ideal patterns and return later. Unless the engineer provides the team and sponsors with confidence about the weeks or months ahead, there will be no engineering work at all.

2. Logical sequencing matters in a build. Doing tasks in a sensible order helps the engineer move forward with confidence, avoids code entanglement, and reduces mistakes.

3. Only the engineer knows the effort required. The data engineer alone understands how long quality work takes and has the responsibility to advocate for that time.

If the engineer does not actively formulate a plan, there will be no plan—leading the project to meander. Or someone else will create the plan for the engineer—leading the project to rush. In either case, the project suffers.

Projects can succeed or fail depending on the data engineer’s plan. It is one of the data engineer’s leadership roles when guiding stakeholders. Formulating a plan for the team is one of the most advanced skills to master and a mark of a confident engineer.

## An effective plan

A construction plan lays out, in sequence, the components the data engineer will build and gives the team a forecast of what will arrive when. It includes user-facing features as well as non-feature work such as unit tests, technical debt clean-up, metadata, and performance tuning.

A plan is effective if it gives the project confidence and momentum. For this purpose, sequence matters more than precise dates. Timelines should not blow out, but the deeper issue is whether the team can keep delivering one sensible step after another.

An effective plan is like a travel itinerary for exploring a new country. An itinerary is not effective merely because it meets a predefined schedule. It is effective when it moves forward logically, gives the traveller a quality experience, and avoids wasting time.

A data engineer can craft an effective plan by aiming for three characteristics:

- ambitious yet grounded;
- orderly yet flexible;
- rotating new features with backend consolidation.

### Ambitious yet grounded

Being ambitious means having a view of the full business process and designing a model that can address future questions, rather than limiting the scope to requirements raised by current stakeholders.

Being grounded means supporting this ambition with well-informed business analysis so that the plan is neither vague nor impossible. The engineer should know enough about the business, data, dependencies, and risks to make a reasonable judgement about the path ahead.

### Orderly yet flexible

An orderly yet flexible plan is like a travel itinerary that is physically sensible but still able to shift. For a data engineer, being orderly means isolating releases in a way that promotes code clarity, avoids code entanglement, and minimises rework.

Flexibility means structuring the plan so that key business priorities can shift forward or backward as a block without disrupting the whole schedule. This requires grouping deliverables around core business processes, rather than maintaining a miscellaneous list of disconnected business questions.

### Rotate features with consolidation

New features excite stakeholders and create momentum. However, the data engineer must balance visible features with invisible but equally important consolidation work.

An effective plan achieves both by alternating between them. This rotation supports quality work by building consolidation into the schedule. It also gives stakeholders time to absorb one feature before moving on to the next. This is because data insights are exploratory. Testing a new feature requires users to interact with the output, understand its implications, and check edge cases thoroughly.

## Formulating an effective plan

A data engineer can craft an effective plan in four stages. Each stage involves increasing commitment to specific outcomes. A simple project may require only the first stage, while a complex project may require a detailed plan at the fourth stage.

The four stages are:

1. Discovery
2. Vision
3. Scope
4. Build

{{< svg >}}
<svg xmlns="http://www.w3.org/2000/svg"
     width="980" height="520"
     viewBox="0 0 980 520"
     style="display:block;width:100%;max-width:44rem;height:auto;background:transparent"
     role="img"
     aria-label="Construction planning stages from discovery to vision to scope to build">

  <defs>
    <marker id="arrowhead-construction-plan-v1" markerWidth="10" markerHeight="8"
            refX="10" refY="4" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L10,4 L0,8 z" fill="#222222"/>
    </marker>

    <style>
      .construction-plan-title-v1 {
        font-family: Inter, Segoe UI, Roboto, Arial, sans-serif;
        font-size: 21px;
        font-weight: 700;
        fill: #111111;
      }

      .construction-plan-label-v1 {
        font-family: Inter, Segoe UI, Roboto, Arial, sans-serif;
        font-size: 16px;
        font-weight: 700;
        fill: #111111;
      }

      .construction-plan-small-v1 {
        font-family: Inter, Segoe UI, Roboto, Arial, sans-serif;
        font-size: 13px;
        fill: #333333;
      }

      .construction-plan-box-v1 {
        fill: #ffffff;
        stroke: #222222;
        stroke-width: 2;
      }

      .construction-plan-lightbox-v1 {
        fill: #ffffff;
        stroke: #999999;
        stroke-width: 1.5;
      }

      .construction-plan-arrow-v1 {
        stroke: #222222;
        stroke-width: 2;
        fill: none;
        marker-end: url(#arrowhead-construction-plan-v1);
      }

      .construction-plan-muted-line-v1 {
        stroke: #999999;
        stroke-width: 1.5;
        stroke-dasharray: 6 5;
        fill: none;
      }
    </style>
  </defs>

  <!-- Title -->
  <text x="70" y="52" class="construction-plan-title-v1">From discovery to construction plan</text>
  <text x="70" y="78" class="construction-plan-small-v1">Planning gives ambiguous work a flexible order without pretending the whole path is certain.</text>

  <!-- Stage boxes -->
  <rect x="65" y="150" width="185" height="135" rx="18" class="construction-plan-lightbox-v1"/>
  <text x="95" y="185" class="construction-plan-label-v1">1. Discovery</text>
  <text x="95" y="214" class="construction-plan-small-v1">business processes</text>
  <text x="95" y="236" class="construction-plan-small-v1">available information</text>
  <text x="95" y="258" class="construction-plan-small-v1">existing artefacts</text>

  <rect x="290" y="150" width="185" height="135" rx="18" class="construction-plan-lightbox-v1"/>
  <text x="320" y="185" class="construction-plan-label-v1">2. Vision</text>
  <text x="320" y="214" class="construction-plan-small-v1">business intent</text>
  <text x="320" y="236" class="construction-plan-small-v1">solution hypothesis</text>
  <text x="320" y="258" class="construction-plan-small-v1">ambitious but grounded</text>

  <rect x="515" y="150" width="185" height="135" rx="18" class="construction-plan-lightbox-v1"/>
  <text x="545" y="185" class="construction-plan-label-v1">3. Scope</text>
  <text x="545" y="214" class="construction-plan-small-v1">selected processes</text>
  <text x="545" y="236" class="construction-plan-small-v1">dependencies</text>
  <text x="545" y="258" class="construction-plan-small-v1">rough estimate</text>

  <rect x="740" y="150" width="185" height="135" rx="18" class="construction-plan-box-v1"/>
  <text x="770" y="185" class="construction-plan-label-v1">4. Build</text>
  <text x="770" y="214" class="construction-plan-small-v1">sequenced releases</text>
  <text x="770" y="236" class="construction-plan-small-v1">features + backend</text>
  <text x="770" y="258" class="construction-plan-small-v1">metadata + tests</text>

  <!-- Arrows -->
  <path d="M250 218 L290 218" class="construction-plan-arrow-v1"/>
  <path d="M475 218 L515 218" class="construction-plan-arrow-v1"/>
  <path d="M700 218 L740 218" class="construction-plan-arrow-v1"/>

  <!-- Commitment / flexibility axis -->
  <line x1="95" y1="365" x2="895" y2="365" class="construction-plan-muted-line-v1"/>
  <path d="M95 365 L895 365" class="construction-plan-arrow-v1"/>

  <text x="95" y="342" class="construction-plan-small-v1">low commitment</text>
  <text x="760" y="342" class="construction-plan-small-v1">higher commitment</text>

  <text x="95" y="405" class="construction-plan-label-v1">Flexible order</text>
  <text x="95" y="430" class="construction-plan-small-v1">The plan becomes more specific as discovery continues.</text>
  <text x="95" y="452" class="construction-plan-small-v1">Only the next few releases need detailed planning.</text>

  <rect x="575" y="398" width="350" height="72" rx="18" class="construction-plan-lightbox-v1"/>
  <text x="605" y="428" class="construction-plan-label-v1">Construction plan</text>
  <text x="605" y="452" class="construction-plan-small-v1">ordered enough to move, flexible enough to revise</text>

</svg>
{{< /svg >}}

<div style="max-width:44rem;text-align:center;font-size:0.95rem;color:#666;margin-top:0.5rem;">
Figure 1. Construction planning moves from discovery to vision, scope, and build. The plan becomes more specific as commitment increases, but remains flexible enough to adapt as discovery continues.
</div>

### Stage 1—Discovery

Formulating a plan begins with discovering facts about the business. The purpose of discovery is to answer key questions. At the highest level, these include:

- What are the major business processes in the end-to-end business lifecycle?
- What information is captured by each process, and where is it stored?
- What is the stakeholders’ interest in each process?
- What reporting artefacts already exist, and how are they currently used in workflows?

The team answers these questions by reviewing artefacts relevant to the business processes and interviewing stakeholders.

To sharpen the focus on business objectives, the team should also answer:

- Intent: What is the business intent?
- Measure: How does the business measure the achievement of this intent, either directly or indirectly?
- Sensor: What instruments does the business have for knowing whether things are going well or not?
- Controls: What levers does the business have to influence this measure?
- Drivers: What external events outside the business’s control may influence this measure?

The outputs of discovery should be expressed as linear process diagrams and cumulative information diagrams, as explained in the chapter [Anticipating questions](/docs/presenting-insights/anticipating-questions/#all-the-facts).


### Stage 2—Vision

A vision translates discovery into a statement of what the data product is trying to make visible. It should cover the business process at the right level: broad enough to guide future questions, but concrete enough to shape delivery.

For example, if the core business processes for an organisation are manufacturing, quality control, sales, shipping, and customer feedback, the vision statement could be:

```md
Understand the factors that drive sales profit and customer satisfaction through an integrated data source covering manufacturing, quality control, sales, shipping, and customer feedback, so the business can monitor manufacturing turnaround, detect quality issues early, understand sales trends, improve shipping efficiency, and respond to customer sentiment.
```

This vision statement is ambitious yet grounded. It resonates with business stakeholders, inspires confidence, and establishes trust by demonstrating that the project team understands the business. Being neither too vague nor too specific, the vision frames the project at the right level for prioritisation and dialogue.

Such vision statements are easy to craft and extend naturally from the discovery questions. Yet many teams produce poor alternatives that lead projects to failure. For example, it is common to see vision statements such as:

```md
Reduce pain points of manual processes and create near real-time dashboard of the operation.
```

This is not a deep analysis of business intent but a reaction to user complaints. As such, it lacks the substance to serve as a foundation for the project.

As part of vision setting, it is important to sketch pen-and-paper wireframes of sample reports that users can build from the data. The wireframe is a playback of what the team has heard, and the beginning of a [solution hypothesis](/docs/judgement-under-ambiguity/working-with-stakeholders/#gather-around-the-solution). Its purpose is to build trust that the team has understood the need and to inspire the project to strive for the finish line. It is akin to an artistic model of a public building before construction. A good model generates excitement and builds public confidence. To achieve this purpose, the wireframe itself needs to be ambitious yet grounded.

When the vision is framed this way, defining the project scope becomes straightforward.

### Stage 3—Scope

The vision is an ambition to cover the business processes end to end. It is a statement of the linear process diagram.

The full vision may be too large to tackle in one project. The scope defines a subset of business processes to focus on. For example, rather than covering manufacturing through to customer feedback, the project scope may concentrate on manufacturing and quality control, or on priorities such as sales and shipping. Dividing the vision this way allows the creation of project phases: the first phase focuses on two business processes, the second on the next two, and so on.

The selection of business processes should consider three factors.

1. Availability of source data. If the information captured by a business process resides in systems that are difficult to access, it may need to be deferred to later phases.

2. Order of the business lifecycle. Where possible, work in the natural sequence: manufacturing, then quality control, then sales, and so forth. Information accumulates along the lifecycle, and working in the same order creates building blocks for the next stage.

3. Business priorities. These often pull toward the tail end of the lifecycle, where most activity occurs. The data engineer must judge based on dependencies. For example, starting with sales without manufacturing may be acceptable, but starting with shipping without sales orders is not—no matter how much users want insights on shipping delays.

The cumulative information diagram, which tracks the flow of information and its storage, is useful for informing scope decisions.

The scope must include a time estimate for project completion. This requires input from an experienced engineer who can make a judgement based on discovery findings.

Like the vision statement, the scope is a straightforward application of the linear process diagram.

A common error is to scope by system. For example, rather than working through the business process one by one, the team works through integrating systems one by one. This is the wrong perspective. One reason is that it easily leads to an unusable product because the system does not contain the minimal set of information needed to describe a business process.

### Stage 4—Build

The final stage is the construction plan. This is the practical roadmap for delivery that translates scope into actionable steps and sets out how the project will progress.

A construction plan is akin to a six-month travel itinerary in a large country. The country is the organisation, and the towns are the major business processes. Features are the specific sites within a town. Building blocks are times of being en route, such as taking a long bus, while technical consolidation is the time of rest in the journey.

This travel itinerary is exploratory in nature, so it needs flexibility. But it also needs order so that the physical route makes sense and there is a continuous flow of experiences alternating with rest. This cannot be achieved if the itinerary is too vague: “Let’s see the country.” Nor can it be too detailed: “Here’s a long, ad hoc list of things we want to do all across the country in the next six months.” Instead, an orderly yet flexible itinerary sketches out the major towns and important sites, while the details of visiting a town only need to be fleshed out when getting close.

If the itinerary is well organised, it can be changed mid-way, such as swapping the order of towns or sites, with minimal disruption to the overall journey.

The same logic applies to construction planning.

#### Sequence by business process

At the highest level, build should proceed in the sequence of business processes. For example, if the scope includes manufacturing, quality control, sales, and shipping, then the build releases should follow this order, process by process. This contrasts with tackling a mix of manufacturing and sales, or sales and shipping, in one release.

If the data engineer finds this cannot be done, then the abstraction of business processes may need to be revisited. For example, if the data for sales and shipping is so entangled that they cannot be separated for build, then sales and shipping may be better understood as one process.

If possible, proceed in the same order as the business process. Avoid jumping to shipping and then doubling back to sales. However, if reverse order is necessary due to business priorities, then organising the build along the boundary of business processes can still avoid creating a mess.

#### Break work into small releases

The releases should be broken down within a business process. For example, a complex project may expect to build 50 tables in total. This may be divided into releases of 3 to 8 tables at a time. The more challenging the project, the smaller the release size.

Each release should be centred on a group of business information to expose. For example, if the scope is manufacturing, one release may focus on basic attributes such as product types, production status, and production date; another on manufacturing details such as material inputs and outputs; and another on aggregated information such as time to manufacture. In grouping releases, priority should be given to what is logical from a business point of view.

#### Build in pipeline order

Once defined, the construction plan must build in order of the pipeline by following table dependencies. This means a gradual increase in computation complexity.

For example, the first release may focus on basic attributes with little transformation. The second release may add more complex computation. A third release may aggregate information from prior tables. This is the natural progression for a data engineer following the filter → compute → reduce steps explained in [Creating information](/docs/creating-information/entity-processing/#building-the-pipeline).

This gradual layering of computation keeps complexity manageable and ensures each part is tested systematically along the way.

#### Interleave Power BI exposure

In a complex project with many attributes, it is risky to work on all the underlying tables and then all the Power BI tables and measures as one release.

Instead, Power BI releases should be interleaved as information is curated in the pipeline. This means features are surfaced to users continuously, so they get exposure to business attributes as soon as they are added to the pipeline.

User features are typically exposed through the self-service Power BI model.

#### Rotate features with consolidation

Releases should be tightly coupled with unit tests, fault tolerance, and metadata. Whenever a feature is released, unit tests and metadata should come with the release, rather than being handled as a bulk afterthought.

Releases should also be kept short in time—approximately two weeks, or three weeks at most. They need to be small enough for thorough code review.

In a construction plan, not all releases will be user features. There is also important backend work such as building blocks or performance tuning. It is important to earmark the feature releases because they are the key driver of project momentum. Users should know when features are coming and receive them continuously in small chunks.

User features should rotate with backend work. This keeps up project momentum, allows data engineers to spend time on quality consolidation, and gives users space to test features between releases.

#### Plan the near future in detail

By anchoring the construction plan on user features, and keeping in mind how releases build up into user features, it becomes easier to reshuffle development as priorities change without ending up in a tangled mess.

It is not necessary to forecast the plan in full detail for the entire project. This rigidity is not fit for the exploratory nature of data analytics. At any given moment, only the next few releases need to be planned in detail, while features further out do not need detailed planning.

For example, when working on manufacturing, the data engineer should know the plan for the next few releases to complete the work on manufacturing, while further processes such as sales and shipping may only need to be noted.

A construction plan designed in this manner is, like a good travel itinerary, both orderly and flexible.

The following is an example of a construction plan for manufacture and quality control.

{{< svg >}}
<svg xmlns="http://www.w3.org/2000/svg"
     width="980" height="700"
     viewBox="0 0 980 700"
     style="display:block;width:100%;max-width:44rem;height:auto;background:transparent"
     role="img"
     aria-label="Example construction plan document for manufacture and quality control">

  <style>
    .construction-plan-doc-title {
      font-family: Inter, Segoe UI, Roboto, Arial, sans-serif;
      font-size: 21px;
      font-weight: 700;
      fill: #111111;
    }

    .construction-plan-doc-label {
      font-family: Inter, Segoe UI, Roboto, Arial, sans-serif;
      font-size: 15px;
      font-weight: 700;
      fill: #111111;
    }

    .construction-plan-doc-small {
      font-family: Inter, Segoe UI, Roboto, Arial, sans-serif;
      font-size: 13px;
      fill: #333333;
    }

    .construction-plan-doc-mono {
      font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
      font-size: 11px;
      fill: #333333;
    }

    .construction-plan-doc-page {
      fill: #ffffff;
      stroke: #222222;
      stroke-width: 2;
    }

    .construction-plan-doc-line {
      stroke: #999999;
      stroke-width: 1.2;
    }

    .construction-plan-doc-darkline {
      stroke: #222222;
      stroke-width: 1.6;
    }
  </style>

  <!-- Page / artefact container -->
  <rect x="70" y="50" width="840" height="600" rx="18" class="construction-plan-doc-page"/>

  <!-- Header -->
  <text x="105" y="95" class="construction-plan-doc-title">Construction plan</text>
  <text x="105" y="122" class="construction-plan-doc-small">Example scope: manufacture and quality control</text>

  <text x="680" y="95" class="construction-plan-doc-label">Planning horizon</text>
  <text x="680" y="122" class="construction-plan-doc-small">Next five releases</text>

  <line x1="105" y1="150" x2="875" y2="150" class="construction-plan-doc-darkline"/>

  <!-- Column headers -->
  <text x="105" y="185" class="construction-plan-doc-label">Release</text>
  <text x="205" y="185" class="construction-plan-doc-label">Information focus</text>
  <text x="430" y="185" class="construction-plan-doc-label">Description</text>
  <text x="680" y="185" class="construction-plan-doc-label">Artefacts</text>

  <line x1="105" y1="202" x2="875" y2="202" class="construction-plan-doc-line"/>

  <!-- Column guide lines -->
  <line x1="180" y1="165" x2="180" y2="615" class="construction-plan-doc-line"/>
  <line x1="405" y1="165" x2="405" y2="615" class="construction-plan-doc-line"/>
  <line x1="655" y1="165" x2="655" y2="615" class="construction-plan-doc-line"/>

  <!-- Row 1 -->
  <text x="110" y="235" class="construction-plan-doc-label">1</text>
  <text x="205" y="230" class="construction-plan-doc-label">Manufacture core</text>
  <text x="205" y="252" class="construction-plan-doc-small">Basic manufacture tables</text>
  <text x="430" y="230" class="construction-plan-doc-small">Describe the manufacture process</text>
  <text x="430" y="252" class="construction-plan-doc-small">with metadata and minor clean-up.</text>
  <text x="680" y="226" class="construction-plan-doc-mono">Cake.Manufacture</text>
  <text x="680" y="244" class="construction-plan-doc-mono">Cake.RefManufactureSite</text>
  <text x="680" y="262" class="construction-plan-doc-mono">Cake.ManufactureStep</text>

  <line x1="105" y1="282" x2="875" y2="282" class="construction-plan-doc-line"/>

  <!-- Row 2 -->
  <text x="110" y="315" class="construction-plan-doc-label">2</text>
  <text x="205" y="310" class="construction-plan-doc-label">Manufacture SLA</text>
  <text x="205" y="332" class="construction-plan-doc-small">Milestones and timing</text>
  <text x="430" y="310" class="construction-plan-doc-small">Compute time-to-manufacture</text>
  <text x="430" y="332" class="construction-plan-doc-small">and compare against SLA.</text>
  <text x="680" y="306" class="construction-plan-doc-mono">Cake.ManufactureBatchMilestone</text>
  <text x="680" y="324" class="construction-plan-doc-mono">Cake.RefManufactureProductSla</text>

  <line x1="105" y1="362" x2="875" y2="362" class="construction-plan-doc-line"/>

  <!-- Row 3 -->
  <text x="110" y="395" class="construction-plan-doc-label">3</text>
  <text x="205" y="390" class="construction-plan-doc-label">Quality control core</text>
  <text x="205" y="412" class="construction-plan-doc-small">Testing and criteria</text>
  <text x="430" y="390" class="construction-plan-doc-small">Describe quality control with</text>
  <text x="430" y="412" class="construction-plan-doc-small">basic source tables.</text>
  <text x="680" y="386" class="construction-plan-doc-mono">Cake.SampleTesting</text>
  <text x="680" y="404" class="construction-plan-doc-mono">Cake.RefQualityControlCriteria</text>
  <text x="680" y="422" class="construction-plan-doc-mono">Cake.RefQualityControlResult</text>

  <line x1="105" y1="442" x2="875" y2="442" class="construction-plan-doc-line"/>

  <!-- Row 4 -->
  <text x="110" y="475" class="construction-plan-doc-label">4</text>
  <text x="205" y="470" class="construction-plan-doc-label">Quality control summary</text>
  <text x="205" y="492" class="construction-plan-doc-small">Batch outcome</text>
  <text x="430" y="470" class="construction-plan-doc-small">Aggregate criteria results</text>
  <text x="430" y="492" class="construction-plan-doc-small">including failure severity.</text>
  <text x="680" y="466" class="construction-plan-doc-mono">Cake.ManufactureBatchOutcome</text>
  <text x="680" y="484" class="construction-plan-doc-mono">Cake.RefBatchOutcome</text>

  <line x1="105" y1="522" x2="875" y2="522" class="construction-plan-doc-line"/>

  <!-- Row 5 -->
  <text x="110" y="555" class="construction-plan-doc-label">5</text>
  <text x="205" y="550" class="construction-plan-doc-label">Power BI exposure</text>
  <text x="205" y="572" class="construction-plan-doc-small">Facts, dimensions, measures</text>
  <text x="430" y="550" class="construction-plan-doc-small">Create views and expose</text>
  <text x="430" y="572" class="construction-plan-doc-small">the model to users.</text>
  <text x="680" y="546" class="construction-plan-doc-mono">PBI_VIEW.Manufacture</text>
  <text x="680" y="564" class="construction-plan-doc-mono">PBI_VIEW.QualityControl</text>
  <text x="680" y="582" class="construction-plan-doc-mono">Power BI measures</text>

  <!-- Footer note -->
  <line x1="105" y1="615" x2="875" y2="615" class="construction-plan-doc-darkline"/>
  <text x="105" y="637" class="construction-plan-doc-small">Ordered enough to move. Flexible enough to revise.</text>

</svg>
{{< /svg >}}

<div style="max-width:44rem;text-align:center;font-size:0.95rem;color:#666;margin-top:0.5rem;">
Figure 2. A construction plan is a delivery artefact. It gives the team a sequenced view of releases, information focus, descriptions, and artefacts without requiring the whole project to be specified in full detail.
</div>

## Reframing stakeholder requirements

A typical IT project is driven by stakeholder requirements. But stakeholder requirements cannot determine the whole plan, any more than a town planner can plan a town-build simply by collecting a list of requirements from citizens. On the contrary, the town planner is expected to contribute expertise in dialogue with the community.

In practice, stakeholder requirements swing between two extremes: too vague to guide development, or too specific so that the forest is lost for the trees. The delivery team should not react to the requirements and build the first thing that is asked.

Instead, the data engineer takes stakeholder input as part of a broader consideration for a data model that anticipates questions across end-to-end business processes.

This can be done by reframing stakeholder requirements as objectives about core business processes. If the requirements are too specific, such as a long list of details like “I want to see count of sales by product type,” they can be brought up a level by categorising them as objectives on sales. If the requirements are too vague, such as “I just want to know about my business,” they can be made more concrete by articulating objectives on key processes such as sales, manufacturing, or shipping.

In short, stakeholder requirements should be reframed to the level explained in the chapter [Anticipating questions](/docs/presenting-insights/anticipating-questions/). The delivery team has responsibility in guiding stakeholders comfortably on this journey, as described in [Working with stakeholders](/docs/judgement-under-ambiguity/working-with-stakeholders/).

## Conclusion


In traditional IT projects, data engineers are often treated as doers who implement specified rules. This is far from their full potential. Being closest to the data, they [actively shape how the organisation understands its business](/docs/foundations/data-and-organisations/#implications-for-data-engineering) by reorganising information at a fundamental level. The plan is one expression of that responsibility.

The data engineer—working with the delivery team—does not merely receive requirements and estimate tasks. The engineer helps turn uncertain business intent into a sequenced path of delivery. This path must be orderly enough to build confidence and flexible enough to adapt as discovery continues.

An effective plan lays the groundwork for success. In a complex project that requires a defined scope, a rough estimate is that:

- 50% of success is determined by the scope
- 35% by the construction planning
- 15% by the actual development work

This is no surprise. As developers mature, development becomes more mechanical and predictable. Familiarity with patterns makes implementation routine. The more experience builds, the more developers can foresee outcomes and issues in advance.

Success hinges increasingly on planning. The mark of an experienced data engineer is not merely the ability to build, but the ability to shape the work through an effective plan.


> [!NOTE]
> **Key ideas**
>
> Ambiguity does not justify meandering.
>
> Order does not require rigidity.
>
> A data engineer is responsible for shaping movement through uncertain work.
>
> A construction plan gives uncertain work enough order to proceed and enough flexibility to adapt.
>
> An effective plan is ambitious yet grounded, orderly yet flexible, and rotates new features with backend consolidation.
>
> A construction plan is formed through discovery, vision, scope, and build.
>
> Stakeholder requirements should be reframed as objectives about core business processes.
>
> The mark of an experienced data engineer is an effective plan.
