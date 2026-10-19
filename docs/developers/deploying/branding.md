---
title: Branding the Web App
description: Replacing the product name, colours, logo, legal pages and chrome with your own
tags:
  - configuration
  - branding
---

# Branding the web app

Everything organisation-specific in the web app lives in one directory you replace wholesale. No application code changes, no environment variables.

!!! info "Branding needs a rebuild, not a restart"
    `branding/` is bundled into the Next.js build, so it is the one customisation that cannot be mounted into a running container — see [Carrying changes across upgrades](carrying-changes.md).

Everything organisation-specific lives in one directory at the repo root:

```
branding/
├── branding.config.ts        # names, URLs, login copy, legal metadata
├── theme.ts                  # MUI palette and typography
├── assets/
│   └── logo.svg              # header logo
└── legal/
    ├── termsAndConditions.mdx
    └── privacyPolicy.mdx
```

A TypeScript path alias makes it swappable — application code imports `@branding/...`, never a relative path:

```json
// tsconfig.json
"paths": {
  "@/*": ["./src/*"],
  "@branding/*": ["./branding/*"]
}
```

Replace the directory's contents and the app is yours. No application code changes, no environment variables.

## `branding.config.ts`

The shape is `BrandingConfig` in `src/types/branding.ts`. Here is a complete worked example for a fictional TRE:

```typescript
import { BrandingConfig } from "@/types/branding";

const branding: BrandingConfig = {
  productName: "DataLink",
  productLongName: "Northern Research Alliance DataLink",
  description: "Cohort discovery for the Northern Research Alliance TRE",
  organisationName: "Northern Research Alliance",
  logoAlt: "Northern Research Alliance DataLink logo",
  loginTitle: ["Northern Research", "Alliance DataLink"],
  loginHeadline: ["Find your cohort.", "Faster, together."],
  loginSubheadline: "Secure cohort discovery for our research partners.",
  copyrightHolder: "Northern Research Alliance",
  hdrukChromeInStandalone: false,
  links: {
    organisation: "https://example.org",
    cookieNotice: "https://example.org/cookies",
    accessibilityStatement: "https://example.org/accessibility",
  },
  legal: {
    termsAndConditions: {
      title: "Terms and conditions",
      lastUpdated: "January 2026",
    },
    privacyPolicy: {
      title: "Privacy policy",
      lastUpdated: "January 2026",
    },
  },
};

export default branding;
```

What each field actually drives, and where:

