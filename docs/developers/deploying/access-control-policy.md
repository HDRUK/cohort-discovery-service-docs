---
title: Access Control Policy
description: When claims from your IdP are read, and how much authority they carry
tags:
  - configuration
  - authentication
  - claims
---

# Access control policy

Your identity provider is connected and its values are mapped. This page is how far those values are trusted — the last of three steps: [connect a provider](identity-provider.md) → [map its values](claim-mapping.md) → **decide how far to trust them**.

`config/claimsaccesscontrol.php` holds both halves. The [mapping tables](claim-mapping.md) say *what a claim value means*; the `sync` block below it says *when it is read and how much authority it carries*. The sync block takes its values from environment variables, so that half can be changed per deployment without editing the file:

```php
'sync' => [
    'workgroups' => [
        'trust' => env('CLAIM_SYNC_WORKGROUPS', 'first_login'),
        'authoritative' => (bool) env('CLAIM_SYNC_WORKGROUPS_AUTHORITATIVE', false),
        'ensure_default' => (bool) env('CLAIM_SYNC_ENSURE_DEFAULT_WORKGROUP', true),
        'sde_from_claim' => (bool) env('CLAIM_SYNC_SDE_WORKGROUPS_FROM_CLAIM', true),
    ],

    'roles' => [
        'trust' => env('CLAIM_SYNC_ROLES', 'always'),
        'authoritative' => (bool) env('CLAIM_SYNC_ROLES_AUTHORITATIVE', true),
        'ensure_default' => (bool) env('CLAIM_SYNC_ENSURE_DEFAULT_ROLE', true),
    ],

    'custodians' => [
        'trust' => env('CLAIM_SYNC_CUSTODIANS', 'always'),
        'authoritative' => (bool) env('CLAIM_SYNC_CUSTODIANS_AUTHORITATIVE', true),
    ],

    'provision' => [
        'defaults_on_create' => (bool) env('CLAIM_PROVISION_DEFAULTS_ON_CREATE', true),
    ],
],
```

Setting `CLAIM_SYNC_ROLES=never` in `.env` is therefore the same thing as changing `'trust' => 'never'` in the file. Use the variables.

---

## The sync policy

Three subjects, each with the same two levers: *trust* decides when the claim is read, *authoritative* decides whether it may take access away as well as grant it.

| Variable | Default | Description |
|---|---|---|
| `CLAIM_SYNC_WORKGROUPS` | `first_login` | `never`, `first_login`, or `always` |
| `CLAIM_SYNC_WORKGROUPS_AUTHORITATIVE` | `false` | True: claims replace local membership. False: they only add |
| `CLAIM_SYNC_ENSURE_DEFAULT_WORKGROUP` | `true` | Keep the default workgroup even under an authoritative sync |
| `CLAIM_SYNC_SDE_WORKGROUPS_FROM_CLAIM` | `true` | Derive SDE workgroups from the claim. **Integrated only** — setting it standalone does nothing |
| `CLAIM_SYNC_ROLES` | `always` | `never`, `first_login`, or `always` |
| `CLAIM_SYNC_ROLES_AUTHORITATIVE` | `true` | True: claims replace local roles |
| `CLAIM_SYNC_ENSURE_DEFAULT_ROLE` | `true` | Floors an authoritative role sync at `user` |
| `CLAIM_SYNC_CUSTODIANS` | `always` | `never`, `first_login`, or `always` |
| `CLAIM_SYNC_CUSTODIANS_AUTHORITATIVE` | `true` | True: claims replace local custodian membership |
| `CLAIM_PROVISION_DEFAULTS_ON_CREATE` | `true` | Give new users sane defaults at creation, independent of sync |

!!! warning "An unrecognised `trust` value means `never`, silently"
    The three `CLAIM_SYNC_*` trust variables accept exactly `never`, `first_login` or `always`. Anything else — a typo, a `true`, or the wrong case as in `Always` — is treated as `never`, with no error raised and nothing written to the log.

    If an entire subject is being ignored, check these values character by character before looking anywhere else.

### Absent is not empty

| Token contains | Authoritative sync does |
|---|---|
| no `groups` key at all | nothing — "this IdP has no opinion" |
| `"groups": []` | clears every workgroup |
| `"groups": [{...}]` | clears every workgroup — objects filter to empty |

A dropped claim fails safe; a claim sent empty does not.

### Floors

`ENSURE_DEFAULT_WORKGROUP` and `ENSURE_DEFAULT_ROLE` are merged in before the sync runs, so a user can never end up with no workgroup or no role. A sync will also not remove the last remaining `admin` in the system.

### Audit trail

Every claim-driven membership change is written to the activity log — what was attached, what was detached, and which sync path did it.

---

## Three worked configurations

The two settings per subject combine into three shapes that cover most deployments. Pick the closest and adjust.

