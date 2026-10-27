---
title: When a Login Fails
description: Every SSO error code, what the user sees, and what actually went wrong
tags:
  - authentication
  - sso
  - troubleshooting
---

# When a login fails

Failures redirect the browser to `SSO_FRONTEND_ERROR_URL` with `?error=<code>`. The code is the only thing the user sees, alongside a generic sentence; the detailed reason is written to the API log and never leaves the server.

| Code | What the user is shown | What actually went wrong |
|---|---|---|
| `provider_not_configured` | This sign-in option is not available right now | Unknown or disabled slug; missing `issuer`, `client_id` or `client_secret`; discovery document's `issuer` does not match; a required endpoint is missing; or the provider publishes endpoints on more than one hostname (see [what we support](../identity-provider.md#what-we-support)) |
| `invalid_state` | Your sign-in session expired or was already used | The `state` is unknown, expired past `SSO_TXN_TTL_SECONDS`, already consumed, or was issued for a different provider |
| `invalid_id_token` | We couldn't verify your identity | Token endpoint returned non-2xx or no `id_token`; signature, `iss`, `aud`, `azp`, `nonce` or `sub` check failed; JWKS empty or malformed; or userinfo reported a different `sub` |
| `account_linking_failed` | We couldn't verify your email address | No `email` claim, or the email matches a local account and `email_verified` was not `true` |
| `idp_error` | Your organisation's login system rejected the attempt | The IdP itself returned `?error=` to the callback |
| `invalid_callback` | That sign-in link is invalid | The callback was reached without a `code` or `state` |
| `provider_unreachable` | *(generic message)* | Network failure reaching discovery, JWKS or the token endpoint |
| `sso_failed` | *(generic message)* | Base error code |
| `exchange_failed` | Your sign-in link expired or was already used | Raised by the web app, not the API: the handoff code was already redeemed or is older than `SSO_HANDOFF_CODE_TTL_SECONDS` |

`provider_unreachable` and `sso_failed` have no entry in the web app's message table, so both fall through to "Something went wrong while signing you in." Seeing the generic message therefore means one of those two — check the API log.
