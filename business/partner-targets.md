Generated `partner-targets.md` for **mesh-sentry** (overwrote a stale glucose-sentry file that was sitting at that path).

8 partners, prioritized by rev-share/distribution leverage then time-to-value:

- **Rev-share leaders:** AWS Marketplace (committed-spend drawdown — biggest ACV lever), Datadog Marketplace (ISV rev-share + inbound), PagerDuty (affiliate/co-sell).
- **Distribution-not-cash:** Grafana, Slack, GitHub marketplaces — treated as CAC reducers.
- **OSS substrates:** Prometheus (signal-in) and Istio xDS (control-out / the automated-optimization moat) — no rev-share but non-negotiable.

Each row carries free-tier limit, S/M/L effort, and the user job it solves, plus a 3-phase sequencing plan (observe→alert→triage → monetize-via-distribution → enterprise-unlock+moat) and PRD risk flags (write-path safety, marketplace cert lead times, multi-substrate metric normalization, Prometheus cardinality).

One thing worth flagging up the chain: the **Market data block was empty (`{}`)** — free-tier limits and effort estimates are from domain knowledge, not validated figures. If BD can supply real market data, the rev-share ceiling estimates should be re-grounded.