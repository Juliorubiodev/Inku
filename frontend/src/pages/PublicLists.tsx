import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { listService } from '../lib/api';
import type { ListSummary } from '../types';
import './Lists.css';

const PublicLists: React.FC = () => {
    const [lists, setLists] = useState<ListSummary[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [page, setPage] = useState(1);
    const [total, setTotal] = useState(0);

    useEffect(() => {
        loadLists();
    }, [page]);

    const loadLists = async () => {
        setLoading(true);
        try {
            const { lists: data, total: count } = await listService.getPublicLists(page, 20);
            setLists(data);
            setTotal(count);
        } catch (err: any) {
            setError('Error al cargar las listas');
        } finally {
            setLoading(false);
        }
    };

    if (loading && page === 1) {
        return <div className="loading">Cargando listas públicas...</div>;
    }

    return (
        <div className="lists-page">
            <div className="lists-header">
                <h1>Listas Públicas</h1>
                <p className="lists-subtitle">{total} listas compartidas por la comunidad</p>
            </div>

            {error && <div className="error-message">{error}</div>}

            {lists.length === 0 ? (
                <p className="no-lists">No hay listas públicas todavía</p>
            ) : (
                <div className="lists-grid">
                    {lists.map(list => (
                        <Link to={`/list/${list.id}`} key={list.id} className="list-card public">
                            <div className="list-card-content">
                                <h3>{list.name}</h3>
                                <div className="list-meta">
                                    <span className="list-author">por {list.owner_name || 'Desconocido'}</span>
                                    <span className="list-count">{list.item_count} mangas</span>
                                </div>
                            </div>
                        </Link>
                    ))}
                </div>
            )}

            {total > 20 && (
                <div className="pagination">
                    <button
                        disabled={page === 1}
                        onClick={() => setPage(p => p - 1)}
                    >
                        ← Anterior
                    </button>
                    <span>Página {page}</span>
                    <button
                        disabled={lists.length < 20}
                        onClick={() => setPage(p => p + 1)}
                    >
                        Siguiente →
                    </button>
                </div>
            )}
        </div>
    );
};

export default PublicLists;
