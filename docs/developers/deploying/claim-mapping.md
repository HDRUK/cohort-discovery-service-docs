---
title: Mapping Claims to the Platform
description: Editing config/claimsaccesscontrol.php so your IdP's group and role names mean something here
tags:
  - configuration
  - authentication
  - claims
---

# Mapping claims to the platform

Your identity provider is connected and sending claims. This page is what those claim *values* mean — the second of the three steps: [connect a provider](identity-provider.md) → **map its values** → [decide how far to trust them](access-control-policy.md).

`config/claimsaccesscontrol.php` in the API decouples what your identity provider calls a group or role from what this platform calls one.

**This file is meant to be edited.** What ships is a starting point that happens to match HDR UK's Gateway, not a fixed contract. Adjust it to your IdP rather than renaming groups at your IdP to suit it.

!!! info "A PHP config file needs a deploy, not a restart"
    It is subject to `php artisan config:cache`, so a change means a redeploy, plus `php artisan config:clear` on the API if config is cached. Keeping your edits across upgrades is covered in [Carrying changes across upgrades](carrying-changes.md).

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

Left is **local**, right is **what arrives in the claim**. The shipped workgroup table is an identity mapping, which makes it easy to misread as fixed — it isn't.

Resolution works by filtering the config on its *values* and returning its *keys*:

```php
// app/Services/Claims/ClaimResolver.php
return collect(config($configKey, []))
    ->filter(fn ($claimValue) => in_array(mb_strtolower((string) $claimValue), $wanted, true))
    ->keys()
    ->all();
```

## Three worked deployments

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

=== "Microsoft Entra ID, group GUIDs"

    Entra emits group **object IDs**, not names, for cloud-only groups. Put the GUIDs on the right-hand side:

    ```php
    'workgroup_mappings' => [
        'admin' => 'f1d4c8a2-9b3e-4c7a-8f12-6d5e4b3a2c10',
        'custodian' => '7a2b9c4d-1e8f-4a6b-9c3d-2f1e0a9b8c7d',
        'default' => 'c3e5a7b9-4d2f-4e8a-b1c6-3a9d7e5f2b40',
    ],
    ```

    Keep a comment-free mapping readable by recording which GUID is which group in your deployment notes, not in this file.

    App roles are the cleaner path — they emit the role **value** string you choose, so `role_mappings` stays human-readable:

    ```php
    'role_mappings' => [
        'user' => 'Platform.User',
        'admin' => 'Platform.Admin',
        'custodian' => 'Platform.Custodian',
    ],
    ```

    See the [Entra ID example](examples/entra-id.md) for the app registration side.

=== "One group, several grants"

    The arrays are keyed by local name, so the *same* IdP value may appear on the right more than once. A single `staff` group can grant two local workgroups:

    ```php
    'workgroup_mappings' => [
        'default' => 'staff',
        'uk-research' => 'staff',
        'admin' => 'platform-admins',
    ],
    ```

    The reverse is not possible: you cannot map two different IdP groups onto one local workgroup, because that would need duplicate keys.

## Rules that bite

| Rule | Consequence |
|---|---|
| The left-hand side must already exist | These tables map onto existing `workgroups.name` rows and existing roles. They never create them — an invented local name silently resolves to nothing |
| Only listed values are honoured | An unlisted claim value is ignored, so an unexpected IdP group can never become a grant |
| Both sides match case-insensitively | Via `mb_strtolower` on both, and `LOWER(name)` in the query |
| Many local names per IdP value, not the reverse | The array is keyed by local name |
| It is a PHP config file | Needs a deploy, plus `php artisan config:clear` if cached. Not runtime-tunable like the `.env` switches |

## Custodians have no mapping table

There is no `custodian_mappings`. A claim value is matched directly against an existing custodian's `name`:

```php
return Custodian::query()
    ->whereIn(DB::raw('LOWER(name)'), $normalised)
    ->pluck('id')
    ->all();
```

Nothing is created on the fly, but any value matching a custodian's name grants membership. Only point `SSO_DEFAULT_CUSTODIANS_CLAIM` at a claim whose values you trust to line up with your custodian records — see the collision warning in [Access control policy](access-control-policy.md).
