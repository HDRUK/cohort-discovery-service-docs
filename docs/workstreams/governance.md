---
title: Governance Workstream
description: Information Governance steps for onboarding to the Cohort Discovery Service
tags:
  - governance
  - onboarding
  - compliance
---

# Governance Workstream

Information Governance (IG) should be started as soon as the project is initiated. Governance steps are not always linear and can occur in any order.

!!! info "Responsible party"
    The **Data Custodian** is responsible for all governance steps. The HDR UK Technology Team can provide support and answer questions.

---

## Steps overview

| Step | Description | Notes |
|------|-------------|-------|
| **G1** | Obtain Data Controller Consent | Required before connecting live data |
| **G2** | Carry out Local Approvals / Processes | Optional; depends on local requirements |
| **G3** | Technical Risk Assessment | Optional; e.g. System Security Policy |

---

## G1 — Obtain Data Controller Consent

**Description**

This step must be completed before you can connect live data and query retrieval software to the Cohort Discovery Service.

!!! warning "No live data before G1"
    You can still carry out D1 (extract a subset), D2 (OMOP mapping), and D3 (create synthetic data). However, **you cannot load any real data** onto the secure network area connected to the Cohort Discovery Service until G1 is complete.

    Only **synthetic data** should be used to test the system until G1 is complete.

**Who is involved**

If a Data Custodian is not the Data Controller, consent must be obtained from the relevant Data Controller(s) regarding the use of the data.

**Flexibility**

The Cohort Discovery architecture is designed on a flexible technical philosophy that means Data Controllers can participate with their current governance and consent frameworks.

---

## G2 — Carry out Local Approvals / Processes

Depending on local processes, Data Custodians may decide that additional protocols are necessary, such as:

- **Public Benefit & Privacy Review** — e.g. the Public Benefit & Privacy Panel (PBPP) in Scotland
- **Internal data access applications** — as required by your organisation
- **Data sharing agreements** — if OMOP mapping is being outsourced to a vendor with direct access to row-level data

---

## G3 — Technical Risk Assessment

Data Custodians may decide that additional technical risk assessments are undertaken, such as:

- Creating and maintaining a **System Security Policy (SSP)**
- Conducting a penetration test of the secure network area

!!! tip "Governance and data selection"
    Governance steps typically require knowing what data you are going to select to make available for discovery, so they often go hand in hand with **D1 — Data Preparation**.

---

## Data Governance and Security Controls

In addition to the governance workstream steps, the Cohort Discovery Service includes several key technical controls to protect patient confidentiality. See the [Data Governance & Security](../architecture/governance.md) architecture page for the full details.

### Summary of built-in controls

=== "Data Protections"

    | Control | Description |
    |---------|-------------|
    | Raw data access | Identifiable data only ever handled within the Data Custodian's own environment |
    | PII removal | All PII (location, DOB, names, etc.) is withheld before data enters the secure area |
    | Pseudonymisation | Data is pseudonymised before being connected to Cohort Discovery |

=== "Query Protections"

    | Control | Description |
    |---------|-------------|
    | Disclosure control | Low-count suppression (counts < 10 → 0) and rounding (nearest 10) |
    | Query control | Queries only via pre-defined fields in the drag-and-drop interface |
    | Authentication | Multi-layer Gateway authentication + Safe People verification |

=== "Infrastructure Protections"

    | Control | Description |
    |---------|-------------|
    | Firewalls | Standard firewall controls; no additional inbound rules required |
    | Outbound-only | Query tool makes only outbound HTTPS requests |
    | Access control | Only authenticated Safe People can run queries |

---

## Note on synthetic data collections

Data Custodians who use synthetic data for testing the ETL processes can make this data available for querying by users who do not fall easily into the Safe Person categories. This can be useful to support ongoing development of Cohort Discovery within the wider community (e.g. governance staff, developers of similar products such as NHS DigiTrials).
