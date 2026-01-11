import React, { useState } from 'react';
import { resolveCoverUrl } from '../lib/cover';
import type { Manga } from '../types';

interface MangaCoverProps {
    manga: Manga | null | undefined;
    alt?: string;
    className?: string;
    placeholderClassName?: string;
}

/**
 * MangaCover component that handles:
 * - Resolving cover URL from manga.cover_url or manga.cover_path
 * - Showing fallback emoji when no cover or on error
 * - Proper object-fit styling
 */
const MangaCover: React.FC<MangaCoverProps> = ({
    manga,
    alt,
    className = '',
    placeholderClassName = '',
}) => {
    const [showFallback, setShowFallback] = useState(false);
    const coverUrl = resolveCoverUrl(manga);

    const handleError = () => {
        setShowFallback(true);
    };

    // Show fallback if no URL or if image failed to load
    if (!coverUrl || showFallback) {
        return (
            <div className={placeholderClassName || className}>
                📖
            </div>
        );
    }

    return (
        <img
            src={coverUrl}
            alt={alt || manga?.title || 'Manga cover'}
            className={className}
            onError={handleError}
            style={{ width: '100%', height: '100%', objectFit: 'cover' }}
        />
    );
};

export default MangaCover;