| Field | Renders in | Notes |
|---|---|---|
| `productLongName` | `<title>` on every page (`layout.tsx`), and `"<page> \| <productLongName>"` on legal pages | This is the browser tab text, not `productName` |
| `productName` | Login page body copy ("Sign in to your *X* workspace"), legal-page source banner | Short form, used in sentences |
| `description` | `<meta name="description">` | |
| `organisationName` | Footer link label, "Visit the *X* site" | **Integrated mode only** — see the gap below |
| `logoAlt` | `alt` on the header logo | Accessibility only, not visible |
| `loginTitle` | Two-line login heading (`LoginLanding.tsx`) | Exactly two strings |
| `loginHeadline` / `loginSubheadline` | Login brand panel (`LoginBrandPanel.tsx`) | `loginHeadline` is exactly two strings |
| `copyrightHolder` | Footer *and* login page copyright line | Year is generated, not configured |
| `hdrukChromeInStandalone` | See [HDR UK chrome](#hdr-uk-chrome) | |
| `links.organisation` | Fallback for the organisation URL when `NEXT_PUBLIC_LOGIN_URL` is unset | Only a fallback — the env var wins |
| `links.cookieNotice` / `links.accessibilityStatement` | Footer secondary links | Standalone: shown only if set. Integrated: always shown, derived from the organisation URL |
| `legal.*.title` / `lastUpdated` | Legal page heading and "Last updated" line | |
| `legal.*.sourceLabel` | Optional "this policy is sourced from X" banner | Omit it once the text is yours |

!!! warning "`organisationName` does nothing in standalone mode"
    The only place it renders is the footer's "Visit the *X* site" link, and `Footer.tsx` suppresses that link entirely when standalone:

    ```typescript
    const showOrganisationLink = !isStandalone;
    ```

    Set it anyway for correctness, but don't expect it on screen. See [Known gaps](#known-gaps).

## `theme.ts`

MUI `ThemeOptions`. There are **three** layers, not two, and the third one catches people out:

```
@hdruk/ui themeOptions          ← HDR UK brand palette, from the npm package
  ↓ deepmerge (app wins)
src/config/theme.ts             ← app-wide component and typography defaults
  ↓ deepmerge (branding wins)
branding/theme.ts               ← yours
```

The first merge happens inside `HdrukUiProvider`, which the app wraps everything in via `ThemeRegistry`. From the published bundle:

```javascript
const mergedTheme = useMemo(() => {
  const theme2 = createTheme(deepmerge(themeOptions, themeOptions2));
  return responsiveFontSizes(theme2);
}, [themeOptions2]);
```

`themeOptions` is the package's own HDR UK palette; `themeOptions2` is what the app passes in.

The second is in `src/config/theme.ts`:

```typescript
export const themeOptions: ThemeOptions = deepmerge(
  baseThemeOptions,
  brandingTheme,
);
```

Anything you set wins; anything you omit falls through — **including to HDR UK's brand colours**.

!!! danger "`primary` and `secondary` are not set by this app at all"
    Neither `src/config/theme.ts` nor the shipped `branding/theme.ts` defines `palette.primary` or `palette.secondary`. Both fall through to `@hdruk/ui`:

    ```javascript
    primary: brandColors.seaGreen,       // #3db28c
    secondary: brandColors.cornflowerBlue, // #475da7
    ```

    So a deployment that replaces `branding/theme.ts` without setting them keeps HDR UK's sea green and cornflower blue — on buttons, and on the header app bar, which is filled with `palette.secondary.main`. **Set both explicitly.** Replacing the logo while leaving these alone is the most common way a rebrand ends up still looking like HDR UK.

A minimal override is valid — you do not need to respecify the whole palette:

```typescript
import { ThemeOptions } from "@mui/material/styles";

const brandingTheme: ThemeOptions = {
  palette: {
    primary: { main: "#1b6ca8" },
    secondary: { main: "#13293d" },
    link: { main: "#1b6ca8" },
    text: { primary: "#22303c", secondary: "#6b7a86" },
  },
  typography: {
    fontFamily: '"Inter", sans-serif',
  },
};

export default brandingTheme;
```

| Token | Affects |
|---|---|
| `palette.primary` | Primary buttons and accents. **Falls through to HDR UK sea green if unset** |
| `palette.secondary` | Header app bar background — the logo sits on this. **Falls through to HDR UK cornflower blue if unset** |
| `palette.link` | Inline links, anywhere `color="link"` is used |
| `palette.success` | Confirmation banners, success chips |
| `palette.table` | Table header and row accent |
| `palette.text.primary` / `.secondary` | Body and muted text |
| `palette.background.default` / `.paper` | Page background vs card surfaces |
| `palette.tooltip` | Tooltip background |
| `palette.yellowCustom`, `sage`, `secondaryBlack` | Component-specific accents — grep before assuming unused |
| `typography.fontFamily` | Base font — see below |

!!! warning "Changing the font takes two edits"
    `theme.ts` only tells MUI which font *name* to apply. The font is loaded in `src/app/layout.tsx` via `next/font/google`, which currently loads three and exposes them as CSS variables on `<body>`:

    ```typescript
    const sourceSans = Source_Sans_3({
      variable: "--font-source-sans-3",
      subsets: ["latin"],
      style: ["normal", "italic"],
      display: "swap",
    });
    ```

    To change the typeface, add your font there in the same pattern, include its `variable` in the `<body className>`, and set `typography.fontFamily` in `branding/theme.ts` to match. Editing only one leaves the font loaded but unused, or named but never fetched.

## Logo and icons

`branding/assets/logo.svg` renders on the app bar, which is filled with `palette.secondary.main` — pick artwork that reads against your secondary colour.

The favicon and app icon are the **one exception** to "everything lives under `branding/`". Next.js resolves them by filename from the app directory, so they cannot be aliased:

| File | Replace in place |
|---|---|
| `src/app/favicon.ico` | Browser tab icon |
| `src/app/icon.svg` | PWA / app icon |

## Legal pages

In standalone mode `/terms-and-conditions` and `/about/privacy-policy` render MDX straight from `branding/legal/`. In integrated mode those links point at the Gateway instead.

```mdx
{/* branding/legal/termsAndConditions.mdx */}

## Who we are

Northern Research Alliance DataLink is operated by the Northern Research
Alliance for federated cohort discovery across our member TREs.

## Using the service

By logging in you agree to use the service only for the research purposes
approved for your account, and not to attempt to identify individuals from
any cohort summary the platform returns.

## Contact

Questions about these terms: [legal@example.org](mailto:legal@example.org).
```

The source banner appears only when `sourceLabel` is set — `sourceHref` is derived automatically:

```typescript
sourceHref={sourceLabel ? externalLinks.termsAndConditions : undefined}
```

!!! danger "Replace the legal text before you deploy"
    `branding/legal/` ships HDR UK's own terms and privacy policy, naming HDR UK as the data controller and giving its company number and contact details. Serving those unchanged from a deployment HDR UK does not operate is wrong, and very likely a data protection problem. Write your own, and clear `sourceLabel` so the "sourced from" banner disappears.

## HDR UK chrome

The `@hdruk/ui` header and footer embed the Gateway logo and an HDR UK copyright line that `branding/` **cannot** override. Three things decide whether they render:

```typescript
// src/hooks/useHdrukChrome.ts
const useHdrukChrome = (): boolean => {
  const { hdrukTheme: hdrukThemeEnabled } = useFeatures();
  const { isStandalone } = useApplicationMode();

  return (
    hdrukThemeEnabled && (!isStandalone || branding.hdrukChromeInStandalone)
  );
};
```

| `hdruk-uk-theme` | Mode | `hdrukChromeInStandalone` | Result |
|---|---|---|---|
| `true` | integrated | ignored | Gateway chrome |
| `true` | standalone | `false` *(default)* | Your chrome only |
| `true` | standalone | `true` | Your logo **and** Gateway logo, plus Gateway footer |
| `false` | either | ignored | Neutral chrome |

For a third-party deployment the default is already correct: leave `hdrukChromeInStandalone` at `false` and replace `branding/assets/logo.svg`.

Turning it on is all-or-nothing — the Gateway logo is rendered by the `@hdruk/ui` header itself, so you cannot take the two logos without also taking the Gateway footer.

!!! warning "`hdruk-uk-theme` is not currently settable"
    The table above describes the code's logic, but the flag is **not seeded by the API** — it is absent from `database/seeders/FeatureSeeder.php`, so no row exists for it and the web app falls back to `DEFAULT_FLAGS`, where it is hardcoded `true`. In practice the bottom row of that table is unreachable today. Use `hdrukChromeInStandalone: false` instead, which works. See [Known gaps](#known-gaps).


---

## Known gaps

!!! bug "`organisationName` is unreachable in standalone mode"
    `Footer.tsx` gates the only consumer behind `!isStandalone`, so a standalone deployment can set `organisationName` and never see it. Either the footer should render an organisation link in standalone using `links.organisation`, or the field should be documented as integrated-only.

!!! bug "The shipped `branding/theme.ts` omits `primary` and `secondary`"
    The two colours that most define the look are absent from the file a deployment is told to edit, so they silently inherit HDR UK's brand palette from `@hdruk/ui`. Adding them to the shipped file — even set to their current effective values — would make the rebrand surface discoverable instead of something you have to trace through a node_modules bundle to find.

!!! bug "`hdruk-uk-theme` cannot be turned off"
    The flag is read by `useHdrukChrome()` and `SupportPopOut`, but it is not in `FeatureSeeder`, so no database row exists and the web app falls back to its hardcoded `true` default. The documented "set it false on the API to force neutral chrome" path does not work today.
