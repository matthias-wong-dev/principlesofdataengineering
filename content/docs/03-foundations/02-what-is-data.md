---
title: What is data?
url: /docs/03-foundations/02-what-is-data/
description: "A short philosophical foundation for the book: data is a fragment of reality captured by process, and that premise shapes everything that follows in data engineering practice."
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

The capture itself may also be imperfect. It can be technically difficult, costly, or impractical to record business events accurately. This challenge is intensified by a rapidly evolving technological landscape. 

Data is therefore never a simple copy of the world. It is an imperfect projection of the real world onto the data world. The work of the data engineer begins by understanding these imperfections. 


## How is data used?

Data is captured by business processes. Once collected, it can be used to return understanding to the business. 

In this perspective, data engineering is the task of taking data projected by business processes and reshaping it into a form required by business intent. This can be summarised in Figure 1.


{{< svg >}}
<svg xmlns="http://www.w3.org/2000/svg"
     width="760" height="520"
     viewBox="0 0 760 520"
     style="background:#ffffff"
     role="img"
     aria-label="Business world projects down into data world, and data world is refashioned back into business understanding">

  <defs>
    <marker id="arrowhead-world" markerWidth="10" markerHeight="8"
            refX="10" refY="4" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L10,4 L0,8 z" fill="#222222"/>
    </marker>
  </defs>

  <!-- Business world domain -->
  <ellipse cx="380" cy="145" rx="285" ry="58"
      fill="#ffffff"
      stroke="#222222"
      stroke-width="2"/>

  <text x="380" y="138"
      text-anchor="middle"
      font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
      font-size="25"
      font-weight="700"
      fill="#111111">
      Business world
  </text>

  <text x="380" y="163"
      text-anchor="middle"
      font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
      font-size="15"
      fill="#555555">
  reality, events, entities
  </text>

  <!-- Data world domain -->
  <ellipse cx="380" cy="390" rx="210" ry="48"
           fill="#ffffff"
           stroke="#222222"
           stroke-width="2"/>

  <text x="380" y="386"
        text-anchor="middle"
        font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
        font-size="23"
        font-weight="700"
        fill="#111111">
    Data world
  </text>

  <text x="380" y="410"
        text-anchor="middle"
        font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
        font-size="15"
        fill="#555555">
    records, tables, files
  </text>


  <!-- Projection arrow: business to data -->
  <path d="M 285 210 C 310 265, 330 305, 355 335"
        fill="none"
        stroke="#222222"
        stroke-width="2.4"
        marker-end="url(#arrowhead-world)"/>

  <text x="245" y="292"
        text-anchor="middle"
        font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
        font-size="15"
        font-weight="600"
        fill="#111111">
    projection
  </text>

  <!-- Shaping arrow: data to business -->
  <path d="M 430 335 C 465 305, 485 265, 505 210"
        fill="none"
        stroke="#222222"
        stroke-width="2.4"
        marker-end="url(#arrowhead-world)"/>

  <text x="535" y="292"
        text-anchor="middle"
        font-family="Inter, Segoe UI, Roboto, Arial, sans-serif"
        font-size="15"
        font-weight="600"
        fill="#111111">
    shaping
  </text>


</svg>
{{< /svg >}}

<div style="text-align: center; font-size: 0.95rem; color: #666; margin-top: 0.5rem;">
Figure 1. Business reality is projected into the data world, then shaped back into business understanding.
</div>

We will return frequently to the concepts illustrated in Figure 1 throughout this book.

> [!NOTE]
> **Key ideas**
>
> Data is a fragment of reality captured by process. At scale, data is the means by which reality remains visible.
>
> The data world can be seen as an imperfect projection of the business world.
>
> Data engineering reshapes the data world into forms the business world can use.