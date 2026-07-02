---
title: Connecting Query Retrieval Tools
description: Overview of connecting Bunny to the HDR UK Cohort Discovery Service
tags:
  - bunny
  - integration
  - onboarding
  - BC|INSIGHT
---

# Connecting Query Retrieval Tools

# Connecting Bunny

**Bunny** is an open-source application developed by the University of Nottingham that supports Cohort Discovery. It fetches tasks from the Cohort Discovery API and resolves them against your local OMOP database.

<div class="grid cards" markdown>

- :material-stairs: **Step-by-Step Setup**

    ---
    Nine-step guide to creating a Host, Collection, and connecting Bunny.

    [:octicons-arrow-right-24: Setup Guide](setup.md)

- :material-cog: **Configuration Reference**

    ---
    All Bunny environment variables for connecting to Cohort Discovery.

    [:octicons-arrow-right-24: Configuration](configuration.md)

- :material-rabbit: **Two-Instance Pattern**

    ---
    Why Bunny requires two instances and how to configure them.

    [:octicons-arrow-right-24: Two-Instance Pattern](two-instance-pattern.md)

</div>

---

## Key features of Bunny

- **Outbound-only** — makes only outgoing requests, enabling safe execution behind your firewall
- **Obfuscation** — configurable low-count suppression and rounding to simplify data governance
- **Federated** — can participate in a federated network via Hutch Relay
- **Flexible deployment** — available as a container image or CLI tool

---

## Prerequisites

Before connecting Bunny, ensure you have:

- [X] Cohort Discovery access approved and a Gateway account
- [X] An OMOP database set up in your secure network area (see [OMOP Requirements](../omop/index.md))
- [X] Docker, Podman, or Kubernetes available in your secure network area
- [X] Outbound HTTPS (port 443) connectivity to the Cohort Discovery Service

---

## External resources

| Resource | Link |
|----------|------|
| Bunny Quickstart | [hutch.health/bunny/quickstart](https://hutch.health/bunny/quickstart) |
| Bunny Configuration | [hutch.health/bunny/config](https://hutch.health/bunny/config) |
| Bunny Deployment Requirements | [hutch.health/bunny/deployment/requirements](https://hutch.health/bunny/deployment/requirements) |
| Bunny User Guide | [health-informatics-uon.github.io/hutch/bunny](https://health-informatics-uon.github.io/hutch/bunny) |
| Bunny GitHub | [github.com/Health-Informatics-UoN/hutch-bunny](https://github.com/Health-Informatics-UoN/hutch-bunny) |
| Report issues | [github.com/Health-Informatics-UoN/hutch-bunny/issues](https://github.com/Health-Informatics-UoN/hutch-bunny/issues) |

!!! hdruk "HDR UK support"
    HDR UK can provide guidance to Data Custodians wishing to use Bunny. Contact [gateway@hdruk.ac.uk](mailto:gateway@hdruk.ac.uk).

## Connecting BC|INSIGHT

BC|INSIGHT uses the same credentials and connection model as Bunny. Refer to the full credential setup for Bunny, as the Client ID, Client Secret, Collection ID, and Task API Base URL are the same regardless of which query tool you use.

BC|INSIGHT requires **two instances** per dataset, equivalent to Bunny's Type A (availability queries) and Type B (distribution jobs). Configure your A and B instances using the same credentials — only the instance type differs.

For installation instructions, contract options, and BC|INSIGHT-specific questions, contact BC Platforms directly.

[bcplatforms.com](https://www.bcplatforms.com){ .md-button }
