---
title: Contributing
description: How to contribute to the Cohort Discovery Service
tags:
  - contributing
  - development workflow
---

# Contributing

This guide covers the contribution workflow for the three services. The process is the same across all three; the per-service pre-PR checklist differs.

---

## Which repo?

| Change | Repo |
|--------|------|
| API behaviour, authentication, OMOP queries, task management | `cohort-discovery-service-api` |
| UI, frontend components, page layouts, Server Actions | `cohort-discovery-service-web` |
| NLP entity extraction, fuzzy matching, text normalisation | `cohort-discovery-service-nlp` |

---

## Branch and PR workflow

1. Fork the relevant repo (or create a branch if you have direct access)
2. Branch from `dev`:
   ```bash
   git checkout dev
   git pull origin dev
   git checkout -b feat/DP-1234-short-description
   ```
3. Make focused changes — one feature or fix per PR
4. Run the pre-PR checks for your service (see below)
5. Push and open a pull request against `dev`

!!! info "Branch naming"
    Branch names are not enforced, but `feat/DP-XXXX-description` and `fix/DP-XXXX-description` are the convention, where `DP-XXXX` is the Jira ticket number.

---

## PR title convention

PR titles are validated in CI. Use one of these formats:

```
feat(DP-1234): short description
fix(DP-5678): short description
fix!(DP-5678): breaking change description
RELEASE: vX.Y.Z
```

Accepted prefixes: `feat`, `fix`, `chore`, `docs`, `style`, `refactor`, `test`, `perf`

---

## Pre-PR checklist

Run these before requesting a review:

=== "API (Laravel)"

    ```bash
    composer run test        # PHPUnit test suite
    composer run lint        # PSR-12 lint (Laravel Pint)
    composer run phpstan     # Static analysis
    npm run lint:workflows   # GitHub Actions lint (requires: brew install actionlint)
    ```

=== "Web (Next.js)"

    ```bash
    npm run lint             # ESLint
    npm run test             # Jest unit tests
    npm run build            # Production build (catches TypeScript errors)
    npm run lint:workflows   # GitHub Actions lint (requires: brew install actionlint)
    ```

    For UI-heavy changes, also:
    ```bash
    npm run build-storybook
    ```

=== "NLP (Python)"

    ```bash
    pytest                   # Full test suite
    npm run lint:workflows   # GitHub Actions lint (requires: brew install actionlint)
    ```

---

## PR template

Each PR should cover:

```markdown
## Summary
- What does this change do?
- Why is it needed?

## Type of change
- [ ] Feature  [ ] Bug fix  [ ] Refactor  [ ] Docs  [ ] Test  [ ] Chore

## Testing
- [ ] Tests pass (`composer run test` / `npm run test` / `pytest`)
- [ ] Linting passes
- [ ] Build passes (Web only)

## Screenshots (if applicable)

## Rollout / risk
- Impacted areas:
- Rollback plan:
```

---

## Coding standards

These apply across all three services:

**Make surgical changes.** Touch only the code necessary for the task. Don't improve adjacent code, refactor neighbours, or add speculative features. Your diff should trace directly to the task.

**Keep controllers thin.** Delegate business logic to services. In the API, controllers in `app/Http/Controllers/Api/V1/` should do no more than validate, call a service, and return a response.

**Don't mock the database in tests.** API tests run against a real MySQL instance. Mocking DB layers has historically masked production failures. The `RefreshDatabaseLite` trait keeps tests fast without mocking.

**No comments for obvious things.** Only add a comment when the *why* is non-obvious — a hidden constraint, a workaround, a subtle invariant. Don't describe what the code does; well-named identifiers do that.

**Match existing style.** Even if you'd prefer a different pattern, match what's already there unless refactoring is the explicit goal of the PR.

**API versioning.** All API routes are under `/api/v1/`. Breaking changes must increment the version; don't modify existing v1 contracts in place.

---

## Release process

Releases are automated via `semantic-release` on the `main` branch. The changelog and version tag are generated from commit messages using conventional commits.

Feature development happens on `dev`. The `main` branch is used only for release automation — do not open feature PRs against `main`.
