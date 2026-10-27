---
title: SSO Environment Variables
description: Every SSO_* variable, its default and what it controls
tags:
  - configuration
  - authentication
  - sso
---

# SSO environment variables

The full reference for the `SSO_*` block. Start at [Connecting an identity provider](../identity-provider.md) if you are wiring up a provider for the first time — these are the knobs, not the walkthrough.

=== "Core"

    | Variable | Default | Description |
    |---|---|---|
    | `SSO_ENABLED` | `false` | Master switch. Standalone only |
    | `SSO_FRONTEND_CALLBACK_URL` | — | Web URL receiving the one-time handoff code. Required: with SSO enabled and this unset, every SSO route returns a 500 |
    | `SSO_FRONTEND_ERROR_URL` | `SSO_FRONTEND_CALLBACK_URL` | Web URL for failed logins (`?error=...`). Falls back to the callback URL, which will not render an error — set it |
    | `SSO_FRONTEND_LOGIN_URL` | callback origin + `/login` | Where to land after logout |
    | `SSO_TXN_TTL_SECONDS` | `600` | Lifetime of an in-flight login (state/nonce/PKCE) |
    | `SSO_HANDOFF_CODE_TTL_SECONDS` | `60` | Window for the web app to exchange its code |
    | `SSO_DISCOVERY_CACHE_TTL_SECONDS` | `3600` | Cache for `.well-known/openid-configuration` |
    | `SSO_JWKS_CACHE_TTL_SECONDS` | `3600` | Cache for the IdP's signing keys |
    | `SSO_ID_TOKEN_LEEWAY_SECONDS` | `30` | Clock-skew forgiveness on `id_token` |

=== "Per provider"

    Shown for the `default` slot; a second provider uses its own prefix.

    | Variable | Default | Description |
    |---|---|---|
    | `SSO_DEFAULT_ENABLED` | `false` | Enable this provider |
    | `SSO_DEFAULT_LABEL` | `Single Sign-On` | Button text |
    | `SSO_DEFAULT_ISSUER` | — | Issuer, exactly as it appears in tokens |
    | `SSO_DEFAULT_DISCOVERY_URL` | `{issuer}/.well-known/openid-configuration` | Override if discovery lives elsewhere |
    | `SSO_DEFAULT_CLIENT_ID` | — | Client ID at the IdP |
    | `SSO_DEFAULT_CLIENT_SECRET` | — | Client secret at the IdP |
    | `SSO_DEFAULT_SCOPES` | `openid profile email` | Requested scopes |
    | `SSO_DEFAULT_REDIRECT_URI` | `{app url}/api/auth/sso/default/callback` | Override if the API is behind a different public URL |

=== "Claim names"

    | Variable | Default if unset | Description |
    |---|---|---|
    | `SSO_DEFAULT_WORKGROUPS_CLAIM` | `eduperson_entitlement` | Claim holding workgroups. **Falls back to that name rather than disabling the subject** |
    | `SSO_DEFAULT_ROLES_CLAIM` | — | Unset means roles are never read from this provider |
    | `SSO_DEFAULT_CUSTODIANS_CLAIM` | — | Unset means custodians are never read from this provider |

    These say *which* claim carries what. *Whether* it is trusted is controlled centrally by [Access control policy](../access-control-policy.md).

!!! warning "Naming a claim is not the same as trusting it"
    These variables say only *which* claim carries what. Whether it is read at all, and whether it may remove membership, is the separate `CLAIM_SYNC_*` policy — and a mistyped value there disables provisioning silently. See [Access control policy](../access-control-policy.md#the-sync-policy).
