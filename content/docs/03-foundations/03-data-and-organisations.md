---
title: Data and organisations
url: /docs/03-foundations/03-data-and-organisations.md
description: TODO
draft: true
weight: 3
lede: TODO
---

## The central premise

Insight is information analysed in the light of intent. However, the data engineer starts one step further back than information. Data engineering starts with data.

Data is what is given before interpretation. It has no fixed meaning by itself, and is not yet information. More precisely:

> Data is a fragment of reality captured by process.

Consider a customer whose seat is cancelled because a flight was overbooked. The experience is real, but it is internal to the customer. The decision-maker does not know about it unless the experience is captured as data and made available to someone who was not there.

Without data, a decision-maker attempting to understand overbooked flights must rely on guesswork, intuition, anecdote, or high-profile complaints. These can all be important, but none is systematic.

The same applies to shopping experiences, cargo delays, transactions, legal decisions, medical observations, and countless other events. Nothing becomes systematically available to an organisation unless it is recorded as data.

This definition means data is neither reality itself nor mere record-keeping. It sits between the world and the organisation’s understanding of the world.

This becomes especially important at scale. In a small organisation, leaders may retain a direct sense of what is happening. In a large organisation, that direct visibility breaks down. Data becomes the means by which reality remains visible across distance, hierarchy, and complexity.


## How is data captured?

Data is captured by process.

This creates two sources of imperfection. The first is the process. The second is the capture. Between both sits the digital system: the medium through which business activity is encoded into data.

A process may be imperfect because it was designed for operational work rather than analytical understanding. Most workflows exist to get something done. The digital systems that support those workflows are usually built around that operational goal.  Therefore, the process may not try to record everything a future analyst may need for business intent. This is especially the case when the source of data is not controlled by the business seeking to analyse it.

The capture itself may also be imperfect. It can be technically difficult, costly, or impractical to record business events accurately. This challenge is intensified by a rapidly evolving technological landscape. 

Data is therefore never a simple copy of the world. It is an imperfect projection of the real world onto the data world. The work of the data engineer begins by understanding these imperfections. 


## How is data used?

Data is captured by business processes. Once collected, it can be used to return understanding to the business. 

In this perspective, data engineering is the task of taking data projected by business processes and refashioning it into a shape required by business intent.

At the simplest level, this can be summarised in the schematic:

> Business world → Data world → Business world

{{< svg >}}
<svg xmlns="http://www.w3.org/2000/svg"
     width="700" height="420"
     viewBox="0 0 700 420"
     style="background:#ffffff"
     role="img"
     aria-label="Business world projected into the data world and returned to business understanding">

  <defs>
    <marker id="arrowhead-world" markerWidth="10" markerHeight="8"
            refX="10" refY="4" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L10,4 L0,8 z" fill="#222222"/>
    </marker>
  </defs>

  <!-- Top world -->
  <g transform="translate(350,80)">
    <circle cx="0" cy="0" r="70"
            fill="#ffffff"
            stroke="#222222"
            stroke-width="1.8"/>

    <text x="0" y="-6"
          text-anchor="middle"
          font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
          font-size="20"
          font-weight="700"
          fill="#111111">
      Business world
    </text>

    <text x="0" y="22"
          text-anchor="middle"
          font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
          font-size="14"
          fill="#555555">
      events, actions, entities
    </text>
  </g>

  <!-- Middle world -->
  <g transform="translate(350,210)">
    <circle cx="0" cy="0" r="70"
            fill="#ffffff"
            stroke="#222222"
            stroke-width="1.8"/>

    <text x="0" y="-6"
          text-anchor="middle"
          font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
          font-size="20"
          font-weight="700"
          fill="#111111">
      Data world
    </text>

    <text x="0" y="22"
          text-anchor="middle"
          font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
          font-size="14"
          fill="#555555">
      records, tables, systems
    </text>
  </g>

  <!-- Bottom world -->
  <g transform="translate(350,340)">
    <circle cx="0" cy="0" r="70"
            fill="#ffffff"
            stroke="#222222"
            stroke-width="1.8"/>

    <text x="0" y="-6"
          text-anchor="middle"
          font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
          font-size="20"
          font-weight="700"
          fill="#111111">
      Business world
    </text>

    <text x="0" y="22"
          text-anchor="middle"
          font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
          font-size="14"
          fill="#555555">
      understanding, judgement, action
    </text>
  </g>

  <!-- Down arrow -->
  <line x1="350" y1="150"
        x2="350" y2="130"
        stroke="#222222"
        stroke-width="2.2"
        marker-end="url(#arrowhead-world)"/>

  <!-- Up arrow -->
  <line x1="350" y1="290"
        x2="350" y2="270"
        stroke="#222222"
        stroke-width="2.2"
        marker-end="url(#arrowhead-world)"/>

  <!-- Labels -->
  <text x="385" y="145"
        font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
        font-size="14"
        font-weight="600"
        fill="#111111">
    projection
  </text>

  <text x="385" y="285"
        font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
        font-size="14"
        font-weight="600"
        fill="#111111">
    interpretation
  </text>

