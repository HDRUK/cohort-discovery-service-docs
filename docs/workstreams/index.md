---
title: Workstreams
description: Overview of the three onboarding workstreams for the Cohort Discovery Service
tags:
  - onboarding
  - workstreams
---

# Workstreams

Onboarding to the Cohort Discovery Service requires completing three core workstreams. These can be run in parallel, though some interdependencies exist.

<div class="grid cards" markdown>

- :material-shield-check: **Governance**

    ---
    Obtain consent, complete local approvals, and conduct risk assessments.

    [:octicons-arrow-right-24: Governance](governance.md)

- :material-database-arrow-right: **Data**

    ---
    Extract, map to OMOP, and ETL your data to the secure environment.

    [:octicons-arrow-right-24: Data](data.md)

- :material-server: **Infrastructure**

    ---
    Set up your secure network area and install query retrieval software.

    [:octicons-arrow-right-24: Infrastructure](infrastructure.md)

</div>

---

## Interdependencies

```mermaid
graph LR
    G1[G1: Data Controller Consent] -->|"Required before\nlive data"| I3[I3: Connect OMOP\nto Query Tool]
    D1[D1: Extract Data] --> D2[D2: Map to OMOP]
    D2 --> D4[D4: ETL to OMOP DB]
    D4 --> I3
    I1[I1: Secure Network Area] --> I2[I2: Install Query Tool]
    I2 --> I3
```

*Figure 4 — Interdependencies between tasks for onboarding to Cohort Discovery*

![Task interdependency diagram showing sequencing constraints across the three workstreams](../images/figures/figure-4-task-interdependencies.png)

!!! warning "Key rule"
    **G1 (Data Controller Consent)** must be complete before live (non-synthetic) data is connected to Cohort Discovery. D1, D2, and D3 can proceed before G1.
