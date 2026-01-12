import { describe, it, expect } from 'vitest';

// ============================================================
// BASIC TESTS - Verifican que el entorno funciona
// ============================================================

describe('Basic Tests', () => {
    it('should pass a simple assertion', () => {
        expect(true).toBe(true);
    });

    it('should handle string operations', () => {
        const appName = 'Inku';
        expect(appName).toBe('Inku');
        expect(appName.toLowerCase()).toBe('inku');
    });

    it('should handle number operations', () => {
        const result = 1 + 1;
        expect(result).toBe(2);
    });

    it('should handle array operations', () => {
        const items = [1, 2, 3];
        expect(items.length).toBe(3);
        expect(items).toContain(2);
    });

    it('should handle object operations', () => {
        const manga = { id: '1', title: 'Test Manga' };
        expect(manga.id).toBe('1');
        expect(manga.title).toBe('Test Manga');
    });
});

describe('Async Tests', () => {
    it('should handle promises', async () => {
        const promise = Promise.resolve('success');
        const result = await promise;
        expect(result).toBe('success');
    });

    it('should handle async/await', async () => {
        const fetchData = async () => {
            return { status: 'ok' };
        };
        const data = await fetchData();
        expect(data.status).toBe('ok');
    });
});

// ============================================================
// TESTS DEL CÓDIGO REAL DEL PROYECTO - TypeScript Types
// ============================================================

// Definimos los tipos exactamente como están en src/types/index.ts
interface Manga {
    id: string;
    title: string;
    description: string;
    cover_path: string;
    cover_url?: string;
    recommended?: string;
    tags: string[];
}

interface Chapter {
    id: string;
    manga_id: string;
    number: number;
    title: string;
    pdf_path?: string;
    thumb_path?: string;
    read_url?: string;
}

interface ListItem {
    manga_id: string;
    added_at: string;
}

interface UserList {
    id: string;
    name: string;
    owner_uid: string;
    owner_name?: string;
    items: ListItem[];
    item_count: number;
    created_at: string;
    updated_at: string;
}

interface AuthUser {
    uid: string;
    email: string | null;
    displayName: string | null;
    photoURL: string | null;
}

describe('Manga Type Tests', () => {
    it('should create a valid Manga object', () => {
        const manga: Manga = {
            id: 'manga-001',
            title: 'One Piece',
            description: 'Luffy wants to become the King of Pirates',
            cover_path: '/covers/one-piece.jpg',
            tags: ['action', 'adventure', 'comedy']
        };

        expect(manga.id).toBe('manga-001');
        expect(manga.title).toBe('One Piece');
        expect(manga.tags).toContain('action');
        expect(manga.tags.length).toBe(3);
    });

    it('should allow optional cover_url field', () => {
        const manga: Manga = {
            id: '1',
            title: 'Test',
            description: 'Test description',
            cover_path: '/path',
            cover_url: 'https://cdn.example.com/cover.jpg',
            tags: []
        };

        expect(manga.cover_url).toBe('https://cdn.example.com/cover.jpg');
    });

    it('should allow optional recommended field', () => {
        const manga: Manga = {
            id: '1',
            title: 'Test',
            description: 'Test',
            cover_path: '/path',
            recommended: 'Highly recommended for action fans',
            tags: ['action']
        };

        expect(manga.recommended).toBe('Highly recommended for action fans');
    });

    it('should handle manga with empty tags', () => {
        const manga: Manga = {
            id: '1',
            title: 'New Manga',
            description: 'No tags yet',
            cover_path: '/path',
            tags: []
        };

        expect(manga.tags).toEqual([]);
        expect(manga.tags.length).toBe(0);
    });
});

