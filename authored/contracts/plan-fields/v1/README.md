---
title: "plan-fields contract v1 (placeholder)"
type: contract
status: placeholder
owner: Andrei
updated: 2026-07-27
---

# plan-fields contract — v1

**Placeholder.** Canonical semantics for the operational plan-fields format and the
governance evidence vocabulary are decided in
[[2026-07-27-adr-eco-005-plan-fields-two-plane-model]] (D4 identity/fields, D3
`plan_item_declared_closed` + `evidence_grade`, D11 delivery). This directory reserves the
physical home for the machine-readable contract.

To be added when the offline `plan-fields` package is extracted (ADR sequencing steps 3–5):

- `schema.json` — checkbox grammar, namespaced identity (`todo://`, `roadmap://`), tag
  placement, freshness quartet, canonical JSON node/edge representation.
- `fixtures/valid/`, `fixtures/invalid/` — conformance fixtures shared by every consumer.

Delivery (D11): this authored contract → generated/reviewed versioned package schema +
fixtures → **pinned/vendored copy** inside each consumer. No parser or runtime reads this
directory (or any neighbor repo) at run time.
