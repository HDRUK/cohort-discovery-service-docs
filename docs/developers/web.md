---
title: Web Service
description: Developer guide for the Cohort Discovery Service Web service (Next.js)
tags:
  - web
  - nextjs
  - typescript
---

# Web Service

The Web service is a Next.js 16 application using the App Router. It renders the Cohort Discovery Service UI for three roles — admin, custodian-admin, and researcher — and communicates with the API exclusively through Next.js Server Actions.

- **Repo:** `cohort-discovery-service-web`
- **Port:** 3000 (dev)
- **Stack:** Next.js 16, React 19, TypeScript, MUI 7, Zustand, TanStack Query

---

## Installation

```bash
npm install
cp .env.example .env
```

---

## Environment variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `API_BASE_URL` | Yes | `http://localhost:8100` | API service URL — used by Server Actions |
| `APPLICATION_MODE` | Yes | `integrated` | `standalone` or `integrated` — see [Deployment modes](index.md#deployment-modes) |
| `NEXT_PUBLIC_LOGIN_URL` | Yes | — | Redirect URL when unauthenticated. Also the base for outbound organisation links; falls back to `links.organisation` in the branding config |
| `NEXT_PUBLIC_TASK_URL` | Yes | `http://localhost:8000/api` | Task endpoints, and the base for the footer's API-docs link |
| `NEXT_PUBLIC_USE_EXAMPLE_QUERY` | No | `false` | Enable example query helpers (debug) |
| `NEXT_PUBLIC_USE_DEBUG_LOGS` | No | `false` | Enable client-side debug logging |
| `COOKIE_TOKEN_NAME` | No | `token` | Name of the session cookie |
| `HIDE_NAV` | No | — | Set to `1` to hide the header and top menu, for embedding in an iframe |
| `CONFIG_SUPPORT_URL` | No | — | Support site used by the support pop-out |
| `CONFIG_SERVICE_DESK_URL` | No | — | Service desk base URL |
| `CONFIG_SERVICE_DESK_SUPPORT_SUFFIX` | No | — | Path appended for support requests |
| `CONFIG_SERVICE_DESK_REPORT_BUG_SUFFIX` | No | — | Path appended for bug reports |
| `DEFAULT_TABLE_REFRESH_INTERVAL` | No | — | Table auto-refresh interval (ms) |
| `DEFAULT_MAX_INVALID_REASONS` | No | — | Maximum invalid-reason messages shown at once |
| `DEFAULT_SEARCH_PREFETCH` | No | — | Search prefetch threshold |
| `DEFAULT_SEARCH_WAIT_TIME` | No | — | Search debounce (ms) |
| `DEFAULT_SEARCH_SUGGESTION_ROTATION` | No | — | Search suggestion rotation interval (ms) |
| `DEFAULT_LOCATION_MIN_RADIUS` | No | — | Minimum location search radius (metres) |

!!! info "Build-time vs per-request"
    Every `NEXT_PUBLIC_*` value is inlined into the client bundle at **build** time and needs a rebuild to change. `CONFIG_*` and `DEFAULT_*` are server-only and read **per request** in `src/providers/ServerDefaultProvider.tsx`, so they can be changed without rebuilding.

!!! tip "Standalone mode login URL"
    For local standalone development, set:
    ```dotenv
    NEXT_PUBLIC_LOGIN_URL=http://localhost:3000/auth/login
    ```
    For integrated mode, this points to the Gateway login endpoint.

!!! info "OIDC / SSO needs no web env vars"
    Standalone-mode SSO is configured entirely on the API (`config/sso.php`) — the web app just renders whatever `GET /api/auth/methods` returns and never holds IdP credentials itself. See [Connecting an identity provider](deploying/identity-provider.md).

The admin Users view (`src/modules/ViewUser/ViewUser.tsx`) shows a user's Details, Sign-in (linked identities, with icons from `ssoProviders.ts`), **Roles**, and **Workgroups** — the latter two as read-only chip lists (`src/components/ChipList/`). `UserTable.tsx` can show the same as columns in the users list. All of it is display-only: role/workgroup assignment is config-driven on the API side (`config/claimsaccesscontrol.php`) — there's no edit UI here. See [Access control policy](deploying/access-control-policy.md).

---

## Branding and customisation

Everything organisation-specific — product name, colours, logo, legal pages, and whether HDR UK chrome appears — lives in one swappable directory at the repo root:

```
branding/
├── branding.config.ts
├── theme.ts
├── assets/logo.svg
└── legal/*.mdx
```

A `@branding/*` → `./branding/*` path alias in `tsconfig.json` is what makes it swappable: application code imports `@branding/branding.config` and `@branding/theme`, never a relative path. Replacing the directory's contents re-skins the app with no code changes and no environment variables.

[:octicons-arrow-right-24: Branding the web app](deploying/branding.md) — full field reference, worked examples, theme tokens, legal pages and the HDR UK chrome switch.

## npm scripts

```bash
# Development
npm run dev              # Dev server with Turbopack on port 3000
npm run dev-debug        # Dev server with Node.js inspector attached

# Production
npm run build            # Production build
npm run start            # Production server on port 3001

# Linting
npm run lint             # ESLint
npm run lint:fix         # ESLint with auto-fix
npm run lint:workflows   # GitHub Actions workflow lint (requires actionlint)

# Unit tests
npm run test             # Jest — all tests
npm run test:watch       # Jest watch mode

# E2E tests
npm run mock-api:start   # Start mock API server on port 8100
npm run cy:open          # Cypress interactive runner
npm run cy:run           # Cypress headless
npm run e2e              # Full pipeline: production build → Cypress
npm run e2e:dev          # Full pipeline: dev server → Cypress

# E2E against a throwaway IdP (standalone SSO)
npm run oidc-mock:start  # Start oidc-server-mock via docker compose
npm run cy:run:oidc      # Run only the *.idp.cy.ts specs
npm run e2e:oidc         # Full pipeline: mock IdP → build → Cypress → teardown
npm run oidc-mock:stop   # Tear the mock IdP down
```

`e2e`, `e2e:dev` and `e2e:oidc` all force `APPLICATION_MODE=standalone`.

---

## Testing

=== "Unit tests (Jest)"

    ```bash
    npm run test
    npm run test:watch

    # Run a specific file
    npm run test -- --testPathPattern=src/utils/__tests__/rules
    ```

    Tests run in a `jsdom` environment. The setup file is `jest.setup.ts`. The path alias `@/` maps to `src/`.

=== "E2E tests (Cypress)"

    The E2E suite requires a running API — use the mock API for isolated front-end testing:

    ```bash
    # Start mock API (port 8100) then open Cypress
    npm run mock-api:start &
    npm run cy:open

    # Or run headlessly against a full stack
    npm run e2e          # production build
    npm run e2e:dev      # dev server
    ```

    Cypress config is in `cypress.config.ts`:
    - Base URL: `http://localhost:3000`
    - Viewport: 1280×900
    - Videos and screenshots on failure are enabled
    - JWT token generation tasks are available for role-based test scenarios

    `cypress/e2e/auth/oidc-login.cy.ts` covers the sign-in options list and SSO error handling (session expired, invalid callback, IdP error passthrough). `cypress/e2e/auth/oidc-login.idp.cy.ts` covers the real round-trip against a throwaway IdP (`oidc-server-mock`, started via `.github/oidc-mock/docker-compose.yml`) — sign-in, cookie set, wrong credentials.

    SSO cookie-setting logic lives in `src/lib/authCookie.ts` and is fully covered by Jest at `src/lib/__tests__/authCookie.test.ts`.

---

## Project structure

```
branding/                    Swappable deployment branding — see Customising your deployment
├── branding.config.ts
├── theme.ts
├── assets/logo.svg
└── legal/*.mdx

src/
├── app/                     Next.js App Router
│   ├── (protected)/         Authenticated routes (admin, custodian, researcher views)
│   ├── (public)/            Unauthenticated routes (login, etc.)
│   └── (error)/             Error boundary pages
├── actions/                 Server Actions — one directory per domain
│   ├── admin/
│   ├── collection/
│   ├── concept/
│   ├── conceptSet/
│   ├── query/
│   ├── task/
│   └── workgroup/
├── modules/                 Feature-level composite components
├── components/              Reusable atoms and molecules
│   ├── Table/               Use via useTable() hook
│   ├── TabsShell/           Page-level tab navigation
│   ├── Modal/               Dialogs
│   ├── SquareCheckbox/      MUI Checkbox wrapper
│   ├── ChipList/            Read-only chip list — used for roles/workgroups display
│   └── UserTable/
│       └── userFilters.ts  Shared filtering logic for user lists
├── hooks/                   Shared React hooks (useTable, useSearchParams, …)
├── lib/                     API client helpers and auth logic
│   └── api.ts               apiGet, apiPost, apiPut, apiDelete
├── utils/
│   └── ssoProviders.ts       Provider slug → icon map for the SSO login buttons
├── config/
│   └── routes.ts            Centralised route builders — always use this for URLs
├── types/                   TypeScript type definitions
└── store/                   Zustand global state (with persistence)
```

---

## Coding patterns

**API calls — always use Server Actions and shared helpers:**
```typescript
// src/actions/query/getQueries.ts
import { apiGet } from "@/lib/api";

export async function getQueries() {
  return apiGet("/api/v1/queries");
}
```

Never use ad-hoc `fetch()` in client components. All backend calls go through Server Actions in `src/actions/`.

**Routing — always use `routes.ts`:**
```typescript
import { routes } from "@/config/routes";

// Good
href={routes.query.detail(query.id)}

// Bad — hardcoded paths break when routes change
href={`/queries/${query.id}`}
```

**State management:**

| State type | Tool |
|------------|------|
| Server / fetched data | Server Actions + React Query (TanStack) |
| Global client state | Zustand (`src/store/`) |
| Form state | React Hook Form + Yup |

**MUI wrappers — use the project's abstractions:**

| Use | Instead of |
|-----|-----------|
| `<Table>` + `useTable()` | MUI `<TableContainer>` directly |
| `<TabsShell>` | MUI `<Tabs>` directly |
| `<Modal>` | MUI `<Dialog>` directly |
| `<SquareCheckbox>` | MUI `<Checkbox>` directly |

**Caching:**
- Read-only data: pass `cacheOptions: { tags: ["queries"] }` to `apiGet`
- Mutations: pass `cacheOptions: { useCache: false }` and call `revalidateTag` in the action

---

## PR title convention

PR titles must match this format (enforced in CI):

```
feat(DP-1234): short description
fix(DP-5678): short description
fix!(DP-5678): breaking change description
RELEASE: vX.Y.Z
```

Accepted prefixes: `feat`, `fix`, `chore`, `docs`, `style`, `refactor`, `test`, `perf`

---

## Pre-PR checklist

Run these before opening a pull request:

```bash
npm run lint
npm run test
npm run build
npm run lint:workflows   # requires: brew install actionlint
```

For changes touching standalone SSO, also run the IdP round-trip:
```bash
npm run e2e:oidc
```
