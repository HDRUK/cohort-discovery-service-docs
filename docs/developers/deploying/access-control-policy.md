---
title: Access Control Policy
description: When claims from your IdP are read, and how much authority they carry
tags:
  - configuration
  - authentication
  - claims
---

# Access control policy

Your identity provider is connected and its values are mapped. This page is how far those values are trusted — the last of the three steps: [connect a provider](identity-provider.md) → [map its values](claim-mapping.md) → **decide how far to trust them**.

```
Your IdP's claims ─→ ClaimSyncPolicy ─→ ClaimResolver ─→ workgroups / roles / custodians
                          (when)           (what)
```

`config/claimsaccesscontrol.php` is the single source of truth, in two halves:

| Half | Answers | Driven by |
|---|---|---|
| Mapping tables | *What does this claim value mean?* | Editing the PHP file — see [Mapping claims to the platform](claim-mapping.md) |
| Sync policy | *When is it read, and how much authority does it carry?* | Environment variables |

This page covers the second half.

!!! note "The same machinery serves integrated mode"
    Nothing here is standalone-specific. HDR UK's own [integrated deployment](../hdruk/integrated.md) feeds the same policy from Gateway JWT claims instead of an OIDC provider's.

!!! note "Don't confuse this with `ClaimBasedAccessControl`"
    A separate, unrelated vendor middleware — `App\Http\Middleware\ClaimBasedAccessControl` from the `hdruk/claims-based-access-control` package, configured via `config/claims-access.php` — does request-time JWT claim gating on API endpoints. It has nothing to do with provisioning. The near-identical names (`claims-access` vendor config vs `claimsaccesscontrol` app config, no hyphen) are easy to mix up.

---

## The sync policy

Three subjects, each with the same two levers.

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

    This is the opposite of how `APP_OPERATION_MODE` behaves, which refuses to boot rather than guess. If an entire subject is being ignored, check these values character by character before looking anywhere else.

### Two behaviours worth internalising

**Absent is not empty.**

| Token contains | Authoritative sync does |
|---|---|
| no `groups` key at all | nothing — "this IdP has no opinion" |
| `"groups": []` | clears every workgroup |
| `"groups": [{...}]` | clears every workgroup — objects filter to empty |

A schema change or partial IdP outage that drops a claim fails safe. A claim deliberately sent empty does not. A mapper emitting the wrong *shape* takes the destructive branch, not the safe one.

**Floors cannot be overridden by a claim.** `ENSURE_DEFAULT_WORKGROUP` and `ENSURE_DEFAULT_ROLE` are merged in before the sync runs, so a user can never end up with no workgroup or no role. Separately, `App\Services\Claims\RoleSyncFloor` will not let a sync remove the **last remaining `admin`** in the system — it retains the role and logs a warning.

### Audit trail

Every claim-driven membership change, from either mode, is written to the activity log via `ActivityLogger::membershipChanged()` — what was attached, what was detached, and which sync path did it.

---

## Three worked configurations

The two settings per subject combine into three shapes that cover almost every real deployment. Pick the closest and adjust. Mixing pieces of different ones is usually how a deployment ends up in the lockout or over-grant cases these rules exist to prevent.

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

## Upgrade warning

!!! warning "Custodian deprovisioning is new"
    `custodians` previously had no `authoritative` key, so standalone custodian sync could only ever *add* membership — a user removed from their IdP group kept access forever.

    `CLAIM_SYNC_CUSTODIANS_AUTHORITATIVE` now exists and **defaults to `true`**, which fixes that. Integrated mode is unaffected; it was always authoritative.

    If you are upgrading a standalone deployment that relied on the old additive-only behaviour, set it explicitly before deploying:

    ```dotenv
    CLAIM_SYNC_CUSTODIANS_AUTHORITATIVE=false
    ```

    Otherwise a user's custodian access can be silently removed on their next login if the claim does not mention them.

This configuration supersedes the per-provider `claim_mapping.enabled` / `authority` / `role_map` keys from earlier builds, and replaces the `sso-ensure-defaults-on-jit` feature flag and its three siblings. `provision.defaults_on_create` is the direct replacement.

---

## Known gaps

Confirmed, open gaps — surfaced here so an operator knows about them before relying on the defaults, not after.

!!! bug "No way to assign a custodian or grant a role over HTTP"
    In standalone mode, with no claim configured for a subject, there is **no path at all** to grant it — not via claims, not via HTTP, not via artisan beyond the bootstrap `custodian:create` command, which creates custodian *records*, not memberships. A deployment with no `roles_claim` cannot create a new admin after the initial seed if the seeded admin account is lost. Tracked in [#342](https://github.com/HDRUK/cohort-discovery-service-api/issues/342) and [#343](https://github.com/HDRUK/cohort-discovery-service-api/issues/343).

!!! bug "Local edits silently evaporate under an authoritative sync"
    When a subject syncs authoritatively on every login — the shipped default for roles and now custodians — anything set locally is wiped on the user's next login, with no error and no warning at the point the admin makes the edit. Tracked in [#344](https://github.com/HDRUK/cohort-discovery-service-api/issues/344).

!!! bug "Custodian membership can be granted by name collision"
    `custodianIdsForClaimValues()` matches claim values straight against `LOWER(custodians.name)` with no mapping table in between. On an IdP where users can create their own groups — Entra ID self-service groups, for instance — a user could create a group matching a custodian's name and be auto-attached on next login. Only set `SSO_DEFAULT_CUSTODIANS_CLAIM` if your IdP's group names can be trusted to match your custodian records. Tracked in [#345](https://github.com/HDRUK/cohort-discovery-service-api/issues/345).

!!! bug "The frontend cannot see which subjects the IdP owns"
    No endpoint exposes the current `trust`/`authoritative` configuration per subject, so the admin Users view cannot warn an operator before they hit the gap above. Tracked in [#347](https://github.com/HDRUK/cohort-discovery-service-api/issues/347).

!!! bug "`/auth/login`, `/auth/methods` and `/auth/sso/providers` carry no rate limiting"
    Every other SSO route has a throttle; these three do not, despite `/auth/login` being the one unauthenticated credential-checking endpoint in the API. Tracked in [#346](https://github.com/HDRUK/cohort-discovery-service-api/issues/346), which names the first two.

!!! note "`LOWER(name)` matching is case-insensitive by design"
    All three claim resolvers match against `LOWER(name)` rather than the raw column. This is redundant on the default `utf8mb4_*_ci` collation, but becomes load-bearing on a deployment that overrides to a case-sensitive or binary collation. Documented here rather than in a code comment so that if it is ever removed as a tidy-up, the decision gets made with the collation in mind.

There is no web UI to edit any of this. The admin Users view is read-only; changes are made via environment variables or the config file and require a deploy.
