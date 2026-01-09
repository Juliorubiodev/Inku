# AG_01 – Hito 5 Compliance Checklist

> **Source**: [CC-25-26 Hito 5](https://github.com/cvillalonga/CC-25-26/blob/main/hitos/5.Despliegue.md)  
> **Date**: 2026-01-09

---

## Scoring Overview

| Criteria | Points | Status |
|----------|--------|--------|
| IaaS/PaaS selection justification | 1.5 | ⬜ Pending |
| Deployment tools description | 1.5 | ⬜ Pending |
| Auto-deploy from GitHub config | 1.5 | ⬜ Pending |
| Observability tools | 1.5 | ⬜ Pending |
| Correct deployment functioning | 2.0 | ⬜ Pending |
| Performance tests | 2.0 | ⬜ Pending |
| **TOTAL** | **10.0** | — |

---

## 1. IaaS/PaaS Selection (1.5 pts)

### Requirements
- [ ] Describe criteria used to choose the platform
- [ ] Justify the selection among alternatives considered
- [ ] Document evaluated options with pros/cons

### Suggested Options for Inku

| Platform | Pros | Cons |
|----------|------|------|
| **Render** | Free tier, auto-deploy from GitHub, EU region | Limited free hours/month |
| **Railway** | Docker support, GitHub integration, EU | Consumption-based pricing |
| **Fly.io** | Edge deployment, EU regions, Docker-native | Complex config |
| **Google Cloud Run** | Serverless, Firebase integration | Requires GCP account |
| **AWS App Runner** | Native S3 integration | No free tier |

### Evidence Required
```
docs/AG_02_IAAS_SELECTION.md:
├── Selection criteria (cost, region, ease of deploy)
├── Comparison table of 3+ options
├── Final choice justification
└── Why others were rejected
```

---

## 2. Deployment Tools (1.5 pts)

### Requirements
- [ ] Describe tools used to deploy to IaaS/PaaS
- [ ] Justify tool selection
- [ ] Infrastructure must be defined in config files (NOT web UI only)

### Current Assets
- ✅ `docker-compose.yml` for local orchestration
- ✅ `Dockerfile` for each service
- ⚠️ No Terraform/Pulumi/platform-specific config yet

### Actions Needed
- [ ] Create platform-specific config (e.g., `render.yaml`, `fly.toml`, `railway.json`)
- [ ] Document CLI commands to reproduce deployment
- [ ] Ensure infrastructure is fully code-defined

### Evidence Required
```
infrastructure/
├── render.yaml OR fly.toml OR railway.json
├── deployment-commands.md (CLI sequence)
└── README section with deployment steps
```

---

## 3. Auto-Deploy from GitHub (1.5 pts)

### Requirements
- [ ] Push to repo triggers automatic deployment
- [ ] Document configuration in README
- [ ] Must be reproducible by authorized users

### Current State
- ✅ `publish-images.yml` pushes to GHCR on changes
- ❌ No automatic deployment trigger to IaaS/PaaS

### Actions Needed
- [ ] Connect GHCR images to IaaS/PaaS OR
- [ ] Configure direct GitHub → IaaS/PaaS deployment
- [ ] Add deployment status badge to README

### Evidence Required
```
.github/workflows/deploy.yml:
├── Deploy on push to main
├── Use platform CLI or API
└── Update README with live URL

README.md:
├── Deployment badge
├── Live URL
└── How to reproduce deployment
```

---

## 4. Observability Tools (1.5 pts)

### Requirements
- [ ] Real-time monitoring for anomaly detection
- [ ] Performance metrics capture
- [ ] Logs and traces collection
- [ ] Justify tool selection

### Suggested Tools

| Tool | Purpose | Integration |
|------|---------|-------------|
| **Prometheus + Grafana** | Metrics & dashboards | Self-hosted or managed |
| **Sentry** | Error tracking | pip install sentry-sdk |
| **Datadog** | Full observability | Free tier available |
| **Render/Railway built-in** | Platform logs | Native integration |
| **OpenTelemetry** | Traces | Standard protocol |

### Actions Needed
- [ ] Add logging middleware to FastAPI services
- [ ] Export metrics endpoint (`/metrics`)
- [ ] Configure alerting rules
- [ ] Set up dashboards

### Evidence Required
```
docs/AG_03_OBSERVABILITY.md:
├── Tool selection justification
├── Configuration steps
├── Dashboard screenshots
└── Alert rules defined

backend/{service}:
├── Add prometheus-fastapi-instrumentator OR
├── Add sentry-sdk initialization
└── Add structured logging
```

---

## 5. Correct Deployment Functioning (2.0 pts)

### Requirements
- [ ] Application functions correctly in the cloud (not just status "running")
- [ ] All endpoints work as expected
- [ ] Include live URL in delivery

### Validation Checklist
```
[ ] GET /api/health → 200 OK
[ ] GET /api/mangas → Returns manga list
[ ] GET /api/mangas/{id}/chapters → Returns chapters
[ ] POST /api/auth/dev/register → Creates user
[ ] POST /api/auth/dev/login → Returns tokens
[ ] GET /api/auth/me (with token) → Returns user info
[ ] Firebase connection works
[ ] S3 presigned URLs work
```

### Evidence Required
```
README.md:
├── Production URL: https://inku-api.{platform}.app
└── curl examples hitting live endpoints

docs/captures/:
├── live-health.png
├── live-mangas.png
└── live-auth.png
```

---

## 6. Performance Tests (2.0 pts)

### Requirements
- [ ] Stress tests to measure load/latency
- [ ] Document test methodology
- [ ] Analyze results

### Suggested Tools

| Tool | Purpose |
|------|---------|
| **k6** | Load testing, JavaScript scripts |
| **Locust** | Python-based load testing |
| **Apache Bench (ab)** | Simple HTTP benchmarking |
| **Vegeta** | HTTP load testing tool |

### Test Scenarios
1. **Baseline**: 10 concurrent users, 60 seconds
2. **Stress**: Ramp to 100 users, measure breaking point
3. **Endurance**: 50 users, 5 minutes

### Metrics to Capture
- Requests per second (RPS)
- Response time (p50, p95, p99)
- Error rate
- Resource utilization (if available)

### Evidence Required
```
tests/load/
├── k6-script.js OR locustfile.py
├── results/
│   ├── baseline-report.html
│   └── stress-report.html
└── README.md (how to run tests)

docs/AG_04_PERFORMANCE.md:
├── Methodology
├── Charts/graphs
├── Analysis
└── Recommendations
```

---

## Delivery Checklist

### README Updates
- [ ] Add deployment section
- [ ] Include live production URL
- [ ] Add CI/CD badges for deployment
- [ ] Document how to reproduce infrastructure

### Required Files
```
docs/
├── AG_02_IAAS_SELECTION.md
├── AG_03_OBSERVABILITY.md
├── AG_04_PERFORMANCE.md
└── captures/ (screenshots of deployed app)

infrastructure/
├── {platform}-config.{yaml|json|toml}
└── deployment-commands.md

.github/workflows/
└── deploy.yml (or update existing)
```

### Pull Request
- [ ] Submit to course repository with project link
- [ ] Ensure all evidence is linked from README
- [ ] URL is accessible during evaluation

---

## Quick Reference

| What | Where | Points |
|------|-------|--------|
| Why this platform? | `docs/AG_02_IAAS_SELECTION.md` | 1.5 |
| How to deploy? | `infrastructure/`, `README` | 1.5 |
| Auto-deploy? | `.github/workflows/deploy.yml` | 1.5 |
| Monitoring? | `docs/AG_03_OBSERVABILITY.md` | 1.5 |
| Does it work? | Live URL + screenshots | 2.0 |
| How fast is it? | `docs/AG_04_PERFORMANCE.md` | 2.0 |
