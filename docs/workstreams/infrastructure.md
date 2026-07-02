---
title: Infrastructure Workstream
description: Infrastructure setup steps for onboarding to the Cohort Discovery Service
tags:
  - infrastructure
  - bunny
  - onboarding
---

# Infrastructure Workstream

The Infrastructure Workstream covers setting up the secure network area, installing the query retrieval software, and connecting it to your OMOP data and the Cohort Discovery Service.

!!! info "Responsible party"
    The **Data Custodian** is responsible for all infrastructure steps. The HDR UK Technology Team is available to answer questions but will not have direct access to your systems.

---

## Steps overview

| Step | Description |
|------|-------------|
| **I1** | Set up a Secure Network Area |
| **I2** | Install Query Retrieving / Running Software |
| **I3** | Connect OMOP Data to Query Retrieving Software |

---

## I1 — Setting up a Secure Network Area

**Description**

Data Custodians must provide a secure environment within their network to house and process their pseudonymised OMOP data. The ETL tool (D4) will load data into this area, and the query retrieval software will be installed here so that queries can be performed.

**Requirements:**

- Isolated from environments containing identifiable data
- Contains only: (1) the pseudonymised OMOP database, and (2) the query retrieval software
- Supports **outbound HTTPS (port 443) only** — no inbound firewall rules required
- Supports OCI-compliant container runtime (Docker, Podman, or Kubernetes)

=== "Virtual Machine (VM)"

    A dedicated VM is the most common deployment model. It provides clear separation between the pseudonymised OMOP data zone and other systems.

=== "Cloud infrastructure"

    Cloud-based deployments (AWS, Azure, GCP) are fully supported. The secure network area can be implemented as a cloud VPC or subnet with appropriate network controls.

=== "On-premises"

    On-premises deployments are supported. The secure network area should be a dedicated VLAN or subnet with outbound-only firewall rules.

!!! note "Governance preference"
    Our experience is that **clear separation** of data zones provides additional comfort to Data Governance panels. We recommend a distinct and minimal deployment model to simplify IG reviews.

### Bunny infrastructure specification

| Requirement | Minimum Specification |
|-------------|----------------------|
| CPU | 2 vCPUs |
| Memory (RAM) | 4 GB |
| Container Runtime | OCI-compliant (Docker, Podman, or Kubernetes) |
| Network | Outbound HTTPS (port 443) only |
| Database | PostgreSQL 14–18 · SQL Server 2019 or 2022 · DuckDB 1.x · Snowflake |

> Requirements may vary depending on workload and deployment environment.

See the [Bunny user guide](https://health-informatics-uon.github.io/hutch/bunny) or contact the University of Nottingham for optimal environment recommendations.

---

## I2 — Install Query Retrieving / Running Software

This software routinely polls the Cohort Discovery API for tasks and runs them against your OMOP database.

=== "Option I2a — Bunny (Recommended)"

    Bunny is the recommended open-source option.

    - Developed by the University of Nottingham
    - Outbound-only requests
    - Supports obfuscation (low-count suppression and rounding)
    - Can participate in federated networks via Hutch Relay
    - Container images available: `ghcr.io/health-informatics-uon/hutch/bunny:latest`

    !!! warning "Two instances required"
        Bunny requires **two instances** per OMOP database — one for availability queries (type `a`) and one for distribution jobs (type `b`). See the [Two-Instance Pattern](../bunny/two-instance-pattern.md).

    For connecting Bunny to the Cohort Discovery Service, see [Connecting Bunny](../bunny/index.md) and [Appendix 2 — Step-by-Step Setup](../bunny/setup.md).

    Bunny user guide: [health-informatics-uon.github.io/hutch/bunny](https://health-informatics-uon.github.io/hutch/bunny)

=== "Option I2b — BC|INSIGHT (Commercial)"

    The Cohort Discovery Service is compatible with BC|INSIGHT as a query retrieval tool.

    As this is a proprietary tool, contact **BC Platforms** directly for:
    - Installation instructions
    - Contract options and pricing
    - Technical support

=== "Option I2c — Build Your Own"

    Data Custodians are welcome to develop their own query retrieval tool.

    Requirements:
    - Must meet the API standards set out in the [Swagger documentation](https://api.cohort-discovery.dev.hdruk.cloud/api/documentation)
    - Contact the HDR UK Technology Team to discuss this option before starting development

---

## I3 — Connect OMOP Data to Query Retrieving Software

**Description**

Once the OMOP database has been created and stored, it needs to be connected to the query retrieval software.

1. **Upload the OMOP database** to the same network space as the query retrieval software
2. **Connect the database** to the query retrieval software (if not already connected)
3. **Ensure recommended indexes** are in place on your OMOP tables (for Bunny):

    | Index | Table |
    |-------|-------|
    | `idx_person_id` | Person |
    | `idx_concept_concept_id` | Concept |
    | `idx_condition_concept_id_1` | Condition Occurrence |
    | `idx_procedure_concept_id_1` | Procedure Occurrence |
    | `idx_observation_concept_id_1` | Observation |
    | `idx_measurement_concept_id_1` | Measurement |

    See [hutch.health/bunny/deployment/requirements](https://hutch.health/bunny/deployment/requirements) for the full index list.

4. **Connect the query retrieval software to Cohort Discovery** — follow the steps in [Connecting Bunny](../bunny/setup.md)
5. **Test** that queries can run from the Cohort Discovery Service

!!! tip "Test with your draft Collection"
    While your Collection is in **Draft** status, you can run test queries visible only to you. See [Step 8 of the Bunny setup guide](../bunny/setup.md#step-8-request-activation-of-your-collection).

!!! tip "Monitoring your Collection"
    We recommend setting up internal monitoring to detect when your Collection goes offline. The most practical approach is to monitor your Bunny instance health and logs — Bunny's own documentation covers available logging and health-check options. You can also check Collection status at any time in the Cohort Discovery admin panel; a Collection that has gone offline will show as **Offline** or **Suspended** in your Collections list. Contact us at gateway@hdruk.ac.uk if you need support diagnosing a persistent issue.
