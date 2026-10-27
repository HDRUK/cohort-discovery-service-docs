---
title: Deploying Your Own Instance
description: Running the Cohort Discovery Service as a self-contained platform, branded and wired to your own identity provider
tags:
  - configuration
  - authentication
  - sso
---

# Deploying your own instance

The Cohort Discovery Service as a fully self-contained platform: its own user database, its own authentication, no Gateway dependency. This is what every deployment outside HDR UK runs, and everything in this section assumes it.

How you host it is up to you. The platform is three services, MySQL and Redis; nothing beyond that is prescribed.

---

## Making it your own

Six steps, in the order they make sense. The first gets a working platform with local accounts; steps 2 to 4 are the single-sign-on path, and each is a prerequisite for the next.

<div class="grid cards" markdown>

- :material-server-network: **1 · Running the services**

    ---
    The three repos, what each needs, and the order to bring them up.

    [:octicons-arrow-right-24: Running the services](running.md)

- :material-login-variant: **2 · Connecting an identity provider**

    ---
    What a provider needs to work here, how the login flow runs, and what goes in `config/sso.php`.

    [:octicons-arrow-right-24: Identity provider](identity-provider.md)

- :material-map-marker-path: **3 · Mapping claims to the platform**

    ---
    What your IdP's group and role names mean here, in `config/claimsaccesscontrol.php`.

    [:octicons-arrow-right-24: Claim mapping](claim-mapping.md)

- :material-shield-key: **4 · Access control policy**

    ---
    When claims are read, and whether they may remove access as well as grant it.

    [:octicons-arrow-right-24: Access control policy](access-control-policy.md)

- :material-palette-swatch: **5 · Branding the web app**

    ---
    Product name, colours, logo, legal pages and chrome — one directory you replace wholesale.

    [:octicons-arrow-right-24: Branding](branding.md)

- :material-source-branch-sync: **6 · Carrying changes across upgrades**

    ---
    Your branding and config files live in the upstream repos. Keeping them is an open question.

    [:octicons-arrow-right-24: Carrying changes](carrying-changes.md)

</div>

Steps 2, 3 and 4 answer three different questions that are easy to confuse: *which* IdP, what its values *mean*, and how far they are *trusted*. Setting any one without the others is the usual reason a login succeeds but grants nothing.

---

## Worked example

[Keycloak](examples/keycloak.md) is verified end to end, from an empty realm to a working login. Follow it rather than assembling the steps yourself.

Using something else? [What we support](identity-provider.md#what-we-support) lists what a provider needs, and a walkthrough for another one is the most useful contribution you could make here.

---

Before you start, [Known limitations](limitations.md) is a short list of what is not finished yet. Upgrading from the removed DP-934 resource-server integration? See [Migrating from the old OIDC integration](migrating-from-dp-934.md).
