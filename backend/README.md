# Inku Backend

Multi-service backend for the Inku manga platform.

## Services

| Service | Port | Description |
|---------|------|-------------|
| manga-service | 8001 | Manga catalog, chapters, S3 presigned URLs |
| auth-service | 8003 | User authentication via Firebase |
| list-service | 8002 | Public user lists (in development) |

## Quick Start

### Prerequisites

- Docker & Docker Compose
- Firebase project with service account
- AWS S3 bucket (optional, for file storage)

### 1. Setup Secrets

Create the `secrets/` directory with your Firebase service account:

```bash
mkdir -p secrets
# Copy your Firebase service account JSON to:
# secrets/firebase-service-account.json
```

> ⚠️ **Never commit secrets!** The `secrets/` directory is gitignored.

### 2. Configure Environment Variables

Each service needs its `.env` file. Copy the examples:

```bash
# manga-service
cp manga-service/.env.example manga-service/.env

# auth-service
cp auth-service/.env.example auth-service/.env

# list-service (minimal config)
# Already has default .env
```

### Required Variables

#### manga-service/.env
```
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_SERVICE_ACCOUNT_FILE=/secrets/firebase-service-account.json
AWS_REGION=eu-north-1
AWS_S3_BUCKET=your-bucket-name
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
API_PREFIX=/api
DEBUG=true
```

#### auth-service/.env
```
FIREBASE_SERVICE_ACCOUNT_PATH=/secrets/firebase-service-account.json
FIREBASE_WEB_API_KEY=your-firebase-web-api-key
API_PREFIX=/api
```

### 3. Run with Docker Compose

```bash
cd backend
docker compose up --build
```

### 4. Verify Health

```bash
# manga-service
curl http://localhost:8001/api/health

# auth-service
curl http://localhost:8003/health

# list-service
curl http://localhost:8002/health
```

All should return: `{"status": "ok", "service": "..."}`

## Development (Without Docker)

### manga-service

```bash
cd manga-service
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python -m uvicorn inku_api.main:app --app-dir src --reload --port 8001
```

### auth-service

```bash
cd auth-service
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8003
```

### list-service

```bash
cd list-service
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn list_service.main:app --app-dir src --reload --port 8002
```

## API Endpoints

### manga-service (port 8001)

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | /api/health | ❌ | Health check |
| GET | /api/mangas | ❌ | List all mangas |
| GET | /api/mangas/{id}/chapters | ❌ | List chapters |
| POST | /api/mangas/{id}/episodes | ❌ | Create episode (upload) |

### auth-service (port 8003)

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | /health | ❌ | Health check |
| GET | /api/auth/me | ✅ | Get current user |
| POST | /api/auth/verify | ✅ | Verify token |
| POST | /api/auth/dev/register | ❌ | Register user |
| POST | /api/auth/dev/login | ❌ | Login user |

### list-service (port 8002)

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | /health | ❌ | Health check |
| GET | /api/lists | ❌ | Get all lists |
| POST | /api/lists | ❌ | Create list (placeholder) |

## CORS Configuration

All services accept CORS from:
- `http://localhost:3000` (React dev server)
- `http://localhost:5173` (Vite dev server)

Custom origins can be set via `CORS_ORIGINS` environment variable.

## Architecture

```
backend/
├── docker-compose.yml      # Orchestration
├── secrets/                # Firebase credentials (gitignored)
├── manga-service/          # Catalog & S3
│   ├── Dockerfile
│   ├── requirements.txt
│   └── src/inku_api/
├── auth-service/           # Authentication
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
└── list-service/           # User lists
    ├── Dockerfile
    ├── requirements.txt
    └── src/list_service/
```
