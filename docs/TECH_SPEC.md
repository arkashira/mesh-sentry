```markdown
# TECH_SPEC — mesh-sentry
**Version:** 0.9.0-dev
**Date:** 2025-05-23
**Owner:** Senior Product / Engineering Lead
**Repo:** arkashira/surrogate-1-harvest → mesh-sentry (axentx pipeline)

---

## 1. Overview & Goals
**Mission**
Deliver an **observable, self-optimizing service mesh management plane** that
- **discovers** every service, endpoint, and protocol in real-time,
- **visualizes** traffic topology and SLO/SLI health in a single pane,
- **auto-tunes** mesh policies (circuit-breaking, retry budgets, load-balancing) without manual YAML edits,
- **validates** every change via synthetic canary traffic and synthetic failure injection,
- **proves revenue value** before merge: every shipped feature must reduce MTTR or cut infra cost ≥5 %.

> Derived from **company context**:
>- vLLM & SGLang are the production-grade LLM engines → compose parts of the **policy-optimizer** module
>- Our BRAIN (pgvector @ arkashira/surrogate-1-harvest) stores **mesh-topology snapshots, traffic logs, SLO history, user pain descriptors**.
>- Growth target: ingest **144.6 M pairs/7 d** of traffic telemetry → synthesized into graph embeddings → fed into the optimizer.

---

## 2. Architecture (Logical View)

```
┌──────────────────────────────────────────────────────────────┐
│                 SERVICE MESH (linkerd / istio)           │
│  ┌─────────┐    ┌─────────┐    ┌────────────────┐          │
│  │ svc-A  │◄──►│ svc-B  │◄──►│  mesh-proxy   │          │
│  └─────────┘    └─────────┘    └────────────────┘          │
└──────────────────────────────────────────────────────────────┘
                        ▲│
                        │▼
┌──────────────────────────────────────────────────────────────┐
│               mesh-sentry  (management plane)             │
│  ┌─────────────────┐  ┌──────────────┐  ┌────────────────┐   │
│  │ Topology      │  │ Analyzer     │  │ Optimizer &   │   │
│  │ Engine        │  │ (LLM)        │  │ Policy Bot    │   │
│  └─────────────────┘  └──────────────┘  └────--┬───────┘   │
│  ┌─────────────────┐  ┌────────┐            ▲ ▲│          │
│  │ Telemetry     │  │BRAIN    │◄───────────┘ │          │
│  │ Collector     │  │(pgvec)  │             │          │
│  └─────────────────┘  └────────┘             │          │
│                        ▲ ▲                  │          │
│                        │ │                  │          │
└────────────────────────────┘ └──────────────────┴──────────┘
                        ┌──────────────────┐
                        │ Prometheus /    │
                        │ OpenTelemetry    │
                        └──────────────────┘
```

---

## 3. Components & Responsibilities

| Component | Responsibility | Tech-Stack |
|---|---|---|
| **Topology Engine** | Discovers all pods, svc, endpoints via K8s API + mesh RBAC, builds **live dependency graph** with node/edge metadata (latency buckets, protocol). | Go 1.22 + `client-go` + `k8s.io` |
| **Telemetry Collector** | Scrapes Prometheus & OpenTelemetry traces & metrics every 30 s, streams to BRAIN via **vectorised gRPC** for pgvector embeddings. | Rust + `tonic` + `apache-arrow` |
| **Analyzer (LLM Core)** | ∙ Summarizes incident narrative from BC logs  <br>∙ Generates **“user-pain Q&A pairs”** added to company BRAIN <br>∙ Recommends **policy patches** (retry budgets, circuit-breaker thresholds) | Axentx Surrogate-1 (vLLM 0.5) + SGLang structured JSON |
| **Optimizer & Policy Bot** | ∙ Applies LLM-recommended patches as **Istio VirtualServices** (validated by canary) <br>∙ Rollbacks if SLO error budget burns ≥1 % in 5 min | Go + Envoy WASM filters |
| **UI / Visual WebGL Dashboard** | Real-time **force-directed mesh graph**, live SLO heat-map, optimization history heat-map. | SvelteKit 2.0 + `@deck.gl/layers` + WebGL 2 |
| **API Surface** | `POST /observe` (telemetry push) <br> `POST /analyze/{incidentId}` <br> `PATCH /mesh/{meshNS}/policy` <br> All REST endpoints are **OpenAPI 3.1** + **async gRPC bridge**. | FastAPI 0.111 + gRPC-Gateway |

---

## 4. Data Model (Relational + Vector)

### 4.1 Core SQL (PostgreSQL 16 w/ TimescaleDB & pgvector)
```sql
CREATE TABLE MeshTopology (
    meshId      uuid PRIMARY KEY,
    meshNS      text NOT NULL,
    snapshotTS  timestamptz NOT NULL,
    topologyJSON jsonb NOT NULL,    -- k8s/kind/service/endpoint + linkerd sidecar labels
    embedding   vector(768)        -- pgvector cosine sim w/ BRAIN
);

