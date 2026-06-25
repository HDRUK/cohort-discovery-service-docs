---
title: Installation
description: How to install somop
tags:
  - somop
  - setup
---

# Installing somop

## Prerequisites

- Python 3.9+
- Docker 24+ (required for `somop load` and `somop run`)

---

## Install

Clone the repo (it lives alongside the other services) and install in editable mode:

```bash
pip install -e path/to/somop
```

If you are working in a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate
pip install -e path/to/somop
```

---

## Verify

```bash
somop --help
```

Expected output:
```
Usage: somop [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  generate  Generate synthetic OMOP CDM CSV files from a YAML config.
  load      Load generated CSV files into a PostgreSQL database.
  multi     Multi-dataset generate and run.
  run       Generate data + start full stack (Postgres + BUNNY).
```

---

## Docker

`somop load` and `somop run` spin up Docker containers. Ensure Docker Desktop (or Docker Engine) is running before using these commands.

The Docker images used are:

| Image | Purpose |
|-------|---------|
| `postgres:16` | OMOP CDM database |
| `ghcr.io/health-informatics-uon/omop-lite:latest` | Schema creation and data loading |
| `ghcr.io/health-informatics-uon/hutch/bunny:edge` | BUNNY task resolver (or a local build) |

These images are pulled automatically on first use.

!!! tip "Using a local BUNNY build"
    If you are developing BUNNY locally, pass `--bunny-build path/to/hutch-bunny` to `somop run` to build the BUNNY image from your local source instead of pulling from the registry.
