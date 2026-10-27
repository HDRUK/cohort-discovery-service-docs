---
title: Mapping Claims to the Platform
description: Editing config/claimsaccesscontrol.php so your IdP's group and role names mean something here
tags:
  - configuration
  - authentication
  - claims
---

# Mapping claims to the platform

Your identity provider is connected and sending claims. This page is what those claim *values* mean — the second of three steps: [connect a provider](identity-provider.md) → **map its values** → [decide how far to trust them](access-control-policy.md).

`config/claimsaccesscontrol.php` in the API decouples what your identity provider calls a group or role from what this platform calls one. **This file is meant to be edited.** What ships matches HDR UK's Gateway; adjust it to your IdP rather than renaming groups at your IdP to suit it.

It is a PHP config file, so a change needs a redeploy, plus `php artisan config:clear` if config is cached. Keeping your edits across upgrades is covered in [Carrying changes across upgrades](carrying-changes.md).

## Required claims

The ID token must carry `sub` and `email`. `sub` is the identity — the `(provider, sub)` pair is what a returning user is recognised by — and without `email` the API can neither link the login to an existing account nor create a new one.

`email_verified` matters only when the email matches an account that already exists: without it the login is rejected rather than linked, so that an IdP cannot assert its way into someone else's account. A brand new user does not need it.

## What you can map onto

The left-hand side of each table is a **local** name that must already exist. These tables map onto rows the platform seeds; they never create them, so an invented name silently resolves to nothing.

=== "Workgroups"

    Created by `WorkgroupSeeder`, and already on the left of the shipped `workgroup_mappings`:

    `admin` · `default` · `custodian` · `non-uk-industry` · `non-uk-research` · `other` · `uk-industry` · `uk-research` · `nhs-sde`

=== "Roles"

    Created by `RolesAndPermissionsSeeder`:

    `user` · `admin` · `custodian` · `default`

## Read the arrays right

```php
// 'local name' => 'the value your IdP sends'

'workgroup_mappings' => [
    'admin' => 'admin',
    'custodian' => 'custodian',
    'default' => 'default',
    'uk-research' => 'uk-research',
],

'role_mappings' => [
    'user' => 'GENERAL_ACCESS',
    'admin' => 'SYSTEM_ADMIN',
    'custodian' => 'CUSTODIAN',
],
```

Left is **local**, right is **what arrives in the claim**.

| | |
|---|---|
| Only listed values are honoured | An unlisted claim value is ignored, so an unexpected IdP group can never become a grant |
| Both sides match case-insensitively | |
| Many local names per IdP value, not the reverse | The array is keyed by local name, so keys cannot repeat |

## Two worked deployments

=== "Keycloak, own naming"

    A realm that already names its groups and roles after the organisation. Nothing is renamed in Keycloak — the mapping absorbs it.

    ```php
    'workgroup_mappings' => [
        'admin' => 'NRA-CohortDiscovery-Admins',
        'custodian' => 'NRA-CohortDiscovery-Custodians',
        'default' => 'NRA-CohortDiscovery-Users',
        'uk-research' => 'NRA-Academic-Researchers',
    ],

    'role_mappings' => [
        'user' => 'nra-platform-user',
        'admin' => 'nra-platform-admin',
        'custodian' => 'nra-data-custodian',
    ],
    ```

    A claim value of `NRA-CohortDiscovery-Admins` now grants the local `admin` workgroup; a claim value of `admin` matches nothing.

=== "One group, several grants"

    The arrays are keyed by local name, so the *same* IdP value may appear on the right more than once. A single `staff` group can grant two local workgroups:

    ```php
    'workgroup_mappings' => [
        'default' => 'staff',
        'uk-research' => 'staff',
        'admin' => 'platform-admins',
    ],
    ```

## Custodians are matched by name

There is no `custodian_mappings` table, because custodians are not a fixed list the platform seeds — they are records an admin creates for your deployment. A claim value is matched straight against an existing custodian's name, case-insensitively, and a value matching nothing is ignored.

That means the names your IdP sends have to line up with your custodian records, and any group whose name happens to match one will grant membership. Only set `SSO_DEFAULT_CUSTODIANS_CLAIM` if you control the group names in that claim.