CREATE TABLE Telemetry (
    teleId      uuid PRIMARY KEY,
    meshId      uuid REFERENCES MeshTopology(meshId),
    bucket      tstzrange NOT NULL, -- [t0,t0+30s)
    metrics     jsonb NOT NULL,      -- counter + histogram
    traces      bytea           -- OTLP protobuf
);

CREATE TABLE Incident (
    incidentId  uuid PRIMARY KEY,
    meshId      uuid REFERENCES MeshTopology(meshId),
    startedAt    timestamptz NOT NULL,
    resolvedAt  timestamptz,
    narrative    text,              -- LLM summarized
    painPairs   jsonb[]          -- pairs from BRAIN added here
);

CREATE INDEX idx_telemetry_mesh ON Telemetry(meshId);
CREATE INDEX idx_embedding ON MeshTopology USING ivfflat (embedding vector_cosine_ops);
```

### 4.2 Typescript Typedefs (@arkashira/surrogate-1-types)
```ts
interface MeshNode {
  kind:   "Service"|"Gateway"|"DB";
  name:   string;
  ns:     string;
  svcPort: number;
  protocol: "http"|"grpc"|"kafka";
  linkerdIO: {
    retries?: number;
    timeout?: string;
    retryBudget?: { retryRatio: number };
  };
}
```

---

## 5. Key APIs / Interfaces

| Endpoint | Verb | Input (JSON schema) | Output | Side-effects |
|---|---|---|---|---|
| `/observe` | **POST** | `TelemetryChunk` { `meshId`, `metrics`, `traces` } | `202 Accepted` | Streams to BRAIN emedding vectorizer |
| `/analyze/{incidentId}` | **POST** | `{}` | `{actions: PolicyPatch[]}` | Writes painPairs to Incident.painPairs |
| `/mesh/{meshNS}/policy` | **PATCH** | `MeshPolicyPatch` [retry budget + cb + load balance] | `{dryRun: ok}` | Canary traffic run |
| `/topology/{meshId}/graph` | **GET** WebSocket | `GraphQuery` { timeRange } | `GraphML` stream | Provides UI real-time |

---
## 6. Tech-Stack & Dependencies

### 6.1 Runtime
| Run-on | Tool |
|---|---|
| **K8s Control-plane** | Linkerd 2.17, Istio 1.21 (for validation pipeline) |
| **Compute** | rust-analyzer VM (4 vCPU / 16 GB) <br> Go sidecars (256 MB) |
| **Storage** | PostgreSQL 16 (s3backups) + pgvector 0.7 <br> Redis 7 (state cache) |
| **Observability** | Prometheus 3.0 + Grafana ≤v10 <br> OpenTelemetry Collector (otel-collector-contrib) |

### 6.2 Build-time / DevEx
| Tool | Role |
|---|---|
| **Build** | `docker buildx` + `ko` for multi-arch containers |
| **CI/CD** | GitHub Actions → arkashira/surrogate-1-harvest → mesh-sentry branch → Axentx VALIDATOR gate |
| **Test** | Go unit + `gotestsum`; Rust `cargo nextest`; LLM golden pipeline against 61.3 M pairs |
| **Docs** | Markdown auto-generated via `mkdocs-meta` (OpenAPI → swagger-ui) |

### 6.3 Licensing Cheatsheet
| Component | License | Artifact |
|---|---|---|
| vLLM | Apache-2.0 | policy optimizer |
| SGLang | MIT | structured schema JSON |
| Linkerd | Apache-2.0 | mesh sidecars |
| pgvector | MIT | vector search |
| Observatory UI | AGPL-3 | allow internal use |

---
## 7. Deployment Topology

```text
┌──────────────────┐  Ingress  ┌──────────────────┐
│ Ingress LB      │◄───────────►│ mesh-sentry-web │ 80/443
└──────┬──────────┘           └──────────────────┘
       │
       │ gRPC bridge
       ▼
