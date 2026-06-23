---
title: Two-Instance Pattern
description: Why Bunny requires two instances and how to configure them for Cohort Discovery
tags:
  - bunny
  - configuration
  - architecture
---

# Two-Instance Pattern

Bunny requires **two instances per OMOP database** when connected to the Cohort Discovery Service:

| Instance | `TASK_API_TYPE` | Purpose |
|----------|-----------------|---------|
| **Bunny-A** | `a` | Availability queries — real-time feasibility counts requested by researchers |
| **Bunny-B** | `b` | Distribution jobs — scheduled scans that seed Demographics and Concepts data |

Both instances use the **same credentials** (`TASK_API_USERNAME`, `TASK_API_PASSWORD`, `COLLECTION_ID`). Only `TASK_API_TYPE` differs.

!!! info "Why two instances?"
    The two types of task have different characteristics: availability queries are real-time and researcher-triggered, while distribution jobs run on a schedule and seed the vocabulary data that makes querying possible. Separating them ensures neither blocks the other.

---

## Docker Compose example

The recommended approach is to define both instances as services in a single `docker-compose.yml`:

```yaml title="docker-compose.yml"
services:

  bunny-a: # Availability queries (real-time feasibility counts)
    image: ghcr.io/health-informatics-uon/hutch/bunny:latest
    restart: unless-stopped
    environment:
      - TASK_API_TYPE=a
      - TASK_API_BASE_URL=https://api.cohort-discovery.healthdatagateway.org/api/v1
      - TASK_API_USERNAME=<your_client_id>
      - TASK_API_PASSWORD=<your_client_secret>
      - COLLECTION_ID=<your_collection_id>
      - DATASOURCE_DB_HOST=<your_db_host>
      - DATASOURCE_DB_DATABASE=<your_db_name>
      - DATASOURCE_DB_SCHEMA=<your_schema>
      - DATASOURCE_DB_USERNAME=<your_db_user>
      - DATASOURCE_DB_PASSWORD=<your_db_password>
      - DATASOURCE_DB_PORT=5432
      - DATASOURCE_DB_DRIVERNAME=postgresql

  bunny-b: # Distribution jobs (seeds Demographics and Concepts)
    image: ghcr.io/health-informatics-uon/hutch/bunny:latest
    restart: unless-stopped
    environment:
      - TASK_API_TYPE=b
      - TASK_API_BASE_URL=https://api.cohort-discovery.healthdatagateway.org/api/v1
      - TASK_API_USERNAME=<your_client_id>
      - TASK_API_PASSWORD=<your_client_secret>
      - COLLECTION_ID=<your_collection_id>
      - DATASOURCE_DB_HOST=<your_db_host>
      - DATASOURCE_DB_DATABASE=<your_db_name>
      - DATASOURCE_DB_SCHEMA=<your_schema>
      - DATASOURCE_DB_USERNAME=<your_db_user>
      - DATASOURCE_DB_PASSWORD=<your_db_password>
      - DATASOURCE_DB_PORT=5432
      - DATASOURCE_DB_DRIVERNAME=postgresql
```

```bash title="Starting both instances"
docker compose up -d
```

!!! note "Other database types"
    For SQL Server, Snowflake, or DuckDB, adjust `DATASOURCE_DB_DRIVERNAME` and the related connection variables. See the [Configuration Reference](configuration.md) and [hutch.health/bunny/config](https://hutch.health/bunny/config).

---

## Multiple collections on one server

Multiple pairs of Bunny instances can run on the same server. Each pair handles one OMOP database / Collection:

```yaml title="docker-compose.yml (multiple collections)"
services:

  # Collection 1 — Dataset A
  bunny-a-dataset1:
    image: ghcr.io/health-informatics-uon/hutch/bunny:latest
    environment:
      - TASK_API_TYPE=a
      - COLLECTION_ID=<collection_id_1>
      # ... other vars for dataset 1

  bunny-b-dataset1:
    image: ghcr.io/health-informatics-uon/hutch/bunny:latest
    environment:
      - TASK_API_TYPE=b
      - COLLECTION_ID=<collection_id_1>
      # ... other vars for dataset 1

  # Collection 2 — Dataset B
  bunny-a-dataset2:
    image: ghcr.io/health-informatics-uon/hutch/bunny:latest
    environment:
      - TASK_API_TYPE=a
      - COLLECTION_ID=<collection_id_2>
      # ... other vars for dataset 2

  bunny-b-dataset2:
    image: ghcr.io/health-informatics-uon/hutch/bunny:latest
    environment:
      - TASK_API_TYPE=b
      - COLLECTION_ID=<collection_id_2>
      # ... other vars for dataset 2
```

!!! tip "Multiple datasets"
    Data Custodians with multiple data cohorts should contact the HDR UK Technology Team for further support on structuring multiple Collections.

---

## Alternative: Bunny setup documentation

If you are not using Docker Compose, follow the [Bunny setup documentation](https://hutch.health/bunny/config) to configure a type-A and type-B instance using your preferred deployment method (Kubernetes, bare metal, etc.).
