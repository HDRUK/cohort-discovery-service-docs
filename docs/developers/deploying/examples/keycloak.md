---
title: Keycloak Worked Example
description: Step-by-step Keycloak setup for standalone OIDC SSO — groups, realm roles, client, and protocol mappers
tags:
  - configuration
  - authentication
  - keycloak
  - sso
---

# Worked example: configuring Keycloak as the identity provider

This walks through a complete Keycloak setup for standalone SSO — groups, realm roles, the client, and the protocol mappers needed to get workgroups, roles, and custodian membership into the ID token. It uses the Keycloak Admin Console (tested against Keycloak 24–26; menu wording drifts slightly between versions).

See [Connecting an identity provider](../identity-provider.md) for the architecture, [SSO environment variables](../reference/sso-environment-variables.md) for the full variable reference, [Mapping claims to the platform](../claim-mapping.md) for what a claim value is matched against, and [Access control policy](../access-control-policy.md) for whether those claims are trusted once they arrive.

---

## Step 0: Run a disposable Keycloak

```bash
docker run -p 8080:8080 \
  -e KC_BOOTSTRAP_ADMIN_USERNAME=admin -e KC_BOOTSTRAP_ADMIN_PASSWORD=admin \
  quay.io/keycloak/keycloak start-dev
```

Log in to the Admin Console at `http://localhost:8080` with `admin`/`admin`.

That command assumes the API runs on your host, so `localhost:8080` means the same thing to your browser and to the API process. If the API runs in a container, it does not — read this before going further.

!!! danger "Containerised API: pick a hostname that works from both sides"
    The API compares the issuer byte-for-byte against the `iss` claim *and* fetches discovery, JWKS and the token endpoint from it server-side. So the issuer URL has to resolve from the browser and from inside the API container, as the same string.

    `http://localhost:8080/realms/...` fails under Docker, Tilt or Kubernetes: the API container's `localhost` is itself. Switching the issuer to `http://keycloak:8080/realms/...` just moves the breakage to the browser, which cannot resolve `keycloak`.

    Give Keycloak one hostname and make that name resolve to it from both sides:

    ```bash
    docker run -p 8080:8080 \
      -e KC_BOOTSTRAP_ADMIN_USERNAME=admin -e KC_BOOTSTRAP_ADMIN_PASSWORD=admin \
      -e KC_HOSTNAME=http://keycloak.test:8080 \
      quay.io/keycloak/keycloak start-dev
    ```

    `KC_HOSTNAME` is what Keycloak advertises in its discovery document and in the `iss` claim. On Keycloak 25 and 26 it takes a full URL as shown; on 24 it takes a bare hostname and the URL is assembled from `KC_HOSTNAME_PORT` and friends, so check which you are running.

    Then make `keycloak.test` resolve to Keycloak from both places — a `/etc/hosts` entry pointing at `127.0.0.1` on your machine, and an `extra_hosts` entry (Compose), `hostAliases` (Kubernetes) or a cluster DNS record pointing at the container on the API side. Set `SSO_DEFAULT_ISSUER=http://keycloak.test:8080/realms/cohort-discovery-service`.

    Resist the temptation to use a wildcard DNS service such as `*.localtest.me` here. It resolves to `127.0.0.1` everywhere, including *inside* the API container, where that is the container itself rather than Keycloak — so discovery fails with a connection error instead of an obvious name-resolution one.

    Setting `SSO_DEFAULT_DISCOVERY_URL` to an internal address does **not** avoid any of this: the token and JWKS URLs are read out of the discovery document and will still be the advertised public ones.

## Step 1: Create a realm

Top-left realm selector → **Create realm**. Name it `cohort-discovery-service`. Everything below happens inside this realm, not `master`.

