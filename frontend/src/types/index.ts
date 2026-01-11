// Manga types
export interface Manga {
    id: string;
    title: string;
    description: string;
    cover_path: string;
    cover_url?: string;
    recommended?: string;
    tags: string[];
}

export interface Chapter {
    id: string;
    manga_id: string;
    number: number;
    title: string;
    pdf_path?: string;
    thumb_path?: string;
    read_url?: string;
}

// List types
export interface ListItem {
    manga_id: string;
    added_at: string;
}

export interface UserList {
    id: string;
    name: string;
    owner_uid: string;
    owner_name?: string;
    items: ListItem[];
    item_count: number;
    created_at: string;
    updated_at: string;
}

export interface ListSummary {
    id: string;
    name: string;
    owner_uid: string;
    owner_name?: string;
    item_count: number;
    created_at: string;
    updated_at: string;
}

// Upload types
export interface PresignResponse {
    manga_id: string;
    chapter_number: number;
    s3_key: string;
    upload_url: string;
    thumb_key: string;
    thumb_upload_url: string;
    expires_in: number;
}

// Auth types
export interface AuthUser {
    uid: string;
    email: string | null;
    displayName: string | null;
    photoURL: string | null;
}
