---
title: Construction planning
description: Shows how to turn discovery, vision, and scope into a practical construction plan for data delivery.
lede: A strong construction plan creates momentum by giving delivery an orderly shape.
weight: 3
draft: true
---

The fourth principle of data engineering is to build momentum through guiding attention rather than reacting to requirements. This can be challenging in projects that are lengthy and overwhelmingly complex. In such cases, the engineer often feels at a loss for where to begin. Because the data engineer sits on the critical path of data projects, this uncertainty directly impacts project momentum. Conversely, a data engineer who delivers outputs in an orderly and predictable way propels the project forward— participants align on the goal and instinctively sense that the team is taking concrete steps toward achieving it. In complex projects, a data engineer stays organised and guides the delivery team by formulating a plan. This plan is expected from an experienced engineer because:

1. 2. 3. No project waits in silence. The engineer cannot disappear for a month to apply

ideal patterns and return later. Unless the engineer provides the team and sponsors with confidence about the weeks or months ahead, there will be no engineering work at all. Logical sequencing matters in a build. Doing tasks in a sensible order helps the engineer move forward with confidence, avoids code entanglement, and reduces mistakes. Only the engineer knows the effort required. The data engineer alone understands how long quality work takes and has the sole responsibility to advocate for that time. If the engineer does not actively formulate a plan, there will be no plan—leading the project to meander. Or someone else will create the plan for the engineer—leading the project to rush. In either case, the project suffers. Projects can succeed or fail depending on the data engineer’s plan. It is one of the data engineer’s leadership roles when guiding stakeholders. Formulating a plan for the team is one of the most advanced skills to master and a mark of a confident engineer.

## An effective plan

A construction plan lays out, in sequence, the components the data engineer will build and provides a forecast for how long each part will take. This plan gives users a clear expectation of what features will arrive and when. In addition, a construction plan includes non-feature components such as unit tests, technical debt clean-up, and performance tuning. The plan defines the project’s momentum. A plan is effective if it provides the project with confidence and momentum. For this purpose, the focus is on sequence rather than precise timings. While it is important not to blow out project timelines, the sequence is more critical than exact estimates

because delivering one feature after another is strongly associated with user satisfaction and project momentum. An effective plan is akin to a travel itinerary for exploring a new country. An itinerary is not effective merely by meeting a predefined schedule; it is effective when it moves forward logically, providing a quality experience without wasting time. A data engineer can craft an effective plan by aiming for three characteristics:

- Ambitious yet grounded

- Orderly yet flexible

- Rotating new features with backend consolidation

Being ambitious means having a view to tackle the full business processes and designing a model that addresses all questions, rather than limiting the scope to specific requirements raised by current stakeholders. Being grounded means supporting this vision with well-informed business analysis so that the plan is neither vague nor impossible, and ensuring that necessary information is available for reliable time estimates. An orderly yet flexible plan is akin to a travel itinerary that is physically sensible (not looping back across half the country) but still organised into reasonable segments that can be shifted. For a data engineer, being orderly means isolating releases into promotes code clarity, avoid code entanglement, and minimises rework. Flexibility means structuring the plan so that key business priorities can shift forward or backward as a block without massively disrupting the schedule. This requires grouping deliverables into logical blocks centred on core business processes, rather than maintaining a long miscellaneous list of business questions. New features excite stakeholders and propel project momentum. However, the data engineer must balance these visible features with invisible but equally important consolidation work. An effective plan achieves both by alternating between them. This rotation not only supports quality work by building consolidation into the schedule but also gives stakeholders time to absorb one feature before moving on to the next. This immersion is necessary because data insights are exploratory in nature. Testing a new feature requires users to interact with the output, grasp its implications, and check edge cases thoroughly.

## Formulating an effective plan

A data engineer can craft an effective plan in four stages. Each stage involves increasing commitment to specific outcomes. A simple project may require only the first stage, while a complex project may demand a detailed plan at the fourth stage. The four stages are:

1. Discovery

2. Vision

3. Scope

4. Build

Stage 1 – Discovery Formulating a plan begins with discovering facts about the business. The purpose of discovery is to answer key questions. At the highest level, these include:

- What are the major business processes in the end-to-end business lifecycle?

