# Repository Conventions

- route files normalize payloads and delegate quickly
- service files own business rules
- shared modules provide infrastructure helpers, not domain ownership
- cross-domain rules should be summarized in durable notes before they are rediscovered from code repeatedly

These conventions matter during onboarding and architecture review because they shape where agents should look first.
