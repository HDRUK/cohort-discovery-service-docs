---
title: Carrying Changes Across Upgrades
description: Keeping your branding, claim mappings and provider config when the upstream repos move on
tags:
  - configuration
  - deployment
---

# Carrying changes across upgrades

Three files make a deployment its own — [`branding/`](branding.md) in the web repo, [`config/claimsaccesscontrol.php`](claim-mapping.md) in the API, and `config/sso.php` if you run more than one identity provider. All three live inside the upstream repos, so every deployment needs a way to keep its own versions across upgrades. Fork-and-rebase, a build-time overlay and a mounted config all work.

What is already fixed, whichever route you take:

| | `branding/` | `claimsaccesscontrol.php` | `sso.php` |
|---|---|---|---|
| Consumed at | Next.js **build** time | PHP **runtime**, subject to config cache | PHP **runtime**, subject to config cache |
| Can be mounted into a running container | No — it is compiled into the bundle | Yes | Yes |
| Needs | A rebuild of the web image | A redeploy, or `config:clear` | A redeploy, or `config:clear` |
| Only needed if | You are rebranding | Your IdP's names differ from the shipped ones | You have more than one IdP |

That asymmetry is the main constraint: any approach that works by mounting files at runtime covers the API but cannot cover web branding.

## One worked answer: the stack

The [Cohort Discovery Service stack](https://hdruk.github.io/cohort-discovery-service-stack/) combines the last two. It never edits the upstream repos:

- The services are git submodules pinned to release tags, so an upgrade is a new pin.
- Everything a deployer changes lives in one `customisations/` folder, one subfolder per service.
- `claimsaccesscontrol.php` and the API's other config files are mounted over the shipped ones at runtime.
- `branding/` is overlaid onto the web source when the image is built.

See [How to customise](https://hdruk.github.io/cohort-discovery-service-stack/customising/) in the stack's docs.
