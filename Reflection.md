# Reflection

## 1. What assumptions did you make?

I treated Urja Meter Ops as a read-only upstream system and used the portal's observed network requests to understand its API behavior. I assumed the wrapper should preserve the upstream JSON response structure instead of introducing an unverified data model. I kept authentication credentials in environment variables and designed the service to return clear errors when the portal is unavailable or misconfigured.

## 2. Which part was the most difficult, and how did you get unstuck?

The most difficult part was understanding how the portal exposed data beyond its user interface. I used the browser's Developer Tools Network panel to inspect requests, query parameters, response payloads, and authentication behavior. I then separated the Flask routes from the HTTP client and used mocked responses to test the API without depending on live portal access.

## 3. If you had another day, what would you improve?

I would add detailed response schemas to the OpenAPI specification, expand automated tests for authentication failures and upstream timeouts, and investigate the portal's network hierarchy and bulk-export functionality. I would also consider caching after defining suitable data-freshness requirements and add structured logging for easier troubleshooting.

## 4. What mistake did you make while solving this?

Initially, pagination validation was inconsistent: the meter endpoint validated the page parameter, while the transformer endpoint did not. I corrected the transformer endpoint and added a regression test. This reminded me to compare similar endpoints and ensure that implementation behavior, tests, and API documentation remain consistent.

## 5. If you were reviewing your own submission, what would you criticise?

The API is a useful starting point, but its responses still depend on the upstream portal's data structure, and the OpenAPI specification does not define detailed response schemas. The current tests use mocked responses and do not fully verify live integration behavior. Before production use, I would strengthen integration testing, schema validation, authentication lifecycle handling, and operational logging.