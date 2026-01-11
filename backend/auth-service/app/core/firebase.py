"""
Firebase initialization - uses shared auth module.
"""
from shared.auth import init_firebase, verify_firebase_token

# Re-export for backwards compatibility
__all__ = ["init_firebase", "verify_firebase_token"]
