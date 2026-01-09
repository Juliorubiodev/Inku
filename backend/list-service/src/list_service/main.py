from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="List Service", version="0.1.0")

# CORS configuration
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", tags=["health"])
def health():
    return {"status": "ok", "service": "list-service"}

@app.get("/", tags=["root"])
def root():
    return {"message": "List Service is running!"}

# Placeholder endpoints for future implementation
@app.get("/api/lists", tags=["lists"])
def get_lists():
    """Get all public lists (placeholder)"""
    return {"lists": []}

@app.post("/api/lists", tags=["lists"])
def create_list():
    """Create a new list (placeholder)"""
    return {"message": "Not implemented yet"}
