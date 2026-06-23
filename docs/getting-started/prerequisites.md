---
title: Prerequisites
description: What you need before starting onboarding to the Cohort Discovery Service
tags:
  - prerequisites
  - onboarding
---

# Prerequisites

Before beginning the Cohort Discovery onboarding process, ensure the following are in place.

---

## For Data Custodians

=== "Access & Accounts"

    | Requirement | Details |
    |-------------|---------|
    | Gateway account | Your organisation must be registered on the [Health Data Research Gateway](https://healthdatagateway.org/en) |
    | Gateway metadata record | A metadata record for your dataset(s) must exist on the Gateway. See [how to contribute metadata](https://healthdatagateway.org/en/data-custodian/support/metadata-onboarding) |
    | Cohort Discovery access request | Submit a request via the **Access Cohort Discovery** button on [healthdatagateway.org/en/about/cohort-discovery](https://healthdatagateway.org/en/about/cohort-discovery) |
    | HDR UK contact | Your organisation will be assigned key contacts within the HDR UK Technology Team |

=== "Data"

    | Requirement | Details |
    |-------------|---------|
    | Source data subset | A relevant subset of your raw data for mapping to OMOP |
    | OMOP mapping capability | Either in-house expertise or access to OMOP mapping services (HDR UK can assist via CaRROT tools) |
    | Pseudonymisation process | A process for removing all PII before data is placed in the secure network area |

=== "Infrastructure"

    | Requirement | Details |
    |-------------|---------|
    | Secure network area | A network zone isolated from identifiable data, supporting OCI-compliant containers (Docker, Podman, or Kubernetes) |
    | Outbound HTTPS | Outbound connectivity only on port 443 to the Cohort Discovery Service IP range |
    | Database | PostgreSQL 14–18, SQL Server 2019/2022, DuckDB 1.x, or Snowflake (for Bunny) |
    | Compute | Minimum 2 vCPUs, 4 GB RAM |

---

## Supported OMOP CDM versions

!!! info "OMOP CDM version support"
    The Cohort Discovery Service supports **OMOP CDM version 5.3 and above**.

    - If you are mapping data for the **first time**, version **5.4** is recommended.
    - If you have an **existing 5.3 mapping**, it is fully supported — no migration is required.
    - If you are using a version other than 5.3 or 5.4, contact the HDR UK team before proceeding.

---

## Support

!!! hdruk "HDR UK"
    The HDR UK Technology Team will not need to see your row-level data at any stage. Support is provided through an introductory meeting and ongoing guidance throughout the onboarding process.

    Contact: [gateway@hdruk.ac.uk](mailto:gateway@hdruk.ac.uk)
