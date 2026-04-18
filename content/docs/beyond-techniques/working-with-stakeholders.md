---
title: Working with stakeholders
weight: 2
draft: true
---

The most common cause of project failure is the inability of the delivery team to build momentum with stakeholders. When momentum stalls, two patterns can often be found. The first is when the delivery team asks stakeholders for a list of "reporting requirements," but the stakeholders struggle to provide one. From their perspective, the richness of their business cannot be reduced to a simple checklist. When the team insists on detailed requirements, the process reaches a stalemate. The second pattern appears more promising at first. Stakeholders provide a clear list of requirements upfront—sales aggregated by date or region, non-compliance by product type, even precise business definitions. The delivery team implements these, and all seems well. Yet during testing, the product does not meet its purpose. It lacks core features, breaks on edge cases, or proves too complex to use. Both scenarios share the same flaw of reacting to requirements. Despite its obvious and repeated failure, this pattern persists. The reason for this persistence is because experts are often familiar with the intricacies of their own discipline but underestimate the challenges of others, expecting simplistic answers for everything else to be given in clear-cut form so they can proceed with their part. The world is not so straightforward. The most difficult part of a data project is not technical complexity but in thinking deeply about the business and its relationship with the data world. Asking stakeholders to enumerate requirements is convenient for delivery teams because it shifts the responsibility for this deep thinking to stakeholders, leaving developers with the easier task of implementing clear technical rules. Instead, in a successful project, the delivery team guides stakeholders to express their intent, then works together to explore the data in light of that business intent. Through this process, the stakeholders uncover what they need to "see" from the data for them to achieve business outcomes. These discovered needs—not an initial list—are the real requirements. This shift turns a one-way process into a two-way dialogue where the delivery team plays a leading role by guiding collective attention. The fourth principle of data engineer is therefore: instead of reacting to requirements, build momentum through guiding attention.

## Guided attention

During development, the delivery team and stakeholders explore the data together to meet business intent. The delivery team contributes expertise by guiding the stakeholders in how they should "see" the data in light of business intent—hence guided attention. This dialogue is an iteration between business and data, between questions and answers, between thinking and testing, and between business and

technical expertise. The seven principles that follow provide a practical framework for making this a success:

1. Focus on trust

2. Lead by listening

3. Own the business intent

4. Anchor a vision

5. Gather around the solution

6. Design for workflows

7. Spot the 20%

Focus on trust Many assume that the primary mode of requirements gathering is that of extracting information. In this view, the question becomes: "How effectively and accurately can I get the information from stakeholders to build a product?" This is the wrong focus. The first responsibility of a delivery team is to gain the stakeholder’s trust. The reasons for focus on growing trust are:

1. Trust is the context for information. Clearly articulating and refining

requirements is arduous. Stakeholders will not be able to give the right information before they have first established a strong trust in the people asking for the information.

2. Relationship with others is the biggest factor for meaningful and enjoyable work.

Strong relationships with stakeholders are more likely to lead to enjoyable collaboration during the development phase, and subsequently the success of the team.

3. The focus on extracting information sees the stakeholders instrumentally as a

vehicle for information. The focus on growing trust sees stakeholders as human beings as an end-to-themselves with whom we work.

4. Delivery teams have recurring partnerships with stakeholders that extend

beyond a particular project. The focus on building trust takes the long-term view. Without trust, no data project can succeed. After each engagement, the question should not be "Do we know more about the requirements?" but "Do our stakeholders trust us more?" The best ways to grow trust are transparency and active listening.

- Transparency means clear communication of the construction plan and regular

demonstrations of progress—weekly or twice-weekly. This is akin to a home buyer seeing the building take shape.

- Active listening means thoughtful paraphrasing and summarising stakeholder

input. When stakeholders hear their own language reflected, they feel understood and affirmed. This also happens when they are invited to check metadata, which gives them a tangible way to contribute. A common mistake is for delivery teams to assume that the purpose of speaking is to transfer information—if they already know what stakeholders are about to say, then they can skip to the next part. This is a mistake. Beneath the surface, the stakeholder is:

1. 2. 3. Developing a feeling of being heard.

