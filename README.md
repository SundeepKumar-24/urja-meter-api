# Urja Meter Operations API

A Flask REST API wrapper for the legacy Urja Meter Ops portal. It exposes endpoints for meter search, transformer listing, meter energy readings, and geographic details.

## Features

- Search and paginate meters
- List distribution transformers
- Retrieve meter energy readings
- Retrieve meter coordinates
- Validate meter-list page parameters
- Forward portal errors with appropriate HTTP status codes
- Configure portal authentication through environment variables
- Automated tests using mocked portal responses

## Requirements

- Python 3.11 or later
- Access to the Urja Meter Ops portal
- A valid portal session cookie or supported bearer token

## Setup on Windows

### 1. Clone the repository

git clone https://github.com/SundeepKumar-24/urja-meter-api.git
cd urja-meter-api

Replace `YOUR_GITHUB_REPOSITORY_URL` with your repository URL.

### 2. Create a virtual environment

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can use the environment's Python directly:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 3. Install dependencies

```powershell
py -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a local `.env` file in the project root:

```dotenv
PORTAL_BASE_URL=https://urja-ops.flockenergy.tech
PORTAL_METERS_URL=https://urja-ops.flockenergy.tech/portal/meters/search
PORTAL_TRANSFORMERS_URL=https://urja-ops.flockenergy.tech/portal/dts
PORTAL_ENERGY_URL=https://urja-ops.flockenergy.tech/portal/meters/{meter_id}/energy
PORTAL_GEO_URL=https://urja-ops.flockenergy.tech/portal/meters/{meter_id}/geo

PORTAL_COOKIE=
PORTAL_BEARER_TOKEN=

REQUEST_TIMEOUT_SECONDS=15
```

Set `PORTAL_COOKIE` to a valid session cookie locally, or configure `PORTAL_BEARER_TOKEN` if the portal supports bearer authentication. Do not commit credentials.

### 5. Run the API

```powershell
py app.py
```

The local server runs at `http://127.0.0.1:5000`.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Check API health |
| GET | `/api/v1/meters?q=&page=1` | Search and paginate meters |
| GET | `/api/v1/transformers?page=1` | List transformers |
| GET | `/api/v1/meters/{meter_id}/energy` | Get meter energy readings |
| GET | `/api/v1/meters/{meter_id}/geo` | Get meter geographic details |

### Examples

Check API health:

```http
GET http://127.0.0.1:5000/health
```

Search meters:

```http
GET http://127.0.0.1:5000/api/v1/meters?q=J100000&page=1
```

List transformers:

```http
GET http://127.0.0.1:5000/api/v1/transformers?page=1
```

Get energy readings:

```http
GET http://127.0.0.1:5000/api/v1/meters/J100000/energy
```

Get geographic details:

```http
GET http://127.0.0.1:5000/api/v1/meters/J100000/geo
```

## Error Handling

| Status | Meaning |
|---|---|
| 400 | Invalid page parameter |
| 404 | Upstream portal reports that a resource was not found |
| 502 | Upstream request failed, or portal returned invalid JSON |
| 503 | Required portal endpoint is not configured |
| 504 | Portal request timed out |

Successful responses preserve the portal's JSON structure.

## Tests

Run automated tests:

```powershell
py -m pytest -v
```

The test suite uses mocked portal responses and does not require a live portal session for its current test cases.

## Documentation

[API Specification](openapi.json) — OpenAPI 3.x specification for the Flask API.
[Portal Protocol Notes](PROTOCOL.md) — Observed portal endpoints, authentication, data formats, and limitations.
[Reflection](Reflection.md) — Assumptions, challenges, mistakes, and future improvements.

## Limitations

The wrapper depends on the legacy portal's availability, authentication, URL patterns, and response schemas. Caching, retries, response-schema validation, and bulk export are not currently implemented.

## Security

Never commit `.env`, session cookies, bearer tokens, passwords, or other credentials. Rotate any credential that has been exposed.