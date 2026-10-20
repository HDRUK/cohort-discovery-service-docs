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

!!! info "This is the default mode"
    Set `APP_OPERATION_MODE=standalone` on the API and `APPLICATION_MODE=standalone` on the web app. The only other value, `integrated`, exists solely so the HDR UK Gateway can act as identity provider for HDR UK's own hosted deployment — it is not a general-purpose SSO mechanism and will not work with a third-party IdP. If you want SSO, you want this section, not that one.

## Minimum configuration

=== "API"

    ```dotenv
    APP_OPERATION_MODE=standalone

    JWT_SECRET=a-long-random-secret-for-local-dev
    STANDALONE_JWT_TTL_MINUTES=120

    PASSPORT_TOKEN_EXPIRES_IN_DAYS=30
    PASSPORT_REFRESH_TOKEN_EXPIRES_IN_DAYS=60
    ```

=== "Web"

    ```dotenv
    APPLICATION_MODE=standalone
    NEXT_PUBLIC_LOGIN_URL=http://localhost:3000/auth/login
    ```

=== "Demo users"

    ```bash
    php artisan db:seed --class=StandaloneDemoSeeder
    ```

    Set credentials before seeding:

    ```dotenv
    DEMO_USER_EMAIL=admin@example.com
    DEMO_USER_PASSWORD=YourPassword1!
    DEMO_RESEARCHER_EMAIL=researcher@example.com
    DEMO_RESEARCHER_PASSWORD=YourPassword1!
    ```

That is a working platform with local accounts. Everything below makes it yours.

---

## Making it your own

Five steps, in the order they make sense. Only the first is needed by every deployment; steps 2 to 4 are the single-sign-on path, and each one is a prerequisite for the next.

<div class="grid cards" markdown>

- :material-palette-swatch: **1 · Branding the web app**

    ---
    Product name, colours, logo, legal pages and chrome — one directory you replace wholesale.

    [:octicons-arrow-right-24: Branding](branding.md)

- :material-login-variant: **2 · Connecting an identity provider**

    ---
    Will your IdP work, how the login flow runs, and what goes in `config/sso.php`.

    [:octicons-arrow-right-24: Identity provider](identity-provider.md)

- :material-map-marker-path: **3 · Mapping claims to the platform**

    ---
    What your IdP's group and role names mean here, in `config/claimsaccesscontrol.php`.

    [:octicons-arrow-right-24: Claim mapping](claim-mapping.md)

- :material-shield-key: **4 · Access control policy**

    ---
    When claims are read, and whether they may remove access as well as grant it.

    [:octicons-arrow-right-24: Access control policy](access-control-policy.md)

- :material-source-branch-sync: **5 · Carrying changes across upgrades**

    ---
    All three files live in the upstream repos. Keeping your versions is an open question.

    [:octicons-arrow-right-24: Carrying changes](carrying-changes.md)

</div>

Steps 2, 3 and 4 answer three different questions that are easy to confuse: *which* IdP, what its values *mean*, and how far they are *trusted*. Setting any one without the others is the usual reason a login succeeds but grants nothing.

---

## Worked example

[Keycloak](examples/keycloak.md) is verified end to end, from an empty realm to a working login. Follow it rather than assembling the steps yourself.

Using something else? [What we support](identity-provider.md#what-we-support) lists what a provider needs, and contributions adding another walkthrough are welcome.

---

Upgrading from the removed DP-934 resource-server integration? See [Migrating from the old OIDC integration](migrating-from-dp-934.md).
