# Deployment Instructions

## Prerequisites

1. GitHub repository with push access
2. Render account (free tier: https://render.com)
3. Firebase project configured
4. AWS S3 bucket for manga storage

## Setup Steps

### 1. Create Render Account

1. Go to https://render.com
2. Sign up with GitHub
3. Authorize Render to access your repositories

### 2. Deploy via Blueprint

The easiest way to deploy is using the Render Blueprint:

```bash
# Click this button in your README or visit:
https://render.com/deploy?repo=https://github.com/YOUR_USERNAME/Inku
```

Or manually:

1. Go to Render Dashboard → Blueprints
2. Click "New Blueprint Instance"
3. Connect your Inku repository
4. Render will read `render.yaml` and create all services

### 3. Configure Environment Variables

After services are created, set secret variables in Render Dashboard:

#### Manga Service
```
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_S3_BUCKET=your-bucket
```

#### Frontend
```
VITE_FIREBASE_API_KEY=your-firebase-key
VITE_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your-project-id
VITE_FIREBASE_APP_ID=your-app-id
```

### 4. Upload Firebase Service Account

For backend services to access Firestore:

1. Download service account JSON from Firebase Console
2. In Render, go to each service → Environment
3. Add as secret file OR encode as base64 environment variable

### 5. GitHub Actions Setup (Optional)

For automatic deploys via GitHub Actions:

1. Go to Render Dashboard → Account Settings → API Keys
2. Create new API key
3. Add to GitHub repository secrets:
   - `RENDER_API_KEY`: Your Render API key
   - `RENDER_FRONTEND_SERVICE_ID`: srv-xxx (from service URL)
   - `RENDER_MANGA_SERVICE_ID`: srv-xxx
   - `RENDER_AUTH_SERVICE_ID`: srv-xxx
   - `RENDER_LIST_SERVICE_ID`: srv-xxx

## CLI Deployment (Alternative)

```bash
# Install Render CLI
npm install -g @render-oss/render-cli

# Login
render login

# Deploy from render.yaml
render blueprint apply
```

## Verification

After deployment, verify each service:

```bash
# Frontend
curl https://inku-frontend.onrender.com

# Manga Service
curl https://inku-manga-service.onrender.com/api/health

# Auth Service
curl https://inku-auth-service.onrender.com/health

# List Service
curl https://inku-list-service.onrender.com/health
```

## URLs (Production)

| Service | URL |
|---------|-----|
| Frontend | https://inku-frontend.onrender.com |
| Manga API | https://inku-manga-service.onrender.com |
| Auth API | https://inku-auth-service.onrender.com |
| List API | https://inku-list-service.onrender.com |

## Troubleshooting

### Service won't start

1. Check Render logs for errors
2. Verify all environment variables are set
3. Ensure Dockerfile builds locally first

### 502 Bad Gateway

Services on free tier sleep after 15 min. First request may take 30-60 seconds.

### Firebase connection fails

1. Verify service account file is accessible
2. Check path in environment variables
3. Ensure Firestore rules allow access

### CORS errors

Update `CORS_ORIGINS` environment variable to include your frontend URL.
