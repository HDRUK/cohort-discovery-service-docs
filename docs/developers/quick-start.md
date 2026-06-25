---
title: Quick Start
description: Get the Cohort Discovery Service full stack running locally from scratch
tags:
  - setup
  - local development
---

# Quick Start

This guide walks you through running the Web, API, and NLP services together on your development machine from scratch. For deeper configuration options, see the per-service pages.

---

## Prerequisites

| Requirement | Version | Notes |
|-------------|---------|-------|
| PHP | 8.2+ | With extensions: `pdo_mysql`, `redis`, `gd`, `zip`, `bcmath` |
| Composer | 2.x | PHP package manager |
| Node.js | 24+ | Required for Web service |
| npm | 10+ | Bundled with Node.js 24 |
| Python | 3.11 | For NLP service |
| MySQL | 8.0 | App database + OMOP vocabulary database |
| Redis | 7.x | Queue and cache backend |
| Docker | 24+ | Required only for `somop` synthetic data tool |

!!! tip "macOS with Homebrew"
    ```bash
    brew install php composer node python@3.11 mysql redis
    brew services start mysql
    brew services start redis
    ```

---

## 1. Clone the repos

```bash
mkdir cohort-discovery && cd cohort-discovery

git clone https://github.com/HDRUK/cohort-discovery-service-api
git clone https://github.com/HDRUK/cohort-discovery-service-web
git clone https://github.com/HDRUK/cohort-discovery-service-nlp
```

---

## 2. Start the NLP service

Start NLP first — the API calls it during operation.

```bash
cd cohort-discovery-service-nlp
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install pip --upgrade
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` to point at your OMOP vocabulary database (shared with the API):

```dotenv
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=omop
DB_USER=root
DB_PASS=yourpassword
OMOP_VIEW=distributions_and_concept_view
APP_ENV=development
```

Start the service:

```bash
uvicorn app:app --host=0.0.0.0 --port=5001 --reload
```

Verify: `curl http://localhost:5001/` — should return `{"status":"ok"}`.

---

## 3. Set up and start the API

```bash
cd ../cohort-discovery-service-api
composer install
npm install
cp .env.example .env
php artisan key:generate
```

Minimum `.env` for standalone local development:

```dotenv
APP_ENV=local
APP_DEBUG=true
APP_OPERATION_MODE=standalone

DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=cohort_discovery
DB_USERNAME=root
DB_PASSWORD=yourpassword

REDIS_HOST=127.0.0.1
REDIS_PORT=6379
REDIS_PASSWORD=null

COHORT_DISCOVER_NLP_SERVICE_BASE_URI=http://localhost:5001
JWT_SECRET=a-long-random-string-for-local-dev
```

### Set up databases

**Primary app database:**
```bash
mysql -u root -p -e "CREATE DATABASE cohort_discovery;"
php artisan migrate:fresh --seed
```

**OMOP vocabulary database (minimal — no Athena download required):**
```bash
mysql -u root -p -e "CREATE DATABASE omop;"
```

Add the OMOP connection to `.env`:
```dotenv
DB_OMOP_CONNECTION=omop
DB_OMOP_HOST=127.0.0.1
DB_OMOP_PORT=3306
DB_OMOP_DATABASE=omop
DB_OMOP_USERNAME=root
DB_OMOP_PASSWORD=yourpassword
```

Run the OMOP schema and minimal seeder:
```bash
php artisan migrate --database omop --path database/migrations_omop
php artisan db:seed --class=MinimalOmopSeeder --database=omop
```

!!! info "Full OMOP vocabulary"
    For production-quality concept search, download vocabularies from [Athena](https://athena.ohdsi.org) and load them with [omop-lite](https://github.com/health-Informatics-UoN/omop-lite). The minimal seeder covers enough concepts for local UI and API development.

### Start the API

```bash
composer run dev
```

This runs four processes concurrently:

- `php artisan serve` — dev server on port 8100
- `php artisan queue:listen --tries=1` — Redis job queue
- `php artisan pail --timeout=0` — log streaming
- `npm run dev` — Vite asset compilation

Verify: `curl http://localhost:8100/api/v1/ping` should return `{"pong":true}`.

---

## 4. Start the Web service

```bash
cd ../cohort-discovery-service-web
npm install
cp .env.example .env
```

Minimum `.env` for standalone mode:

```dotenv
API_BASE_URL=http://localhost:8100
APPLICATION_MODE=standalone
NEXT_PUBLIC_LOGIN_URL=http://localhost:3000/auth/login
```

Start the dev server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000). You should see the login page.

---

## 5. Smoke test

| Service | Check | Expected |
|---------|-------|---------|
| NLP | `curl http://localhost:5001/` | `{"status":"ok"}` |
| API | `curl http://localhost:8100/api/v1/ping` | `{"pong":true}` |
| Web | Open `http://localhost:3000` | Login page loads |

---

## Default demo credentials

After `migrate:fresh --seed` (standalone mode), the `StandaloneDemoSeeder` creates:

| Role | Email | Password |
|------|-------|---------|
| Admin | Set via `DEMO_USER_EMAIL` in `.env` | Set via `DEMO_USER_PASSWORD` |
| Researcher | Set via `DEMO_RESEARCHER_EMAIL` in `.env` | Set via `DEMO_RESEARCHER_PASSWORD` |

If those env vars are not set, check the seeder output or run `php artisan db:seed --class=StandaloneDemoSeeder` after setting them.

---

## Next steps

- [API Service](api.md) — full environment variable reference, custom artisan commands, testing
- [Web Service](web.md) — testing with Jest and Cypress, Storybook, project structure
- [NLP Service](nlp.md) — tuning fuzzy matching, debugging concept resolution
- [Deployment Modes](modes.md) — switching to integrated mode or wiring up the Gateway
- [Synthetic Data (somop)](somop/index.md) — spin up a local BUNNY instance with synthetic OMOP data for end-to-end testing
