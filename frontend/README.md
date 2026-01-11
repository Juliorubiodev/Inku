# Inku Web Frontend

React web frontend for the Inku manga reader.

## Quick Start

### Prerequisites

- Node.js 18+
- Backend services running (see `../backend/README.md`)

### Development Setup

```bash
# 1. Install dependencies
npm install

# 2. Create environment file
cp .env.example .env.local

# 3. Configure Firebase credentials in .env.local
#    Get these from Firebase Console > Project Settings > Your Apps > Web App

# 4. Start dev server
npm run dev

# 5. Open browser
open http://localhost:5173
```

> ⚠️ **Important**: Vite does NOT hot-reload `.env` changes. Restart `npm run dev` after editing.

### Production-like Local Setup

For testing with Nginx reverse proxy (same-origin, no CORS):

```bash
# From project root
docker compose -f docker-compose.prod.yml up --build

# Access at http://localhost
```

## Environment Variables

### Required for Dev (.env.local)

```bash
# API URLs (pointing to local backend)
VITE_API_BASE_URL=http://localhost:8001
VITE_AUTH_API_URL=http://localhost:8003
VITE_LIST_API_URL=http://localhost:8002

# Firebase (REQUIRED - get from Firebase Console)
VITE_FIREBASE_API_KEY=AIzaSy...
VITE_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your-project-id
VITE_FIREBASE_STORAGE_BUCKET=your-project.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=123456789012
VITE_FIREBASE_APP_ID=1:123456789012:web:abcdef123456
```

### For Production (.env.production)

```bash
# Empty = same-origin (Nginx proxies to backend)
VITE_API_BASE_URL=
VITE_AUTH_API_URL=
VITE_LIST_API_URL=

# Firebase (same as dev)
VITE_FIREBASE_API_KEY=...
```

## Features

| Feature | Route | Auth |
|---------|-------|------|
| 📚 Catalog | `/` | No |
| 📖 Manga Detail | `/manga/:id` | No |
| 📄 Reader | `/read/:mangaId/:chapterId` | No |
| 📋 Public Lists | `/lists` | No |
| 🔐 Login | `/login` | No |
| ✍️ Register | `/register` | No |
| 👤 Profile | `/profile` | Yes |
| 📝 My Lists | `/my-lists` | Yes |
| ⬆️ Upload | `/upload` | Yes |

## Project Structure

```
src/
├── config/
│   └── env.ts          # Environment validation
├── context/
│   └── AuthContext.tsx # Auth state
├── lib/
│   ├── firebase.ts     # Firebase init
│   └── api.ts          # API client
├── components/
│   └── Layout.tsx      # Main layout
├── pages/
│   ├── Catalog.tsx
│   ├── Reader.tsx
│   ├── Login.tsx
│   └── ...
└── types/
    └── index.ts
```

## Troubleshooting

### "API Key inválida" error

1. Check `.env.local` exists with valid `VITE_FIREBASE_*` values
2. **Restart** `npm run dev` (Vite doesn't reload .env changes)
3. Open browser DevTools > Console to see config status

### "AccessDenied" in PDF Reader

The reader requests presigned URLs from the backend. If you see S3 errors:
- Ensure backend is running with valid AWS credentials
- Check `manga-service` logs for S3 errors

### Blank page

1. Open DevTools > Console for errors
2. Check environment config status (logged on load)
3. Verify all TypeScript imports use `import type` for types

## Scripts

```bash
npm run dev      # Start dev server
npm run build    # Build for production
npm run preview  # Preview production build
npm run lint     # Run ESLint
```
