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
- **Stack:** Next.js 16, React 18, TypeScript, Material-UI, Zustand, Storybook

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
| `APPLICATION_MODE` | Yes | `integrated` | `standalone` or `integrated` — see [Deployment Modes](modes.md) |
| `NEXT_PUBLIC_LOGIN_URL` | Yes | — | Redirect URL when unauthenticated |
| `NEXT_PUBLIC_TASK_URL` | No | `http://localhost:8100/api/v1` | Task API endpoint |
| `NEXT_PUBLIC_USE_EXAMPLE_QUERY` | No | `false` | Enable example query helpers (debug) |
| `NEXT_PUBLIC_USE_DEBUG_LOGS` | No | `false` | Enable client-side debug logging |
| `CONFIG_SERVICE_DESK_URL` | No | — | Service desk URL for support links |
| `DEFAULT_TABLE_REFRESH_INTERVAL` | No | — | Table auto-refresh interval in ms |
| `DEFAULT_SEARCH_WAIT_TIME` | No | — | Debounce delay before search fires (ms) |

!!! tip "Standalone mode login URL"
    For local standalone development, set:
    ```dotenv
    NEXT_PUBLIC_LOGIN_URL=http://localhost:3000/auth/login
    ```
    For integrated mode, this points to the Gateway login endpoint.

---

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

# Unit & component tests
npm run test             # Jest — all tests
npm run test:watch       # Jest watch mode

# Storybook
npm run storybook        # Component explorer on port 6006
npm run build-storybook  # Build static Storybook output

# E2E tests
npm run mock-api:start   # Start mock API server on port 8100
npm run cy:open          # Cypress interactive runner
npm run cy:run           # Cypress headless
npm run e2e              # Full pipeline: production build → Cypress
npm run e2e:dev          # Full pipeline: dev server → Cypress
```

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

=== "Storybook"

    Storybook documents and visually tests isolated components:

    ```bash
    npm run storybook        # Open at http://localhost:6006
    npm run build-storybook  # Build for static hosting
    ```

---

## Project structure

```
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
│   └── SquareCheckbox/      MUI Checkbox wrapper
├── hooks/                   Shared React hooks (useTable, useSearchParams, …)
├── lib/                     API client helpers and auth logic
│   └── api.ts               apiGet, apiPost, apiPut, apiDelete
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

For component-heavy changes, also run:
```bash
npm run build-storybook
```
