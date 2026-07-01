---
title: Minimum OMOP Dataset
description: The minimum set of OMOP CDM tables and fields required for Cohort Discovery
tags:
  - omop
  - minimum-dataset
  - data
---

# Minimum OMOP Dataset

This page defines the OMOP CDM requirements for making your data discoverable 
via the Cohort Discovery Service.

!!! abstract "Objective"
    The minimum dataset represents basic information about a patient — their 
    condition, procedure, drug exposure, observations, and measurements — that 
    helps researchers find and access cohorts for further analysis.

---

## OMOP CDM Version Support

The Cohort Discovery Service supports OMOP CDM versions 5.3 and above. If you 
are mapping data for the first time, version 5.4 is recommended. If you have an 
existing 5.3 mapping, this is fully supported and no migration is required.

Supported versions are ultimately constrained by Bunny's deployment requirements. 
See the [Bunny documentation](https://hutch.health/bunny) for the latest 
information. If you are using a version older than 5.3, please contact 
us before proceeding.

---

## Mandatory data requirements

Two tables are mandatory to be populated for all datasets:

- **Person** — must be populated with `person_id`s for all individuals in the 
dataset.
- **Concept** — must be populated with the `concept_id`s for whatever clinical 
concepts are in use.

OHDSI defines the full [OMOP CDM definition for version 5.3](https://ohdsi.github.io/CommonDataModel/cdm53.html){ .md-button } . Tables other than Person and Concept might be present but are optional for being populated. Which ones you populate will depend on the nature 
of your dataset. 

---

## Field-Level Requirements

For full field-level detail — including data types, constraints, and descriptions 
for each OMOP table — refer to the official OMOP CDM documentation maintained 
by OHDSI:

[OMOP CDM Documentation (OHDSI)](https://ohdsi.github.io/CommonDataModel/){ .md-button }

This is the authoritative reference for how each field should be populated across 
all supported CDM versions. Use it alongside this guide when preparing your 
OMOP mapping.

---

## Bunny Compatibility

The Cohort Discovery minimum dataset is fully aligned with Bunny's deployment 
requirements. For field-level requirements specific to Bunny, see:

[Bunny Deployment Requirements](https://hutch.health/bunny/deployment/requirements){ .md-button }

!!! note "Unsupported tables"
    Tables not yet supported by Bunny can still be included in your OMOP CDM, 
    but will only be surfaced by the Cohort Discovery Service after agreed adoption.
