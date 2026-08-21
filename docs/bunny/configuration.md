---
title: Bunny Configuration Reference
description: All Bunny environment variables required to connect to the Cohort Discovery Service
tags:
  - bunny
  - configuration
  - reference
---

# Bunny Configuration Reference

Bunny is configured entirely via environment variables. This page lists the variables required to connect Bunny to the Cohort Discovery Service.

!!! info "Full Bunny docs"
    This page covers the configuration required for Cohort Discovery integration. For full Bunny configuration documentation, see [hutch.health/bunny/config](https://hutch.health/bunny/config).

---

## Cohort Discovery connection variables

| Variable | Required | Description |
|----------|----------|-------------|
| `TASK_API_BASE_URL` | ✓ | Base URL for the Cohort Discovery Task API |
| `TASK_API_USERNAME` | ✓ | Client ID from your Host in Cohort Discovery |
| `TASK_API_PASSWORD` | ✓ | Client Secret from your Host in Cohort Discovery |
| `COLLECTION_ID` | ✓ | Collection ID from your Collection in Cohort Discovery |
| `TASK_API_TYPE` | ✓ | `a` for availability queries; `b` for distribution jobs |

### Production API URL

```
https://api.cohort-discovery.healthdatagateway.org/api/v1
```

---

## Database connection variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DATASOURCE_DB_HOST` | ✓ | Hostname or IP of your OMOP database |
| `DATASOURCE_DB_DATABASE` | ✓ | Database name |
| `DATASOURCE_DB_SCHEMA` | ✓ | Schema name containing OMOP tables |
| `DATASOURCE_DB_USERNAME` | ✓ | Database username |
| `DATASOURCE_DB_PASSWORD` | ✓ | Database password |
| `DATASOURCE_DB_PORT` | ✓ | Database port |
| `DATASOURCE_DB_DRIVERNAME` | ✓ | SQLAlchemy driver name (see table below) |

### Supported database drivers

| Database | `DATASOURCE_DB_DRIVERNAME` | Default port |
|----------|---------------------------|-------------|
| PostgreSQL | `postgresql` | `5432` |
| SQL Server | `mssql+pyodbc` | `1433` |
| DuckDB | `duckdb` | — |
| Snowflake | `snowflake` | `443` |

!!! note "Additional variables for some drivers"
    SQL Server and Snowflake may require additional configuration variables. See [hutch.health/bunny/config](https://hutch.health/bunny/config) for driver-specific settings.

---

## Optional feature flags

These variables enable Bunny to query optional OMOP CDM tables. Both default to `false` and require the corresponding table to be populated in your OMOP database:

| Variable | Required | Description |
|----------|----------|--------------|
| `OMOP_SPECIMEN_ENABLED` | | Enables filtering on the Specimen table. Available from Bunny v1.7. |
| `OMOP_LOCATION_ENABLED` | | Enables geo-radius filtering against the Location table (`latitude`/`longitude`). Requires **OMOP CDM v5.4**. Available from Bunny v1.8. |
| `OMOP_DEATH_ENABLED` | | Enables querying the Death table (`death_date`, `cause_concept_id`). No CDM version requirement. Available from Bunny v1.9 — see [Death & Cause-of-Death Filtering](../omop/death.md). |

See [hutch.health/bunny/config#database](https://hutch.health/bunny/config#database) for full details, and [Availability — Location filtering](https://hutch.health/concepts/availability#location-filtering) for how the `GEO_RADIUS` rule is used.

---

## Example configurations

=== "PostgreSQL"

    ```yaml title="docker-compose.yml"
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
    ```

=== "SQL Server"

    ```yaml title="docker-compose.yml"
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
      - DATASOURCE_DB_PORT=1433
      - DATASOURCE_DB_DRIVERNAME=mssql+pyodbc
    ```

=== "Snowflake"

    ```yaml title="docker-compose.yml"
    environment:
      - TASK_API_TYPE=a
      - TASK_API_BASE_URL=https://api.cohort-discovery.healthdatagateway.org/api/v1
      - TASK_API_USERNAME=<your_client_id>
      - TASK_API_PASSWORD=<your_client_secret>
      - COLLECTION_ID=<your_collection_id>
      - DATASOURCE_DB_DRIVERNAME=snowflake
      # See hutch.health/bunny/config for full Snowflake variables
    ```

---

## Obfuscation settings

Data Custodians should configure obfuscation on their Bunny instance to meet disclosure control requirements:

| Setting | Recommended value | Description |
|---------|-------------------|-------------|
| Low count suppression | `< 10` → return `0` | Counts below this threshold are suppressed |
| Rounding | Round to nearest 10 | Counts above suppression threshold are rounded |

See [hutch.health/bunny/config](https://hutch.health/bunny/config) for the environment variables that control obfuscation.
