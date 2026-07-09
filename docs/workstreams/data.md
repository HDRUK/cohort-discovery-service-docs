---
title: Data Workstream
description: Data preparation, OMOP mapping, and ETL steps for Cohort Discovery onboarding
tags:
  - data
  - omop
  - etl
  - onboarding
---

# Data Workstream

The Data Workstream covers all steps from extracting a subset of your raw identifiable data to loading a pseudonymised OMOP database into your secure network area.

!!! info "Responsible party"
    The **Data Custodian** is responsible for all data steps. HDR UK can assist with OMOP mapping support.

---

## Steps overview

| Step | Description | Notes |
|------|-------------|-------|
| **D1** | Extract a subset of raw identifiable data | Identify the subset of data to be made discoverable |
| **D2** | Map the extracted subset to OMOP CDM | Can be done in-house or with HDR UK / external support |
| **D3** | Create synthetic data (bonus) | Strongly recommended for safe testing |
| **D4** | ETL the extracted subset to create an OMOP database | Loaded into your secure network area |

!!! tip "Start before governance is complete"
    D1, D2, and D3 can proceed before **G1 (Data Controller Consent)** is complete. Only D4 (loading real data into the system connected to Cohort Discovery) requires G1 to be done.

---

## D1 — Extract a subset of your raw identifiable data

**Purpose:** Identify and extract the relevant portion of your source data for mapping to the minimum OMOP CDM.

**Key considerations:**

- Identify which data fields will be made discoverable (aligns with governance step G1)
- Consider the minimum viable set of OMOP fields required — see [Minimum OMOP Dataset](../omop/minimum-dataset.md)
- Data profiling with [White Rabbit](../omop/mapping-tools.md) can help you understand the structure of your extracted subset

---

## D2 — Map the extracted subset to the OMOP CDM

**Purpose:** Create a mapping from your source data schema to the OMOP CDM.

The minimum OMOP fields required for Cohort Discovery are defined in [OMOP Requirements](../omop/index.md).

=== "In-house mapping"

    If you have OMOP expertise in-house:

    1. Use **White Rabbit** to profile your source data
    2. Use **Carrot Mapper** (or another mapping tool) to define field-level mappings
    3. Produce a mapping file for use in the ETL step (D4)

=== "HDR UK mapping support"

    HDR UK and partners at the Health Informatics Centre (HIC), University of Dundee offer OMOP mapping services using Carrot tools.

    Contact [gateway@hdruk.ac.uk](mailto:gateway@hdruk.ac.uk) to discuss.

=== "External vendor"

    Commercial vendors also provide OMOP mapping services. If a vendor requires direct access to row-level data, you will need to put in place appropriate data sharing, confidentiality, and access agreements.

!!! note "See the mapping tools page"
    For full tool descriptions and links, see [OMOP Mapping Tools](../omop/mapping-tools.md).

---

## D3 — Create synthetic data (recommended)

**Purpose:** Create a synthetic version of your dataset to safely test the ETL process and infrastructure without using real patient data.

Synthetic data allows you to:

- Test the full ETL pipeline before G1 is complete
- Validate your Bunny setup without exposing real data
- Onboard a synthetic collection to Cohort Discovery for development and testing purposes

!!! tip "Test with synthetic data first"
    HDR UK strongly recommends using synthetic data for all testing until G1 (Data Controller Consent) is complete.

---

## D4 — ETL to create the OMOP database

**Purpose:** Transform your extracted source data into OMOP format and load it into the database in your secure network area.

This step produces the OMOP database that Bunny (or your chosen query tool) will query.

=== "Using Carrot-CDM"

    Carrot-CDM automates the full ETL process using the mapping file produced in D2:

    ```bash title="Running Carrot-CDM"
    pip install carrot-cdm
    carrot run --rules mapping_rules.json --input source_data/
    ```

    See [Carrot documentation](https://carrot.ac.uk/documentation) for more detail.

=== "Custom ETL"

    You may use any ETL tool or process, provided the output conforms to the OMOP CDM schema. The output must be loaded into a database that is accessible to your query retrieval software within the secure network area.

**After ETL:**

- Upload the OMOP database to the same network space as your query retrieval software
- Ensure [recommended indexes](../omop/schema.md) are in place
- Connect the database to Bunny (see [Infrastructure Workstream](infrastructure.md) step I3)

---

## Iterative data onboarding

Cohort Discovery supports an iterative approach. You do not need to onboard all fields at once:

- Focus initially on the **key fields** needed to answer the most pressing research questions
- Additional fields can be added over time following the same governance process
- The community can request new fields to be added as needs evolve