!!! tip "Two ways round: rename in Keycloak, or edit the mapping file"
    Steps 2 and 3 name Keycloak objects to match the **shipped** `workgroup_mappings` / `role_mappings` values, which keeps this walkthrough short. That is not the only option, and usually not the right one for an existing realm.

    If Keycloak already has groups and roles with their own naming, leave them alone and **edit `config/claimsaccesscontrol.php` in the API instead** — change the right-hand side of each mapping to whatever your realm emits. See [Mapping claims to the platform](../claim-mapping.md). Everything downstream of this page works identically either way.

## Step 2: Create groups

Left nav → **Groups** → **Create group**.

Create one group per workgroup you intend to grant, named to match the **values** in `workgroup_mappings` (the external claim-value side of each `=>`). Out of the box those values are `admin`, `custodian`, `default`, `non-uk-industry`, `non-uk-research`, `other`, `uk-industry`, `uk-research`, `nhs-sde`:

- **Create group** → name `admin` → **Create**
- Repeat for `default` and any others you need

Equally, name the group whatever your organisation already uses and put that string on the right-hand side of the mapping instead — `'admin' => 'Cohort-Discovery-Admins'`.

If you also want custodian membership driven by Keycloak, create one group per custodian, named to match that custodian's `name` in the database exactly (case-insensitively). Custodians have **no** mapping table, so this one really is match-by-name with no indirection available:

- **Create group** → name `North Region TRE` → **Create**

!!! warning "Keep groups top-level, and leave Full group path off"
    A nested group exported with **Full group path** on produces `/parent/North Region TRE` rather than `North Region TRE`. That value matches neither a `workgroup_mappings` entry nor a custodian's bare `name`, so the membership silently fails to resolve. Keep these groups flat and the toggle off (Step 4).

## Step 3: Create realm roles

Left nav → **Realm roles** → **Create role**. Name these to match the values in `role_mappings` — out of the box `GENERAL_ACCESS`, `SYSTEM_ADMIN`, `CUSTODIAN` (which map to the local roles `user`, `admin`, `custodian` respectively):

- **Create role** → Role name `GENERAL_ACCESS` → **Save**
- Repeat for `SYSTEM_ADMIN` and `CUSTODIAN`

As with groups, the alternative is to keep your existing realm role names and point the mapping at them — `'admin' => 'Platform-Administrators'`. The left-hand side must stay as the local role name (`user`, `admin`, `custodian`), since that has to match a role that already exists in the database.

Roles are kept as realm roles rather than being folded into the group structure so that each Keycloak object maps to exactly one app-side concern — groups drive `workgroup_mappings` (and optionally custodians), realm roles drive `role_mappings`.

## Step 4: Create the client

Left nav → **Clients** → **Create client**.

**General settings:**

| Field | Value |
|---|---|
| Client type | `OpenID Connect` |
| Client ID | `cohort-discovery-service-api` (becomes `SSO_DEFAULT_CLIENT_ID`) |

**Capability config:**

| Field | Value |
|---|---|
| Client authentication | **On** — the API is a confidential client and sends a client secret at the token endpoint |
| Standard flow | **On** — authorization code flow with PKCE is the only flow the API uses |
| Direct access grants | Off |
| Service accounts roles | Off |

**Login settings:**

| Field | Value |
|---|---|
| Valid redirect URIs | `http://localhost:8100/api/auth/sso/default/callback` — must match exactly, including the provider slug |
| Valid post logout redirect URIs | `http://localhost:3000/login` — **set this explicitly**, see below |
| Web origins | Leave blank — the browser is only ever redirected, it makes no CORS calls to Keycloak |

!!! warning "Logout fails if you leave the post-logout field at its default"
    Keycloak's default for **Valid post logout redirect URIs** is `+`, meaning "reuse the Valid redirect URIs list". That list holds the API's callback URL, but the URL actually sent at logout is the *frontend* login page — `SSO_FRONTEND_LOGIN_URL`, or the callback URL's origin plus `/login` when that is unset.

    Those are different hosts and ports in a normal deployment, so with `+` left in place Keycloak rejects the logout with *Invalid parameter: redirect_uri*. Sign-in works perfectly and only sign-out breaks, which makes this an easy one to ship.

