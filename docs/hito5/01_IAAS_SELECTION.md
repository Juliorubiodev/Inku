# IaaS/PaaS Selection for Inku

## Selection Criteria

1. **Free tier availability** - Essential for academic project
2. **EU region deployment** - Legal requirement (GDPR)
3. **GitHub integration** - Automatic deployment on push
4. **Docker support** - Required for our containerized services
5. **Configuration-as-code** - Reproducible infrastructure
6. **Multiple services support** - 3 microservices + frontend

## Options Evaluated

| Platform | Free Tier | EU Region | GitHub Deploy | Docker | Config as Code | Multi-service |
|----------|-----------|-----------|---------------|--------|----------------|---------------|
| **Render** | ✅ 750h/month | ✅ Frankfurt | ✅ Native | ✅ | ✅ render.yaml | ✅ |
| **Railway** | ⚠️ $5 credit | ✅ | ✅ | ✅ | ⚠️ Limited | ✅ |
| **Fly.io** | ✅ 3 VMs | ✅ AMS/FRA | ⚠️ CLI only | ✅ | ✅ fly.toml | ✅ |
| **Google Cloud Run** | ⚠️ Complex | ✅ | ⚠️ Needs GCP | ✅ | ⚠️ | ✅ |
| **Vercel** | ✅ | ✅ | ✅ | ❌ | ⚠️ | ❌ Frontend only |
| **AWS App Runner** | ❌ | ✅ | ⚠️ | ✅ | ⚠️ | ✅ |

## Detailed Analysis

### Render (Selected ✅)

**Pros:**
- 750 free hours/month (enough for 3 services)
- Native GitHub integration with auto-deploy
- `render.yaml` for infrastructure-as-code
- Frankfurt region (EU compliant)
- Built-in health checks and logging
- Automatic HTTPS with custom domains
- Private networking between services

**Cons:**
- Services sleep after 15 min inactivity (free tier)
- Cold starts on first request
- Limited to 512MB RAM on free tier

### Railway (Rejected)

**Pros:**
- Easy Docker deployment
- Good DX

**Cons:**
- Only $5 credit, then paid
- Limited config-as-code options
- No true free tier for production

### Fly.io (Considered)

**Pros:**
- Edge deployment, low latency
- Good Docker support

**Cons:**
- Complex configuration (requires Fly CLI)
- Less intuitive for beginners
- Credit card required even for free tier

### Google Cloud Run (Rejected)

**Pros:**
- Serverless, scales to zero
- Good integration with Firebase

**Cons:**
- Requires Google Cloud account setup
- Complex IAM configuration
- No simple GitHub deploy without Cloud Build

## Final Decision: Render

**Justification:**

Render is the optimal choice for Inku because:

1. **Cost**: 750 free hours/month is sufficient for 3 microservices within academic requirements
2. **Compliance**: Frankfurt region meets EU GDPR requirements
3. **Reproducibility**: `render.yaml` allows anyone to replicate the infrastructure
4. **Simplicity**: Direct GitHub integration with zero configuration needed for auto-deploy
5. **Observability**: Built-in logs, metrics, and health check monitoring
6. **Docker-native**: Our existing Dockerfiles work without modification

The main trade-off (sleep on inactivity) is acceptable for a course project where continuous uptime is not critical.

## References

- [Render Documentation](https://render.com/docs)
- [Render Blueprint Spec](https://render.com/docs/blueprint-spec)
- [Render EU Region](https://render.com/docs/regions)
