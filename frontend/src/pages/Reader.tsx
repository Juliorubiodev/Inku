import React, { useEffect, useState, useCallback } from 'react';
import { useParams, Link } from 'react-router-dom';
import { mangaService } from '../lib/api';
import './Reader.css';

const Reader: React.FC = () => {
    const { mangaId, chapterId } = useParams<{ mangaId: string; chapterId: string }>();
    const [pdfUrl, setPdfUrl] = useState<string | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [errorDetail, setErrorDetail] = useState('');

    const [chapterTitle, setChapterTitle] = useState('');
    const [prevChapterId, setPrevChapterId] = useState<string | null>(null);
    const [nextChapterId, setNextChapterId] = useState<string | null>(null);

    const loadChapter = useCallback(async () => {
        if (!mangaId || !chapterId) return;

        setLoading(true);
        setError('');
        setErrorDetail('');

        try {
            // Fetch current chapter and all chapters for navigation
            const [chapter, allChapters] = await Promise.all([
                mangaService.getChapter(mangaId, chapterId),
                mangaService.getChapters(mangaId, 'asc')
            ]);

            if (!chapter.read_url) {
                throw new Error('No se recibió URL del capítulo');
            }

            setPdfUrl(chapter.read_url);
            setChapterTitle(chapter.title || `Capítulo ${chapter.number}`);

            // Calculate Prev/Next
            const currentIndex = allChapters.findIndex(c => c.id === chapterId);

            if (currentIndex > 0) {
                setPrevChapterId(allChapters[currentIndex - 1].id);
            } else {
                setPrevChapterId(null);
            }

            if (currentIndex !== -1 && currentIndex < allChapters.length - 1) {
                setNextChapterId(allChapters[currentIndex + 1].id);
            } else {
                setNextChapterId(null);
            }

        } catch (err: unknown) {
            console.error('Error loading chapter:', err);

            let message = 'Error al cargar el capítulo';
            let detail = '';

            if (err instanceof Error) {
                // Check for specific S3 errors
                if (err.message.includes('AccessDenied') || err.message.includes('403')) {
                    message = 'Acceso denegado al archivo';
                    detail = 'El servidor no pudo generar la URL de lectura. Contacta al administrador.';
                } else if (err.message.includes('404') || err.message.includes('Not Found')) {
                    message = 'Capítulo no encontrado';
                    detail = 'Este capítulo no existe o fue eliminado.';
                } else if (err.message.includes('Network')) {
                    message = 'Error de conexión';
                    detail = 'Verifica tu conexión a internet e intenta de nuevo.';
                } else {
                    detail = err.message;
                }
            }

            setError(message);
            setErrorDetail(detail);
        } finally {
            setLoading(false);
        }
    }, [mangaId, chapterId]);

    useEffect(() => {
        loadChapter();
    }, [loadChapter]);

    if (loading) {
        return (
            <div className="reader-loading">
                <div className="spinner"></div>
                <p>Cargando capítulo...</p>
            </div>
        );
    }

    if (error || !pdfUrl) {
        return (
            <div className="reader-error">
                <h2>😔 {error || 'Error'}</h2>
                <p>{errorDetail || 'No se pudo cargar el capítulo'}</p>
                <div className="error-actions">
                    <button onClick={loadChapter} className="btn-retry">
                        🔄 Reintentar
                    </button>
                    <Link to={`/manga/${mangaId}`} className="btn-back">
                        ← Volver al manga
                    </Link>
                </div>
            </div>
        );
    }

    return (
        <div className="reader-page">
            <div className="reader-header">
                <Link to={`/manga/${mangaId}`} className="back-link">
                    ← Volver
                </Link>

                <div className="chapter-nav">
                    {prevChapterId ? (
                        <Link to={`/read/${mangaId}/${prevChapterId}`} className="nav-btn">
                            ← Anterior
                        </Link>
                    ) : (
                        <span className="nav-btn disabled">← Anterior</span>
                    )}

                    {nextChapterId ? (
                        <Link to={`/read/${mangaId}/${nextChapterId}`} className="nav-btn">
                            Siguiente →
                        </Link>
                    ) : (
                        <span className="nav-btn disabled">Siguiente →</span>
                    )}
                </div>

                <span className="chapter-info">{chapterTitle}</span>
            </div>

            <div className="reader-content">
                <iframe
                    src={pdfUrl}
                    title="PDF Reader"
                    className="pdf-viewer"
                />
            </div>

            <div className="reader-tip">
                <p>
                    💡 Si el PDF no carga, puedes{' '}
                    <a href={pdfUrl} target="_blank" rel="noopener noreferrer">
                        abrirlo en una nueva pestaña
                    </a>
                </p>
            </div>
        </div>
    );
};

export default Reader;
