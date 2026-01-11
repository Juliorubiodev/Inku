"""
Firebase initialization - uses shared auth module.
Provides compatibility layer with existing code.
"""
from shared.auth import init_firebase as _shared_init

_initialized = False

def init_firebase() -> None:
    """Initialize Firebase Admin SDK (singleton, uses shared module)."""
    global _initialized
    if _initialized:
        return
    
    _shared_init()
    _initialized = True
