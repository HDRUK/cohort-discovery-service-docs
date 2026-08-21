---
title: Death & Cause-of-Death Filtering
description: How Bunny's optional Death table support works, and what it means for Cohort Discovery
tags:
  - omop
  - death
  - bunny
  - mapping
---

# Death & Cause-of-Death Filtering

!!! info "Released in Bunny v1.9"
    Death filtering is available from Bunny v1.9 onwards, gated behind the
    `OMOP_DEATH_ENABLED` flag. See the [Availability concept — Death filtering](https://hutch.health/concepts/availability#death-filtering)
    page for the canonical Bunny-side documentation this page summarises.

Bunny can answer **death-related** cohort queries — "how many matching patients have died?",
"...died of a specific cause?", or "...are still living?" — using the OMOP `DEATH` table,
gated behind the `OMOP_DEATH_ENABLED` flag (default `false`), following the same
optional-table pattern as [Specimen](../bunny/configuration.md#optional-feature-flags) and
[Location](location.md).

---

## How Bunny uses the Death table

| Requirement | Detail |
|-------------|--------|
| Available from | Bunny v1.9 |
| OMOP CDM version | No specific version required — `death_date`/`cause_concept_id` are standard across CDM 5.x (unlike [Location](location.md), which needs 5.4) |
| Enable flag | `OMOP_DEATH_ENABLED` (default `false`) |
| Rule shape | `varcat: "Death"`, `type: "TEXT"` — reuses the existing text rule type, unlike Location's new `GEO_RADIUS` type |
| Fields used | `death_date` (age/temporal constraints), `cause_concept_id` (concept match) |
| Fields modelled but not yet used | `death_type_concept_id` — present on the entity, not wired into any filter |

A `Death` varcat rule targets the `DEATH` table **alone** — like Location, it bypasses the
usual UNION with other clinical tables. The rationale, per the implementation's own docstring:
a concept recorded as `cause_concept_id` describes what someone died of, which is not the same
clinical fact as that concept appearing in their ongoing clinical history — unioning the two
would conflate "has this condition" with "died of this condition."

A `Death` rule can be combined with rules from other varcats in the same group using
`rules_oper: "AND"` — e.g. "deceased **and** previously diagnosed with condition X."

!!! info "Explicit `varcat: Death` overrides the flag"
    Same behaviour as Specimen and Location: a rule that explicitly sets `varcat: "Death"`
    queries the Death table regardless of `OMOP_DEATH_ENABLED`. The flag only governs whether
    Death is folded into general availability/distribution queries alongside other domains.

---

## Example rules

Three shapes, per the [Availability concept — Death filtering](https://hutch.health/concepts/availability#death-filtering) page:

```json title="Any deceased patient (any death record)"
{
  "varname": "OMOP",
  "varcat": "Death",
  "type": "TEXT",
  "oper": "=",
  "value": ""
}
```

```json title="Living patients (excludes anyone with a death record)"
{
  "varname": "OMOP",
  "varcat": "Death",
  "type": "TEXT",
  "oper": "!=",
  "value": ""
}
```

```json title="Died of a specific cause"
{
  "varname": "OMOP",
  "varcat": "Death",
  "type": "TEXT",
  "oper": "=",
  "value": "4329847"
}
```

An empty `value` matches on presence/absence of a death record; a populated `value` is a
`cause_concept_id`, matched against `death.cause_concept_id` — the same concept vocabulary
already used elsewhere in Cohort Discovery.

---

## Disclosure risk: cause of death is a small-cell risk, not a geographic one

Location filtering needed a blurring step because a coordinate is directly identifying.
Death doesn't have that problem — a death date and cause aren't geographic — but cause of
death is itself a sensitive, often rare attribute. A narrow cause-of-death filter, even
combined with a broad demographic filter, can shrink a matching cohort to a handful of
people faster than most clinical filters do. There's nothing Death-specific to configure:
the existing [obfuscation settings](../bunny/configuration.md#obfuscation-settings) (low-number
suppression, rounding) apply to Death-derived counts the same as any other query — but treat
a specific cause-of-death filter the way you'd treat any rare condition: a candidate for
suppression, not something to combine casually with other narrow filters.

---

## Populating the Death table

`DEATH` is a standard OMOP CDM table, populated the same way as any other clinical table in
your ETL. There's no blurring/anonymisation step analogous to
[Location's centroid approach](location.md#the-recommended-approach-blur-to-an-lsoa-centroid) —
a person's own recorded death date and cause aren't the kind of identifier that needs coarsening.

| Field | Used for |
|-------|----------|
| `person_id` | Join key |
| `death_date` | Age/temporal constraints |
| `cause_concept_id` | Concept match (the `value` in a `Death` rule) |
| `death_type_concept_id`, `cause_source_value`, `cause_source_concept_id` | Modelled by Bunny, not currently used in filtering — populate them anyway if you have them, for forward compatibility (see [Schema compliance notes](schema.md#schema-compliance-notes)) |

---

## See also

- [Location & Geo-radius Filtering](location.md) — the closest existing parallel: optional table, flag-gated, varcat bypasses the union
- [CDM Schema Reference](schema.md) — `LOCATION`/`Specimen` optional-table pattern this follows
- [Bunny configuration](../bunny/configuration.md) — `OMOP_DEATH_ENABLED`
- [Availability concept — Death filtering](https://hutch.health/concepts/availability#death-filtering) — canonical Bunny-side documentation