</svg>
{{< /svg >}}

<div style="text-align: center; font-size: 0.95rem; color: #666; margin-top: 0.5rem;">
Figure 1. Business reality is projected into the data world, then interpreted back into business understanding.
</div>


## The organisation agency cycle

In summary, data is the interface through which organisations encounter reality. In most  This interface revolves around three central components: business processes, digital systems, and captured data.

These components form a cycle. Business processes define digital systems. Digital systems collect data. That data then feeds back into business understanding, influencing future decisions and actions. Business intent evaluates this evolution.

This relationship is illustrated in the agency cycle, Figure 1.


{{< svg >}}
<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600" viewBox="0 0 800 600"
     style="background:#ffffff" role="img"
     aria-label="Policy, Business, Digital, Data cycle with Defines, Collect, Informs transitions">

  <rect x="0" y="0" width="800" height="600" fill="#ffffff"/>

  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="8"
            refX="10" refY="4" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L10,4 L0,8 z" fill="#222222"/>
    </marker>
  </defs>

  <!-- Intent -->
  <text x="400" y="70" text-anchor="middle"
        font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
        font-size="20" font-weight="700" fill="#111111">Business intent</text>
  <line x1="260" y1="86" x2="540" y2="86"
        stroke="#bbbbbb" stroke-width="1.4"/>

  <!-- Dotted structural guide -->
  <circle cx="400" cy="320" r="170"
          fill="none" stroke="#c8c8c8"
          stroke-width="1.8" stroke-dasharray="3 6"/>

  <!-- Nodes -->
  <!-- Business (Expectation) -->
  <g transform="translate(400,150)">
    <circle cx="0" cy="0" r="54"
            fill="#ffffff" stroke="#222222" stroke-width="1.6"/>
    <text x="0" y="6" text-anchor="middle"
          font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
          font-size="18" font-weight="600" fill="#111111">Business</text>
  </g>

  <!-- Digital (Effort) -->
  <g transform="translate(550,410)">
    <circle cx="0" cy="0" r="54"
            fill="#ffffff" stroke="#222222" stroke-width="1.6"/>
    <text x="0" y="6" text-anchor="middle"
          font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
          font-size="18" font-weight="600" fill="#111111">Digital</text>
  </g>

  <!-- Data (Effect) -->
  <g transform="translate(250,410)">
    <circle cx="0" cy="0" r="54"
            fill="#ffffff" stroke="#222222" stroke-width="1.6"/>
    <text x="0" y="6" text-anchor="middle"
          font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
          font-size="18" font-weight="600" fill="#111111">Data</text>
  </g>

  <!-- Arrows (clockwise) -->
  <path d="M 440 190 A 170 170 0 0 1 510 360"
        fill="none" stroke="#222222" stroke-width="2.2"
        marker-end="url(#arrowhead)"/>

  <path d="M 510 450 A 170 170 0 0 1 290 450"
        fill="none" stroke="#222222" stroke-width="2.2"
        marker-end="url(#arrowhead)"/>

  <path d="M 290 360 A 170 170 0 0 1 360 190"
        fill="none" stroke="#222222" stroke-width="2.2"
        marker-end="url(#arrowhead)"/>

  <!-- Edge labels -->
  <!-- Business -> Digital -->
  <text x="530" y="245" text-anchor="middle"
        font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
        font-size="15" font-weight="600" fill="#111111">Defines</text>

  <!-- Digital -> Data -->
  <text x="400" y="525" text-anchor="middle"
        font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
        font-size="15" font-weight="600" fill="#111111">Captures</text>

  <!-- Data -> Business -->
  <text x="260" y="245" text-anchor="middle"
        font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
        font-size="15" font-weight="600" fill="#111111">Feedback</text>

</svg>
{{< /svg >}}
<div style="text-align: center; font-size: 0.95rem; color: #666; margin-top: 0.5rem;">
Figure 1. Business intent defines business process, business process defines digital systems, digital systems capture data, and data feeds back into business understanding.
</div>

The cycle also shows both the work and the organisational influence of the data engineer.

It shows the work because the data engineer reshapes imperfectly captured data so it can feed back into business understanding. It shows the influence because this feedback determines what the organisation can see about itself and reality. 

Data engineering is not one capability among others. It is the capability through which other capabilities become visible.

> [!NOTE]
> **Key ideas**
>
> Data is a fragment of reality captured by process.
>
> At scale, data is the means by which reality remains visible.
>
> Data engineering shapes the feedback through which organisations understand themselves.
