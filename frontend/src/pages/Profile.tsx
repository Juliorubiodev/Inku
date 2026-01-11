import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './Profile.css';

const Profile: React.FC = () => {
    const { user, updateProfile, logout } = useAuth();
    const [displayName, setDisplayName] = useState(user?.displayName || '');
    const [saving, setSaving] = useState(false);
    const [message, setMessage] = useState('');
    const [error, setError] = useState('');

    const handleSave = async (e: React.FormEvent) => {
        e.preventDefault();
        setSaving(true);
        setError('');
        setMessage('');

        try {
            await updateProfile(displayName);
            setMessage('Perfil actualizado correctamente');
        } catch (err: any) {
            setError(err.message || 'Error al actualizar el perfil');
        } finally {
            setSaving(false);
        }
    };

    if (!user) {
        return (
            <div className="auth-required">
                <h2>Inicia sesión</h2>
                <p>Necesitas iniciar sesión para ver tu perfil</p>
                <Link to="/login" className="btn-primary">Iniciar Sesión</Link>
            </div>
        );
    }

    return (
        <div className="profile-page">
            <h1>Mi Perfil</h1>

            <div className="profile-card">
                <div className="profile-avatar">
                    {user.photoURL ? (
                        <img src={user.photoURL} alt={user.displayName || 'Avatar'} />
                    ) : (
                        <span>{(user.displayName || user.email || 'U')[0].toUpperCase()}</span>
                    )}
                </div>

                <div className="profile-info">
                    <p className="profile-email">{user.email}</p>
                    <p className="profile-uid">UID: {user.uid}</p>
                </div>
            </div>

            {message && <div className="success-message">{message}</div>}
            {error && <div className="error-message">{error}</div>}

            <form onSubmit={handleSave} className="profile-form">
                <div className="form-group">
                    <label htmlFor="displayName">Nombre de usuario</label>
                    <input
                        type="text"
                        id="displayName"
                        value={displayName}
                        onChange={(e) => setDisplayName(e.target.value)}
                        placeholder="Tu nombre..."
                        maxLength={50}
                    />
                </div>

                <button type="submit" className="btn-save" disabled={saving}>
                    {saving ? 'Guardando...' : 'Guardar Cambios'}
                </button>
            </form>

            <div className="profile-actions">
                <button onClick={logout} className="btn-logout-profile">
                    Cerrar Sesión
                </button>
            </div>
        </div>
    );
};

export default Profile;
