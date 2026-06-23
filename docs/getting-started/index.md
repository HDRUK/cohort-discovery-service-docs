---
title: Getting Started
description: Overview of what you need to know before onboarding to the Cohort Discovery Service
tags:
  - onboarding
  - getting-started
---

# Getting Started

This section helps Data Custodians understand what is involved in onboarding their datasets to the HDR UK Cohort Discovery Service.

!!! info "Who is this guide for?"
    A **Data Custodian** is any organisation onboarding data onto the Cohort Discovery Service — typically also the Data Controller, but not always. This could be an NHS Trust, university, or other healthcare organisation.

---

## What you will need to do

To make your data discoverable via Cohort Discovery, you must complete three parallel workstreams:

<div class="grid cards" markdown>

- :material-shield-check: **Governance**

    ---
    Obtain Data Controller consent, complete local approvals, and conduct any required technical risk assessments.

    [:octicons-arrow-right-24: Governance Workstream](../workstreams/governance.md)

- :material-database-arrow-right: **Data**

    ---
    Extract a subset of your data, map it to the OMOP Common Data Model, and ETL it to your secure environment.

    [:octicons-arrow-right-24: Data Workstream](../workstreams/data.md)

- :material-server: **Infrastructure**

    ---
    Set up a secure network area and install query retrieval software (e.g. Bunny).

    [:octicons-arrow-right-24: Infrastructure Workstream](../workstreams/infrastructure.md)

</div>

---

## First steps

1. **Read the prerequisites** — ensure your organisation meets the access requirements.
2. **Contact the HDR UK team** — an introductory meeting will be arranged to define tasks and responsibilities.
3. **Contribute Gateway metadata** — a metadata record on the Gateway is required before Cohort Discovery can go live. See [how to contribute metadata](https://healthdatagateway.org/en/data-custodian/support/metadata-onboarding).

!!! tip "Governance first"
    Start the Governance workstream as soon as the project is initiated — it typically has the longest lead time. Data and Infrastructure workstreams can run in parallel once governance steps are underway.

!!! note "Gateway metadata"
    The Cohort Discovery Service links to your Gateway metadata record so researchers can find contact details and data descriptions. Cohort Discovery and Gateway onboarding can occur simultaneously.
