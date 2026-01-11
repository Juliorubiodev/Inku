"""
Pydantic models for List Service.
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class ListItem(BaseModel):
    """A manga item in a list."""
    manga_id: str = Field(..., description="ID from manga catalog")
    added_at: datetime = Field(default_factory=datetime.utcnow)


class UserList(BaseModel):
    """A user's public list of mangas."""
    id: str = Field(..., description="Firestore document ID")
    name: str = Field(..., min_length=1, max_length=100)
    owner_uid: str = Field(..., description="Firebase UID of owner")
    owner_name: Optional[str] = None
    items: List[ListItem] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class UserListSummary(BaseModel):
    """Summary view of a list (without items)."""
    id: str
    name: str
    owner_uid: str
    owner_name: Optional[str] = None
    item_count: int
    created_at: datetime
    updated_at: datetime


# Request/Response models

class CreateListRequest(BaseModel):
    """Request body for creating a list."""
    name: str = Field(..., min_length=1, max_length=100)


class UpdateListRequest(BaseModel):
    """Request body for updating a list."""
    name: str = Field(..., min_length=1, max_length=100)


class AddItemRequest(BaseModel):
    """Request body for adding a manga to a list."""
    manga_id: str = Field(..., min_length=1)


class ListResponse(BaseModel):
    """Response for a single list."""
    id: str
    name: str
    owner_uid: str
    owner_name: Optional[str] = None
    items: List[ListItem]
    item_count: int
    created_at: datetime
    updated_at: datetime


class ListsResponse(BaseModel):
    """Response for list of lists."""
    lists: List[UserListSummary]
    total: int
    page: int = 1
    page_size: int = 20


class MessageResponse(BaseModel):
    """Generic message response."""
    message: str
    id: Optional[str] = None
