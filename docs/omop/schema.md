---
title: CDM Schema Reference
description: Reference for the OMOP Common Data Model schema as used in Cohort Discovery
tags:
  - omop
  - schema
  - reference
---

# CDM Schema Reference

The Cohort Discovery Service is aligned with the **OMOP Common Data Model (CDM)**, versions 5.3 and 5.4. This page provides reference links and key notes on schema compliance.

---

## Official OMOP CDM documentation

The authoritative schema reference is maintained by OHDSI:

| Version | Documentation |
|---------|--------------|
| OMOP CDM 5.3 | [ohdsi.github.io/CommonDataModel/cdm53.html](https://ohdsi.github.io/CommonDataModel/cdm53.html) |
| OMOP CDM 5.4 | [ohdsi.github.io/CommonDataModel/cdm54.html](https://ohdsi.github.io/CommonDataModel/cdm54.html) |

---

## Bunny deployment requirements

The Cohort Discovery minimum dataset is fully aligned with Bunny's deployment requirements. Always check the Bunny documentation for the latest supported versions and any additional configuration requirements:

[:octicons-arrow-right-24: Bunny deployment requirements](https://hutch.health/bunny/deployment/requirements)

---

## Optional CDM tables

Some OMOP CDM tables are only used by Bunny when explicitly enabled via configuration:

| OMOP Table | Fields used | Enabled by | Supported from |
|------------|-------------|------------|-----------------|
| Specimen | `specimen_id`, `person_id`, `specimen_concept_id`, `specimen_date` | `OMOP_SPECIMEN_ENABLED` | Bunny v1.7 |
| Location | `location_id`, `latitude`, `longitude` (joined via `person.location_id`) | `OMOP_LOCATION_ENABLED` | Bunny v1.8 |
| Death | `death_date`, `cause_concept_id` | `OMOP_DEATH_ENABLED` | Bunny v1.9 — see [Death & Cause-of-Death Filtering](death.md) |

!!! warning "Location filtering requires OMOP CDM 5.4"
    The `latitude` and `longitude` fields were only added to the Location table in **OMOP CDM v5.4** — a v5.3 database cannot use Bunny's geo-radius location filter. See [Bunny deployment requirements](https://hutch.health/bunny/deployment/requirements#omop-cdm) for the full table/field reference, and the [Availability concept — Location filtering](https://hutch.health/concepts/availability#location-filtering) page for how the `GEO_RADIUS` rule works.

---

## Recommended database indexes

If you are using Bunny as your query retrieval software, ensure the following indexes are in place on your OMOP tables to support efficient query processing:

| Index name | Table |
|------------|-------|
| `idx_person_id` | Person |
| `idx_concept_concept_id` | Concept |
| `idx_condition_concept_id_1` | Condition Occurrence |
| `idx_procedure_concept_id_1` | Procedure Occurrence |
| `idx_observation_concept_id_1` | Observation |
| `idx_measurement_concept_id_1` | Measurement |

See [hutch.health/bunny/deployment/requirements](https://hutch.health/bunny/deployment/requirements) for the full list of recommended indexes.

```sql title="Example: creating an index on Person"
CREATE INDEX idx_person_id ON person (person_id);
```

---

## Schema compliance notes

!!! warning "Include all columns"
    When implementing any OMOP CDM table, **all columns defined by the CDM schema should ideally be present** in the table structure — even if some are not populated. This ensures forward compatibility as Bunny adds support for additional fields.

!!! info "Vocabulary tables"
    The **Concept** table (`concept_id`, `domain_id`) is mandatory and must be populated. Cohort Discovery uses concept vocabulary lookups to translate query criteria into SQL filters against your OMOP data.