Clarifying their own thinking through articulation. Growing in data literacy through dialogue with technical experts. All these build trust. By remembering that the first responsibility of the team is to gain trust, we resist the temptation to cut people off or jump in to correct them. Patience is paramount. Lead by listening In some types of partner dancing, there are two designated roles: Lead and Follow. The Lead initiates all the movements and the Follow completes the sequence with an elegant response. An analogous dynamic is needed with stakeholders. The delivery team should formulate its own statements as responding gracefully to a previous statement from stakeholders. These responses typically take one of the following forms:

- Clarifying question: "You said X, can you please clarify whether X means...?" or

"You said your team needs X—can you help us understand how this fits into your goal?"

- Playback: "There’s a lot in what you just said—can I paraphrase to check I’m on

the right track?" or "I’ve summarised your explanation into workflows—can I share them for confirmation?"

- Proposal: "Based on what you said about your workflows, here are wireframes

of our solution hypothesis—does this align?"

- Amendment: "You gave feedback on our hypothesis—here’s a refinement. What

do you think?" By responding to stakeholder initiatives, the delivery team is, in reality, leading. This is achieved by listening closely to what has been said and naturally guiding the stakeholder’s attention through a technical problem. This approach ensures:

- Stakeholders are heard, feel heard, and are seen to be heard.

- The conversation remains structured, logical, and focused on business

objectives. There will be times when the team needs to correct an error, redirect focus, or counter unconscious bias. This principle still applies. A common scenario is when stakeholders describe solutions before the problem is fully explored—for example, asking for a detailed data dump dashboard when analysis suggests a summarised view is better. Saying "Let’s focus on requirements instead of jumping to the solution" sounds natural but often feels dismissive. For stakeholders, the solution is the requirement. Regardless of content, stakeholders are trying to communicate something important. This should always be affirmed. Even if the content is incorrect, the underlying intent is valuable. Respond by continuing with their initiative rather than breaking off. For example:

- Explore the intent: "You said your goal is to detect potential non-compliance—

how does the data dump help?"

- Explore the utility: "You want a detailed data dump—can you give an example

of a workflow where this is used?"

- Re-orient: "Thanks for raising the data dump idea. You previously said your goal

is detecting non-compliance. Can we explore scenarios where that happens, then revisit the data dump in that context?" These approaches respect intent and apply the first principle: focus on trust. It also applies the fifth principle: gather around the solution. This principle should never be used as a shield for blame ("I just did what you told me to do"). Own the business intent The task of data engineering is to align data to business intent. It is an experimental process that demands the data engineer see the stakeholder’s perspective "firsthand." Without this, the team will never truly see what the stakeholder sees, and the potential of the solution will remain unrealised. This act of viewing the data through the stakeholder’s lens is owning the business intent. The data engineer who owns the business intent must be committed to in-depth business analysis. This document is not a guide to business analysis, except to note that business processes often conform to recurring patterns. Mastering these patterns helps the team achieve high-quality analysis quickly, even for complex scenarios. The team can do this by consistently asking stakeholders five key questions:

- Intent: What is the business intent?

- Measure: How does the business measure the achievement of this intent, either

directly or indirectly?

- Sensor: What instruments does the business have for knowing whether things

are going well or not?

- Controls: What levers does the business have to influence this measure?

- Drivers: What external events outside of does the business’s control may

influence this measure? Business analysis needs to permeate the project from start to finish. For example, concepts such as "good vs bad" entities or milestones for measuring processes are rarely defined in source systems. It is unrealistic to expect stakeholders to define these upfront before seeing the data. Instead, these definitions evolve through exploration and require input by technical expertise and experience with similar problems. This, once again, demands that the team see the business problem first-hand. Owning the business intent is an extension of the first principle of trust. Nothing gains trust with stakeholders as quickly as a team who can fluently speak the details of a business language. From this perspective, business analysis is a delivery team’s way of active listening. Whether a team owns the business intent will define its passion, drive, business knowledge, and creativity. These qualities will determine whether its output is a mediocre reflection of the current state or a solution that pushes the business forward to excellence. Anchor the vision The natural extension of owning the business intent is a vision for the business. A vision is a view of the value the team aspires to achieve. It is both ambitious and concrete. Whilst having a vision is important for any project, it is particularly critical in exploratory data projects for the following reasons:

