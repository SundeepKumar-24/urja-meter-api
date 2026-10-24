# Reflection

## Priorities
I prioritized a small read-only API, separation between routes and upstream HTTP handling, explicit upstream errors, and documentation that distinguishes observed facts from assumptions.

## Trade-offs
The adapter passes through opaque JSON because the actual upstream schemas are not yet captured. This avoids fabricating field names but means the API contract is not yet normalized. The current tests validate local behavior only.

## What I would improve with more time
1. Implement the verified login/session flow.
2. Normalize observed geo, energy, meter, and transformer response shapes.
3. Add sanitized response fixtures and integration tests.
4. Add validated filters and pagination.
5. Add short-TTL caching after confirming freshness requirements.
6. Add structured logs, request IDs, and metrics without exposing secrets.
7. Implement bulk export after inspecting its actual request and format.

## What was skipped
Frontend, write operations, caching, bulk export, and custom login were skipped pending confirmation of the portal protocol and assignment priorities.
