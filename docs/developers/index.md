---
title: Developer Guide
description: How to set up, run, and contribute to the Daphne full-stack platform
icon: material/code-braces
---

# Developer Guide

This guide is for engineers working on the Daphne platform — the three services that make up the Cohort Discovery Service, plus the tooling around them.

<div class="grid cards" markdown>

- :material-rocket-launch: **Quick Start**

    ---
    Get all three services running locally in one go.

    [:octicons-arrow-right-24: Quick Start](quick-start.md)

- :material-server: **API Service**

    ---
    Laravel API: env config, OMOP setup, artisan commands, testing.

    [:octicons-arrow-right-24: API Service](api.md)

- :material-monitor: **Web Service**

    ---
    Next.js frontend: env config, dev server, testing, patterns.

    [:octicons-arrow-right-24: Web Service](web.md)

- :material-brain: **NLP Service**

    ---
    FastAPI NLP: env config, endpoints, fuzzy matching tuning.

    [:octicons-arrow-right-24: NLP Service](nlp.md)

- :material-swap-horizontal: **Deployment Modes**

    ---
    Standalone vs Integrated — what changes and how to configure each.

    [:octicons-arrow-right-24: Deployment Modes](modes.md)

- :material-flask: **Synthetic Data (somop)**

    ---
    Generate synthetic OMOP data for local BUNNY testing without real patient records.

    [:octicons-arrow-right-24: somop](somop/index.md)

- :material-source-pull: **Contributing**

    ---
    Branch workflow, pre-PR checks, PR title conventions, coding standards.

    [:octicons-arrow-right-24: Contributing](contributing.md)

</div>

---

## Platform Overview

Daphne is a federated cohort discovery platform. Researchers build cohort queries in the **Web** frontend; the **API** manages those queries, dispatches tasks to data custodians, and calls the **NLP** service to handle free-text input. At each custodian site, **BUNNY** polls the API for tasks, runs them against a local OMOP CDM database, and posts obfuscated results back — the raw data never leaves the custodian's infrastructure.

```mermaid
graph TD
    Browser["Browser"] -->|HTTP| Web["Web (Next.js :3000)"]
    Web -->|Server Actions| API["API (Laravel :8100)"]
    API -->|HTTP POST /extract| NLP["NLP (FastAPI :5001)"]
    API --- MySQL[("MySQL\napp DB + OMOP vocab")]
    API --- Redis[("Redis\nqueue + cache")]

    subgraph Custodian["Data Custodian Site"]
        Bunny["BUNNY (Python)"] -->|queries| OMOPDB[("OMOP CDM DB")]
    end

    API <-->|poll tasks / POST results| Bunny
```

The **Web** layer calls the **API** only — it never contacts the NLP service or custodian databases directly. The **API** and **NLP** service both connect to the shared OMOP vocabulary database.

---

## Services at a glance

| Service | Repo | Stack | Dev Port | Role |
|---------|------|-------|----------|------|
| Web | `cohort-discovery-service-web` | Next.js 16, React 18, TypeScript | 3000 | Frontend UI — App Router, Server Actions, role-based views |
| API | `cohort-discovery-service-api` | Laravel 12, PHP 8.2+, MySQL, Redis | 8100 | Core backend — queries, tasks, OMOP concepts, async jobs |
| NLP | `cohort-discovery-service-nlp` | FastAPI, Python 3.11, RapidFuzz | 5001 | Free-text → OMOP concept extraction via fuzzy matching |
| BUNNY | `hutch-bunny` (external, Univ. Nottingham) | Python 3.13+, SQLAlchemy | — | Custodian-side task resolver |

---

## Deployment modes

The platform supports two authentication modes, controlled by an environment variable in each service:

| Mode | API (`APP_OPERATION_MODE`) | Web (`APPLICATION_MODE`) | Auth mechanism |
|------|---------------------------|--------------------------|----------------|
| **Standalone** | `standalone` | `standalone` | Laravel Passport + local JWT |
| **Integrated** | `integrated` | `integrated` | HDR UK Gateway OAuth2 SSO |

Use **standalone** for local development. Use **integrated** for production deployments embedded within the HDR UK Gateway.

See [Deployment Modes](modes.md) for the full configuration walkthrough.