- What information is captured by each process, and where is it stored?

- What is the stakeholders’ interest in each process?

- What reporting artefacts already exist, and how are they currently used in

workflows? The team answers these questions by reviewing artefacts relevant to the business processes and interviewing stakeholders. To sharpen the focus on business objectives, the team should also answer:

- Intent: What is the business intent?

- Measure: How does the business measure the achievement of this intent, either

directly or indirectly?

- Sensor: What instruments does the business have for knowing whether things

are going well or not?

- Controls: What levers does the business have to influence this measure?

- Drivers: What external events outside of does the business’s control may

influence this measure? The outputs of discovery should be expressed as linear process diagrams and cumulative information diagrams, as explained in the chapter Anticipating Questions. Recall that a linear process diagram is a simple diagram that lays out the major business processes in chronological order, without loops or branches. Its purpose is to give a clear, high-level view of the end-to-end flow, making it easy to see where each process fits in the overall lifecycle. A cumulative information diagram is a table that lists business information as rows and business processes as columns, showing which process captures or inherits each piece of information. This diagram helps identify what data is available at each stage and ensures completeness for answering business questions. Stage 2 – Vision The vision for all data engineering projects is the same: advance business intent by obtaining insights across all underlying business processes. This vision is adapted to each project using findings from the discovery phase, especially the linear process diagrams.

For example, if the core business processes for an organisation are manufacturing, quality control, sales, shipping, and customer feedback, the vision statement could be: "Understand the factors that drive sales profit and customer satisfaction through an integrated data source of complete business processes—from manufacturing, quality control, sales, shipping, to customer feedback. Obtaining timely and accurate insights into measures such as manufacturing turnaround, early detection of quality issues, changes in sales trend, efficiencies in shipping and latest customer sentiment." This vision statement is ambitious yet grounded. It resonates with business stakeholders, inspires confidence, and establishes trust by demonstrating that the project team understands the business. Being neither too vague nor too specific, the vision frames the project at the right level for prioritisation and dialogue. Such vision statements are easy to craft and extend naturally from the discovery questions. Yet many teams produce poor alternatives that lead projects to failure. For example, it is common to see vision statements such as: "Reduce pain points of manual processes and create near real-time dashboard of the operation." These statements are not a deep analysis of business intent but a reaction to user complaints. As such, they lack the substance to serve as a foundation for the project. As part of vision setting, it is important to sketch pen-and-paper wireframes of sample reports that user can build off the data. The wireframe is a play-back what the team has heard, and the beginning of a solution hypothesis. Its purpose is to build trust that the team has understood the needs and inspire the project to strive for the finish line. It is akin to an artistic model of a public building prior to build—a good model generates excitement and builds public confidence. To achieve this purpose, the wireframe itself needs to be ambitious yet grounded. When the vision is framed as above, defining the project scope becomes straightforward. Stage 3 – Scope The vision is an ambition to cover the business processes end to end. It is a visionary statement of the linear process diagram. The full vision may be too large to tackle in one project. The scope defines a subset of business processes to focus on. For example, rather than covering manufacturing through to customer feedback, the project scope may concentrate on the first two— manufacturing and quality control—or on priorities such as sales and shipping. Dividing the vision this way allows the creation of project phases: the first phase focuses on two business processes, the second on the next two, and so on.

The selection of business processes should consider three factors:

1. Availability of source data. If the information captured by a business process

resides in systems that are difficult to access, it may need to be deferred to later phases.

2. Order of the business lifecycle. Where possible, work in the natural

sequence—manufacturing, then quality control, then sales, and so forth. Information accumulates along the lifecycle, and working in the same order creates building blocks for the next stage.

3. Business priorities. These often pull toward the tail end of the lifecycle, where

