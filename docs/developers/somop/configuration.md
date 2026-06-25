---
title: Configuration
description: YAML configuration reference for somop
tags:
  - somop
  - configuration
  - omop
---

# Configuration Reference

somop datasets are defined in YAML files. Each file describes the synthetic population and the clinical data to generate across OMOP CDM tables.

---

## Minimal example

```yaml
seed: 42
out_dir: ./data/my_dataset

person:
  n_people: 1000

condition:
  enabled: true
  items:
    - concept_id: 201826   # Type 2 diabetes mellitus
      p: 0.14
```

---

## Full annotated example

```yaml
# Reproducibility seed — use the same seed to regenerate identical data
seed: 42

# Output directory for generated CSV files
out_dir: ./data/my_dataset

# Number of person records to process per chunk (controls memory use)
# Default: 100_000. Lower this if you run out of RAM on large datasets.
chunk_size: 100_000


# ── Person table ──────────────────────────────────────────────────────────────

person:
  enabled: true
  n_people: 5000

  # Gender distribution — probabilities must sum to 1.0
  genders:
    - concept_id: 8507   # Male
      p: 0.5
    - concept_id: 8532   # Female
      p: 0.5

  # Race distribution (optional)
  races:
    - concept_id: 8527     # White
      p: 0.85
    - concept_id: 38003600 # Black or African American
      p: 0.08
    - concept_id: 0        # Unknown
      p: 0.07

  # Ethnicity distribution (optional)
  ethnicities:
    - concept_id: 0        # Unknown / not recorded
      p: 1.0

  # Age sampling distribution: normal | lognormal | uniform
  age_dist: normal
  age_param1: 55.0         # mean (normal/lognormal) or lower bound (uniform)
  age_param2: 15.0         # std dev (normal/lognormal) or upper bound (uniform)
  min_age: 18.0
  max_age: 100.0


# ── Condition occurrence ──────────────────────────────────────────────────────

condition:
  enabled: true
  items:
    - concept_id: 201826   # Type 2 diabetes mellitus
      p: 0.14
    - concept_id: 255573   # Essential hypertension
      p: 0.35
    - concept_id: 198185   # Chronic kidney disease
      p: 0.12


# ── Drug exposure ─────────────────────────────────────────────────────────────

drug_exposure:
  enabled: true
  items:
    - concept_id: 1503297  # Metformin
      p: 0.30
    - concept_id: 1551803  # Atorvastatin
      p: 0.40


# ── Measurement ───────────────────────────────────────────────────────────────

measurement:
  enabled: true
  items:
    - concept_id: 3004410      # HbA1c
      unit_concept_id: 100080  # % — OMOP unit concept
      p: 0.70
      dist: lognormal          # normal | lognormal | uniform
      param1: 7.0              # mu (lognormal) or mean (normal) or lower (uniform)
      param2: 0.7              # sigma (lognormal) or std dev (normal) or upper (uniform)

    - concept_id: 3004249      # Systolic blood pressure
      unit_concept_id: 100030  # mmHg
      p: 0.75
      dist: normal
      param1: 138.0
      param2: 18.0


# ── Observation ───────────────────────────────────────────────────────────────

observation:
  enabled: true
  items:
    - concept_id: 4275495  # Observation concept
      p: 0.40


# ── Procedure occurrence ──────────────────────────────────────────────────────

procedure:
  enabled: true
  items:
    - concept_id: 4047494  # Some procedure
      p: 0.25


# ── Specimen ──────────────────────────────────────────────────────────────────

specimen:
  enabled: true
  items:
    - concept_id: 4001225  # Blood specimen
      p: 0.80


# ── Death ─────────────────────────────────────────────────────────────────────

death:
  enabled: true
  p: 0.05                          # Overall mortality rate
  death_type_concept_id: 32519     # EHR (standard type)
  causes:
    - concept_id: 4306655          # Cause of death concept
      p: 1.0


# ── Location ──────────────────────────────────────────────────────────────────

location:
  enabled: true
  items:
    - location_id: 1
      city: London
      country_source_value: GBR
      latitude: 51.5074
      longitude: -0.1278


# ── Interaction effects ────────────────────────────────────────────────────────
# Multiply downstream probabilities for persons who have records in an upstream table.
# Example: people who have any drug exposure are 1.5× more likely to also have a measurement.

interactions:
  after_drug_exposure:
    measurement: 1.5
  after_condition:
    measurement: 1.3
    observation: 1.2
```

---

## Key fields

| Field | Type | Description |
|-------|------|-------------|
| `seed` | int | Random seed for reproducibility |
| `out_dir` | path | Directory where CSV files are written |
| `chunk_size` | int | Records per processing chunk (default: 100,000) |
| `person.n_people` | int | Total number of persons to generate |
| `concept_id` | int | OMOP CDM v5.4.3 concept identifier |
| `p` | float (0–1) | Probability that a person has this concept |
| `unit_concept_id` | int | OMOP unit concept for measurements |
| `dist` | string | Value distribution: `normal`, `lognormal`, or `uniform` |
| `param1` | float | Distribution param 1: mean (normal), mu (lognormal), lower bound (uniform) |
| `param2` | float | Distribution param 2: std dev (normal), sigma (lognormal), upper bound (uniform) |

---

## Age distributions

| Distribution | `param1` | `param2` | Typical use |
|--------------|----------|----------|-------------|
| `normal` | mean | std dev | General adult populations |
| `lognormal` | mu | sigma | Right-skewed populations (children + adults) |
| `uniform` | lower bound | upper bound | Uniform spread across an age range |

Rejection sampling ensures generated ages stay within `min_age` and `max_age`.

---

## Interaction effects

Interactions multiply downstream `p` values for persons who have a record in the upstream table. This creates realistic co-morbidity patterns without requiring explicit conditional logic.

```yaml
interactions:
  after_drug_exposure:
    condition: 1.2       # p for each condition × 1.2 for people with any drug
    measurement: 1.5
  after_condition:
    observation: 1.3
```

Interactions are applied at chunk level. They affect **all** items in the downstream table (not just specific concepts).

---

## Bundled example configs

The `configs/` directory includes ready-to-use configurations:

| Config | Population | Focus |
|--------|-----------|-------|
| `simple.yaml` | 2,750 | Vaccine exposures only — minimal setup for quick tests |
| `conditions.yaml` | 400,000 | Broad range of conditions (metabolic, cardiovascular, renal, respiratory) |
| `mortality_conditions.yaml` | 5,000 | Older population, conditions + measurements, 5% mortality |
| `uk_t2d_primary_care.yaml` | 200,000 | Type 2 diabetes primary care: drugs, measurements, observations |
| `ckd_antibodies_v2.yaml` | 21,200 | Chronic kidney disease staging, proteinuria qualifiers |
| `multi_example.yaml` | — | Multi-dataset: references four other configs, each with its own collection ID |

!!! tip "Finding concept IDs"
    Use the web UI concept search, or query [Athena](https://athena.ohdsi.org) directly. The OMOP CDM v5.4.3 standard concepts are stable across environments.
