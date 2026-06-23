---
title: OMOP Requirements
description: OMOP CDM requirements for the HDR UK Cohort Discovery Service
tags:
  - omop
  - data
---

# OMOP Requirements

The Cohort Discovery Service operates on data mapped to the **OMOP Common Data Model (CDM)**. This section defines the minimum set of OMOP fields that must be populated for your data to be discoverable.

!!! info "What is OMOP?"
    OMOP (Observational Medical Outcomes Partnership) CDM is a global standard for observational health data. It is patient-centric, tabular, extendable, built for analytics, and has a relational design. For background, see the [OHDSI OMOP CDM documentation](https://ohdsi.github.io/CommonDataModel/).

---

## Quick summary

<div class="grid cards" markdown>

- :material-check-circle: **Mandatory tables**

    ---
    **Person** and **Concept** must be populated for all collections.

- :material-database: **Minimum dataset**

    ---
    8 additional tables cover conditions, procedures, drugs, observations, measurements, death, visits, and specimens.

    [:octicons-arrow-right-24: View minimum dataset](minimum-dataset.md)

- :material-code-tags: **CDM versions**

    ---
    OMOP CDM **5.3** (supported) and **5.4** (recommended for new mappings).

- :material-tools: **Mapping tools**

    ---
    White Rabbit + Carrot Mapper + Carrot-CDM. HDR UK can assist.

    [:octicons-arrow-right-24: Mapping tools](mapping-tools.md)

</div>

---

## Mandatory tables

The following two tables must be populated for all collections:

| Table | Required Fields |
|-------|----------------|
| **Person** | `person_id`, `gender_concept_id`, `year_of_birth`, `race_concept_id`, `ethnicity_concept_id` |
| **Concept** | `concept_id`, `domain_id` |

---

## OMOP CDM version support

| Version | Status |
|---------|--------|
| **5.4** | Recommended for new mappings |
| **5.3** | Fully supported — no migration required |
| Other | Contact HDR UK before proceeding |

Supported versions are ultimately constrained by Bunny's deployment requirements. See [hutch.health/bunny/deployment/requirements](https://hutch.health/bunny/deployment/requirements) for the latest information.
