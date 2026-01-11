import React, { useEffect, useState } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { listService, mangaService } from '../lib/api';
import { resolveCoverUrl } from '../lib/cover';
import { useAuth } from '../context/AuthContext';
import AddMangaModal from '../components/AddMangaModal';
import ConfirmModal from '../components/ConfirmModal';
import type { UserList, Manga } from '../types';
import './ListDetail.css';

// Sub-component for list item cover with error handling
const ListItemCover: React.FC<{ manga: Manga | undefined; fallbackId: string }> = ({ manga, fallbackId }) => {
    const [coverError, setCoverError] = useState(false);
    const coverUrl = resolveCoverUrl(manga ?? null);

    if (coverUrl && !coverError) {
        return (
            <img
                src={coverUrl}
                alt={manga?.title || fallbackId}
                onError={() => setCoverError(true)}
            />
        );
    }
    return <span>📖</span>;
};

const ListDetail: React.FC = () => {
    const { id } = useParams<{ id: string }>();
    const navigate = useNavigate();
    const { user, loading: authLoading } = useAuth();
    const [list, setList] = useState<UserList | null>(null);
    const [mangaDetails, setMangaDetails] = useState<Map<string, Manga>>(new Map());
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [editing, setEditing] = useState(false);
    const [newName, setNewName] = useState('');
    const [showAddModal, setShowAddModal] = useState(false);
    const [toast, setToast] = useState<{ type: 'success' | 'error'; message: string } | null>(null);

    // State for delete list confirmation modal
    const [deleteListModalOpen, setDeleteListModalOpen] = useState(false);
    const [isDeletingList, setIsDeletingList] = useState(false);

    // State for remove manga confirmation modal
    const [removeMangaModalOpen, setRemoveMangaModalOpen] = useState(false);
    const [mangaToRemove, setMangaToRemove] = useState<string | null>(null);
    const [isRemovingManga, setIsRemovingManga] = useState(false);

    const isOwner = user && list && user.uid === list.owner_uid;

    useEffect(() => {
        if (id && !authLoading) {
            loadList();
        }
    }, [id, authLoading]);

    const loadList = async () => {
        if (!id) return;
        try {
            const data = await listService.getList(id);
            setList(data);
            setNewName(data.name);

            // Load manga details for each item
            const details = new Map<string, Manga>();
            for (const item of data.items) {
                try {
                    const manga = await mangaService.getManga(item.manga_id);
                    details.set(item.manga_id, manga);
                } catch {
                    // Ignore errors for individual mangas
                }
            }
            setMangaDetails(details);
        } catch (err: any) {
            setError('Error al cargar la lista');
        } finally {
            setLoading(false);
        }
    };

    const handleRename = async () => {
        if (!id || !newName.trim()) return;
        try {
            const updated = await listService.updateList(id, newName);
            setList(updated);
            setEditing(false);
        } catch (err: any) {
            setError('Error al renombrar la lista');
        }
    };

    // Remove manga modal handlers
    const openRemoveMangaModal = (mangaId: string) => {
        setMangaToRemove(mangaId);
        setRemoveMangaModalOpen(true);
    };

    const closeRemoveMangaModal = () => {
        setRemoveMangaModalOpen(false);
        setMangaToRemove(null);
    };

    const confirmRemoveManga = async () => {
        if (!id || !mangaToRemove) return;

        setIsRemovingManga(true);
        try {
            const updated = await listService.removeMangaFromList(id, mangaToRemove);
            setList(updated);
            closeRemoveMangaModal();
        } catch (err: any) {
            console.error('Error removing manga:', err);
            setError('Error al quitar el manga');
            closeRemoveMangaModal();
        } finally {
            setIsRemovingManga(false);
        }
    };

    // Delete list modal handlers
    const openDeleteListModal = () => {
        setDeleteListModalOpen(true);
    };

    const closeDeleteListModal = () => {
        setDeleteListModalOpen(false);
    };

    const confirmDeleteList = async () => {
        if (!id) return;

        setIsDeletingList(true);
        try {
            await listService.deleteList(id);
            navigate('/my-lists');
        } catch (err: any) {
            console.error('Error deleting list:', err);
            setError('Error al eliminar la lista');
            setToast({ type: 'error', message: 'No se pudo eliminar la lista' });
            closeDeleteListModal();
        } finally {
            setIsDeletingList(false);
        }
    };

    const handleAddManga = async (mangaId: string) => {
        if (!id) return;
        const updated = await listService.addMangaToList(id, mangaId);
        setList(updated);
        // Load new manga details
        try {
            const manga = await mangaService.getManga(mangaId);
            setMangaDetails(prev => new Map(prev).set(mangaId, manga));
        } catch {
            // Ignore if can't load details
        }
        setToast({ type: 'success', message: 'Manga añadido a la lista' });
        setTimeout(() => setToast(null), 3000);
    };

    if (loading || authLoading) {
        return <div className="loading">Cargando lista...</div>;
    }

    if (error || !list) {
        return (
            <div className="error-page">
                <h2>Error</h2>
                <p>{error || 'Lista no encontrada'}</p>
                <Link to="/lists" className="btn-back">Volver a listas</Link>
            </div>
        );
    }

    return (
        <div className="list-detail-page">
            <button className="btn-back" onClick={() => navigate(-1)}>
                ← Volver
            </button>
            <div className="list-header">
                {editing ? (
                    <div className="edit-name">
                        <input
                            type="text"
                            value={newName}
                            onChange={(e) => setNewName(e.target.value)}
                            maxLength={100}
                        />
                        <button onClick={handleRename}>Guardar</button>
                        <button onClick={() => { setEditing(false); setNewName(list.name); }}>Cancelar</button>
                    </div>
                ) : (
                    <div className="list-title">
                        <h1>{list.name}</h1>
                        {isOwner && (
                            <div className="list-actions">
                                <button onClick={() => setShowAddModal(true)} className="btn-add-manga">
                                    ➕ Agregar manga
                                </button>
                                <button onClick={() => setEditing(true)} className="btn-edit">
                                    ✏️ Editar
                                </button>
                                <button onClick={openDeleteListModal} className="btn-delete-list">
                                    🗑️ Eliminar
                                </button>
                            </div>
                        )}
                    </div>
                )}
                <p className="list-meta">
                    Creada por {list.owner_name || 'Desconocido'} • {list.item_count} mangas • Creada el {new Date(list.created_at).toLocaleDateString()}
                </p>
            </div>

            {list.items.length === 0 ? (
                <p className="no-items">Esta lista está vacía</p>
            ) : (
                <div className="list-items">
                    {list.items.map(item => {
                        const manga = mangaDetails.get(item.manga_id);
                        return (
                            <div key={item.manga_id} className="list-item">
                                <Link to={`/manga/${item.manga_id}`} className="list-item-link">
                                    <div className="item-cover">
                                        <ListItemCover manga={manga} fallbackId={item.manga_id} />
                                    </div>
                                    <div className="item-info">
                                        <h3>{manga?.title || item.manga_id}</h3>
                                        {manga?.tags && manga.tags.length > 0 && (
                                            <div className="item-tags">
                                                {manga.tags.slice(0, 2).map(tag => (
                                                    <span key={tag} className="tag">{tag}</span>
                                                ))}
                                            </div>
                                        )}
                                    </div>
                                </Link>
                                {isOwner && (
                                    <button
                                        className="btn-remove"
                                        onClick={() => openRemoveMangaModal(item.manga_id)}
                                    >
                                        ✕
                                    </button>
                                )}
                            </div>
                        );
                    })}
                </div>
            )}

            {/* Toast notification */}
            {toast && (
                <div className={`toast toast-${toast.type}`}>
                    {toast.message}
                </div>
            )}

            {/* Add manga modal */}
            <AddMangaModal
                isOpen={showAddModal}
                onClose={() => setShowAddModal(false)}
                onAdd={handleAddManga}
                existingMangaIds={list.items.map(item => item.manga_id)}
            />

            {/* Delete list confirmation modal */}
            <ConfirmModal
                isOpen={deleteListModalOpen}
                title="¿Estás seguro?"
                message="¿Estás seguro de que quieres eliminar esta lista? Esta acción no se puede deshacer."
                confirmText="Eliminar"
                cancelText="Cancelar"
                onConfirm={confirmDeleteList}
                onCancel={closeDeleteListModal}
                isLoading={isDeletingList}
            />

            {/* Remove manga confirmation modal */}
            <ConfirmModal
                isOpen={removeMangaModalOpen}
                title="¿Quitar manga?"
                message="¿Estás seguro de que quieres quitar este manga de la lista?"
                confirmText="Quitar"
                cancelText="Cancelar"
                onConfirm={confirmRemoveManga}
                onCancel={closeRemoveMangaModal}
                isLoading={isRemovingManga}
            />
        </div>
    );
};

export default ListDetail;