most activity occurs. The data engineer must judge based on dependencies. For example, starting with sales without manufacturing may be acceptable, but starting with shipping without sales orders is not—no matter how much users want insights on shipping delays. The cumulative information diagram, which tracks the flow of information and its storage, is useful for informing scope decisions. The scope must include a time estimate for project completion. This requires input from an experienced engineer who can make a judgment based on discovery findings. Like the vision statement, the scope is a straightforward application of the linear process diagram. A common error is to scope by system. For example, rather than working through the business process one by one, the team works through integrating systems one by one. This is the wrong perspective. One reason, amongst many, is that it easily leads to a situation where the project creates an unusable product because the system does not have the minimal set of information to describe one business process. Stage 4 – Build The final stage is the construction plan. This is the practical roadmap for delivery that translates scope into actionable steps and sets out how the project will progress. A construction plan is akin to a six-month travel itinerary in a large country. The country is the organisation, and the towns are the major business processes. Features are the specific sites within a town. Building blocks are times of being en route, such as taking a long bus, while technical consolidation is the time of rest in the journey. This travel itinerary is exploratory in nature, so it needs flexibility, but it also needs order so that the physical route makes sense and there is a continuous flow of experiences alternating with rest. This cannot be achieved if the itinerary is too vague: "Let’s see the country." Nor can it be too detailed: "Here’s a long, ad hoc list of things we want to do all across the country in the next six months." Instead, an orderly yet flexible itinerary

sketches out the major towns and important sites, while the details of visiting a town only need to be fleshed out when getting close. If the itinerary is well organised, it can be changed mid-way, such as swapping the order of towns or sites, with minimal disruption to the overall journey. An engineer guiding stakeholders through a data project is akin to a tour guide crafting a travel itinerary for a traveller experiencing a country. The analogous concepts apply. The two primary considerations are: how the delivery is divided into releases, and the sequencing of those releases. At the highest level, build should proceed in the sequence of business processes. For example, if the scope includes manufacturing, quality control, sales, and shipping, then the build releases should follow this order, process by process. This contrasts with tackling a mix of manufacturing and sales, or sales and shipping, in one release. If the data engineer finds this cannot be done, then the abstraction of business processes may need to be revisited. For example, if the data for sales and shipping are so entangled that they cannot be separated for build, then it is arguable that sales and shipping in the organisation are better seen as one process. If possible, proceed in the same order as the business process. For example, avoid jumping to shipping and then doubling back to sales. However, if reverse order is necessary due to business priorities, then organising the build along the boundary of business processes can still avoid creating a mess. The releases should be further broken down within a business process. For example, a complex project may expect to build 50 tables in total; this may be divided into releases of 3 to 8 tables at a time. The more challenging the project, the smaller the release size. Each release should be centred on a group of business information to expose. For example, if the scope is manufacturing, one release may focus on basic attributes such as product types, production status, and production date; another release on manufacturing details such as material inputs and outputs; and another release on aggregated information such as time to manufacture. In grouping releases, priorities should be given to being as logical as possible from a business point of view. Once defined, the construction plan must build in order of the pipeline by following table dependencies. This means a gradual increase in computation complexity. For example, the first release focuses on basic attributes with little transformation, the second release adds more complex computation, and a third release aggregates information from prior tables. This is the natural progression for a data engineer following the filter -> compute -> reduce steps explained in Creating information. This gradual layering of computation keeps complexity manageable and ensures each part is tested systematically along the way.

In a complex project with many attributes, it is bad practice to work on all the underlying tables and then all the Power BI tables and measures as one release. Instead, Power BI releases should be interleaved as information is curated in the pipeline. This means that features are surfaced to users continuously, so they get exposure to business attributes as soon as they are added to the pipeline. Releases should be tightly coupled with unit tests, fault tolerance, and metadata. Whenever a feature is released, unit tests and metadata should come with the release, rather than as a bulk afterthought. Releases should be kept short in time—approximately two weeks, or three weeks at most. They need to be small enough for thorough code review. In a construction plan, not all releases will be user features. There is also important backend work such as building blocks or performance tuning. It is important to earmark the feature releases because they are the key driver of project momentum. Users should know when features are coming and receive them continuously in small chunks. User features are typically exposed to users in the self-service Power BI model. User features should rotate with backend work. Not only does this keep up project momentum, it allows data engineers to spend time on quality consolidation and gives users space to fully immerse in testing features between releases. By anchoring the construction plan on the user features, and keeping in mind how releases build up into a user feature, it becomes easier to reshuffle development as priorities change without ending up in a tangled mess. Finally, it is not necessary to forecast the plan in full detail for the entire project. This rigidity is not fit for the exploratory nature of data analytics. At any given moment, only the next four or so releases need to be planned in detail, while features further out do not need detailed planning. For example, when working on manufacturing, the data engineer should know the plan for the next few releases to complete the work on manufacturing, while the further processes such as sales and shipping only need to be noted. A construction plan designed in this manner is, like a good travel itinerary, both orderly and flexible. The following is an example of a construction plan for manufacture and quality control. Release Information focus Description Artefacts

