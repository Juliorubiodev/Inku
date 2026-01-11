import React, { useEffect, useState } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { mangaService } from '../lib/api';
import { resolveCoverUrl } from '../lib/cover';
import { useAuth } from '../context/AuthContext';
import AddToListModal from '../components/AddToListModal';
import type { Manga, Chapter } from '../types';
import './MangaDetail.css';

const MangaDetail: React.FC = () => {
    const { id } = useParams<{ id: string }>();
    const navigate = useNavigate();
    const { user } = useAuth();
    const [manga, setManga] = useState<Manga | null>(null);
    const [chapters, setChapters] = useState<Chapter[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [showListModal, setShowListModal] = useState(false);
    const [toast, setToast] = useState<{ type: 'success' | 'error'; message: string } | null>(null);
    const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('asc');
    const [coverError, setCoverError] = useState(false);

    const coverUrl = resolveCoverUrl(manga);

    useEffect(() => {
        if (id) {
            loadManga();
        }
    }, [id]);

    const loadManga = async (sort: 'asc' | 'desc' = 'asc') => {
        if (!id) return;
        try {
            const [mangaData, chaptersData] = await Promise.all([
                mangaService.getManga(id),
                mangaService.getChapters(id, sort),
            ]);
            setManga(mangaData);
            // Always sort locally to ensure correct order (backend may not be running)
            const sortedChapters = [...chaptersData].sort((a, b) =>
                sort === 'asc' ? a.number - b.number : b.number - a.number
            );
            setChapters(sortedChapters);
        } catch (err: any) {
            setError('Error al cargar el manga');
        } finally {
            setLoading(false);
        }
    };

    const toggleSortOrder = () => {
        const newOrder = sortOrder === 'asc' ? 'desc' : 'asc';
        setSortOrder(newOrder);
        // Sort locally for instant feedback
        setChapters(prev => [...prev].sort((a, b) =>
            newOrder === 'asc' ? a.number - b.number : b.number - a.number
        ));
    };

    if (loading) {
        return <div className="loading">Cargando manga...</div>;
    }

    if (error || !manga) {
        return (
            <div className="error-page">
                <h2>Error</h2>
                <p>{error || 'Manga no encontrado'}</p>
                <Link to="/" className="btn-back">Volver al catálogo</Link>
            </div>
        );
    }

    return (
        <div className="manga-detail-page">
            <div className="manga-header">
                <div className="manga-cover-large">
                    {coverUrl && !coverError ? (
                        <img
                            src={coverUrl}
                            alt={manga.title}
                            onError={() => setCoverError(true)}
                        />
                    ) : (
                        <div className="cover-placeholder">📖</div>
                    )}
                </div>

                <div className="manga-meta">
                    <h1>{manga.title || manga.id}</h1>

                    {manga.description && (
                        <p className="manga-description">{manga.description}</p>
                    )}

                    {manga.recommended && (
                        <p className="manga-recommended">
                            <strong>Recomendado:</strong> {manga.recommended}
                        </p>
                    )}

                    {manga.tags.length > 0 && (
                        <div className="manga-tags-large">
                            {manga.tags.map(tag => (
                                <span key={tag} className="tag-large">{tag}</span>
                            ))}
                        </div>
                    )}

                    <button
                        className="btn-add-to-list-action"
                        onClick={() => {
                            if (!user) {
                                setToast({ type: 'error', message: 'Debes iniciar sesión para agregar a una lista' });
                                setTimeout(() => {
                                    setToast(null);
                                    navigate('/login');
                                }, 2000);
                                return;
                            }
                            setShowListModal(true);
                        }}
                    >
                        📚 Agregar a lista
                    </button>
                </div>
            </div>

            <div className="chapters-section">
                <div className="chapters-header">
                    <h2>Capítulos ({chapters.length})</h2>
                    <button
                        className="btn-sort-toggle"
                        onClick={toggleSortOrder}
                        title={sortOrder === 'asc' ? 'Ordenar descendente' : 'Ordenar ascendente'}
                    >
                        {sortOrder === 'asc' ? '↑ 1-9' : '↓ 9-1'}
                    </button>
                </div>

                {chapters.length === 0 ? (
                    <p className="no-chapters">No hay capítulos disponibles</p>
                ) : (
                    <div className="chapters-list">
                        {chapters.map(chapter => (
                            <Link
                                key={chapter.id}
                                to={`/read/${manga.id}/${chapter.id}`}
                                className="chapter-item"
                            >
                                <span className="chapter-number">Cap. {chapter.number}</span>
                                <span className="chapter-title">{chapter.title || `Capítulo ${chapter.number}`}</span>
                                <span className="chapter-arrow">→</span>
                            </Link>
                        ))}
                    </div>
                )}
            </div>

            {/* Toast notification */}
            {toast && (
                <div className={`toast toast-${toast.type}`}>
                    {toast.message}
                </div>
            )}

            {/* Add to list modal */}
            {id && (
                <AddToListModal
                    isOpen={showListModal}
                    onClose={() => setShowListModal(false)}
                    mangaId={id}
                />
            )}
        </div>
    );
};

export default MangaDetail;
