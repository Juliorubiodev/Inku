"""
Shared Firebase Authentication Module

Provides consistent Firebase token validation across all backend services.
Usage:
    from shared.auth import init_firebase, get_current_user

Convention:
    - Header: Authorization: Bearer <Firebase idToken>
    - 401: Missing or invalid token
    - 403: Token valid but insufficient permissions
"""
from __future__ import annotations
import os
import logging
from typing import Optional, Dict, Any

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

import firebase_admin
from firebase_admin import credentials, auth as firebase_auth

logger = logging.getLogger(__name__)

# Global Firebase app instance
_firebase_app: Optional[firebase_admin.App] = None

# Bearer token extractor
bearer_scheme = HTTPBearer(auto_error=False)


def init_firebase(
    cred_path: Optional[str] = None,
    project_id: Optional[str] = None,
) -> firebase_admin.App:
    """
    Initialize Firebase Admin SDK (singleton pattern).
    
    Args:
        cred_path: Path to service account JSON. Falls back to env vars:
                   FIREBASE_SERVICE_ACCOUNT_PATH, FIREBASE_SERVICE_ACCOUNT_FILE,
                   GOOGLE_APPLICATION_CREDENTIALS
        project_id: Firebase project ID (optional, usually in cred file)
    
    Returns:
        Firebase App instance
    """
    global _firebase_app
    
    if _firebase_app is not None:
        return _firebase_app
    
    # Find credential path from multiple sources
    if cred_path is None:
        cred_path = (
            os.getenv("FIREBASE_SERVICE_ACCOUNT_PATH") or
            os.getenv("FIREBASE_SERVICE_ACCOUNT_FILE") or
            os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        )
    
    if not cred_path:
        raise ValueError(
            "Firebase credentials not found. Set FIREBASE_SERVICE_ACCOUNT_PATH "
            "or GOOGLE_APPLICATION_CREDENTIALS environment variable."
        )
    
    if not os.path.exists(cred_path):
        raise FileNotFoundError(f"Firebase credentials file not found: {cred_path}")
    
    try:
        cred = credentials.Certificate(cred_path)
        options = {"projectId": project_id} if project_id else {}
        _firebase_app = firebase_admin.initialize_app(cred, options)
        logger.info("Firebase Admin SDK initialized successfully")
        return _firebase_app
    except Exception as e:
        logger.error(f"Failed to initialize Firebase: {e}")
        raise


def verify_firebase_token(
    token: str,
    check_revoked: bool = False,
) -> Dict[str, Any]:
    """
    Verify a Firebase ID token.
    
    Args:
        token: The Firebase ID token to verify
        check_revoked: Whether to check if token has been revoked
    
    Returns:
        Decoded token claims (uid, email, etc.)
    
    Raises:
        HTTPException: 401 if token is invalid or expired
    """
    if _firebase_app is None:
        init_firebase()
    
    try:
        decoded = firebase_auth.verify_id_token(token, check_revoked=check_revoked)
        return decoded
    except firebase_auth.RevokedIdTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except firebase_auth.ExpiredIdTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except firebase_auth.InvalidIdTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        logger.error(f"Token verification failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token verification failed",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
) -> Dict[str, Any]:
    """
    FastAPI dependency to get the current authenticated user.
    
    Usage:
        @router.get("/protected")
        def protected_endpoint(user: dict = Depends(get_current_user)):
            return {"uid": user["uid"]}
    
    Returns:
        Decoded Firebase token claims containing:
        - uid: User's Firebase UID
        - email: User's email (if available)
        - email_verified: Whether email is verified
        - name: Display name (if available)
        - picture: Profile picture URL (if available)
        - ... other custom claims
    
    Raises:
        HTTPException 401: Missing or invalid Authorization header
    """
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header. Use: Authorization: Bearer <token>",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication scheme. Use: Bearer <token>",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return verify_firebase_token(credentials.credentials)


def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
) -> Optional[Dict[str, Any]]:
    """
    FastAPI dependency for optional authentication.
    Returns None if no token provided, user claims if valid token.
    
    Usage:
        @router.get("/items")
        def list_items(user: Optional[dict] = Depends(get_optional_user)):
            if user:
                # Show personalized content
            else:
                # Show public content
    """
    if credentials is None:
        return None
    
    if credentials.scheme.lower() != "bearer":
        return None
    
    try:
        return verify_firebase_token(credentials.credentials)
    except HTTPException:
        return None


# Convenience type alias
UserClaims = Dict[str, Any]
