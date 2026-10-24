# Legacy Portal Protocol

## Overview

This project wraps the existing Urja Meter Ops portal in a small REST API. The wrapper forwards GET requests to the portal, passes through query parameters or meter identifiers, and returns the portal's JSON data.

**Base URL:** `https://urja-ops.flockenergy.tech`

The portal requires an authenticated session. Authentication is supplied locally through environment variables and is not hard-coded in the source.

## Observed Endpoints

| Portal endpoint | Method | Purpose |
|---|---|---|
| `/portal/meters/search?q={query}&page={page}` | GET | Search and paginate meters |
| `/portal/dts?page={page}` | GET | List distribution transformers |
| `/portal/meters/{meter_id}/energy` | GET | Retrieve energy readings for a meter |
| `/portal/meters/{meter_id}/geo` | GET | Retrieve geographic coordinates for a meter |

These routes were observed in the browser's Network panel while using the portal.

## Observed Meter Search Behavior

The meter search response contains:

- `data`: an array of meter records
- `page`: the current page number
- `pageSize`: the number of records per page
- `total`: the total number of matching records

Each observed meter record includes `meterId`, `serialNo`, `make`, `phaseType`, `installStatus`, and `dtCode`.

The observed page size is 20. A search for `J100000` returned one matching record, while an unfiltered request reported 403 total records.

## Observed Geographic Response

For meter `J100000`, the portal returned latitude and longitude values as strings:

- Latitude: `26.938961002479868`
- Longitude: `75.83095696146852`

The wrapper returns the portal's JSON structure without adding an additional outer `data` wrapper.

## Authentication

The portal uses a session cookie in the observed browser request. The wrapper supports authentication through:

- `PORTAL_COOKIE`
- `PORTAL_BEARER_TOKEN`

These values are read from local environment configuration. Real credentials must not be committed to source control, included in documentation, or shared publicly.

## Error Handling

The wrapper handles the following conditions:

- Missing endpoint configuration: HTTP 503
- Invalid meter-list page parameter: HTTP 400
- Portal HTTP errors: the upstream status code is preserved
- Portal request timeout: HTTP 504
- Other portal request failures: HTTP 502
- Invalid JSON returned by the portal: HTTP 502

The wrapper does not currently convert every portal response into a newly designed domain schema; successful responses retain the portal's JSON structure.

## Assumptions and Limitations

1. The portal endpoints observed during development represent the interface available to the wrapper.
2. The portal may change its response fields, pagination behavior, authentication requirements, or URL patterns.
3. Only GET operations are implemented.
4. The wrapper does not modify portal data.
5. Authentication depends on a valid portal session or supported bearer token.
6. The API has been tested against observed portal responses and with automated tests using mocked responses.
7. The implementation does not currently provide caching, retries, or a local database.

## Future Improvements

- Add schema validation for portal responses.
- Add integration tests using a controlled authenticated test environment.
- Add structured logging and request correlation IDs.
- Consider short-lived caching for frequently requested data.
- Improve upstream error normalization and document exact response schemas.
- Add bulk export or hierarchy endpoints if required by consumers.