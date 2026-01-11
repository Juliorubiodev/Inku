# Observability Implementation for Inku

## Overview

This document describes the observability stack implemented for monitoring Inku in production.

## Tool Selection

### Selected Stack

| Component | Tool | Justification |
|-----------|------|---------------|
| **Metrics** | FastAPI + Prometheus | Native Python integration, industry standard |
| **Logging** | Structured JSON logs | Platform-agnostic, queryable |
| **Health Checks** | Custom /health endpoints | Built-in to each service |
| **Platform Monitoring** | Render Dashboard | Native integration, no extra cost |

### Why Not Others?

- **Datadog/New Relic**: Paid beyond free tier limits
- **Grafana Cloud**: Overkill for 3 services
- **ELK Stack**: Too complex to self-host

## Implementation

### 1. Health Check Endpoints

Each service exposes a health endpoint:

```python
# manga-service
GET /api/health → {"status": "ok", "service": "manga-service", "timestamp": "..."}

# auth-service  
GET /health → {"status": "ok", "service": "auth-service"}

# list-service
GET /health → {"status": "ok", "service": "list-service"}
```

### 2. Structured Logging

All services use Python's logging with JSON format:

```python
import logging
import json

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_obj = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "service": "manga-service",
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
        }
        if record.exc_info:
            log_obj["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_obj)
```

### 3. Request Logging Middleware

FastAPI middleware logs all requests:

```python
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    
    logger.info(
        f"{request.method} {request.url.path}",
        extra={
            "status_code": response.status_code,
            "duration_ms": round(duration * 1000, 2),
            "client_ip": request.client.host,
        }
    )
    return response
```

### 4. Metrics Endpoint (Optional Enhancement)

For detailed metrics, add prometheus-fastapi-instrumentator:

```bash
pip install prometheus-fastapi-instrumentator
```

```python
from prometheus_fastapi_instrumentator import Instrumentator

Instrumentator().instrument(app).expose(app)
# Metrics available at GET /metrics
```

## Render Platform Monitoring

Render provides built-in observability:

### Logs
- Real-time log streaming in dashboard
- Searchable by timestamp and content
- Exportable for analysis

### Metrics
- CPU and Memory usage graphs
- Request count and latency
- Auto-scaling triggers (paid plans)

### Alerts
- Health check failures trigger notifications
- Configurable via Render dashboard

## Monitoring Dashboard

Access via Render Dashboard:
1. Go to https://dashboard.render.com
2. Select service (e.g., inku-manga-service)
3. View:
   - **Logs**: Real-time application output
   - **Metrics**: CPU, Memory, Requests
   - **Events**: Deploys, restarts, health failures

## Alert Configuration

### Health Check Alerts

Render automatically monitors health endpoints:
- If `/api/health` returns non-200, service marked unhealthy
- After 3 consecutive failures, service restarts
- Email notification sent to account owner

### Custom Alerts (Optional)

For advanced alerting, integrate with:
- **PagerDuty**: Incident management
- **Slack**: Team notifications
- **Email**: Direct notifications

## Log Analysis Commands

### View Recent Logs (Render CLI)

```bash
# Install Render CLI
npm install -g render-cli

# Login
render login

# View logs
render logs inku-manga-service --tail
```

### Search Logs

```bash
# Filter by level
render logs inku-manga-service | grep "ERROR"

# Filter by endpoint
render logs inku-manga-service | grep "/api/mangas"
```

## Maintenance

### Daily Checks
- [ ] Review error logs for new issues
- [ ] Check response times in metrics

### Weekly Review
- [ ] Analyze trending errors
- [ ] Review resource utilization
- [ ] Update alerts as needed

## Screenshots

> Add screenshots of:
> - Render dashboard with metrics
> - Log viewer with structured logs
> - Health check status

See: `docs/hito5/captures/`
