---
title: Running the Services
description: The three repos, what each one needs, and the order to bring them up
tags:
  - setup
  - deployment
---

# Running the services

A deployment is three services you run yourself, plus MySQL and Redis. **How you host them is entirely your choice** — containers, Kubernetes, plain VMs, whatever your organisation already runs. This page covers what each service is, what it needs, and the order to start them in. It does not prescribe a topology.

[Quick Start](../quick-start.md) is the same material for a development machine, with every command spelled out. If you are standing up a real deployment, read this page and borrow the commands from there.

??? note "Setting up with a coding agent? Copy this into your workspace as `AGENTS.md`"

    Save this beside the three cloned repos. Claude Code, Codex and similar tools read it automatically and will have the layout and the ordering rules without being told.

    ````markdown
    # Cohort Discovery Service — local setup

    Three services make up the platform. They are separate repos and run as
    separate processes.

    | Directory | Stack | Port |
    |---|---|---|
    | `cohort-discovery-service-api` | Laravel 12, PHP 8.2+ | 8100 |
    | `cohort-discovery-service-web` | Next.js 16, Node 24+ | 3000 |
    | `cohort-discovery-service-nlp` | FastAPI, Python 3.11 | 5001 |

    Also required: MySQL 8 and Redis 7. Two MySQL databases — the application
    database, and a second one holding the OMOP vocabulary.

    ## Order

    Bring them up in this order. The API calls NLP, and the web app calls the API.

    1. MySQL and Redis
    2. NLP
    3. API
    4. Web

    ## NLP

    ```bash
    cd cohort-discovery-service-nlp
    python -m venv venv && source venv/bin/activate
    pip install -r requirements.txt
    cp .env.example .env
    uvicorn app:app --host=0.0.0.0 --port=5001
    ```

    Point `DB_*` in its `.env` at the OMOP vocabulary database.
    Health check: `GET /health/ready` returns 503 while concepts load, then 200.

    ## API

    ```bash
    cd cohort-discovery-service-api
    composer install && npm install
    cp .env.example .env
    php artisan key:generate
    php artisan migrate
    ```

    Set at minimum: `APP_OPERATION_MODE=standalone`, `JWT_SECRET`, the `DB_*`
    and `DB_OMOP_*` connections, `REDIS_*`, and
    `COHORT_DISCOVER_NLP_SERVICE_BASE_URI`.

    Then seed the reference data:

    ```bash
    php artisan db:seed --class=WorkgroupSeeder
    php artisan db:seed --class=RolesAndPermissionsSeeder
    php artisan db:seed --class=StateSeeder
    php artisan db:seed --class=FeatureSeeder
    php artisan db:seed --class=PersonalAccessClientSeeder
    ```

    Do **not** run bare `php artisan db:seed` or `migrate:fresh --seed` against
    anything you care about. The default seeder also runs `CustodianSeeder`,
    which truncates the custodians table and inserts ten fake ones.

    A queue worker is needed as well as the HTTP process:
    `php artisan queue:work`.

    Health check: `GET /up` returns 200.

    ## Web

    ```bash
    cd cohort-discovery-service-web
    npm install
    cp .env.example .env
    npm run build && npm run start
    ```

    Set `API_BASE_URL`, `APPLICATION_MODE=standalone` and
    `NEXT_PUBLIC_LOGIN_URL`. `NEXT_PUBLIC_*` values and everything under
    `branding/` are compiled into the build, so changing them means rebuilding.

    ## Rules

    - Never commit a `.env`, a client secret or a JWT secret.
    - After editing anything in the API's `config/`, run
      `php artisan config:clear`.
    - `APP_OPERATION_MODE` is `standalone` unless you are HDR UK.
      An unrecognised value refuses to boot.
    ````

---

## The repos

