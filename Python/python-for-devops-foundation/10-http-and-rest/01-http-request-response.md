# HTTP Request and Response

An HTTP request contains a method, URL, headers and optionally a body. A response contains a status code, headers and often a body.

Common methods: GET retrieves, POST creates or initiates, PUT replaces, PATCH partially updates and DELETE removes. Follow the provider's API contract rather than assuming every endpoint follows generic conventions.

Useful headers:
- `Accept`: response formats the client can handle.
- `Content-Type`: request body format.
- `Authorization`: credentials or token.
- `Retry-After`: may indicate when to retry.

HTTPS protects traffic with TLS and authenticates the server when certificate validation is enabled. Do not disable certificate verification to bypass trust errors; fix the certificate, hostname or trust-store issue.

Exercises: inspect headers from a public API, compare query parameters with JSON bodies and explain why HTTPS does not replace authorization.
