# Architecture Overview

The system is split into `auth`, `billing`, and `shared` domains.

`auth` owns user identity, session issuance, and access guards.
`billing` owns invoices, subscription status, and payment synchronization.
`shared` contains logging, event publication, and cross-cutting helpers.

Cross-module changes usually require understanding how auth session state influences billing entitlements and how shared events flow between domains.
