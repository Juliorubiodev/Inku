import React, { useEffect, useState } from 'react';
import { mangaService } from '../lib/api';
import { resolveCoverUrl } from '../lib/cover';
import type { Manga } from '../types';
import './AddMangaModal.css';

// Sub-component for manga cover with error handling
const MangaSelectCover: React.FC<{ manga: Manga }> = ({ manga }) => {
    const [coverError, setCoverError] = useState(false);
    const coverUrl = resolveCoverUrl(manga);

    if (coverUrl && !coverError) {
        return (
            <img
                src={coverUrl}
                alt={manga.title}
                onError={() => setCoverError(true)}
            />
        );
    }
    return <span>📖</span>;
};

interface AddMangaModalProps {
    isOpen: boolean;
    onClose: () => void;
    onAdd: (mangaId: string) => Promise<void>;
    existingMangaIds: string[];
}

const AddMangaModal: React.FC<AddMangaModalProps> = ({
    isOpen,
    onClose,
    onAdd,
    existingMangaIds,
}) => {
    const [mangas, setMangas] = useState<Manga[]>([]);
    const [search, setSearch] = useState('');
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [addingId, setAddingId] = useState<string | null>(null);
    const [successId, setSuccessId] = useState<string | null>(null);

    useEffect(() => {
        if (isOpen) {
            loadMangas();
        }
    }, [isOpen]);

    const loadMangas = async () => {
        setLoading(true);
        setError('');
        try {
            const data = await mangaService.getMangas();
            setMangas(data);
        } catch (err: any) {
            setError('Error al cargar el catálogo');
        } finally {
            setLoading(false);
        }
    };

    const handleAdd = async (mangaId: string) => {
        setAddingId(mangaId);
        setError('');
        try {
            await onAdd(mangaId);
            setSuccessId(mangaId);
            setTimeout(() => setSuccessId(null), 2000);
        } catch (err: any) {
            setError(err.message || 'Error al agregar manga');
        } finally {
            setAddingId(null);
        }
    };

    const filteredMangas = mangas.filter(manga =>
        manga.title.toLowerCase().includes(search.toLowerCase()) ||
        manga.id.toLowerCase().includes(search.toLowerCase()) ||
        manga.tags.some(tag => tag.toLowerCase().includes(search.toLowerCase()))
    );

    if (!isOpen) return null;

    return (
        <div className="modal-overlay" onClick={onClose}>
            <div className="modal-content add-manga-modal" onClick={e => e.stopPropagation()}>
                <div className="modal-header">
                    <h2>Agregar manga a la lista</h2>
                    <button className="modal-close" onClick={onClose}>✕</button>
                </div>

                <div className="modal-search">
                    <input
                        type="text"
                        placeholder="Buscar por título, id o tag..."
                        value={search}
                        onChange={e => setSearch(e.target.value)}
                        autoFocus
                    />
                </div>

                {error && <div className="modal-error">{error}</div>}

                <div className="modal-body">
                    {loading ? (
                        <div className="modal-loading">Cargando catálogo...</div>
                    ) : filteredMangas.length === 0 ? (
                        <div className="modal-empty">No se encontraron mangas</div>
                    ) : (
                        <div className="manga-select-grid">
                            {filteredMangas.map(manga => {
                                const isInList = existingMangaIds.includes(manga.id);
                                const isAdding = addingId === manga.id;
                                const justAdded = successId === manga.id;

                                return (
                                    <div key={manga.id} className="manga-select-card">
                                        <div className="manga-select-cover">
                                            <MangaSelectCover manga={manga} />
                                        </div>
                                        <div className="manga-select-info">
                                            <h4>{manga.title || manga.id}</h4>
                                            {manga.tags.length > 0 && (
                                                <div className="manga-select-tags">
                                                    {manga.tags.slice(0, 2).map(tag => (
                                                        <span key={tag} className="tag-small">{tag}</span>
                                                    ))}
                                                </div>
                                            )}
                                        </div>
                                        <button
                                            className={`btn-add-to-list ${isInList || justAdded ? 'added' : ''}`}
                                            onClick={() => handleAdd(manga.id)}
                                            disabled={isInList || isAdding || justAdded}
                                        >
                                            {isAdding ? '...' : isInList ? 'Ya está' : justAdded ? '✓ Añadido' : 'Añadir'}
                                        </button>
                                    </div>
                                );
                            })}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default AddMangaModal;
