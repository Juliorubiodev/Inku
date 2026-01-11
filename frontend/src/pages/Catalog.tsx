import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { mangaService } from '../lib/api';
import { resolveCoverUrl } from '../lib/cover';
import type { Manga } from '../types';
import './Catalog.css';

// Individual manga card component with error handling for cover
const MangaCard: React.FC<{ manga: Manga }> = ({ manga }) => {
    const [coverError, setCoverError] = useState(false);
    const coverUrl = resolveCoverUrl(manga);

    return (
        <Link to={`/manga/${manga.id}`} className="manga-card">
            <div className="manga-cover">
                {coverUrl && !coverError ? (
                    <img
                        src={coverUrl}
                        alt={manga.title}
                        onError={() => setCoverError(true)}
                    />
                ) : (
                    <div className="manga-cover-placeholder">📖</div>
                )}
            </div>
            <div className="manga-info">
                <h3>{manga.title || manga.id}</h3>
                {manga.tags.length > 0 && (
                    <div className="manga-tags">
                        {manga.tags.slice(0, 3).map(tag => (
                            <span key={tag} className="tag">{tag}</span>
                        ))}
                    </div>
                )}
            </div>
        </Link>
    );
};

const Catalog: React.FC = () => {
    const [mangas, setMangas] = useState<Manga[]>([]);
    const [search, setSearch] = useState('');
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        loadMangas();
    }, []);

    const loadMangas = async () => {
        try {
            const data = await mangaService.getMangas();
            setMangas(data);
        } catch (err: any) {
            setError('Error al cargar el catálogo');
        } finally {
            setLoading(false);
        }
    };

    const filteredMangas = mangas.filter(manga =>
        manga.title.toLowerCase().includes(search.toLowerCase()) ||
        manga.tags.some(tag => tag.toLowerCase().includes(search.toLowerCase()))
    );

    if (loading) {
        return <div className="loading">Cargando catálogo...</div>;
    }

    return (
        <div className="catalog-page">
            <div className="catalog-header">
                <h1>Catálogo de Manga</h1>
                <div className="search-box">
                    <input
                        type="text"
                        placeholder="Buscar por título o tag..."
                        value={search}
                        onChange={(e) => setSearch(e.target.value)}
                    />
                </div>
            </div>

            {error && <div className="error-message">{error}</div>}

            <div className="manga-grid">
                {filteredMangas.length === 0 ? (
                    <p className="no-results">No se encontraron mangas</p>
                ) : (
                    filteredMangas.map(manga => (
                        <MangaCard key={manga.id} manga={manga} />
                    ))
                )}
            </div>
        </div>
    );
};

export default Catalog;

