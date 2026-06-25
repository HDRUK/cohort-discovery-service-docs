---
title: NLP Service
description: Developer guide for the Cohort Discovery Service NLP service (FastAPI)
tags:
  - nlp
  - python
  - fastapi
---

# NLP Service

The NLP service is a FastAPI microservice that extracts and normalises clinical entities from free-text queries. It maps those entities to OMOP concept IDs using multi-stage fuzzy matching, then returns them to the API for query construction.

- **Repo:** `cohort-discovery-service-nlp`
- **Port:** 5001
- **Stack:** Python 3.11, FastAPI, RapidFuzz, Uvicorn

---

## Installation

```bash
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install pip --upgrade
pip install -r requirements.txt
cp .env.example .env
```

---

## Environment variables

=== "Database"

    | Variable | Required | Description |
    |----------|----------|-------------|
    | `DB_HOST` | Yes | MySQL host (OMOP vocabulary database) |
    | `DB_PORT` | No | MySQL port (default: 3306) |
    | `DB_NAME` | Yes | OMOP database name |
    | `DB_USER` | Yes | MySQL username |
    | `DB_PASS` | Yes | MySQL password |
    | `OMOP_VIEW` | Yes | View used for concept queries (default: `distributions_and_concept_view`) |

=== "Application"

    | Variable | Default | Description |
    |----------|---------|-------------|
    | `APP_ENV` | `development` | Environment (`development` or `production`) |
    | `APP_DEBUG` | `true` | Enable debug output |
    | `STORE_REFRESH_TTL` | `60` | Concept cache TTL in seconds |
    | `DEFAULT_THRESHOLD` | `70` | Fuzzy match threshold (0–100) |

=== "Fuzzy Matching"

    | Variable | Default | Description |
    |----------|---------|-------------|
    | `FUZZY_TOKEN_OVERLAP` | `true` | Use fuzzy matching for token overlap instead of exact intersection |
    | `FUZZY_TOKEN_MIN_SCORE` | `85` | Minimum score for individual token matches |
    | `RESOLVER_MAX_MATCHES` | `5` | Maximum OMOP concepts returned per query term |
    | `COLLECTION_BOOST_WEIGHT` | `1.5` | Logarithmic boost for concepts appearing in multiple collections |

=== "Advanced"

    | Variable | Default | Description |
    |----------|---------|-------------|
    | `ACRONYM_ENABLED` | `true` | Enable acronym expansion (e.g. T2DM → type 2 diabetes mellitus) |
    | `LOG_RESOLVER_MATCHES` | `false` | Log detailed scoring for each concept match |
    | `LOG_RESOLVER_MATCH_LIMIT` | `50` | Cap on number of logged matches |

---

## Running locally

```bash
uvicorn app:app --host=0.0.0.0 --port=5001 --reload
```

The `--reload` flag restarts the server on code changes. Omit it for a production-like environment.

---

## API endpoints

### `GET /`

Health check. Returns `{"status":"ok"}` when the service is running and the concept store has loaded.

### `POST /extract`

Extracts OMOP concepts from a free-text clinical query.

**Request:**
```bash
curl -X POST http://localhost:5001/extract \
  -H "Content-Type: application/json" \
  -d '{"query": "Type 2 diabetes mellitus with chronic kidney disease stage 3"}'
```

**Query parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `threshold` | int | `DEFAULT_THRESHOLD` | Override fuzzy match threshold for this request |
| `phrase_first` | bool | `true` | Prefer phrase-level overlap scoring |

**Response:**
```json
{
  "entities": [
    {
      "text": "type 2 diabetes mellitus",
      "label": "PROBLEM",
      "negated": false,
      "concept_id": 201826
    },
    {
      "text": "chronic kidney disease stage 3",
      "label": "PROBLEM",
      "negated": false,
      "concept_id": 46271022
    }
  ],
  "groups": [],
  "warnings": [],
  "age_constraints": null,
  "time_constraints": null
}
```

### `GET /acronyms`

Query the acronym expansion index.

| Parameter | Description |
|-----------|-------------|
| `prefix` | Filter by acronym prefix |
| `min_len` | Minimum acronym length |
| `max_len` | Maximum acronym length |
| `limit` | Page size |
| `offset` | Page offset |

---

## Testing

```bash
pytest                                                  # Run all tests
pytest -v                                               # Verbose output
pytest tests/test_fuzzy_concept_resolver.py             # Single file
pytest tests/test_fuzzy_concept_resolver.py::TestNormaliseText  # Single class
pytest --cov=.                                          # With coverage
```

---

## Tuning fuzzy matching

The service uses a multi-stage pipeline for concept matching:

1. **Tokenisation** — the input phrase is split into tokens
2. **Token overlap** — checks which OMOP concept names share tokens with the query
3. **Fuzzy scoring** — RapidFuzz WRatio scores remaining candidates
4. **Penalty scoring** — penalises overly specific matches (e.g. concepts with "stage", "secondary", "complication")
5. **Collection boost** — concepts appearing in more collections get a logarithmic boost

**To increase recall** (return more concepts at lower confidence):
```dotenv
DEFAULT_THRESHOLD=50        # Lower the global threshold
RESOLVER_MAX_MATCHES=10     # Return more candidates
```

**To improve precision** (stricter matches only):
```dotenv
DEFAULT_THRESHOLD=85
FUZZY_TOKEN_MIN_SCORE=90
```

**To debug match scoring:**
```dotenv
LOG_RESOLVER_MATCHES=true
LOG_RESOLVER_MATCH_LIMIT=100
APP_DEBUG=true
```

---

## Architecture

The NLP pipeline has three main components:

**`QueryParser` (`parsing.py`)** — Entry point. Splits input into candidate phrases, extracts age and time constraints, applies text normalisations, detects negation, and deduplicates results by `(concept_id, candidate_text, position)`.

**`RuleEngine` (`rules_engine.py`)** — Stateless processor. Loads patterns from `rules.json` and mappings from `mappings.json`. Handles splitting, demographic normalisation (e.g. "men" → MALE), BMI group mappings, and acronym index building.

**`FuzzyConceptResolver` (`fuzzy_concept_resolver.py`)** — Multi-stage fuzzy matcher. Loads concepts from the OMOP vocabulary database via `OMOP_VIEW` and caches them with a TTL. Scores candidates using tokenisation + RapidFuzz + penalty + boost.

**Text normalisation order:**

1. Extract age constraints → strip patterns
2. Extract time constraints → strip patterns
3. Clean punctuation
4. Strip dangling logical operators
5. Strip leading verbs (e.g. "diagnosed with", "treated for")
6. Apply demographic patterns
7. Apply normalise-group mappings
8. Expand acronyms (if enabled)
9. Apply BMI-group mappings

**To add a new text mapping:** edit `mappings.json` under the appropriate group (`demographic`, `bmi`, or `normalise`).

**To add age or time patterns:** edit `rules.json` under `age_patterns` or `time_patterns`.

---

## Pre-PR checklist

```bash
pytest
npm run lint:workflows   # requires: brew install actionlint
```
