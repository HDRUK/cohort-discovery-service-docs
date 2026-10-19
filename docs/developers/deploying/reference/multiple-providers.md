---
title: Running More Than One Provider
description: What changes when a deployment has two identity providers
tags:
  - configuration
  - authentication
  - sso
---

# Running more than one provider

The schema supports it — `user_identities` is unique on `(provider, provider_sub)` and indexed on `(user_id, provider)`, so one person can hold an identity at several IdPs. Three behaviours catch people out, because claim sync was designed around a single provider.

!!! warning "`first_login` means the user's first login, not their first login *here*"
    `claims_synced_at` is a column on `users`, not on `user_identities`. Once any provider has synced claims for a user, that timestamp is set for good.

    So a user who signs in via provider A, then later via provider B, gets **no claim sync at all** from B under `CLAIM_SYNC_*=first_login` — including the [Mixed control](../access-control-policy.md#three-worked-configurations) shape, which uses `first_login` for workgroups. Use `always` if a second provider needs to grant anything.

!!! warning "Authoritative sync is global, not per provider"
    `CLAIM_SYNC_*_AUTHORITATIVE` is a single setting across all providers. Under `always` + authoritative, whichever IdP a user most recently authenticated with replaces what the other granted — two IdPs with different group vocabularies will overwrite each other on every login.

    Either keep the vocabularies identical across providers, or don't run more than one authoritatively.

!!! danger "A second provider can only attach to an existing user if it asserts `email_verified`"
    The identity is `(provider, sub)`, so signing in at provider B always looks like a new identity. To attach it to the user already linked to provider A, B has to go through the verified-email route — and that requires `email_verified: true`.

    A provider that does not emit `email_verified` can still create *new* users, but can never link to one that already exists. In a multi-provider deployment that means the first such provider locks those users out of the second door permanently.
