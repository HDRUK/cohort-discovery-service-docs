---
title: Developer Guide
description: How to set up, run, and contribute to the Cohort Discovery Service full stack
icon: material/code-braces
---

# Developer Guide

The Cohort Discovery Service is a federated platform that lets researchers run cohort queries against pseudonymised health data held by Data Custodians — without the underlying data ever leaving a custodian's infrastructure. This guide covers everything you need to develop, run, and contribute to the three services that make it up.

---

## Services

Three services are actively developed in this codebase. A fourth — **BUNNY** — is an external dependency deployed at each custodian site.

```mermaid
graph TD
    Browser["Browser"] -->|HTTPS| Web

    subgraph cds-web["cohort-discovery-service-web · Next.js 16 · :3000"]
        Web["Web"]
    end

    subgraph cds-api["cohort-discovery-service-api · Laravel 12 · :8100"]
        API["API"]
    end

    subgraph cds-nlp["cohort-discovery-service-nlp · FastAPI · :5001"]
        NLP["NLP"]
    end

    Web -->|Server Actions| API
    API -->|POST /extract| NLP
    API --- MySQL[("MySQL\napp DB + OMOP vocab")]
    API --- Redis[("Redis\nqueue + cache")]

    subgraph Custodian["Data Custodian Site"]
        BUNNY["BUNNY · hutch-bunny\nPython 3.13+"] -->|SQL| OMOPDB[("OMOP CDM DB\nPostgres · MSSQL · DuckDB · Snowflake")]
    end

    API <-->|"poll tasks / POST results"| BUNNY
```

| Service | Repo | Stack | Dev Port | Role |
|---------|------|-------|----------|------|
| **Web** | `cohort-discovery-service-web` | Next.js 16, React 19, TypeScript | 3000 | Frontend UI — App Router, Server Actions, role-based views |
| **API** | `cohort-discovery-service-api` | Laravel 12, PHP 8.2+, MySQL, Redis | 8100 | Core backend — queries, tasks, OMOP concepts, async jobs |
| **NLP** | `cohort-discovery-service-nlp` | FastAPI, Python 3.11, RapidFuzz | 5001 | Free-text → OMOP concept extraction via fuzzy matching |
| BUNNY | `hutch-bunny` (external — Univ. Nottingham) | Python 3.13+, SQLAlchemy | — | Custodian-side task resolver |

The **Web** layer calls the **API** only — it never contacts the NLP service or custodian databases directly. The **API** and **NLP** service both share access to the OMOP vocabulary database.

---

## Deployment modes

Run **standalone**: `APP_OPERATION_MODE=standalone` on the API, `APPLICATION_MODE=standalone` on the web app. It is self-contained — local accounts, Laravel Passport and a local JWT, with optional OIDC SSO in front — and it is what local development and every deployment outside HDR UK uses, including deployments that want single sign-on.

The only other value, `integrated`, delegates authentication to the HDR UK Gateway for HDR UK's own hosted deployment. It is not a general-purpose SSO mechanism and will not work with a third-party identity provider. Unless you are running that deployment, ignore it.

An unrecognised value refuses to boot rather than quietly defaulting to one or the other.

[:octicons-arrow-right-24: Deploying your own instance](deploying/index.md)

---

## In this guide

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

- :material-rocket-launch-outline: **Deploying Your Own Instance**

    ---
    Branding, your identity provider, claim mapping and access control policy.

    [:octicons-arrow-right-24: Deploying Your Own Instance](deploying/index.md)

- :material-flask: **Synthetic Data (somop)**

    ---
    Generate synthetic OMOP data for local BUNNY testing without real patient records.

    [:octicons-arrow-right-24: somop](somop/index.md)

- :material-source-pull: **Contributing**

    ---
    Branch workflow, pre-PR checks, PR title conventions, coding standards.

    [:octicons-arrow-right-24: Contributing](contributing.md)

</div>
