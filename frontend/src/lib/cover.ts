import type { Manga } from '../types';

/**
 * Checks if a URL appears to be malformed (e.g., contains an encoded URL within it)
 */
function isValidCoverUrl(url: string): boolean {
    // Check if URL contains encoded URL characters that suggest double-encoding
    // e.g., "https://bucket.s3.amazonaws.com/https%3A//..." is malformed
    if (url.includes('https%3A') || url.includes('http%3A')) {
        return false;
    }
    // Basic URL validation
    try {
        new URL(url);
        return true;
    } catch {
        return false;
    }
}

/**
 * Resolves the cover URL for a manga.
 * Priority:
 * 1. cover_url (presigned URL from backend) - if valid
 * 2. cover_path if it starts with "http" (direct URL stored in Firestore)
 * 3. null (no cover available)
 * 
 * Note: If cover_path is a relative S3 key (not starting with http),
 * we don't use it directly as it requires presigning.
 */
export function resolveCoverUrl(manga: Manga | null | undefined): string | null {
    if (!manga) return null;

    // Priority 1: Use cover_url if available and valid
    if (manga.cover_url && manga.cover_url.trim() !== '') {
        if (isValidCoverUrl(manga.cover_url)) {
            return manga.cover_url;
        }
        // cover_url is malformed, try cover_path instead
    }

    // Priority 2: Use cover_path if it's a complete URL
    if (manga.cover_path && manga.cover_path.trim() !== '') {
        if (manga.cover_path.startsWith('http://') || manga.cover_path.startsWith('https://')) {
            return manga.cover_path;
        }
        // cover_path is a relative S3 key - would need presigning
        // For now, return null (prepared for future presigned URL support)
        return null;
    }

    return null;
}

/**
 * Handler for image load errors - sets the target to hidden
 * and shows fallback content (should be handled by parent component)
 */
export function handleCoverError(
    event: React.SyntheticEvent<HTMLImageElement>,
    setShowFallback: (show: boolean) => void
): void {
    event.currentTarget.style.display = 'none';
    setShowFallback(true);
}
