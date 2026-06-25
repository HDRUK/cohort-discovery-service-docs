---
title: CLI Reference
description: somop command-line reference — generate, load, run, multi
tags:
  - somop
  - cli
---

# CLI Reference

somop has four top-level commands: `generate`, `load`, `run`, and `multi`.

```bash
somop --help
```

---

## `somop generate`

Generates synthetic OMOP CDM CSV files from a YAML config without starting any containers.

```bash
somop generate --config configs/conditions.yaml [OPTIONS]
```

**Options:**

| Option | Default | Description |
|--------|---------|-------------|
| `--config` | required | Path to YAML configuration file |
| `--out-dir` | from config | Override the output directory |
| `--n-people` | from config | Override `person.n_people` |
| `--seed` | from config | Override the random seed |
| `--chunk-size` | from config | Override chunk size |
| `--concepts` | — | Path to a `CONCEPT.csv` to copy into the output directory |

**Output:** Tab-separated CSV files in `out_dir`:

```
PERSON.csv
CONDITION_OCCURRENCE.csv
DRUG_EXPOSURE.csv
MEASUREMENT.csv
OBSERVATION.csv
PROCEDURE_OCCURRENCE.csv
SPECIMEN.csv
DEATH.csv
LOCATION.csv
```

**Example:**

```bash
somop generate \
  --config configs/conditions.yaml \
  --n-people 50000 \
  --seed 99 \
  --out-dir ./data/test_run
```

---

## `somop load`

Loads generated CSV files into a PostgreSQL database using [omop-lite](https://github.com/health-Informatics-UoN/omop-lite) via Docker Compose. Use this when you want a persistent database you can query directly.

```bash
somop load --config configs/conditions.yaml [OPTIONS]
```

**Options:**

| Option | Default | Description |
|--------|---------|-------------|
| `--config` | required | Path to YAML configuration file |
| `--db-name` | config file stem | Postgres database name |
| `--db-password` | `postgres` | Postgres password (also reads `DB_PASSWORD` env var) |
| `--db-url` | — | Use an existing Postgres instance: `postgresql://user:pass@host:port/db` (also reads `DATABASE_URL` env var) |
| `--db-port` | — | Expose the containerised Postgres on this host port |
| `--drop-db / --no-drop-db` | drop | Drop and recreate the DB before loading (when using `--db-url`) |
| `--concepts` | — | Path to a `CONCEPT.csv` to copy into the data directory |
| `--compose-out` | `<out_dir>/docker-compose.load.yaml` | Where to write the generated Compose file |

**Containerised Postgres (default):**

```bash
somop load --config configs/simple.yaml --db-port 5433
```

A Postgres container is started, data is loaded via omop-lite, then the containers stop.

**External Postgres:**

```bash
somop load \
  --config configs/simple.yaml \
  --db-url postgresql://postgres:postgres@localhost:5432/my_omop
```

---

## `somop run`

The main end-to-end command. Generates data, writes a Docker Compose file, and starts a full stack: PostgreSQL + omop-lite + two BUNNY instances. Press `Ctrl+C` to stop and remove all containers.

```bash
somop run \
  --config configs/conditions.yaml \
  --collection-id <uuid> \
  --api-url http://host.docker.internal:8100/api/v1 \
  --api-username admin@example.com \
  --api-password yourpassword
```

**Options:**

| Option | Default | Description |
|--------|---------|-------------|
| `--config` | required | Path to YAML configuration file |
| `--collection-id` | required | BUNNY collection UUID registered in the API |
| `--api-url` | required | API base URL — use `host.docker.internal` to reach the host from inside Docker |
| `--api-username` | required | API username (also reads `TASK_API_USERNAME` env var) |
| `--api-password` | required | API password (also reads `TASK_API_PASSWORD` env var) |
| `--db-name` | config stem | Postgres database name |
| `--db-password` | `postgres` | Postgres password (also reads `DB_PASSWORD` env var) |
| `--db-url` | — | Use an external Postgres instead of a container |
| `--db-port` | — | Expose containerised Postgres on this host port |
| `--drop-db / --no-drop-db` | drop | Drop and recreate DB before loading (with `--db-url`) |
| `--concepts` | — | Path to a `CONCEPT.csv` |
| `--bunny-build` | — | Path to a local BUNNY Dockerfile directory — builds instead of pulling from the registry |
| `--compose-out` | `<out_dir>/docker-compose.run.yaml` | Where to write the generated Compose file |

### What happens when you run `somop run`

```mermaid
flowchart TD
    A["somop run ..."] --> B["Load YAML config"]
    B --> C["Generate OMOP CSV files\n(somop.generate)"]
    C --> D["Build docker-compose.run.yaml"]
    D --> E["docker compose down\n(clean up previous run)"]
    E --> F["docker compose up --build"]
    F --> db["db (Postgres 16)\n⬛ healthcheck: pg_isready"]
    db --> loader["loader (omop-lite)\n creates schema, loads CSVs"]
    loader --> bunny_a["bunny-a\n TASK_API_TYPE=a"]
    loader --> bunny_b["bunny-b\n TASK_API_TYPE=b"]
    bunny_a --> poll["Poll API for tasks"]
    bunny_b --> poll
```

Services start in dependency order:

1. **`db`** — Postgres 16; waits for `pg_isready` healthcheck
2. **`loader`** — omop-lite; waits for `db` to be healthy, creates the OMOP schema and loads the CSVs
3. **`bunny-a`** and **`bunny-b`** — both wait for `loader` to complete, then register with the API and begin polling for tasks

Press `Ctrl+C` to trigger a graceful shutdown: `docker compose down`.

### Example with local BUNNY build and external Postgres

```bash
somop run \
  --config configs/uk_t2d_primary_care.yaml \
  --collection-id e2da6447-8e9b-444a-845b-501a206c0199 \
  --api-url http://host.docker.internal:8100/api/v1 \
  --api-username admin@example.com \
  --api-password secret \
  --db-url postgresql://postgres:postgres@host.docker.internal:5435/t2d_primary_care \
  --bunny-build ../hutch-bunny
```

!!! info "`host.docker.internal`"
    When BUNNY runs inside Docker and needs to reach the API running on your host machine, use `host.docker.internal` instead of `localhost`. This resolves to the host machine's IP from within a Docker container on macOS and Windows. On Linux, add `--add-host host.docker.internal:host-gateway` to the container, or use your host's LAN IP directly.

---

## `somop multi`

Runs multiple datasets in a single Docker Compose stack, each with its own BUNNY instance and collection ID.

```bash
somop multi generate --config configs/multi_example.yaml
somop multi run --config configs/multi_example.yaml
```

The multi config file references other configs by path:

```yaml
# configs/multi_example.yaml
datasets:
  - config: conditions.yaml
    collection_id: <uuid-1>
    db_port: 5433

  - config: mortality_conditions.yaml
    collection_id: <uuid-2>
    db_port: 5434

api_url: http://host.docker.internal:8100/api/v1
api_username: admin@example.com
api_password: secret
bunny_build: ../hutch-bunny   # optional local BUNNY build
```

Each dataset gets its own `db` and `loader` service, namespaced by dataset name in the Compose file.
