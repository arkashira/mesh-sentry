Generated `user-stories.md` for **mesh-sentry** — 12 stories across 4 epics, Connextra format with acceptance criteria + S/M/L sizing.

# mesh-sentry — User Stories

**Epic 1 — Real-Time Topology & Observability** (the visibility wedge)
- US-1.1 Live mesh topology map `L`
- US-1.2 Golden-signal drill-down `M`
- US-1.3 Distributed trace correlation `M`

**Epic 2 — Automated Optimization & Recommendations** (the differentiator vs. free dashboards)
- US-2.1 Traffic-policy recommendations `L`
- US-2.2 One-click apply with diff preview `M`
- US-2.3 Anomaly detection & auto-flagging `L`

**Epic 3 — Reliability Alerting & Incident Workflow** (makes it the on-call default)
- US-3.1 SLO-based burn-rate alerting `M`
- US-3.2 Incident snapshot `S`
- US-3.3 Change-to-incident correlation `M`

**Epic 4 — Security Posture & Multi-Cluster Governance** (zero-trust moat)
- US-4.1 mTLS & policy coverage audit `M`
- US-4.2 Multi-cluster unified view `L`
- US-4.3 RBAC & tamper-evident audit log `M`

**Sizing:** 1 S / 8 M / 3 L. **MVP cut:** US-1.1, US-1.2, US-2.1, US-3.1, US-4.1 — proves see → drill → tune → page → prove-posture. Automated apply + anomaly detection + multi-cluster are the premium-pricing wedge over Kiali.

Two notes for the chain:
- I **overwrote** a stale `/tmp/user-stories.md` that contained the prior `medtech-engineers` product's stories — flagging in case downstream steps expected that file to persist.
- **Market data was empty (`{}`)**, so the prioritization rationale (positioning vs. Kiali, mTLS as the moat) is inferred from the hypothesis and the mesh domain, not from validated numbers. Worth grounding before the PRD locks scope.