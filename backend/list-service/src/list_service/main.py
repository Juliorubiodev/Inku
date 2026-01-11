"""
List Service - Public Lists API

Allows authenticated users to create and manage public manga lists.
"""
from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
import os
import logging

from shared.auth import init_firebase, get_current_user, get_optional_user

from .models import (
    CreateListRequest,
    UpdateListRequest,
    AddItemRequest,
    ListResponse,
    ListsResponse,
    MessageResponse,
    UserListSummary,
)
from .repository import FirestoreListRepo

logger = logging.getLogger(__name__)

app = FastAPI(
    title="List Service",
    description="Public manga lists API",
    version="1.0.0",
)

# CORS configuration
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    try:
        init_firebase()
        logger.info("Firebase initialized for list-service")
    except Exception as e:
        logger.warning(f"Firebase init failed (may retry on first request): {e}")


# Dependency to get repository
def get_repo() -> FirestoreListRepo:
    return FirestoreListRepo()


# Health check
@app.get("/health", tags=["health"])
def health():
    return {"status": "ok", "service": "list-service"}


@app.get("/", tags=["root"])
def root():
    return {"message": "List Service API v1.0.0"}


# ============================================
# Public Endpoints (No Auth Required)
# ============================================

@app.get(
    "/api/lists/public",
    response_model=ListsResponse,
    tags=["lists"],
    summary="Get public lists",
)
def get_public_lists(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    repo: FirestoreListRepo = Depends(get_repo),
):
    """Get paginated list of all public lists."""
    lists, total = repo.get_public(page=page, page_size=page_size)
    return ListsResponse(
        lists=lists,
        total=total,
        page=page,
        page_size=page_size,
    )


# ============================================
# Authenticated Endpoints (MUST come before /{list_id})
# ============================================

@app.get(
    "/api/lists/me",
    response_model=ListsResponse,
    tags=["lists"],
    summary="Get my lists",
)
def get_my_lists(
    user: dict = Depends(get_current_user),
    repo: FirestoreListRepo = Depends(get_repo),
):
    """Get all lists owned by the current user."""
    lists = repo.get_by_owner(user["uid"])
    return ListsResponse(
        lists=lists,
        total=len(lists),
        page=1,
        page_size=len(lists),
    )


# ============================================
# Parameterized Routes (after specific routes)
# ============================================

@app.get(
    "/api/lists/{list_id}",
    response_model=ListResponse,
    tags=["lists"],
    summary="Get list by ID",
)
def get_list(
    list_id: str,
    repo: FirestoreListRepo = Depends(get_repo),
):
    """Get a specific list with all items."""
    lst = repo.get_by_id(list_id)
    if lst is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"List {list_id} not found",
        )
    return ListResponse(
        id=lst.id,
        name=lst.name,
        owner_uid=lst.owner_uid,
        owner_name=lst.owner_name,
        items=lst.items,
        item_count=len(lst.items),
        created_at=lst.created_at,
        updated_at=lst.updated_at,
    )


@app.post(
    "/api/lists",
    response_model=ListResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["lists"],
    summary="Create new list",
)
def create_list(
    request: CreateListRequest,
    user: dict = Depends(get_current_user),
    repo: FirestoreListRepo = Depends(get_repo),
):
    """Create a new list for the current user."""
    owner_name = user.get("name") or user.get("email") or "Unknown"
    lst = repo.create(name=request.name, owner_uid=user["uid"], owner_name=owner_name)
    logger.info(f"User {user['uid']} created list {lst.id}")
    return ListResponse(
        id=lst.id,
        name=lst.name,
        owner_uid=lst.owner_uid,
        owner_name=lst.owner_name,
        items=lst.items,
        item_count=len(lst.items),
        created_at=lst.created_at,
        updated_at=lst.updated_at,
    )


# ============================================
# Owner-Only Endpoints
# ============================================

def verify_owner(list_id: str, user_uid: str, repo: FirestoreListRepo):
    """Verify user is owner of the list, raise 403 if not."""
    lst = repo.get_by_id(list_id)
    if lst is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"List {list_id} not found",
        )
    if lst.owner_uid != user_uid:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to modify this list",
        )
    return lst


@app.post(
    "/api/lists/{list_id}/items",
    response_model=ListResponse,
    tags=["lists"],
    summary="Add manga to list",
)
def add_item_to_list(
    list_id: str,
    request: AddItemRequest,
    user: dict = Depends(get_current_user),
    repo: FirestoreListRepo = Depends(get_repo),
):
    """Add a manga to a list. Only the owner can add items."""
    verify_owner(list_id, user["uid"], repo)
    
    lst = repo.add_item(list_id, request.manga_id)
    if lst is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"List {list_id} not found",
        )
    
    logger.info(f"User {user['uid']} added manga {request.manga_id} to list {list_id}")
    return ListResponse(
        id=lst.id,
        name=lst.name,
        owner_uid=lst.owner_uid,
        owner_name=lst.owner_name,
        items=lst.items,
        item_count=len(lst.items),
        created_at=lst.created_at,
        updated_at=lst.updated_at,
    )


@app.delete(
    "/api/lists/{list_id}/items/{manga_id}",
    response_model=ListResponse,
    tags=["lists"],
    summary="Remove manga from list",
)
def remove_item_from_list(
    list_id: str,
    manga_id: str,
    user: dict = Depends(get_current_user),
    repo: FirestoreListRepo = Depends(get_repo),
):
    """Remove a manga from a list. Only the owner can remove items."""
    verify_owner(list_id, user["uid"], repo)
    
    lst = repo.remove_item(list_id, manga_id)
    if lst is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"List {list_id} not found",
        )
    
    logger.info(f"User {user['uid']} removed manga {manga_id} from list {list_id}")
    return ListResponse(
        id=lst.id,
        name=lst.name,
        owner_uid=lst.owner_uid,
        owner_name=lst.owner_name,
        items=lst.items,
        item_count=len(lst.items),
        created_at=lst.created_at,
        updated_at=lst.updated_at,
    )


@app.patch(
    "/api/lists/{list_id}",
    response_model=ListResponse,
    tags=["lists"],
    summary="Update list",
)
def update_list(
    list_id: str,
    request: UpdateListRequest,
    user: dict = Depends(get_current_user),
    repo: FirestoreListRepo = Depends(get_repo),
):
    """Rename a list. Only the owner can rename."""
    verify_owner(list_id, user["uid"], repo)
    
    lst = repo.update_name(list_id, request.name)
    if lst is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"List {list_id} not found",
        )
    
    logger.info(f"User {user['uid']} renamed list {list_id} to '{request.name}'")
    return ListResponse(
        id=lst.id,
        name=lst.name,
        owner_uid=lst.owner_uid,
        owner_name=lst.owner_name,
        items=lst.items,
        item_count=len(lst.items),
        created_at=lst.created_at,
        updated_at=lst.updated_at,
    )


@app.delete(
    "/api/lists/{list_id}",
    response_model=MessageResponse,
    tags=["lists"],
    summary="Delete list",
)
def delete_list(
    list_id: str,
    user: dict = Depends(get_current_user),
    repo: FirestoreListRepo = Depends(get_repo),
):
    """Delete a list. Only the owner can delete."""
    verify_owner(list_id, user["uid"], repo)
    
    repo.delete(list_id)
    logger.info(f"User {user['uid']} deleted list {list_id}")
    return MessageResponse(message=f"List {list_id} deleted successfully", id=list_id)
