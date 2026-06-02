# ADR 0001: Read-Only and Dry-Run First

Status: Accepted

The Open Perps Reliability Stack starts as read-only and dry-run infrastructure. It may include adapters, data models, replay logic, risk calculations, dashboards, and non-signing simulations.

It must not include production trading, custody, private-key handling, capital deployment, or live execution. Production execution requires a separate security review, signer isolation plan, protocol allowlist, capital limits, runbooks, and explicit founder approval.
