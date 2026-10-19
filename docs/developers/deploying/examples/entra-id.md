---
title: Microsoft Entra ID Example
description: Standalone OIDC SSO against Microsoft Entra ID — app registration, app roles, group claims, and the gotchas
tags:
  - configuration
  - authentication
  - entra
  - sso
---

# Worked example: Microsoft Entra ID

Entra ID (formerly Azure AD) as the identity provider for standalone SSO. Covers the app registration, getting roles and groups into the ID token, and three Entra-specific behaviours that will catch you out.

!!! danger "Entra ID does not currently work, and this is a platform limitation"
    The API requires every URL in a provider's discovery document to sit on the issuer's origin, across [five endpoints](../identity-provider.md#the-same-origin-rule). Entra serves `userinfo_endpoint` from `https://graph.microsoft.com/oidc/userinfo` — a different host from its `login.microsoftonline.com` issuer — so discovery is rejected.

    The failure is immediate and total. Discovery runs during `/redirect`, so the user clicks **Sign in with Microsoft** and is bounced straight to the error page with `?error=provider_not_configured` ("This sign-in option is not available right now"). They never reach Entra, and none of the three gotchas below is ever exercised.

    Every other Entra endpoint the login needs — authorisation, token, JWKS, end session — *is* on the issuer's origin, and `userinfo_endpoint` is only read as a fallback when the ID token lacks `email` or `name`. So the endpoint that blocks the integration is one a correctly configured app registration never needs. Tracked in [#350](https://github.com/HDRUK/cohort-discovery-service-api/issues/350).

    **Follow this page to prepare the Entra side, but expect the login itself to fail until #350 ships.** For a working deployment today, use [Keycloak](keycloak.md).

!!! note "Written from documented behaviour, not verified end to end"
    This walkthrough has **not** been run against a live tenant, and because of the blocker above it cannot be until #350 is fixed. The steps follow Entra's documented claim behaviour and the API's claim handling, but expect to adjust portal wording and to verify the emitted token yourself. If you do run it, please feed corrections back into this page.

See [Connecting an identity provider](../identity-provider.md) for the architecture, [SSO environment variables](../reference/sso-environment-variables.md) for the full variable reference, and [Mapping claims to the platform](../claim-mapping.md) for the mapping tables.

---

## Read this before you start

Three Entra behaviours matter more than any step below.

!!! danger "Entra does not emit `email_verified`"
    The API links an incoming identity to an **existing local account** only when the IdP asserts the email is verified:

    ```php
    emailVerified: ($claims['email_verified'] ?? false) === true,
    ```

    Entra does not emit `email_verified` for work or school accounts. Absent reads as `false`, and the comparison is strict, so a string `"true"` would not help either.

    **Consequence:** a *brand-new* user is created on first login without issue — JIT provisioning works. But if a local account with that email already exists (a seeded admin, a user who signed up with a password), the login fails with a linking error rather than attaching the identity. Plan for this: either create accounts only via SSO, or expect to need a fix before migrating existing accounts.

!!! warning "Group claims are object IDs, not names"
    For cloud-only groups Entra emits GUIDs in the `groups` claim, not display names:

    ```json
    { "groups": ["f1d4c8a2-9b3e-4c7a-8f12-6d5e4b3a2c10"] }
    ```

    Names are available only for groups synced from on-premises AD, via the `sAMAccountName` group claim option. For everything else the GUID is what arrives, so it is the GUID that goes on the right-hand side of `workgroup_mappings`.

    This also makes `SSO_DEFAULT_CUSTODIANS_CLAIM=groups` impractical, since custodians match on name with no mapping table — a GUID will never match a custodian's name.

!!! warning "Group overage silently drops the claim"
    If a user is a member of more than roughly 200 groups, Entra omits `groups` and emits `_claim_names` / `_claim_sources` pointing at the Graph API instead. The API reads flat claims only, so it sees `groups` as **absent**.

    Absent is treated as "the IdP has no opinion", so nothing is removed — it fails safe rather than wiping memberships. But that user gets no workgroups from the claim either. App roles do not have this limit, which is one more reason to prefer them.

---

## Step 1: Register the application

**Entra admin centre** → **App registrations** → **New registration**.

| Field | Value |
|---|---|
| Name | `Cohort Discovery Service` |
| Supported account types | Accounts in this organisational directory only (single tenant) |
| Redirect URI | **Web** — `https://api.example.org/api/auth/sso/entra/callback` |

The slug in that path (`entra` here) must match the key you add to `config/sso.php` in Step 5. Platform type must be **Web**, not SPA — the API is a confidential client and sends a secret at the token endpoint.

Note the **Application (client) ID** and **Directory (tenant) ID** from the Overview page.

## Step 2: Create a client secret

**Certificates & secrets** → **Client secrets** → **New client secret**.

Copy the **Value** immediately — Entra will not show it again. It goes in `SSO_ENTRA_CLIENT_SECRET`.

Set a calendar reminder for the expiry. A silently expired secret presents as every SSO login failing at the token exchange.

## Step 3: Define app roles

App roles are the cleanest route into `role_mappings`, because the emitted claim value is a string you choose.

**App roles** → **Create app role**:

| Field | Value |
|---|---|
| Display name | `Platform Admin` |
| Allowed member types | Users/Groups |
| Value | `Platform.Admin` |
| Description | Full administrative access to Cohort Discovery |

Repeat for `Platform.User` and `Platform.Custodian`. The **Value** is what lands in the `roles` claim.

Assign them under **Enterprise applications** → your app → **Users and groups** → **Add user/group**. Note this is the *enterprise application*, not the app registration — a common wrong turn.

## Step 4: Configure token claims

**Token configuration** on the app registration.

**Add the email optional claim:**

**Add optional claim** → token type **ID** → tick `email` → Add. If prompted to turn on the Microsoft Graph `email` permission, accept — without an email claim the API can neither link nor create an account.

**Add the groups claim (only if you need group-driven workgroups):**

**Add groups claim** → choose which groups to include → **ID** token → **Group ID**.

If your groups are synced from on-premises AD you can instead expand **Customise token properties by type** and select `sAMAccountName`, which emits names rather than GUIDs and makes the mapping table far more readable. Cloud-only groups do not offer this.

With both configured, a user holding the `Platform.Admin` app role and membership of one group gets an ID token containing:

```json
{
  "roles": ["Platform.Admin"],
  "groups": ["f1d4c8a2-9b3e-4c7a-8f12-6d5e4b3a2c10"],
  "email": "jane.doe@example.org",
  "sub": "AAAAAAAAAAAAAAAAAAAAAIkzqFVrSaSaFHy782bbtaQ"
}
```

Note what is **not** there: no `email_verified`.

## Step 5: Add the provider to the API

Entra needs its own slug, so add it to the `providers` array in `config/sso.php`:

```php
'providers' => [
    'default' => [
        // ... the shipped example slot
    ],

    'entra' => [
        'enabled' => (bool) env('SSO_ENTRA_ENABLED', false),
        'label' => env('SSO_ENTRA_LABEL', 'Sign in with Microsoft'),
        'issuer' => env('SSO_ENTRA_ISSUER'),
        'discovery_url' => env('SSO_ENTRA_DISCOVERY_URL'),
        'client_id' => env('SSO_ENTRA_CLIENT_ID'),
        'client_secret' => env('SSO_ENTRA_CLIENT_SECRET'),
        'scopes' => env('SSO_ENTRA_SCOPES', 'openid profile email'),
        'redirect_uri' => env('SSO_ENTRA_REDIRECT_URI'),

        'claim_mapping' => [
            'workgroups_claim' => env('SSO_ENTRA_WORKGROUPS_CLAIM', 'groups'),
            'roles_claim' => env('SSO_ENTRA_ROLES_CLAIM', 'roles'),
            'custodians_claim' => env('SSO_ENTRA_CUSTODIANS_CLAIM'),
        ],
    ],
],
```

Then the `.env`, with `{tenant}` replaced by your Directory (tenant) ID:

```dotenv
SSO_ENABLED=true
SSO_FRONTEND_CALLBACK_URL=https://app.example.org/auth/sso/callback
SSO_FRONTEND_ERROR_URL=https://app.example.org/auth/sso/error

SSO_ENTRA_ENABLED=true
SSO_ENTRA_LABEL="Sign in with Microsoft"
SSO_ENTRA_ISSUER=https://login.microsoftonline.com/{tenant}/v2.0
SSO_ENTRA_CLIENT_ID=<application-client-id>
SSO_ENTRA_CLIENT_SECRET=<secret-value-from-step-2>
SSO_ENTRA_SCOPES="openid profile email"

SSO_ENTRA_WORKGROUPS_CLAIM=groups
SSO_ENTRA_ROLES_CLAIM=roles
# Deliberately unset: custodians match on name, Entra sends GUIDs
```

`discovery_url` can be left unset — the API derives `{issuer}/.well-known/openid-configuration`, which is correct for Entra v2.0.

!!! danger "This is where the login currently stops"
    The API checks five discovered endpoints against the issuer's origin, not just the ones it uses. Entra's issuer, authorisation endpoint, token endpoint, JWKS URI and end-session endpoint are all on `login.microsoftonline.com` and pass. Its `userinfo_endpoint` is `https://graph.microsoft.com/oidc/userinfo` and does not, so discovery throws and the login fails with `provider_not_configured` before the browser leaves the API.

    Nothing in your Entra configuration causes this and nothing in it can fix it — see the notice at the top of this page and [#350](https://github.com/HDRUK/cohort-discovery-service-api/issues/350).

## Step 6: Map the claim values

In `config/claimsaccesscontrol.php`, put the app role **values** and the group **GUIDs** on the right:

```php
'role_mappings' => [
    'user' => 'Platform.User',
    'admin' => 'Platform.Admin',
    'custodian' => 'Platform.Custodian',
],

'workgroup_mappings' => [
    'admin' => 'f1d4c8a2-9b3e-4c7a-8f12-6d5e4b3a2c10',
    'custodian' => '7a2b9c4d-1e8f-4a6b-9c3d-2f1e0a9b8c7d',
    'default' => 'c3e5a7b9-4d2f-4e8a-b1c6-3a9d7e5f2b40',
],
```

Keep a record elsewhere of which GUID is which group — the file itself gives no clue.

If you would rather avoid GUIDs entirely, point workgroups at the `roles` claim too and drive both subjects from app roles:

```dotenv
SSO_ENTRA_WORKGROUPS_CLAIM=roles
SSO_ENTRA_ROLES_CLAIM=roles
```

Each subject resolves independently, so one claim can feed both. You then define app roles covering both vocabularies and map them separately.

## Step 7: Set the trust policy and test

Claim names only say *which* claim carries what. Whether it is trusted is the separate `CLAIM_SYNC_*` policy — see [the three worked configurations](../access-control-policy.md#three-worked-configurations).

Restart the API, then visit `https://api.example.org/api/auth/sso/entra/redirect`, or use the button on the login page. Check the resulting roles and workgroups in the admin Users view.

Until [#350](https://github.com/HDRUK/cohort-discovery-service-api/issues/350) ships this returns `provider_not_configured` without reaching Entra, so there is no token to inspect yet.

## Troubleshooting

A failed login redirects to the error page with `?error=<code>`. The code is all the user sees — the detailed reason below it is written to the API log only. The full code list is in [When a login fails](../reference/login-errors.md).

| `?error=` | Logged reason | Cause |
|---|---|---|
| `provider_not_configured` | `Discovery document [userinfo_endpoint] ... does not belong to the configured issuer` | The blocker — see the top of this page. Also raised if `SSO_ENTRA_ISSUER` has the wrong tenant, since the document's `issuer` must match byte-for-byte |
| `account_linking_failed` | `Account with this email exists but provider [entra] email is unverified` | Expected — Entra sends no `email_verified`. The local account must not already exist, or the identity must be linked another way |
| `account_linking_failed` | `Provider [entra] released no email claim` | The `email` optional claim was not added in Step 4, or the account has no mail attribute populated |
| `invalid_id_token` | `Token endpoint returned 401 ...` | `AADSTS7000215` — secret expired, or the secret **ID** was copied instead of the **Value** |
| `idp_error` | `SSO login rejected by IdP` | `AADSTS50011` — the registered redirect URI does not match `{app url}/api/auth/sso/entra/callback` exactly, including the slug |

And problems that let the login succeed but grant the wrong access:

| Symptom | Likely cause |
|---|---|
| Roles never apply | App roles assigned on the **app registration** rather than under **Enterprise applications → Users and groups** |
| Groups resolve to nothing | GUIDs are arriving but `workgroup_mappings` still lists names on the right |
| Groups work for some users, not others | Group overage — those users exceed the claim limit and Entra replaced `groups` with `_claim_names` |
| All logins fail at token exchange, suddenly | Client secret expired |