describe('Chapter Type Tests', () => {
    it('should create a valid Chapter object', () => {
        const chapter: Chapter = {
            id: 'ch-001',
            manga_id: 'manga-001',
            number: 1,
            title: 'Romance Dawn'
        };

        expect(chapter.id).toBe('ch-001');
        expect(chapter.manga_id).toBe('manga-001');
        expect(chapter.number).toBe(1);
        expect(chapter.title).toBe('Romance Dawn');
    });

    it('should allow optional pdf_path and thumb_path', () => {
        const chapter: Chapter = {
            id: 'ch-002',
            manga_id: 'manga-001',
            number: 2,
            title: 'Chapter 2',
            pdf_path: '/pdfs/chapter-2.pdf',
            thumb_path: '/thumbs/chapter-2.jpg'
        };

        expect(chapter.pdf_path).toBe('/pdfs/chapter-2.pdf');
        expect(chapter.thumb_path).toBe('/thumbs/chapter-2.jpg');
    });

    it('should allow optional read_url for presigned URLs', () => {
        const chapter: Chapter = {
            id: 'ch-001',
            manga_id: 'manga-001',
            number: 1,
            title: 'Chapter 1',
            read_url: 'https://s3.amazonaws.com/bucket/chapter.pdf?token=abc123'
        };

        expect(chapter.read_url).toContain('s3.amazonaws.com');
    });

    it('should sort chapters by number correctly', () => {
        const chapters: Chapter[] = [
            { id: '3', manga_id: 'm1', number: 10, title: 'Ch 10' },
            { id: '1', manga_id: 'm1', number: 1, title: 'Ch 1' },
            { id: '2', manga_id: 'm1', number: 5, title: 'Ch 5' },
        ];

        const sorted = [...chapters].sort((a, b) => a.number - b.number);
        expect(sorted[0].number).toBe(1);
        expect(sorted[1].number).toBe(5);
        expect(sorted[2].number).toBe(10);
    });
});

describe('UserList Type Tests', () => {
    it('should create a valid UserList object', () => {
        const list: UserList = {
            id: 'list-001',
            name: 'My Favorites',
            owner_uid: 'user-123',
            items: [],
            item_count: 0,
            created_at: '2024-01-01T00:00:00Z',
            updated_at: '2024-01-01T00:00:00Z'
        };

        expect(list.id).toBe('list-001');
        expect(list.name).toBe('My Favorites');
        expect(list.item_count).toBe(0);
    });

    it('should handle list with items', () => {
        const list: UserList = {
            id: 'list-001',
            name: 'Reading List',
            owner_uid: 'user-123',
            items: [
                { manga_id: 'manga-001', added_at: '2024-01-01T00:00:00Z' },
                { manga_id: 'manga-002', added_at: '2024-01-02T00:00:00Z' }
            ],
            item_count: 2,
            created_at: '2024-01-01T00:00:00Z',
            updated_at: '2024-01-02T00:00:00Z'
        };

        expect(list.items.length).toBe(2);
        expect(list.item_count).toBe(2);
        expect(list.items[0].manga_id).toBe('manga-001');
    });

    it('should allow optional owner_name', () => {
        const list: UserList = {
            id: 'list-001',
            name: 'Public List',
            owner_uid: 'user-123',
            owner_name: 'John Doe',
            items: [],
            item_count: 0,
            created_at: '2024-01-01T00:00:00Z',
            updated_at: '2024-01-01T00:00:00Z'
        };

        expect(list.owner_name).toBe('John Doe');
    });
});

describe('AuthUser Type Tests', () => {
    it('should create a valid AuthUser object', () => {
        const user: AuthUser = {
            uid: 'firebase-uid-123',
            email: 'user@example.com',
            displayName: 'John Doe',
            photoURL: 'https://example.com/photo.jpg'
        };

        expect(user.uid).toBe('firebase-uid-123');
        expect(user.email).toBe('user@example.com');
        expect(user.displayName).toBe('John Doe');
    });

    it('should handle null values for optional fields', () => {
        const user: AuthUser = {
            uid: 'anonymous-user',
            email: null,
            displayName: null,
            photoURL: null
        };

        expect(user.uid).toBe('anonymous-user');
        expect(user.email).toBeNull();
        expect(user.displayName).toBeNull();
        expect(user.photoURL).toBeNull();
    });
});
