---
title: Data Governance & Security
description: Data governance and security controls for the Cohort Discovery Service
tags:
  - governance
  - security
  - data-protection
---

# Data Governance & Security

The Cohort Discovery Service architecture has been specifically designed to allow Data Custodians to retain full control of their data while simplifying data governance requirements.

---

## Summary of controls

| # | Protection Mechanism | Description |
|---|----------------------|-------------|
| 1 | **Raw data access** | Identifiable data is only handled by the Data Custodian within their own secure environment. Full control of which data is uploaded. |
| 2 | **PII removal** | All Personally Identifiable Information (PII) — patient location, date of birth, names, etc. — must be withheld. No PII is held in any software. |
| 3 | **Disclosure control** | Only aggregated results leave the Data Custodian's control. Configurable low-count suppression and rounding are applied. |
| 4 | **Query control** | Queries can only be constructed from pre-defined fields via the drag-and-drop interface. |

---

## Control 1 — Raw Data Access

!!! warning "Identifiable data never leaves your environment"
    Identifiable data is **only ever handled by Data Custodian employees** within the Data Custodian's IT infrastructure. The HDR UK Technology Team will not need to see your row-level data at any point.

- **(a) Handling** — Identifiable data is only ever handled by Data Custodian employees within their IT infrastructure.
- **(b) Pseudonymisation** — Data is pseudonymised and all PII removed by the Data Custodian before being connected to the Cohort Discovery query retrieval software. Pseudonymised record-level data will not be available outside of the Data Custodian's infrastructure.
- **(c) PII removal** — All PII (patient location, date of birth, names, etc.) must be withheld. No PII will be held in any software outside the raw data store.

---

## Control 2 — Firewalls

Firewalls are in place with standard controls against malicious attacks. **No additional inbound firewall rules are required** — the query tool (e.g. Bunny) makes only outbound requests.

---

## Control 3 — Pseudonymised Data Access (OMOP)

**(a) Cohort Discovery Accessibility**

The Cohort Discovery Service is accessible to end users **only via the Gateway**. End users, HDR UK employees, and support staff will not be able to directly access the row-level pseudonymised OMOP data hosted by the Data Custodian.

**(b) Disclosure Control**

Only **metadata and aggregated results** leave the Data Custodian's control. Two configurable controls protect against re-identification:

=== "Low Count Suppression"

    Counts below a configurable threshold are returned as `0`. The recommended setting is:

    - Counts of **less than 10** → returned as `0`

=== "Rounding"

    Counts above the suppression threshold are rounded to the nearest 10. The recommended setting is:

    - Counts of **5 to 10** → rounded to nearest 10

!!! info "Differencing attacks"
    It is not possible to query the ID of an individual person in the Cohort Discovery query builder. This means **differencing attacks are not possible**.

**(c) Query Control**

End user queries can **only be constructed from pre-defined fields** within the Cohort Discovery Service. The drag-and-drop interface ensures users can only query data that has been authorised.

HDR UK can also query Cohort Discovery application logs to provide additional transparency to Data Custodians on who is using the application.

---

## Authentication

### Authentication I — Gateway identity

All users of Cohort Discovery must firstly be authenticated users of the Gateway. Anyone can register with the Gateway (via Google, Microsoft, LinkedIn, ORCID, or OpenAthens). Gateway users who also wish to use Cohort Discovery undergo **additional authentication**.

Access is assessed using the **Five Safes Framework**, focusing on:

- **Safe People** — verified identity and appropriate credentials
- **Safe Projects** — legitimate research purpose for public benefit

### Authentication II — Safe People criteria

Cohort Discovery can only be accessed by **Safe People**. Requests are validated manually by the HDR UK administration team. Safe Person criteria can be set by each Data Custodian.

Checks currently undertaken by HDR UK include:

- Checking a user's publication record (e.g. ORCID)
- General internet checks on an individual's profile
- Users must work for appropriate and trusted organisations (academia, public sector, or industry)
- Generic email domains (gmail, hotmail, etc.) are **not accepted**

!!! info "NHS SDE Network"
    The NHS SDE Network is responsible for additional review of users interested in accessing their data collections. See the [NHS SDE Network page](https://healthdatagateway.org/en/about/cohort-discovery?tab=nhs-sde-network) for details. **This is an ongoing area of development and is subject to change.**

### Authentication III — Terms of use

All users must agree to the following terms of use and **re-sign every 6 months**:

> *"I confirm that my use of the tool will be for the sole purpose of understanding the size of populations relevant to a particular research question and that any resulting study or clinical trial will be for public benefit as defined by the National Data Guardian.*
>
> *I will not: share, publish or communicate the results or findings from the tool (except with collaborators for research funding applications); use the results for marketing or policy development.*
>
> *I understand that my access to the tool may be terminated if I do not comply."*

All users must also adhere to the [Gateway Terms and Conditions](https://www.healthdatagateway.org/about/terms-and-conditions).

---

## DPIA

!!! tip "DPIA not required"
    Data Custodians are **not required** to carry out a Data Protection Impact Assessment (DPIA) for participation in the Cohort Discovery Service. If a Custodian wishes to carry one out, HDR UK can answer relevant questions. Given the anonymisation and controls in place, a DPIA would typically return that GDPR does not apply.
