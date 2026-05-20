---
title: What is data?
url: /docs/03-foundations/02-what-is-data/
description: "A short philosophical foundation for the book: data is a fragment of reality captured by process, and that premise shapes everything that follows in data engineering practice."
draft: true
weight: 2
lede: Data is a fragment of reality.
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
<!-- 
This is why the process that creates the data may differ from the business interest that later seeks to analyse it.

The capture itself may also be imperfect. It can be technically difficult, costly, or impractical to record business events accurately. Some events are too complex to capture fully. Some occur across multiple systems. Some depend on human judgement. Some change faster than the system can adapt.

This challenge is intensified by a rapidly evolving technological landscape. Business processes increasingly span cloud platforms, SaaS tools, legacy systems, APIs, spreadsheets, machine-generated logs, and AI-assisted workflows. Each may capture a different fragment of the same underlying reality, with different assumptions, constraints, and levels of reliability.

Data is therefore never a simple copy of the world. It is a fragment of reality captured through a process, mediated by a digital system, and shaped by the purpose, limitations, and cost of capture.

The work of the data engineer begins by understanding these imperfections. -->


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
        font-size="20" font-weight="700" fill="#111111">Intent</text>
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
        font-size="15" font-weight="600" fill="#111111">Collects</text>

  <!-- Data -> Business -->
  <text x="260" y="245" text-anchor="middle"
        font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
        font-size="15" font-weight="600" fill="#111111">Feedback</text>

</svg>
{{< /svg >}}

> [!NOTE]
> **Key ideas**
>
> Data is a fragment of reality captured by process.
>
> At scale, data is the means by which reality remains visible.