- Improves the probability of arrival. Complex data projects are often

ambiguous and uncertain. Teams that articulate and revisit a vision are more likely to reach the intended outcome.

- Sustains engagement. Long projects involve hard work, such as resolving edge

cases. A clear vision inspires a sense of meaning to maintain engagement.

- Keeps debates in perspective. Under constraints, debates are inevitable and

can become flashpoints of tension. A vision keeps these debates in perspective. Teams often relax around specific problems when they see those problems as only one part of the whole.

- Structures discussion. Data projects are open-ended and can easily drift.

Anchoring the project in a vision, and deriving each step from that vision, keeps the team on track. Using the vision to structure discussions begins with agreement on the overall intent of the business. The project objective is situated within the business objective, which is itself a part of the broader organisation’s objectives. The discussion on each delivery feature should be anchored to this hierarchy, with constant reference back to the higher-level intent. When the conversation becomes lost, the team moves up one level and reorients. Example dialogue: Team & stakeholder: Introductions Stakeholder: Jumps into details about needing a dashboard Team: "Can you start by telling us the purpose of your business, your role, and what success means to you?" Stakeholder: Provides some context, still detailed Team: "So your organisation’s goal is to improve customer experience, and your team supports this by monitoring service quality?" Stakeholder: "Yes, but also…" Team: "Okay, so you track service quality, but you also need to identify recurring issues to prevent them. Is that right?" Stakeholder: "Yes…" Team: "At the start you mentioned a dashboard. What is its purpose in this context? Is it for your team’s internal use, or to share insights with other areas?" This pattern—bringing stakeholders up to the highest level and then unpacking details step by step—requires fast thinking and familiarity with the organisation’s goals. It is harder than it appears, but essential for clarity. When priorities conflict, reference to the higher-level intent provides common ground. Agreement is easier at higher levels and can be used to resolve issues. This approach works only when the conversation has been structured from the vision downward. Unlike a building project, which relies on well-defined specifications of the target building and strict timelines to track progress, data projects are exploratory and openended. In this setting, a clear vision, rather than detailed specifications, plays the role of guiding the team. It serves as a north star and compass that sustains quality and momentum across a long project. For this reason, team leaders should insist on vision, quality, and momentum rather than rigid deadlines.

Gather around the solution Data projects often waste time through too much talking and not enough doing. Instead, the best way to collaborate is to gather around a solution—start with a penand-paper solution hypothesis and refine it through discussion and experimentation. The project should develop hypotheses as early as possible, even by the second engagement. Early development matters because:

- A convincing solution is the only proof the team has understood the

requirements.

- Hypotheses provide a concrete point for clarifying stakeholder thinking.

- Refinement creates excitement as all parties see an early vision come to life.

A solution hypothesis is the most important part of requirements gathering because it is the only real proof the team has done the work. In an analogy of commissioning a building, it is futile if the builder only has a list of requirements (four rooms, lots of sunlight). The builder wins the contract by providing an architectural sketch—nothing less will do. No buyer would pay a mortgage deposit for a building without a sketch. Why expect stakeholders to work with a team without showing a solution hypothesis? When projects meander, it is often because direction is unclear. The best advice for such situations: "When the project is stuck, draw a picture of the solution." The best way to refine the solution hypothesis is through an open workbench format. In an open workbench, the delivery team and stakeholders meet twice a week to explore the data model, experiment with new features, test definitions, and provide feedback for the next iteration. Stakeholders may come from different business areas, making the data model a centre for converging perspectives. This format requires developers to be confident hosting discussions and responding to impromptu questions from stakeholders. The entire team should support them in doing so. When done well, the open workbench has a transformative effect: it builds trust through transparency and enables genuine dialogue. Teams sometimes say, "Let’s not jump into solution mode." This statement is not acceptable with stakeholders. For them, the solution is the requirement. When asked to describe requirements, most stakeholders are painting a mental picture of the solution. Even if it is a bad solution, it still describes what they imagine they are working toward. The team should playback the intent or seek clarification. The error is to draw a hard line between requirements and solution. This is a distinction developers make, not stakeholders. The real distinction is between the why (intent) and the what (solution). Stakeholders will often mix both. It is the team’s job to discern one from the other.

