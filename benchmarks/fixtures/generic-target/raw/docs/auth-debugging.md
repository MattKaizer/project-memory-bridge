# Auth Debugging Guide

Authentication starts in the route layer, delegates to the service layer, and persists session snapshots through a shared audit helper.

Typical debugging steps include checking login payload normalization, token validation, failure mapping, and shared event emission.

Without compact notes, an agent often opens this guide plus several source files just to recover the same flow.
