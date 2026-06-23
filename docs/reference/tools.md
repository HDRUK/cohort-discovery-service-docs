---
title: Query Retrieval Tools
description: Comparison of query retrieval tools supported by the Cohort Discovery Service
tags:
  - tools
  - bunny
  - reference
---

# Query Retrieval Tools

The Cohort Discovery Service supports multiple query retrieval tools. Data Custodians choose the tool that best fits their environment and governance requirements.

---

## Comparison

| Tool | Type | Developer | Key characteristics |
|------|------|-----------|---------------------|
| **Bunny** | Open source | University of Nottingham | Outbound-only; containerised; obfuscation built-in; federated via Hutch Relay |
| **BC\|INSIGHT** | Commercial | BC Platforms | Proprietary; contact BC Platforms for details |
| **Custom** | Build your own | Data Custodian | Must meet HDR UK API standards |

---

## Bunny

Bunny is the **recommended open-source option** for most Data Custodians.

=== "Overview"

    - Fetches Cohort Discovery queries and resolves them against an OMOP database
    - Deployed in your local environment — makes **only outgoing requests**
    - Enables obfuscation of query results (low-count suppression and rounding)
    - Can participate in a federated network through **Hutch Relay**
    - Available as a container image for easy deployment
    - Also runnable as a CLI query executor

=== "Infrastructure requirements"

    | Requirement | Minimum |
    |-------------|---------|
    | CPU | 2 vCPUs |
    | Memory | 4 GB RAM |
    | Runtime | OCI-compliant (Docker, Podman, Kubernetes) |
    | Network | Outbound HTTPS port 443 only |
    | Database | PostgreSQL 14–18 / SQL Server 2019–2022 / DuckDB 1.x / Snowflake |

=== "Resources"

    | Resource | Link |
    |----------|------|
    | Quickstart | [hutch.health/bunny/quickstart](https://hutch.health/bunny/quickstart) |
    | Configuration | [hutch.health/bunny/config](https://hutch.health/bunny/config) |
    | Deployment requirements | [hutch.health/bunny/deployment/requirements](https://hutch.health/bunny/deployment/requirements) |
    | User guide | [health-informatics-uon.github.io/hutch/bunny](https://health-informatics-uon.github.io/hutch/bunny) |
    | GitHub | [github.com/Health-Informatics-UoN/hutch-bunny](https://github.com/Health-Informatics-UoN/hutch-bunny) |
    | Report issues | [github.com/Health-Informatics-UoN/hutch-bunny/issues](https://github.com/Health-Informatics-UoN/hutch-bunny/issues) |

---

## BC|INSIGHT

BC|INSIGHT is a commercial query retrieval tool developed by BC Platforms.

- Cohort Discovery Service is **compatible** with BC|INSIGHT
- Contact BC Platforms directly for installation instructions, contract options, and support
- [bcplatforms.com](https://www.bcplatforms.com)

---

## Build Your Own

Data Custodians are welcome to develop their own query retrieval tool.

!!! warning "API compliance required"
    Any custom tool must meet the required API standards set out in the Cohort Discovery [Swagger documentation](https://api.cohort-discovery.dev.hdruk.cloud/api/documentation).

Contact the HDR UK Technology Team at [gateway@hdruk.ac.uk](mailto:gateway@hdruk.ac.uk) to discuss this option before beginning development.

---

## OMOP mapping tools

For tools to help you map your source data to OMOP (White Rabbit, Carrot Mapper, Carrot-CDM), see the [OMOP Mapping Tools](../omop/mapping-tools.md) page.
