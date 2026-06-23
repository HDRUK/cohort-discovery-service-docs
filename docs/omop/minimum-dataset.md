---
title: Minimum OMOP Dataset
description: The minimum set of OMOP CDM tables and fields required for Cohort Discovery
tags:
  - omop
  - minimum-dataset
  - data
---

# Minimum OMOP Dataset

This page defines the minimum set of OMOP CDM tables and fields that must be populated for your data to be discoverable via the Cohort Discovery Service.

!!! info "Objective"
    The minimum dataset represents basic information about a patient — their condition, procedure, drug exposure, observations, and measurements — that helps researchers find and access cohorts for further analysis.

---

## Minimum viable OMOP fields

Items marked with `*` are optional but useful.

| OMOP Table | Required Fields |
|------------|----------------|
| **Person** | `person_id`, `gender_concept_id`, `year_of_birth`, `race_concept_id`, `ethnicity_concept_id` |
| **Condition_Occurrence** | `condition_occurrence_id`, `person_id`, `condition_concept_id`, `condition_start_date` |
| **Procedure_Occurrence** | `procedure_occurrence_id`, `person_id`, `procedure_concept_id`, `procedure_date` |
| **Drug_Exposure** | `drug_exposure_id`, `person_id`, `drug_concept_id`, `drug_exposure_start_date` |
| **Observation** | `observation_id`, `person_id`, `observation_concept_id`, `observation_date`, `value_as_number`*, `value_as_concept_id`* |
| **Measurement** | `measurement_id`, `person_id`, `measurement_concept_id`, `measurement_date`, `value_as_number`*, `value_as_concept_id`* |
| **Death** * | `person_id`, `death_date`, `death_type_concept_id`, `cause_concept_id` |
| **Visit_Occurrence** * | `visit_occurrence_id`, `person_id`, `visit_concept_id`, `visit_start_date` |
| **Concept** | `concept_id`, `domain_id` |
| **Specimen** * | `specimen_id`, `person_id`, `specimen_concept_id`, `specimen_date` |

---

## Field-by-field rationale

=== "Person"

    | Field | Required | Rationale |
    |-------|----------|-----------|
    | `person_id` | ✓ | Unique identifier for each individual; enables linking across all tables |
    | `gender_concept_id` | ✓ | Identifies sex category for sex-specific cohort definitions |
    | `year_of_birth` | ✓ | Determines age groups; facilitates age-related analyses |
    | `race_concept_id` | ✓ | Potentially informative for understanding health disparities |
    | `ethnicity_concept_id` | ✓ | Identifies ethnicity for cohort stratification and health disparities analysis |

=== "Condition Occurrence"

    | Field | Required | Rationale |
    |-------|----------|-----------|
    | `condition_occurrence_id` | ✓ | Unique identifier for each condition; enables tracking and analysis |
    | `person_id` | ✓ | Key — links to Person table |
    | `condition_concept_id` | ✓ | Identifies specific medical condition for cohort definition and disease progression analysis |
    | `condition_start_date` | ✓ | Tracks date of condition onset; enables disease trajectory analysis |

=== "Procedure Occurrence"

    | Field | Required | Rationale |
    |-------|----------|-----------|
    | `procedure_occurrence_id` | ✓ | Unique identifier for each procedure |
    | `person_id` | ✓ | Key |
    | `procedure_concept_id` | ✓ | Identifies the specific type of procedure for cohort definition and utilisation analysis |
    | `procedure_date` | ✓ | Tracks the date of each procedure for temporal trends |

=== "Drug Exposure"

    | Field | Required | Rationale |
    |-------|----------|-----------|
    | `drug_exposure_id` | ✓ | Unique identifier for each drug exposure |
    | `person_id` | ✓ | Key |
    | `drug_concept_id` | ✓ | Identifies the specific drug for cohort definition and medication effectiveness research |
    | `drug_exposure_start_date` | ✓ | Tracks date of drug exposure initiation; enables treatment pattern analysis |

=== "Observation"

    | Field | Required | Rationale |
    |-------|----------|-----------|
    | `observation_id` | ✓ | Unique identifier for each observation |
    | `person_id` | ✓ | Key |
    | `observation_concept_id` | ✓ | Identifies the type of observation (e.g. physical exam finding, imaging result) |
    | `observation_date` | ✓ | Tracks the date; enables temporal analysis |
    | `value_as_number` | Optional | Observation value — useful for quantitative analysis |
    | `value_as_concept_id` | Optional | Coded observation value |

=== "Measurement"

    | Field | Required | Rationale |
    |-------|----------|-----------|
    | `measurement_id` | ✓ | Unique identifier for each measurement |
    | `person_id` | ✓ | Key |
    | `measurement_concept_id` | ✓ | Identifies the type of measurement (e.g. blood pressure, lab test) |
    | `measurement_date` | ✓ | Tracks date of each measurement |
    | `value_as_number` | Optional | Value of the measurement |
    | `value_as_concept_id` | Optional | Coded value of the measurement |

=== "Death"

    | Field | Required | Rationale |
    |-------|----------|-----------|
    | `person_id` | ✓ | Key |
    | `death_date` | ✓ | Records the date of death; enables mortality cohorts and survival analysis |
    | `death_type_concept_id` | ✓ | Identifies the type of death (e.g. natural, accidental) |
    | `cause_concept_id` | ✓ | Identifies the underlying cause of death; enables disease burden analysis |

=== "Visit Occurrence"

    | Field | Required | Rationale |
    |-------|----------|-----------|
    | `visit_occurrence_id` | Optional | Unique identifier for each visit |
    | `person_id` | Optional | Key |
    | `visit_concept_id` | Optional | Identifies the type of visit (e.g. inpatient, outpatient) |
    | `visit_start_date` | Optional | Tracks the timing of each visit for temporal analysis |

=== "Concept"

    | Field | Required | Rationale |
    |-------|----------|-----------|
    | `concept_id` | ✓ | Identifies the specific concept for cohort definition and vocabulary lookups |
    | `domain_id` | ✓ | Identifies the domain of the concept (e.g. Condition, Drug, Procedure) to support query filtering |

=== "Specimen"

    | Field | Required | Rationale |
    |-------|----------|-----------|
    | `specimen_id` | Optional | Unique identifier for each specimen |
    | `person_id` | Optional | Key — links specimen to the patient record |
    | `specimen_concept_id` | Optional | Identifies the type of specimen (e.g. blood, tissue) |
    | `specimen_date` | Optional | Tracks the date the specimen was collected |

---

## Schema compliance

When implementing any OMOP CDM table, **all columns defined by the CDM schema should ideally be present** in the table structure — even if some fields are not used. Refer to the [official OMOP CDM schema documentation](https://ohdsi.github.io/CommonDataModel/cdm53.html) for full data types, constraints, and descriptions.

!!! warning "Unsupported tables"
    Tables not yet supported by Bunny could still be included in your OMOP CDM, but will only be surfaced by the Cohort Discovery Service after agreed adoption.
