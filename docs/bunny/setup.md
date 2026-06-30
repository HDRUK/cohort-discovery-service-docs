---
title: Step-by-Step Bunny Setup
description: Nine-step guide to connecting Bunny to the HDR UK Cohort Discovery Service
tags:
  - bunny
  - setup
  - onboarding
---

# Step-by-Step Bunny Setup

This guide walks through connecting Bunny to the Cohort Discovery Service and onboarding your first dataset as a Collection.

Test change

!!! info "Prerequisites"
    Before starting, ensure you have:

    - Submitted an access request via the **Access Cohort Discovery** button on [healthdatagateway.org/en/about/cohort-discovery](https://healthdatagateway.org/en/about/cohort-discovery)
    - Valid Gateway login credentials
    - If your Cohort Discovery access was approved recently, **sign out and sign back in** to refresh your access token

---

## Quick reference

| # | Step | Action |
|---|------|--------|
| 1 | Log in | Sign in to the Gateway and navigate to the Cohort Discovery Service |
| 2 | Management area | Select your organisation tab to access Hosts and Collections |
| 3 | Create a Host | Generates Client ID and Client Secret for Bunny |
| 4 | Navigate to Collections | Open the Collections tab in your management area |
| 5 | Create a Collection | Register your dataset, link it to the Host, set sync frequency |
| 6 | Copy credentials | Note Collection ID, Client ID, Client Secret, and Task API URL |
| 7 | Configure Bunny | Enter credentials into Bunny and point it at the Prod environment |
| 8 | Request activation | Submit your Collection for review by the Cohort Discovery team |
| 9 | Verify | Run distribution jobs; confirm Collection shows as Active |

---

## Step 1 — Log in to Cohort Discovery

1. Go to [healthdatagateway.org/en](https://healthdatagateway.org/en)
2. Click **Sign In** (top-right) and log in with your Gateway account
3. On the Gateway home page, click the **Cohort Discovery** tile
4. Click the grey **Access Cohort Discovery** button on the About page
5. In the pop-up, click the green **New (Beta) Service** button

On first access you will see a welcome message confirming Cohort Discovery has been enabled for your account. Close it to continue.

!!! tip "Missing management tab?"
    You should see a management tab at the top of the page labelled with your team or organisation name. If this tab is missing, ask your organisation's Gateway team admin to add you as a Cohort Discovery manager.

---

## Step 2 — Access Your Management Area

Select your management tab (your organisation or team name). This area is where you configure:

- **Hosts** — credentials that allow Bunny to authenticate with Cohort Discovery
- **Collections** — the datasets you are onboarding

---

## Step 3 — Create a Host (Bunny Credentials)

A **Host** is the authentication mechanism that allows your Bunny instance to connect to Cohort Discovery. It does not represent data by itself.

6. In your management area, select the **Hosts** sub-tab
7. Click **+ Host** under Create
8. Enter a **Host name** — this is for your reference only (e.g. your dataset name or environment)
9. Click **Create**
10. Your new Host appears in the Collection Hosts list. Click on it and note the **Client ID** and **Client Secret** from the right-hand panel — you will need these in Step 7.

| Credential | Description |
|------------|-------------|
| **Client ID** | Username for authenticating with Cohort Discovery (also called `TASK_API_USERNAME` in Bunny config) |
| **Client Secret** | Password (also called `TASK_API_PASSWORD` in Bunny config) |

!!! note "Reusing a Host"
    One Host can be reused across multiple Collections. If you have multiple Bunny instances, you can use a single Host for all of them, or create one Host per instance — whichever suits your setup.

---

## Step 4 — Navigate to Collections

After creating a Host, select the **Collections** tab from your management area.

A Host alone does nothing until at least one Collection is linked to it.

---

## Step 5 — Create a Data Collection

A **Collection** represents a single dataset that Bunny will surface to Cohort Discovery.

11. In the Collections tab, click **+ Collection** under Create
12. Provide a **name and description** — use meaningful names (e.g. `Diabetes Cohort`). The query results view already displays Custodian name and Network, so do not repeat these in the Collection name.
13. Provide the **link to associated Gateway dataset(s)** — the URL to your dataset record in the HDR UK Gateway (e.g. `https://healthdatagateway.org/en/dataset/1378`)
14. In the **Collection Host** dropdown, select the Host you created in Step 3
15. Choose a **Configuration Frequency** for your distribution scan jobs:

    | Frequency | When to use |
    |-----------|-------------|
    | Weekly | Underlying data changes regularly |
    | Monthly | Data changes monthly |
    | Quarterly | Data changes quarterly |
    | Biannually | Data changes infrequently |

16. Click **Create**

---

## Step 6 — Copy Host and Collection Credentials

Your new Collection appears in the All Collections list. Click **Draft Collections** in the left panel for a shorter list.

17. Click on your Collection to open the right-hand panel
18. Click the **lock icon** to unlock the panel if you need to edit
19. Note the following credentials — you will enter these into Bunny in the next step:

| Value | Description |
|-------|-------------|
| **Collection ID** | Unique identifier for this Collection in Cohort Discovery |
| **Client ID** | From your Host (`TASK_API_USERNAME` in Bunny) |
| **Client Secret** | From your Host (`TASK_API_PASSWORD` in Bunny) |
| **Task API Base URL (Prod)** | `https://api.cohort-discovery.healthdatagateway.org/api/v1` |

---

## Step 7 — Connect Bunny to Cohort Discovery

Configure Bunny using the credentials from Step 6:

| Bunny variable | Value |
|----------------|-------|
| `TASK_API_USERNAME` | Client ID |
| `TASK_API_PASSWORD` | Client Secret |
| `COLLECTION_ID` | Collection ID |
| `TASK_API_BASE_URL` | `https://api.cohort-discovery.healthdatagateway.org/api/v1` |
| `TASK_API_TYPE` | `a` or `b` (see [Two-Instance Pattern](two-instance-pattern.md)) |

!!! warning "Always use Production"
    Point Bunny at the **Production** environment unless you have been explicitly instructed otherwise.

See [bunny/configuration.md](configuration.md) for the full list of configuration variables, including database connection settings.

---

## Step 8 — Request Activation of Your Collection

Once Bunny is connected and you are satisfied with your setup:

20. Navigate to your organisation's **Collections** tab
21. Select your draft Collection from the list
22. Click the **lock icon** to unlock the right-hand panel. Click **Run now** against **Demographics** and **Concepts** to seed the concept terms required for querying.
23. Click **Request to make active**

!!! tip "Testing before activation"
    While your Collection is in **Draft**, you can run queries against it that are only visible to you. On the **New Query** tab, click **Filter Collections** (top-right) and select your draft Collection(s). This lets you verify queries work before going live.

### Collection statuses

| Status | Meaning |
|--------|---------|
| **Draft** | Set up but not yet submitted for activation |
| **Pending** | Submitted for activation — under review by the Cohort Discovery team |
| **Active** | Accepted and live for end users to query |
| **Offline** | Collection is temporarily offline |
| **Rejected** | Rejected or removed from active availability |

---

## Step 9 — Verify Successful Onboarding

Confirm everything is working:

- **Bunny authenticates successfully** — no permission or authentication errors in Bunny logs
- **Run distribution jobs** — click **Run now** against **Demographics** and **Concepts** if you haven't already. Without this step, jobs will only run on the next scheduled interval.
- Your Collection appears as **Active** in the Collections tab once approved

### Troubleshooting

| Problem | Fix |
|---------|-----|
| Authentication errors | Sign out and back in to refresh your Gateway access token |
| Wrong environment | Confirm `TASK_API_BASE_URL` is pointing to the Production URL |
| Credentials not working | Verify `Client ID` and `Client Secret` were copied exactly into Bunny |
| No query results | Check Bunny logs for specific error messages |

!!! hdruk "Support"
    Contact the Cohort Discovery support team via the **Need Support?** button on the site, or email [gateway@hdruk.ac.uk](mailto:gateway@hdruk.ac.uk).