Save, then **Credentials** tab → copy the **Client secret** into `SSO_DEFAULT_CLIENT_SECRET` in your `.env`. Treat it like any other credential: never commit it, never paste it into a ticket or chat.

## Step 5: Add the protocol mappers

**Clients** → your client → **Client scopes** tab → the `cohort-discovery-service-api-dedicated` row → **Mappers** → **Add mapper** → **By configuration**.

**Mapper 1 — Group Membership:**

| Field | Value |
|---|---|
| Mapper type | `Group Membership` |
| Name | `groups` |
| Token Claim Name | `groups` — flat, no dots |
| Full group path | **Off** |
| Add to ID token | **On** |
| Add to access token | On (optional) |
| Add to userinfo | On (optional) |

**Mapper 2 — User Realm Role:**

| Field | Value |
|---|---|
| Mapper type | `User Realm Role` |
| Name | `roles` |
| Token Claim Name | `roles` — **change this from the default `realm_access.roles`** (see below) |
| Multivalued | **On** — without this only one role is emitted |
| Add to ID token | **On** |

!!! warning "Don't keep Keycloak's default `realm_access.roles`"
    Keycloak treats a `.` in a Token Claim Name as nesting, so that default emits `{"realm_access": {"roles": [...]}}`. The API reads flat, top-level claim names only, so it sees nothing there and treats roles as absent. Use `roles` — no dots.

"Add to ID token" is the toggle that matters on both mappers: the API reads claims from the validated ID token, and only falls back to the userinfo endpoint when `email` or `name` is missing.

With both saved, a user in the `admin` and `North Region TRE` groups holding the `SYSTEM_ADMIN` realm role gets an ID token containing:

```json
{
  "groups": ["admin", "North Region TRE"],
  "roles": ["SYSTEM_ADMIN"],
  "email": "jane.doe@example.org",
  "email_verified": true
}
```

Pointing `SSO_DEFAULT_WORKGROUPS_CLAIM` and `SSO_DEFAULT_CUSTODIANS_CLAIM` both at `groups` resolves `admin` as a workgroup (it's in `workgroup_mappings`) and `North Region TRE` as a custodian (it matches a custodian's name), out of that one array.

!!! warning "One group list feeding two subjects needs disjoint naming"
    Because custodians match on name with no allow-list, a group named `admin` would also attach the user to a custodian literally called "admin", if one existed. Keeping the two vocabularies obviously distinct — short lowercase slugs for workgroups, full proper names for custodians — is what prevents overlap. If you would rather separate them properly, add a second `Group Membership` mapper with Token Claim Name `teams` and set `SSO_DEFAULT_CUSTODIANS_CLAIM=teams`.

    Note that this does **not** filter anything: Keycloak's `Group Membership` mapper always emits *every* group the user belongs to, so two mappers give you the same full list under two different claim names, not a split. Scoping a mapper to one subtree needs a custom Keycloak SPI. What a group means is decided entirely by the mapping tables and custodian names on the API side.

## Step 6: Create a test user

Left nav → **Users** → **Add user**.

- Username / email: `jane.doe@example.org` (use an address you control for real testing)
- **Email verified**: **On** — not optional. The API only links or creates an account when the IdP asserts the email is verified; an unverified email is treated as a possible account takeover and sent to the error page.
- Save → **Credentials** → **Set password**, with "Temporary" unticked.

Then assign membership:

- **Groups** tab → **Join Group** → `admin`, and/or a custodian group such as `North Region TRE`
- **Role mapping** tab → **Assign role** → `SYSTEM_ADMIN`

## Step 7: Point the API at the realm

