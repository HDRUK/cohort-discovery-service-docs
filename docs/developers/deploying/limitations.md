---
title: Known Limitations
description: What is not finished yet, and where contributions are most welcome
tags:
  - deployment
  - contributing
---

# Known limitations

This is an open-source project and standalone deployment is newer than the rest of the platform. These are the rough edges we know about, gathered in one place so they are not a surprise halfway through a deployment.

None of them are architectural. All are places where a pull request would be welcome — see [Contributing](../contributing.md).

## Identity providers

**Only Keycloak is tested end to end.** Any provider meeting [what we support](identity-provider.md#what-we-support) should work, and a walkthrough for another one is the single most useful contribution to this section.

**Entra ID and Google cannot be used yet.** Both publish OIDC endpoints across more than one hostname, which the API currently rejects. Tracked in [#350](https://github.com/HDRUK/cohort-discovery-service-api/issues/350).

**More than one provider at a time is untested.** The configuration exists, but claim sync was built around a single IdP and three of its behaviours change meaning — see [Running more than one provider](reference/multiple-providers.md).

## Access control

**Assignment is configuration-driven.** Roles, workgroups and custodian membership come from your claim mapping and sync policy. The admin Users view shows what a user holds but cannot change it, so adjusting access means a configuration change and a deploy.

**A mistyped trust value fails quietly.** The `CLAIM_SYNC_*` trust variables accept `never`, `first_login` or `always`. Anything else is treated as `never`, with nothing written to the log.

## Branding

**`organisationName` does not render in standalone mode.** Its only consumer is the footer's organisation link, which standalone suppresses.

**The `hdruk-uk-theme` flag cannot be turned off.** The API does not seed it, so the web app always sees its default of `true`. Use `hdrukChromeInStandalone: false` in your branding config instead, which has the same effect for a third-party deployment.

## Deployment

**No published images and no general-purpose Helm chart.** Each repo has a `Dockerfile` you can build from; the `chart/` directories are scaffolding for HDR UK's own pipeline. [Running the services](running.md) covers what a deployment needs.
