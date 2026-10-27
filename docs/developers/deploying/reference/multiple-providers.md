---
title: Running More Than One Provider
description: What changes when a deployment has two identity providers
tags:
  - configuration
  - authentication
  - sso
---

# Running more than one provider

Add a second slot to the `providers` array in `config/sso.php`, keyed by its own slug, with its own `SSO_<SLUG>_*` variables and its own callback URL registered at that IdP.

One person can hold an identity at several providers. Claim sync, though, was built around a single one, so three things change:

- **`first_login` means the user's first login anywhere**, not their first at this provider. A user who has already signed in via provider A gets no claim sync from provider B. Use `always` if the second provider needs to grant anything.
- **`CLAIM_SYNC_*_AUTHORITATIVE` is global.** Under `always` and authoritative, whichever provider was used most recently replaces what the other granted. Keep the group vocabularies identical across providers, or do not run more than one authoritatively.
- **Linking to an existing user needs `email_verified`.** Each `(provider, sub)` pair is a new identity, so a provider that does not assert a verified email can create new users but never attach to existing ones.

This configuration is not one we have tested end to end — if you run it, we would welcome the feedback.
