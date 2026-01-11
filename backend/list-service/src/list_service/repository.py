"""
Firestore repository for lists.
"""
from datetime import datetime
from typing import List, Optional, Tuple
import logging

from firebase_admin import firestore as admin_firestore
from google.cloud.firestore_v1 import DocumentSnapshot

from .models import UserList, UserListSummary, ListItem

logger = logging.getLogger(__name__)

COLLECTION = "lists"


class FirestoreListRepo:
    """Repository for user lists stored in Firestore."""
    
    def __init__(self, db=None):
        if db is None:
            db = admin_firestore.client()
        self._db = db
        self._collection = self._db.collection(COLLECTION)
    
    def _doc_to_list(self, doc: DocumentSnapshot) -> Optional[UserList]:
        """Convert Firestore document to UserList model."""
        if not doc.exists:
            return None
        
        data = doc.to_dict()
        items = []
        for item in data.get("items", []):
            items.append(ListItem(
                manga_id=item.get("manga_id", ""),
                added_at=item.get("added_at", datetime.utcnow()),
            ))
        
        return UserList(
            id=doc.id,
            name=data.get("name", ""),
            owner_uid=data.get("owner_uid", ""),
            owner_name=data.get("owner_name"),
            items=items,
            created_at=data.get("created_at", datetime.utcnow()),
            updated_at=data.get("updated_at", datetime.utcnow()),
        )
    
    def _doc_to_summary(self, doc: DocumentSnapshot) -> Optional[UserListSummary]:
        """Convert Firestore document to UserListSummary."""
        if not doc.exists:
            return None
        
        data = doc.to_dict()
        return UserListSummary(
            id=doc.id,
            name=data.get("name", ""),
            owner_uid=data.get("owner_uid", ""),
            owner_name=data.get("owner_name"),
            item_count=len(data.get("items", [])),
            created_at=data.get("created_at", datetime.utcnow()),
            updated_at=data.get("updated_at", datetime.utcnow()),
        )
    
    # CRUD Operations
    
    def create(self, name: str, owner_uid: str, owner_name: str = None) -> UserList:
        """Create a new list."""
        now = datetime.utcnow()
        data = {
            "name": name,
            "owner_uid": owner_uid,
            "owner_name": owner_name,
            "items": [],
            "created_at": now,
            "updated_at": now,
        }
        doc_ref = self._collection.document()
        doc_ref.set(data)
        
        logger.info(f"Created list {doc_ref.id} for user {owner_uid}")
        return UserList(id=doc_ref.id, **data)
    
    def get_by_id(self, list_id: str) -> Optional[UserList]:
        """Get a list by ID."""
        doc = self._collection.document(list_id).get()
        return self._doc_to_list(doc)
    
    def get_by_owner(self, owner_uid: str) -> List[UserListSummary]:
        """Get all lists owned by a user."""
        docs = self._collection.where("owner_uid", "==", owner_uid).stream()
        return [self._doc_to_summary(doc) for doc in docs if doc.exists]
    
    def get_public(
        self, 
        page: int = 1, 
        page_size: int = 20
    ) -> Tuple[List[UserListSummary], int]:
        """Get paginated public lists."""
        # Get total count (inefficient but Firestore doesn't have count)
        all_docs = list(self._collection.stream())
        total = len(all_docs)
        
        # Get paginated results
        offset = (page - 1) * page_size
        docs = (
            self._collection
            .order_by("created_at", direction=admin_firestore.Query.DESCENDING)
            .offset(offset)
            .limit(page_size)
            .stream()
        )
        
        lists = [self._doc_to_summary(doc) for doc in docs if doc.exists]
        return lists, total
    
    def update_name(self, list_id: str, name: str) -> Optional[UserList]:
        """Update list name."""
        doc_ref = self._collection.document(list_id)
        doc_ref.update({
            "name": name,
            "updated_at": datetime.utcnow(),
        })
        return self.get_by_id(list_id)
    
    def delete(self, list_id: str) -> bool:
        """Delete a list."""
        doc_ref = self._collection.document(list_id)
        doc_ref.delete()
        logger.info(f"Deleted list {list_id}")
        return True
    
    # Item operations
    
    def add_item(self, list_id: str, manga_id: str) -> Optional[UserList]:
        """Add a manga to a list."""
        doc_ref = self._collection.document(list_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            return None
        
        data = doc.to_dict()
        items = data.get("items", [])
        
        # Check if already exists
        if any(item.get("manga_id") == manga_id for item in items):
            return self.get_by_id(list_id)  # Already exists, return current
        
        items.append({
            "manga_id": manga_id,
            "added_at": datetime.utcnow(),
        })
        
        doc_ref.update({
            "items": items,
            "updated_at": datetime.utcnow(),
        })
        
        logger.info(f"Added manga {manga_id} to list {list_id}")
        return self.get_by_id(list_id)
    
    def remove_item(self, list_id: str, manga_id: str) -> Optional[UserList]:
        """Remove a manga from a list."""
        doc_ref = self._collection.document(list_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            return None
        
        data = doc.to_dict()
        items = [
            item for item in data.get("items", [])
            if item.get("manga_id") != manga_id
        ]
        
        doc_ref.update({
            "items": items,
            "updated_at": datetime.utcnow(),
        })
        
        logger.info(f"Removed manga {manga_id} from list {list_id}")
        return self.get_by_id(list_id)
    
    def is_owner(self, list_id: str, user_uid: str) -> bool:
        """Check if user is owner of list."""
        lst = self.get_by_id(list_id)
        if lst is None:
            return False
        return lst.owner_uid == user_uid