```dotenv
SSO_ENABLED=true
SSO_FRONTEND_CALLBACK_URL=http://localhost:3000/auth/sso/callback
SSO_FRONTEND_ERROR_URL=http://localhost:3000/auth/sso/error

SSO_DEFAULT_ENABLED=true
SSO_DEFAULT_LABEL="Single Sign-On"
SSO_DEFAULT_ISSUER=http://localhost:8080/realms/cohort-discovery-service
SSO_DEFAULT_CLIENT_ID=cohort-discovery-service-api
SSO_DEFAULT_CLIENT_SECRET=<the secret from Step 4>
SSO_DEFAULT_SCOPES="openid profile email"

SSO_DEFAULT_WORKGROUPS_CLAIM=groups
SSO_DEFAULT_ROLES_CLAIM=roles
SSO_DEFAULT_CUSTODIANS_CLAIM=groups
```

These say *which* claim carries what. *Whether* each is trusted, and whether it may remove membership, is the separate `CLAIM_SYNC_*` policy — see the three worked configurations in [Access control policy](../access-control-policy.md#three-worked-configurations). Setting the claim names above without setting a sync policy does nothing on its own.

Restart the API — and run `php artisan config:clear` if config is cached, or these variables will not be picked up. Then visit `http://localhost:8100/api/auth/sso/default/redirect` (or use the SSO button on the login page) and sign in as the test user. Check the resulting roles and workgroups on that user in the admin Users view.

## Troubleshooting

Claim and mapping problems — the login succeeds, but the user ends up with the wrong access:

| Symptom | Likely cause |
|---|---|
| Roles never apply, workgroups do | Token Claim Name left as `realm_access.roles` — the nested path can't be read. Use a flat name. |
| Only one role ever applies | **Multivalued** off on the realm-role mapper |
| Groups resolve to nothing | **Full group path** on, emitting `/admin` instead of `admin`; or the group name doesn't match a `workgroup_mappings` value — fix it at either end, by renaming the group or by editing the mapping in `config/claimsaccesscontrol.php` |
| Edited `claimsaccesscontrol.php` but nothing changed | Config is cached — run `php artisan config:clear`, and redeploy if the file only changed locally |
| A custodian group grants nothing | No custodian record exists with that exact name — custodians are matched against existing records and never created from a claim |
| Membership gets wiped on login | The claim is present but holds non-string values (or an empty array), which reads as "none" and clears under an authoritative sync |
| Claims ignored entirely | Mapper not added to the **ID token**, or the matching `CLAIM_SYNC_*` trust is `never` — check the spelling and case of that variable, since an unrecognised value silently means `never` |

Login failures. The user lands on the error page and the URL carries `?error=<code>`; the detailed reason is in the API log, not on screen. Full list in [When a login fails](../reference/login-errors.md):

| `?error=` | Likely cause here |
|---|---|
| `provider_not_configured` | `SSO_DEFAULT_ISSUER` doesn't match the realm's own issuer, or the API can't reach it — see the hostname warning in Step 0. Also raised when `SSO_DEFAULT_ENABLED` is false or the secret is missing |
| `invalid_id_token` | Wrong client secret, or the realm signs with something other than RS256 without declaring `alg` on the key |
| `account_linking_failed` | **Email verified** left off on the test user, or the realm isn't releasing `email` at all |
| `invalid_state` | The login took longer than `SSO_TXN_TTL_SECONDS`, or the back button replayed a used callback |
| `provider_unreachable` | The API container can't reach the issuer host — the Step 0 problem, again |
| *Invalid parameter: redirect_uri*, shown by **Keycloak** on sign-out | **Valid post logout redirect URIs** left at `+` — see Step 4 |

## Adding a second IdP

Everything above configures the `default` provider slot. To add another, add an entry to the `providers` array in `config/sso.php` with its own slug — the realm, group, role and mapper steps repeat identically, with that slug replacing `default` in both the env var names and the callback URL.

Read [Running more than one provider](../reference/multiple-providers.md) first. Claim sync was built around a single IdP, and three of its behaviours change meaning once there are two.