1 Manufacture core tables Basic tables from source system to describe the manufacture process, with metadata and minor clean-up Cake.Manufacture Cake.RefManufactureSite Cake.RefManufactureStatus Cake.ManufactureStep Cake.RefProductType

2. Manufacture

SLA tables Define milestone points in the manufacture process, and compute time between milestones and totaltime-to-manufacture by aggregating over Cake.ManufactureStep, compare the results against SLA for different product types Cake.ManufactureBatchMilestone Cake.RefManufactureProductSla

3. Quality

control core tables Basic tables from source system to describe the quality control, with metadata and minor clean-up Cake.SampleTesting Cake.RefQualityControlCriteria Cake.RefQualityControlResult

4. Quality

control summary Aggregate results from different quality control criteria testing, to compute an overall result for a batch, with the concepts of failure severity Cake.ManufactureBatchOutcome Cake.RefBatchOutcome

5. Power BI

model for exposure Create the views that define the fact and dimension tables for a Power BI report, and expose them in a Power BI model with corresponding measures, including metatada Driver views for facts & dimensions: PBI_VIEW.Manufacture PBI_VIEW.QualityControl PBI_VIEW.ReportingCalendar PBI_VIEW.BatchOutcome PBI_VIEW.ProductType etc Corresponding Power BI tables: Manufacture, Quality control, Reporting calendar, Product type etc Measures

## Stakeholder requirements

A typical IT project is driven by stakeholder requirements. But stakeholder requirements cannot determine the whole plan, any more than a town planner can plan a town-build simply by collecting a list of requirements from citizens. On the contrary, the town planner is expected to contribute expertise in dialogue with community. In practice, stakeholder requirements swing between two extremes—too vague to guide development, or too specific so that the forest is lost for the trees. Consequently, the delivery team should not react to the requirements and build the first thing that is

asked. Such an approach is destined to lead to a tangled build if the requirements are too specific, or meandering if they are too vague. Instead, the data engineer takes stakeholder input as part of a broader consideration for a data model that anticipates questions across end-to-end business processes. This can be done by reframing stakeholder requirements as objectives about core business processes. If the requirements are too specific, such as a long list of details like "I want to see count of sales by product type," they can be brought up a level by categorising them as objectives on sales. If the requirements are too vague, such as "I just want to know about my business," they can be made more concrete by articulating objectives on key processes such as sales, manufacturing, or shipping. In short, stakeholder requirements should be reframed to the level explained in [Anticipating questions](/docs/presenting-insights/anticipating-questions/). The delivery team has responsibility in guiding the stakeholders comfortably on this journey as described in [Working with stakeholders](/docs/beyond-techniques/working-with-stakeholders/).

## Conclusion

In traditional IT projects, data engineers are often seen as "doers" who implement specified rules. This is far from their full potential. Being closest to the data, they actively shape how the organisation understands its business by reorganising information at a fundamental level. Data engineers are true influencers. This chapter continues the theme of a data engineer’s influence. In a high-intensity project, the data engineer—working with other team members—formulates a plan that not only addresses business requirements but reshapes them, using this plan to build project momentum. The data engineer is doing the build, and only the data engineer can craft the plan. The way to create an effective plan is to use the tools explained in Anticipating Questions: linear process diagrams and cumulative information diagrams. These tools break down organisational complexity into a level that is useful for all parties and especially conducive to the data engineer shaping data under these frames. In this sense, the linear process diagram becomes a common ground between business stakeholders and the delivery team for planning and prioritisation. An effective plan lays the groundwork for success. In a complex project that requires a defined scope, a rough estimate is that:

- 50% of success is determined by the scope

- 35% by the construction planning

- 15% by the actual development work

This is no surprise. As developers mature, development becomes more mechanical and predictable. Familiarity with patterns makes implementation routine. The more experience builds, the more developers can foresee outcomes and issues in advance.