| Service | Repo | Stack | Port | Health check |
|---|---|---|---|---|
| **API** | [`cohort-discovery-service-api`](https://github.com/HDRUK/cohort-discovery-service-api) | Laravel 12, PHP 8.2+ | 8100 | `GET /up` |
| **Web** | [`cohort-discovery-service-web`](https://github.com/HDRUK/cohort-discovery-service-web) | Next.js 16, Node 24+ | 3000 | `GET /` |
| **NLP** | [`cohort-discovery-service-nlp`](https://github.com/HDRUK/cohort-discovery-service-nlp) | FastAPI, Python 3.11 | 5001 | `GET /health/ready` |

Alongside them you need **MySQL 8** and **Redis 7**, and two MySQL databases: the application database, and a second holding the OMOP vocabulary that the API and NLP service both read.

**BUNNY** is not part of your deployment. It runs inside each data custodian's own infrastructure, polls your API for tasks and posts results back — see [Connecting Bunny](../../bunny/index.md).

---

## Minimum configuration

=== "API"

    ```dotenv
    APP_OPERATION_MODE=standalone

    JWT_SECRET=a-long-random-secret
    STANDALONE_JWT_TTL_MINUTES=120

    PASSPORT_TOKEN_EXPIRES_IN_DAYS=30
    PASSPORT_REFRESH_TOKEN_EXPIRES_IN_DAYS=60

    COHORT_DISCOVER_NLP_SERVICE_BASE_URI=http://nlp:5001
    ```

    Plus the `DB_*`, `DB_OMOP_*` and `REDIS_*` connections. The full list is in [API Service](../api.md).

=== "Web"

    ```dotenv
    APPLICATION_MODE=standalone
    API_BASE_URL=https://api.example.org
    NEXT_PUBLIC_LOGIN_URL=https://app.example.org/auth/login
    ```

=== "NLP"

    ```dotenv
    DB_HOST=mysql
    DB_NAME=omop
    OMOP_VIEW=distributions_and_concept_view
    ```

`APP_OPERATION_MODE=standalone` on the API and `APPLICATION_MODE=standalone` on the web app are what make this a self-contained deployment. The only other value, `integrated`, exists so the HDR UK Gateway can authenticate HDR UK's own hosted instance; it is not a general-purpose SSO mechanism. An unrecognised value refuses to boot rather than guessing.

---

## Seeding the database

Run `php artisan migrate`, then seed the reference data the platform needs to function:

| Seeder | Creates |
|---|---|
| `WorkgroupSeeder` | The nine workgroups claim mapping targets |
| `RolesAndPermissionsSeeder` | The four roles and their permissions |
| `StateSeeder` | Query and task lifecycle states |
| `FeatureSeeder` | Feature flags, at their shipped defaults |
| `PersonalAccessClientSeeder` | The Passport personal access client |

```bash
php artisan db:seed --class=WorkgroupSeeder
```

!!! warning "Don't run the bare seeder on a deployment"
    `php artisan db:seed` and `migrate:fresh --seed` run `DatabaseSeeder`, which also calls `CustodianSeeder` — it truncates the custodians table and replaces it with ten randomly generated ones. Seed the five above by class instead.

Create your own admin account afterwards, or seed demo accounts with `php artisan db:seed --class=StandaloneDemoSeeder` after setting `DEMO_USER_EMAIL` and `DEMO_USER_PASSWORD`.

---

## What runs where

The API needs **two processes**: the HTTP server, and `php artisan queue:work` for the Redis-backed job queue. Results posted back by custodians are processed on the queue, as are concept view refreshes, so without a worker queries are accepted and never complete.

---

## Build time versus runtime

This is the one asymmetry worth knowing before you choose how to deploy.

| | Web | API |
|---|---|---|
| Configuration is read | At **build** time for `NEXT_PUBLIC_*` and everything under `branding/` | At **runtime** |
| Changing it needs | A rebuild of the image | A restart, plus `php artisan config:clear` if config is cached |

So every deployment builds its own web image — [branding](branding.md) cannot be mounted into a running container. Keeping those edits across upgrades is [its own question](carrying-changes.md).

---

## Images and charts

Each repo has a `Dockerfile` at its root. We do not publish images to a public registry, so build your own from the tag you want to run. The `chart/` directory in each repo is scaffolding for HDR UK's own deployment pipeline rather than a general-purpose Helm chart — treat it as a reference, not something to install.

Beyond that, deployment is yours. Nothing in the platform assumes Kubernetes, a particular ingress or a particular secret store.

---

Once it runs, [make it your own](index.md#making-it-your-own): branding, your identity provider, and how far its claims are trusted.
