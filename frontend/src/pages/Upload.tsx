import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { mangaService } from '../lib/api';
import { useAuth } from '../context/AuthContext';
import type { Manga } from '../types';
import './Upload.css';

type MangaMode = 'existing' | 'new';

const Upload: React.FC = () => {
    const { user, loading: authLoading } = useAuth();

    // Mode selection
    const [mode, setMode] = useState<MangaMode>('existing');

    // Existing manga selection
    const [mangas, setMangas] = useState<Manga[]>([]);
    const [selectedManga, setSelectedManga] = useState('');
    const [mangaSearch, setMangaSearch] = useState('');

    // New manga fields
    const [newMangaId, setNewMangaId] = useState('');
    const [newMangaTitle, setNewMangaTitle] = useState('');
    const [newMangaDescription, setNewMangaDescription] = useState('');
    const [newMangaRecommended, setNewMangaRecommended] = useState('');
    const [newMangaTags, setNewMangaTags] = useState('');

    // Chapter fields
    const [chapterNumber, setChapterNumber] = useState(1);
    const [chapterTitle, setChapterTitle] = useState('');
    const [pdfFile, setPdfFile] = useState<File | null>(null);

    // UI state
    const [loading, setLoading] = useState(false);
    const [step, setStep] = useState<'form' | 'uploading' | 'success'>('form');
    const [error, setError] = useState('');
    const [progress, setProgress] = useState('');
    const [createdMangaId, setCreatedMangaId] = useState('');

    useEffect(() => {
        loadMangas();
    }, []);

    const loadMangas = async () => {
        try {
            const data = await mangaService.getMangas();
            setMangas(data);
        } catch (err) {
            console.error('Error loading mangas:', err);
        }
    };

    // Auto-generate slug from title
    const generateSlug = (title: string): string => {
        return title
            .toLowerCase()
            .trim()
            .replace(/[^\w\s-]/g, '')
            .replace(/\s+/g, '-')
            .replace(/-+/g, '-');
    };

    const handleTitleChange = (title: string) => {
        setNewMangaTitle(title);
        if (!newMangaId || newMangaId === generateSlug(newMangaTitle)) {
            setNewMangaId(generateSlug(title));
        }
    };

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (file && file.type === 'application/pdf') {
            setPdfFile(file);
            setError('');
        } else {
            setError('Por favor selecciona un archivo PDF');
        }
    };

    const handleUpload = async (e: React.FormEvent) => {
        e.preventDefault();

        const mangaId = mode === 'existing' ? selectedManga : newMangaId;

        if (!mangaId || !pdfFile) {
            setError('Completa todos los campos requeridos');
            return;
        }

        if (mode === 'new' && !newMangaTitle) {
            setError('El título del manga es requerido');
            return;
        }

        setLoading(true);
        setStep('uploading');
        setError('');

        try {
            // Step 0: Create manga if new
            if (mode === 'new') {
                setProgress('Creando manga...');
                await mangaService.createManga({
                    id: newMangaId,
                    title: newMangaTitle,
                    description: newMangaDescription,
                    recommended: newMangaRecommended || undefined,
                    tags: newMangaTags ? newMangaTags.split(',').map(t => t.trim()).filter(Boolean) : [],
                });
            }

            // Step 1: Get presigned URL
            setProgress('Obteniendo URL de subida...');
            const presign = await mangaService.getPresignedUrl(mangaId, chapterNumber);

            // Step 2: Upload to S3
            setProgress('Subiendo PDF a S3...');
            const uploadResponse = await fetch(presign.upload_url, {
                method: 'PUT',
                body: pdfFile,
                headers: {
                    'Content-Type': 'application/pdf',
                },
            });

            if (!uploadResponse.ok) {
                throw new Error('Error al subir el archivo a S3');
            }

            // Step 3: Register metadata
            setProgress('Registrando capítulo...');
            await mangaService.registerChapter(
                mangaId,
                chapterNumber,
                chapterTitle || `Capítulo ${chapterNumber}`,
                presign.s3_key,
                presign.thumb_key
            );

            setCreatedMangaId(mangaId);
            setStep('success');

            // Reload mangas list
            await loadMangas();
        } catch (err: any) {
            console.error('Upload error:', err);
            if (err.response?.data?.detail === 'MANGA_ALREADY_EXISTS') {
                setError('Ya existe un manga con ese ID. Usa un ID diferente.');
            } else if (err.response?.status === 401) {
                setError('Sesión expirada. Por favor, refresca la página o inicia sesión de nuevo.');
            } else if (err.response?.status === 403) {
                setError('No tienes permisos para realizar esta acción.');
            } else {
                setError(err.message || 'Error durante la subida');
            }
            setStep('form');
        } finally {
            setLoading(false);
        }
    };

    const resetForm = () => {
        setStep('form');
        setPdfFile(null);
        setChapterTitle('');
        setChapterNumber(1);
        if (mode === 'new') {
            setNewMangaId('');
            setNewMangaTitle('');
            setNewMangaDescription('');
            setNewMangaRecommended('');
            setNewMangaTags('');
        }
    };

    if (authLoading) {
        return <div className="loading">Cargando...</div>;
    }

    if (!user) {
        return (
            <div className="auth-required">
                <h2>Inicia sesión</h2>
                <p>Necesitas iniciar sesión para subir contenido</p>
                <Link to="/login" className="btn-primary">Iniciar Sesión</Link>
            </div>
        );
    }

    if (step === 'success') {
        return (
            <div className="upload-success">
                <div className="success-icon">✅</div>
                <h2>¡{mode === 'new' ? 'Manga y capítulo creados' : 'Capítulo subido'}!</h2>
                <p>Tu contenido está pendiente de revisión.</p>
                <div className="success-actions">
                    <button onClick={resetForm}>
                        Subir otro
                    </button>
                    <Link to={`/manga/${createdMangaId}`}>Ver manga</Link>
                </div>
            </div>
        );
    }

    return (
        <div className="upload-page">
            <h1>Subir Contenido</h1>
            <p className="upload-subtitle">Contribuye a la comunidad subiendo nuevos mangas o capítulos</p>

            {error && <div className="error-message">{error}</div>}

            {step === 'uploading' ? (
                <div className="upload-progress">
                    <div className="spinner"></div>
                    <p>{progress}</p>
                </div>
            ) : (
                <form onSubmit={handleUpload} className="upload-form">
                    {/* Mode Selection */}
                    <div className="mode-selector">
                        <button
                            type="button"
                            className={`mode-btn ${mode === 'existing' ? 'active' : ''}`}
                            onClick={() => setMode('existing')}
                        >
                            📚 Manga existente
                        </button>
                        <button
                            type="button"
                            className={`mode-btn ${mode === 'new' ? 'active' : ''}`}
                            onClick={() => setMode('new')}
                        >
                            ✨ Nuevo manga
                        </button>
                    </div>

                    {mode === 'existing' ? (
                        /* Existing Manga Selection */
                        <div className="existing-manga-section">
                            <div className="form-group">
                                <label>Buscar manga</label>
                                <input
                                    type="text"
                                    placeholder="Escribe para filtrar..."
                                    value={mangaSearch}
                                    onChange={(e) => setMangaSearch(e.target.value)}
                                    className="manga-search-input"
                                />
                            </div>
                            <div className="form-group">
                                <label>Seleccionar manga</label>
                                <select
                                    value={selectedManga}
                                    onChange={(e) => setSelectedManga(e.target.value)}
                                    required
                                >
                                    <option value="">Seleccionar manga...</option>
                                    {mangas
                                        .filter(manga =>
                                            !mangaSearch ||
                                            (manga.title || manga.id).toLowerCase().includes(mangaSearch.toLowerCase())
                                        )
                                        .map(manga => (
                                            <option key={manga.id} value={manga.id}>
                                                {manga.title || manga.id}
                                            </option>
                                        ))}
                                </select>
                                {mangaSearch && mangas.filter(m => (m.title || m.id).toLowerCase().includes(mangaSearch.toLowerCase())).length === 0 && (
                                    <small className="no-results">No se encontraron mangas</small>
                                )}
                            </div>
                        </div>
                    ) : (
                        /* New Manga Fields */
                        <div className="new-manga-section">
                            <h3>Información del manga</h3>

                            <div className="form-group">
                                <label>Título *</label>
                                <input
                                    type="text"
                                    value={newMangaTitle}
                                    onChange={(e) => handleTitleChange(e.target.value)}
                                    placeholder="Ej: My Hero Academia"
                                    required
                                />
                            </div>

                            <div className="form-group">
                                <label>ID/Slug</label>
                                <input
                                    type="text"
                                    value={newMangaId}
                                    onChange={(e) => setNewMangaId(e.target.value)}
                                    placeholder="auto-generado-del-titulo"
                                    pattern="^[a-z0-9-]+$"
                                    title="Solo letras minúsculas, números y guiones"
                                />
                                <small>Se usa en la URL. Solo letras minúsculas, números y guiones.</small>
                            </div>

                            <div className="form-group">
                                <label>Descripción</label>
                                <textarea
                                    value={newMangaDescription}
                                    onChange={(e) => setNewMangaDescription(e.target.value)}
                                    placeholder="Sinopsis o descripción del manga..."
                                    rows={3}
                                />
                            </div>

                            <div className="form-row">
                                <div className="form-group">
                                    <label>Recomendado si te gusta</label>
                                    <input
                                        type="text"
                                        value={newMangaRecommended}
                                        onChange={(e) => setNewMangaRecommended(e.target.value)}
                                        placeholder="Ej: Naruto, One Piece"
                                    />
                                </div>

                                <div className="form-group">
                                    <label>Tags (separados por coma)</label>
                                    <input
                                        type="text"
                                        value={newMangaTags}
                                        onChange={(e) => setNewMangaTags(e.target.value)}
                                        placeholder="acción, aventura, shonen"
                                    />
                                </div>
                            </div>
                        </div>
                    )}

                    {/* Chapter Section */}
                    <div className="chapter-section">
                        <h3>{mode === 'new' ? 'Primer capítulo *' : 'Capítulo'}</h3>

                        <div className="form-row">
                            <div className="form-group">
                                <label>Número de capítulo</label>
                                <input
                                    type="number"
                                    min="1"
                                    value={chapterNumber}
                                    onChange={(e) => setChapterNumber(parseInt(e.target.value))}
                                    required
                                />
                            </div>

                            <div className="form-group">
                                <label>Título (opcional)</label>
                                <input
                                    type="text"
                                    placeholder="Ej: El comienzo"
                                    value={chapterTitle}
                                    onChange={(e) => setChapterTitle(e.target.value)}
                                    maxLength={200}
                                />
                            </div>
                        </div>

                        <div className="form-group">
                            <label>Archivo PDF *</label>
                            <div className="file-input">
                                <input
                                    type="file"
                                    accept="application/pdf"
                                    onChange={handleFileChange}
                                    required
                                />
                                {pdfFile && <span className="file-name">{pdfFile.name}</span>}
                            </div>
                        </div>
                    </div>

                    <button
                        type="submit"
                        className="btn-upload"
                        disabled={loading || !pdfFile || (mode === 'existing' ? !selectedManga : !newMangaTitle)}
                    >
                        {mode === 'new' ? 'Crear manga y subir capítulo' : 'Subir Capítulo'}
                    </button>

                    <p className="upload-note">
                        ⚠️ <strong>Nota:</strong> Los PDFs se almacenan en un bucket privado.
                        El acceso directo a la URL no funcionará; el lector usa URLs temporales firmadas.
                    </p>
                </form>
            )}
        </div>
    );
};

export default Upload;
