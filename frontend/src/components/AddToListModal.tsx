import React, { useEffect, useState } from 'react';
import { listService } from '../lib/api';
import type { ListSummary } from '../types';
import './AddToListModal.css';

interface AddToListModalProps {
    isOpen: boolean;
    onClose: () => void;
    mangaId: string;
}

const AddToListModal: React.FC<AddToListModalProps> = ({
    isOpen,
    onClose,
    mangaId,
}) => {
    const [lists, setLists] = useState<ListSummary[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [addingToListId, setAddingToListId] = useState<string | null>(null);
    const [addedToLists, setAddedToLists] = useState<Set<string>>(new Set());

    useEffect(() => {
        if (isOpen) {
            loadMyLists();
            setAddedToLists(new Set());
        }
    }, [isOpen]);

    const loadMyLists = async () => {
        setLoading(true);
        setError('');
        try {
            const { lists: myLists } = await listService.getMyLists();
            setLists(myLists);
        } catch (err: any) {
            setError('Error al cargar tus listas');
        } finally {
            setLoading(false);
        }
    };

    const handleAddToList = async (listId: string) => {
        setAddingToListId(listId);
        setError('');
        try {
            await listService.addMangaToList(listId, mangaId);
            setAddedToLists(prev => new Set(prev).add(listId));
        } catch (err: any) {
            if (err.response?.status === 400 || err.message?.includes('duplicate')) {
                setAddedToLists(prev => new Set(prev).add(listId));
            } else {
                setError(err.message || 'Error al agregar a la lista');
            }
        } finally {
            setAddingToListId(null);
        }
    };

    if (!isOpen) return null;

    return (
        <div className="modal-overlay" onClick={onClose}>
            <div className="modal-content add-to-list-modal" onClick={e => e.stopPropagation()}>
                <div className="modal-header">
                    <h2>Agregar a una lista</h2>
                    <button className="modal-close" onClick={onClose}>✕</button>
                </div>

                {error && <div className="modal-error">{error}</div>}

                <div className="modal-body">
                    {loading ? (
                        <div className="modal-loading">Cargando tus listas...</div>
                    ) : lists.length === 0 ? (
                        <div className="modal-empty">
                            <p>No tienes listas creadas.</p>
                            <p className="modal-hint">Ve a "Mis Listas" para crear una.</p>
                        </div>
                    ) : (
                        <div className="lists-select">
                            {lists.map(list => {
                                const isAdding = addingToListId === list.id;
                                const isAdded = addedToLists.has(list.id);

                                return (
                                    <div key={list.id} className="list-select-item">
                                        <div className="list-select-info">
                                            <h4>{list.name}</h4>
                                            <span className="list-count">{list.item_count} mangas</span>
                                        </div>
                                        <button
                                            className={`btn-add-to-list ${isAdded ? 'added' : ''}`}
                                            onClick={() => handleAddToList(list.id)}
                                            disabled={isAdding || isAdded}
                                        >
                                            {isAdding ? '...' : isAdded ? '✓ Añadido' : 'Añadir'}
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

export default AddToListModal;