This cannot be stressed enough: to stakeholders, the solution is the requirement—not something separate from it. In a data project, it is never too early to gather around the solution. Gathering around the solution is the ultimate way the delivery team guides stakeholders toward clarity. It helps them see how reshaped data interacts with business intent, turning abstract requirements into something tangible. Through iterative refinement—testing, visualising, and adjusting—the solution evolves until it displays fidelity with business reality. In doing so, attention is guided deliberately, ensuring that every discussion converges on what matters most: a solution that stakeholders can recognise, trust, and act upon. Design for workflows It is common for data projects to deliver reports that are rarely used. Stakeholders may specify many requirements— "I want to see count of X per country"—and show excitement during development and testing. Yet after deployment, usage often drops quickly. This happens when solutions are not anchored in real workflows. Anchoring a solution with workflows ensure that it will have usage when deployed. Every workflow has at least two elements: an intent and a trigger. As an example of a business working at the helpdesk, see Figure 1. Figure 1. Example of a workflow. A trigger can be a specific event (e.g., receiving an email from a customer) or a schedule (e.g., publishing a quarterly report). Contextualising requirements in workflows offers key advantages:

1. Ensures the product delivers value because it meets the intent of an established

workflow.

2. Ensures the product will be used because real-world triggers exist for its use.

3. Integrates the product seamlessly into the user’s daily role.

4. Helps stakeholders recognise when a requirement is not important and can be

dropped.

5. Provides a natural way to rationalise requirements—for example, one report

page per workflow. Designing for workflows is a simple tool to ensure that project teams are grounded in real world problems. Spot the 20% The 80/20 rule says 80% of results come from 20% of effort. Its flip side is that the remaining 20% consumes 80% of the effort. This creates an illusion that most work is done when the hardest part remains—the hidden, complex 20%. The 20/80 trap is dangerous because:

1. Foundational elements are missed until production.

2. Expectations are mismanaged when stakeholders think the work is complete.

3. Technical debt piles up when essentials are discovered late.

Teams avoid the trap by:

1. Grounding requirements in thorough business analysis to uncover hidden

assumptions.

2. Focusing equally on what works and what doesn’t—the parts that work are often

forgotten.

3. Asking not only "What should this do?" but "What could go wrong?"

4. Balancing common cases and edge cases without bias.

5. Developing in sound engineering order, not simply in the order stakeholders

want to see. As an analogy, home buyers focus on visible features—"How many rooms?" or "Is there good ventilation?"—based on obvious needs and past pain. A good builder starts with the foundation. Likewise, a good data team begins with the start of the business process and systematically work through the business processes in order, rather than jumping to flashy features. Because of this, the team will often run counter to stakeholder instincts. This is healthy. In effect, the team acts as:

- A counterweight to natural biases that overlook fundamentals.

- A safeguard against missed edge cases that matter.

Foreseeing hidden elements is hard. It takes strong business knowledge, technical experience, and high engagement skills to counter bias. Only the best teams do it well.

## Conclusion

The hardest part of any data project is thinking deeply about the business and how it relates to data. This can only be achieved when stakeholders and the delivery team explore the data together—thinking together through a dialogue focused on the solution. In this dialogue, the relationship is not symmetrical. Stakeholders, often new to data, do not know what to look for. This is why the experienced delivery team plays an important role in guiding the dialogue’s attention to relevant observations. The seven principles of engagement capture hard-earned wisdom for facilitating these dialogues. They run counter to ingrained habits that focus on visible details while ignoring complexity. They are treasures for any delivery team. The principles change the team’s view of engagement from receiving requirements and getting product sign-off to that of building trust with stakeholders. Trust is the guiding principle. Fluently speaking the business language establishes trust early in the project, gathering the solution and continuing to demonstrate progress on the business vision carries trust to the end. These principles move the team beyond reacting to requirements. Applied well, they enable the team to guide stakeholders through complexity and build momentum toward a solution that truly meets business intent.
