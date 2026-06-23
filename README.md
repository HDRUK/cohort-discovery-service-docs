# Cohort Discovery Service — Documentation

Implementation and onboarding documentation for the [HDR UK Cohort Discovery Service](https://healthdatagateway.org/en/about/cohort-discovery).

## Published site

**https://hdruk.github.io/cohort-discovery-service-docs/**

| Section | URL |
|---------|-----|
| Home | https://hdruk.github.io/cohort-discovery-service-docs/ |
| Getting Started | https://hdruk.github.io/cohort-discovery-service-docs/getting-started/ |
| Architecture | https://hdruk.github.io/cohort-discovery-service-docs/architecture/ |
| OMOP Requirements | https://hdruk.github.io/cohort-discovery-service-docs/omop/ |
| Connecting Bunny | https://hdruk.github.io/cohort-discovery-service-docs/bunny/ |
| Workstreams | https://hdruk.github.io/cohort-discovery-service-docs/workstreams/ |
| Glossary | https://hdruk.github.io/cohort-discovery-service-docs/reference/glossary/ |

## Source documents

The documentation is derived from the following source documents in [`original_docs/`](original_docs/):

| Document | Description |
|----------|-------------|
| `Cohort Discovery Implementation Guide v5.docx` | Main implementation guide covering architecture, workstreams, and onboarding steps |
| `Appendix_2_CDS_Connect_Query_Retrieval_Software_Onboarding_Guide.docx` | Step-by-step guide for connecting Bunny to the Cohort Discovery Service |
| `Appendix_1_Minimum_OMOP_Dataset_2026_v2.docx` | OMOP CDM requirements and minimum field specification |

## Local development

```bash
pip install -r requirements.txt
mkdocs serve
```

The site will be available at http://127.0.0.1:8000.

## Deployment

The site is deployed automatically to GitHub Pages on every push to `main` via [`.github/workflows/docs.yml`](.github/workflows/docs.yml).

To deploy manually:

```bash
mkdocs gh-deploy --force
```

## Contact

General enquiries: [gateway@hdruk.ac.uk](mailto:gateway@hdruk.ac.uk)
