"""
Auth service dependencies - uses shared auth module.
"""
from shared.auth import (
    init_firebase,
    verify_firebase_token,
    get_current_user,
    get_optional_user,
    UserClaims,
)

# Re-export for backwards compatibility
__all__ = [
    "init_firebase",
    "verify_firebase_token", 
    "get_current_user",
    "get_optional_user",
    "UserClaims",
]
