import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { listService } from '../lib/api';
import { useAuth } from '../context/AuthContext';
import ConfirmModal from '../components/ConfirmModal';
import type { ListSummary, UserList } from '../types';
import './Lists.css';

const MyLists: React.FC = () => {
    const { user, loading: authLoading } = useAuth();
    const [lists, setLists] = useState<ListSummary[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [newListName, setNewListName] = useState('');
    const [creating, setCreating] = useState(false);

    // State for delete confirmation modal
    const [deleteModalOpen, setDeleteModalOpen] = useState(false);
    const [listToDelete, setListToDelete] = useState<string | null>(null);
    const [isDeleting, setIsDeleting] = useState(false);

    useEffect(() => {
        // Only load lists when auth is ready and user is logged in
        if (user && !authLoading) {
            loadLists();
        }
    }, [user, authLoading]);

    const loadLists = async () => {
        setError('');
        try {
            const { lists: data } = await listService.getMyLists();
            setLists(data);
        } catch (err: any) {
            setError('Error al cargar las listas');
        } finally {
            setLoading(false);
        }
    };

    const handleCreate = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!newListName.trim()) return;

        setCreating(true);
        setError('');
        try {
            const newList = await listService.createList(newListName);
            setLists([...lists, {
                id: newList.id,
                name: newList.name,
                owner_uid: newList.owner_uid,
                item_count: 0,
                created_at: newList.created_at,
                updated_at: newList.updated_at,
            }]);
            setNewListName('');
        } catch (err: any) {
            setError('Error al crear la lista');
        } finally {
            setCreating(false);
        }
    };

    const openDeleteModal = (listId: string) => {
        setListToDelete(listId);
        setDeleteModalOpen(true);
    };

    const closeDeleteModal = () => {
        setDeleteModalOpen(false);
        setListToDelete(null);
    };

    const confirmDelete = async () => {
        if (!listToDelete) return;

        setIsDeleting(true);
        setError('');
        try {
            await listService.deleteList(listToDelete);
            setLists(lists.filter(l => l.id !== listToDelete));
            closeDeleteModal();
        } catch (err: any) {
            console.error('Error deleting list:', err);
            setError('Error al eliminar la lista');
            closeDeleteModal();
        } finally {
            setIsDeleting(false);
        }
    };

    if (!user) {
        return (
            <div className="auth-required">
                <h2>Inicia sesión</h2>
                <p>Necesitas iniciar sesión para ver tus listas</p>
                <Link to="/login" className="btn-primary">Iniciar Sesión</Link>
            </div>
        );
    }

    // Show loading while auth is initializing
    if (authLoading || loading) {
        return <div className="loading">Cargando listas...</div>;
    }

    return (
        <div className="lists-page">
            <div className="lists-header">
                <h1>Mis Listas</h1>
            </div>

            {error && <div className="error-message">{error}</div>}

            <form onSubmit={handleCreate} className="create-list-form">
                <input
                    type="text"
                    placeholder="Nombre de la nueva lista..."
                    value={newListName}
                    onChange={(e) => setNewListName(e.target.value)}
                    maxLength={100}
                />
                <button type="submit" disabled={creating || !newListName.trim()}>
                    {creating ? 'Creando...' : 'Crear Lista'}
                </button>
            </form>

            {lists.length === 0 ? (
                <p className="no-lists">No tienes listas todavía. ¡Crea una!</p>
            ) : (
                <div className="lists-grid">
                    {lists.map(list => (
                        <div key={list.id} className="list-card">
                            <Link to={`/list/${list.id}`} className="list-card-content">
                                <h3>{list.name}</h3>
                                <span className="list-count">{list.item_count} mangas</span>
                            </Link>
                            <button
                                type="button"
                                className="btn-delete"
                                onClick={(e) => {
                                    e.preventDefault();
                                    e.stopPropagation();
                                    openDeleteModal(list.id);
                                }}
                            >
                                🗑️
                            </button>
                        </div>
                    ))}
                </div>
            )}

            {/* Delete confirmation modal */}
            <ConfirmModal
                isOpen={deleteModalOpen}
                title="¿Estás seguro?"
                message="¿Estás seguro de que quieres eliminar esta lista? Esta acción no se puede deshacer."
                confirmText="Eliminar"
                cancelText="Cancelar"
                onConfirm={confirmDelete}
                onCancel={closeDeleteModal}
                isLoading={isDeleting}
            />
        </div>
    );
};

export default MyLists;
