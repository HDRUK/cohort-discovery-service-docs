---
title: Migrating from the Old OIDC Integration
description: Upgrading from the removed DP-934 bearer-token resource-server integration to relying-party SSO
tags:
  - configuration
  - authentication
  - sso
  - migration
---

# Migrating from the old OIDC resource-server integration

Only relevant if you deployed the earlier DP-934 OIDC feature. On a fresh deployment, skip this page entirely.

## What changed

An earlier version of the API made it a bearer-token **resource server**: it validated OIDC access tokens issued externally, on every incoming request. Standalone SSO replaces that entirely — the API is now a **relying party** that drives its own login flow and issues its own JWT.

The two are incompatible. There is no way to keep the old `OIDC_*` configuration working alongside the new one.

| Old (removed) | New equivalent |
|---|---|
| `OIDC_ENABLED` | `SSO_ENABLED` — now also requires `APP_OPERATION_MODE=standalone` |
| `OIDC_ISSUER_URL` | `SSO_DEFAULT_ISSUER` / `SSO_DEFAULT_DISCOVERY_URL` |
| `OIDC_WORKGROUPS_CLAIM` | `SSO_DEFAULT_WORKGROUPS_CLAIM` says *which* claim; *whether* it is trusted is now `CLAIM_SYNC_WORKGROUPS` / `CLAIM_SYNC_WORKGROUPS_AUTHORITATIVE` |
| `OIDC_AUDIENCE`, `OIDC_USERINFO_ENDPOINT`, `OIDC_*_TIMEOUT_SECONDS`, `OIDC_CLOCK_SKEW_SECONDS` | No equivalent — not applicable to a client-driven flow |

## Two things that will change behaviour silently

!!! danger "Claim sync now defaults on, and roles are authoritative"
    Claim-driven sync used to be **off by default**. It no longer is. The shipped defaults are:

    - `CLAIM_SYNC_WORKGROUPS=first_login`, non-authoritative — additive only
    - `CLAIM_SYNC_ROLES=always` **and authoritative**

    On upgrade, existing users have their workgroups adjusted on next login and their **roles overwritten to match the IdP on every login**. That can silently change who holds admin or custodian access.

    Set these deliberately before deploying:

    ```dotenv
    CLAIM_SYNC_ROLES=never
    # or
    CLAIM_SYNC_ROLES_AUTHORITATIVE=false
    ```

!!! warning "Set the migration slug before you migrate"
    The old `users.oidc_sub` column is dropped. A migration copies existing values into the new `user_identities` table under the slug named by `SSO_MIGRATION_PROVIDER_SLUG` (default `default`).

    That slug must match the one you configure for the same IdP in `config/sso.php`. If they differ, migrated identities land under a slug with no matching provider and are orphaned — those users will not be recognised as already linked next time they sign in.

## Upgrade steps

1. Back up the database.
2. Set the `CLAIM_SYNC_*` variables deliberately — do not accept the new defaults blind.
3. Deploy the new code.
4. Confirm `SSO_MIGRATION_PROVIDER_SLUG` matches the provider slug you intend to configure.
5. Run `php artisan migrate`.
6. Configure that provider in `config/sso.php` and the matching `SSO_*` environment variables.
7. Verify in the admin Users view that previously-linked users still show a linked identity and the expected roles and workgroups.

There is no equivalent migration on the web side — no OIDC implementation from that era was ever merged there.