All three assume a single identity provider. If you run more than one, read [Running more than one provider](reference/multiple-providers.md) first — `first_login` and `authoritative` both change meaning, and the Mixed control shape below is the one most affected.

| | Full IdP control | Mixed control | Authentication only |
|---|---|---|---|
| **Workgroups** | IdP | IdP on first login, then local | Local |
| **Roles** | IdP | IdP | Local |
| **Custodians** | IdP | Local | Local |
| **Do local edits survive a login?** | No | Workgroups and custodians yes, roles no | Yes, always |
| **What the IdP is for** | Identity *and* authorisation | Identity, plus role authority | Identity only |

=== "Full IdP control"

    The IdP is the complete source of truth for all three subjects, on every login. Use this when its groups and roles are already your organisation's genuine system of record.

    ```dotenv
    SSO_DEFAULT_WORKGROUPS_CLAIM=groups
    SSO_DEFAULT_ROLES_CLAIM=roles
    SSO_DEFAULT_CUSTODIANS_CLAIM=groups

    CLAIM_SYNC_WORKGROUPS=always
    CLAIM_SYNC_WORKGROUPS_AUTHORITATIVE=true
    CLAIM_SYNC_ENSURE_DEFAULT_WORKGROUP=true

    CLAIM_SYNC_ROLES=always
    CLAIM_SYNC_ROLES_AUTHORITATIVE=true
    CLAIM_SYNC_ENSURE_DEFAULT_ROLE=true

    CLAIM_SYNC_CUSTODIANS=always
    CLAIM_SYNC_CUSTODIANS_AUTHORITATIVE=true

    CLAIM_PROVISION_DEFAULTS_ON_CREATE=true
    ```

    **Consequence:** nothing an admin changes locally survives that user's next login. Access is granted and revoked at the IdP, nowhere else.

=== "Mixed control"

    Roles track the IdP because they gate the admin surface. Workgroups are seeded once then left to local administration. Custodians are never claim-driven, because custodian membership is usually a contractual data-access decision rather than something an IdP group should decide.

    ```dotenv
    SSO_DEFAULT_WORKGROUPS_CLAIM=groups
    SSO_DEFAULT_ROLES_CLAIM=roles
    # SSO_DEFAULT_CUSTODIANS_CLAIM deliberately unset

    CLAIM_SYNC_WORKGROUPS=first_login
    CLAIM_SYNC_WORKGROUPS_AUTHORITATIVE=false
    CLAIM_SYNC_ENSURE_DEFAULT_WORKGROUP=true

    CLAIM_SYNC_ROLES=always
    CLAIM_SYNC_ROLES_AUTHORITATIVE=true
    CLAIM_SYNC_ENSURE_DEFAULT_ROLE=true

    CLAIM_SYNC_CUSTODIANS=never

    CLAIM_PROVISION_DEFAULTS_ON_CREATE=true
    ```

    **Consequence:** workgroup edits stick after first login. Role edits do not — they are corrected back to the claim on every login. Custodian membership is entirely local.

    This is the most common shape for a deployment whose IdP is authoritative for staff roles but which manages data-access relationships itself.

=== "Authentication only"

    The IdP proves who someone is and nothing more.

    ```dotenv
    # Claim names are irrelevant here - trust=never short-circuits
    # before any claim is read.

    CLAIM_SYNC_WORKGROUPS=never
    CLAIM_SYNC_ROLES=never
    CLAIM_SYNC_CUSTODIANS=never

    CLAIM_PROVISION_DEFAULTS_ON_CREATE=true
    ```

    **Consequence:** every assignment is made locally and persists. New users are created on first SSO login with the `DEFAULT` workgroup and the `user` role — or nothing at all, if `CLAIM_PROVISION_DEFAULTS_ON_CREATE=false` — and an admin takes it from there.

    !!! note "`never` is what disables sync, not an unset claim name"
        `SSO_DEFAULT_WORKGROUPS_CLAIM` falls back to `eduperson_entitlement` when unset rather than disabling workgroup sync, so leaving it blank is **not** how you turn workgroups off. Only `CLAIM_SYNC_WORKGROUPS=never` does that. Roles and custodians do behave the other way — unset claim names skip those subjects entirely.

---

## Upgrading

!!! warning "Custodian sync can now remove access"
    `CLAIM_SYNC_CUSTODIANS_AUTHORITATIVE` is new and defaults to `true`. If you are upgrading a deployment that relied on custodian sync only ever *adding* membership, set it explicitly before you deploy:

    ```dotenv
    CLAIM_SYNC_CUSTODIANS_AUTHORITATIVE=false
    ```

These settings supersede the per-provider `claim_mapping.enabled` / `authority` / `role_map` keys from earlier builds, and replace the `sso-ensure-defaults-on-jit` feature flag. `CLAIM_PROVISION_DEFAULTS_ON_CREATE` is the direct replacement.

There is no web UI for any of this. The admin Users view is read-only; changes are made via environment variables and require a deploy.
