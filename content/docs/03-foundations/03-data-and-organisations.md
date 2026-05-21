---
title: Data and organisations
url: /docs/03-foundations/03-data-and-organisations/
description: "Explains how data helps organisations understand both their environment and themselves, and why data definitions become sites of organisational meaning."
weight: 3
lede: Data helps organisations see themselves.
---

## Data and organisational self-understanding

Data helps organisations perceive reality. This includes the reality of the environment in which they operate, but also the reality of the organisation itself.

Understanding this matters not only for why data engineering is valued, but for how it is done in practice. The veteran data engineer instinctively works within the entanglement between data and organisation.

To understand this, it is useful to visualise an organisation as a feedback loop.


## The organisation agency cycle

Data is a fragment of reality captured by process. This can be interpreted as a feedback loop around three components: business processes, digital systems, and captured data.  Business processes define digital systems. Digital systems collect data. That data, representing reality, then feeds back into business understanding, influencing future decisions and actions. This relationship is illustrated in Figure 1.


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

Like many cycles, an organisation's feedback loop can become vicious or virtuous. Business intent is the determinant. An organisation moving toward its intent is in a virtuous cycle; an organisation drifting away from its intent is in a vicious cycle.

The feedback loop is therefore a model of how an organisation exercises its goals in the world. It is an **agency cycle**.

The agency cycle also shows both the work and the organisational influence of the data engineer.

It shows the work because the data engineer reshapes imperfectly captured data in light of intent, so it can feed back into business understanding. It shows the influence because this feedback determines what the organisation can see about itself.

Consequently, data is one way an organisation perceives itself. Data engineering is not one capability among others. It is the capability through which other capabilities become visible.


> [!NOTE]
> **Key ideas**
>
> Data is a fragment of reality captured by process.
>
> At scale, data is the means by which reality remains visible.
>
> Data engineering shapes the feedback through which organisations understand themselves.