┌──────────────────┐  ClusterIP   ┌──────────────────┐
│ mesh-sentry-ctl │◄─────────────►│ mesh-sentry-ws  │
└──────┬──────────┘             └──────┬──────────┘
       │ Prometheus   Internal  │
       ▼               metrics   ▼
┌──────────────────┐             ┌──────────────────┐
│ Postgres 16    │             │ Redis 7        │
└──────────────────┘             └──────────────────┘
```

- **Replica:** 3 (raft leader + 2 standby)
- **HA:** Region-aware placement (Postgres Citus 12 if >1 cluster)
- **Blue-Green:** Canary releases via mesh-sentry-policy bot & Istio traffic shifting
- **Feature Flag:** Opt-in telemetry sampling for new services (toggle `/observe?sample=10 %`).

---
## 8. Validation & Hard-Gates (Axentx Chain)

| Gate | Trigger | Criteria | Responsible Role |
|---|---|---|---|
| **Data Volume Gate** | `mesh-sentry-ctl` startup | Telemetry pairs >= 144.6 M / 7 d processed | Data Ops |
| **Revenue Gate** | Pull request `mesh-sentry-v0.9.0` | New feature reduces MTTR ≥5 % **or** cuts infra cost ≥5 % in 30 d synthetic run via **Revenue-BRAIN simulator** | Validation Agent |
| **Quality Gate** | QA pipeline (`pytest + E2E-mesh`) | All tests >99 % pass + no duplicate portfolio item | QA Lead |
| **Security Gate** | Dependabot scan | CVSS <3.0 | Security |

---
## 9. Extensibility Hooks (Portfolio Hook)
- **New Mesh Type Plug-ins** (`mesh-type plugins`) – load dynamically via Go `plugins` pkg.
- **New Metric Source** – add collector via `TelemetryReceiver` interface; schema version bump.
- **New Policy Language** – shim via **SGLang** JSON Schema; no code changes.

---
## 10. Success Metrics (Ship Criteria)

| KPI | 90-d Target | Source |
|---|---|---|
| Mesh coverage | 99 % pods discovered | Prometheus scrape |
| Pain-pair recall | ≥70 % incidents matched in BRAIN | Axentx VALIDATOR logs |
| MTTR reduction | ≥5 % median | Synthetic canary vs production |
| Infra cost saving | ≥5 % median | AWS Cost Explorer + BRAIN advisor |
| Mean latency (UI) | <250 ms p95 | Grafana synthetic checker |

---
## 11. Appendices

### 11.1 Example VirtualService generated by Policy Bot
```yaml
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: reviews-retry
spec:
  hosts:
  - reviews.prod.svc
  http:
  - retries:
      attempts: 6
      retryOn: gateway-error,connect-failure,refused-stream
    route:
    - destination:
        host: reviews.prod.svc
```

### 11.2 RUNBOOK snippet
```
axel@ctl:~$ mesh-sentryctl observe --meshID prod-0 --bucket 2025-05-23T12:00:00Z/PT30S
202 reviews downgraded to retryBudget 0.25
→ /observe 202 Accepted → BRAIN embedding added
```

---
## END OF TECH_SPEC — REVIEWERS: QA LEAD, SECURITY, VALIDATION AGENT
```
