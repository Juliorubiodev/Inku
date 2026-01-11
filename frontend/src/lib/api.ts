import axios from 'axios';
import type { AxiosInstance, InternalAxiosRequestConfig } from 'axios';
import { getIdToken } from './firebase';
import { env } from '../config/env';
import type { Manga, Chapter, UserList, ListSummary, PresignResponse } from '../types';

// ============================================
// API Client Setup
// ============================================

// Use env config for base URLs
const API_BASE_URL = env.apiBaseUrl;
const AUTH_API_URL = env.authApiUrl;
const LIST_API_URL = env.listApiUrl;

// Create axios instance with auth interceptor and automatic 401 retry
const createApiClient = (baseURL: string): AxiosInstance => {
    const client = axios.create({ baseURL });

    // Auth interceptor - adds Bearer token if user is logged in
    client.interceptors.request.use(async (config: InternalAxiosRequestConfig) => {
        try {
            // Always force refresh to ensure fresh token
            const token = await getIdToken(true);
            if (token) {
                config.headers.Authorization = `Bearer ${token}`;
            }
        } catch (error) {
            // Silently fail if no auth - some endpoints don't require it
            console.debug('No auth token available');
        }
        return config;
    });

    // Response interceptor with automatic 401 retry
    client.interceptors.response.use(
        (response) => response,
        async (error) => {
            const originalRequest = error.config;

            // If we get a 401 and haven't already retried this request
            if (error.response?.status === 401 && !originalRequest._retry) {
                originalRequest._retry = true;
                console.log('[API] 401 received, forcing token refresh and retrying...');

                try {
                    // Force a fresh token
                    const newToken = await getIdToken(true);
                    if (newToken) {
                        originalRequest.headers.Authorization = `Bearer ${newToken}`;
                        console.log('[API] Token refreshed, retrying request...');
                        return client(originalRequest);
                    }
                } catch (refreshError) {
                    console.error('[API] Token refresh failed:', refreshError);
                }
            }

            // Enhance error message for common issues
            if (error.response?.status === 401) {
                error.message = 'No autorizado. Por favor, inicia sesión de nuevo.';
            } else if (error.response?.status === 403) {
                error.message = 'Acceso denegado.';
            } else if (error.response?.status === 404) {
                error.message = 'Recurso no encontrado.';
            } else if (!error.response) {
                error.message = 'Error de conexión. Verifica que el backend esté corriendo.';
            }
            return Promise.reject(error);
        }
    );

    return client;
};

export const mangaApi = createApiClient(API_BASE_URL);
export const authApi = createApiClient(AUTH_API_URL);
export const listApi = createApiClient(LIST_API_URL);

// ============================================
// Manga Service API
// ============================================

export const mangaService = {
    // Catalog
    async getMangas(): Promise<Manga[]> {
        const { data } = await mangaApi.get<Manga[]>('/api/mangas');
        return data;
    },

    async getManga(id: string): Promise<Manga> {
        const { data } = await mangaApi.get<Manga>(`/api/mangas/${id}`);
        return data;
    },

    async createManga(manga: {
        id: string;
        title: string;
        description?: string;
        recommended?: string;
        tags?: string[];
        cover_path?: string;
    }): Promise<Manga> {
        const { data } = await mangaApi.post<Manga>('/api/mangas', manga);
        return data;
    },

    async getChapters(mangaId: string, sort: 'asc' | 'desc' = 'asc'): Promise<Chapter[]> {
        const { data } = await mangaApi.get<Chapter[]>(`/api/mangas/${mangaId}/chapters`, {
            params: { sort }
        });
        return data;
    },

    async getChapter(mangaId: string, chapterId: string): Promise<Chapter> {
        const { data } = await mangaApi.get<Chapter>(`/api/mangas/${mangaId}/chapters/${chapterId}`);
        return data;
    },

    /**
     * Get presigned URL for reading a chapter PDF
     * This URL is temporary and can be used directly in an iframe/embed
     */
    async getReadUrl(mangaId: string, chapterId: string): Promise<{ url: string }> {
        // Try the dedicated read-url endpoint first
        try {
            const { data } = await mangaApi.get<{ url: string }>(
                `/api/mangas/${mangaId}/chapters/${chapterId}/read-url`
            );

            // Validate the URL - it should be a complete URL, not a path
            if (data.url && (data.url.startsWith('http://') || data.url.startsWith('https://'))) {
                return data;
            }

            // If we got a relative path, that's an error
            console.warn('Got relative URL from read-url endpoint:', data.url);
            throw new Error('Invalid URL format from server');
        } catch (error) {
            // Fallback: try getting chapter with include_url param
            console.log('Trying fallback: chapter with include_url');
            const { data } = await mangaApi.get<Chapter & { read_url?: string }>(
                `/api/mangas/${mangaId}/chapters/${chapterId}`,
                { params: { include_url: true } }
            );

            if (data.read_url) {
                return { url: data.read_url };
            }

            throw error;
        }
    },

    // Uploads
    async getPresignedUrl(mangaId: string, chapterNumber: number): Promise<PresignResponse> {
        const { data } = await mangaApi.post<PresignResponse>('/api/uploads/presign', {
            manga_id: mangaId,
            chapter_number: chapterNumber,
        });
        return data;
    },

    async registerChapter(
        mangaId: string,
        chapterNumber: number,
        title: string,
        s3Key: string,
        thumbKey: string
    ) {
        const { data } = await mangaApi.post('/api/uploads/register', {
            manga_id: mangaId,
            chapter_number: chapterNumber,
            title,
            s3_key: s3Key,
            thumb_key: thumbKey,
        });
        return data;
    },
};

// ============================================
// List Service API
// ============================================

export const listService = {
    async getPublicLists(page = 1, pageSize = 20): Promise<{ lists: ListSummary[]; total: number }> {
        const { data } = await listApi.get('/api/lists/public', {
            params: { page, page_size: pageSize },
        });
        return data;
    },

    async getMyLists(): Promise<{ lists: ListSummary[]; total: number }> {
        const { data } = await listApi.get('/api/lists/me');
        return data;
    },

    async getList(listId: string): Promise<UserList> {
        const { data } = await listApi.get<UserList>(`/api/lists/${listId}`);
        return data;
    },

    async createList(name: string): Promise<UserList> {
        const { data } = await listApi.post<UserList>('/api/lists', { name });
        return data;
    },

    async updateList(listId: string, name: string): Promise<UserList> {
        const { data } = await listApi.patch<UserList>(`/api/lists/${listId}`, { name });
        return data;
    },

    async deleteList(listId: string): Promise<void> {
        await listApi.delete(`/api/lists/${listId}`);
    },

    async addMangaToList(listId: string, mangaId: string): Promise<UserList> {
        const { data } = await listApi.post<UserList>(`/api/lists/${listId}/items`, {
            manga_id: mangaId,
        });
        return data;
    },

    async removeMangaFromList(listId: string, mangaId: string): Promise<UserList> {
        const { data } = await listApi.delete<UserList>(`/api/lists/${listId}/items/${mangaId}`);
        return data;
    },
};

// ============================================
// Auth Service API (for dev endpoints)
// ============================================

export const authService = {
    async devRegister(email: string, password: string) {
        const { data } = await authApi.post('/api/auth/dev/register', { email, password });
        return data;
    },

    async devLogin(email: string, password: string) {
        const { data } = await authApi.post('/api/auth/dev/login', { email, password });
        return data;
    },

    async getMe() {
        const { data } = await authApi.get('/api/auth/me');
        return data;
    },
};
