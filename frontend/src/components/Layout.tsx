import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './Layout.css';

interface LayoutProps {
    children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
    const { user, logout } = useAuth();
    const navigate = useNavigate();

    const handleLogout = async () => {
        await logout();
        navigate('/');
    };

    return (
        <div className="layout">
            <header className="header">
                <div className="header-content">
                    <Link to="/" className="logo">
                        <img src="/logo.png" alt="Inku Logo" className="logo-image" />
                        <span className="logo-text">Inku</span>
                    </Link>

                    <nav className="nav">
                        <Link to="/" className="nav-link">Catálogo</Link>
                        <Link to="/lists" className="nav-link">Listas Públicas</Link>
                        {user && (
                            <>
                                <Link to="/my-lists" className="nav-link">Mis Listas</Link>
                                <Link to="/upload" className="nav-link">Subir</Link>
                            </>
                        )}
                    </nav>

                    <div className="user-section">
                        {user ? (
                            <div className="user-menu">
                                <Link to="/profile" className="user-name">
                                    {user.displayName || user.email}
                                </Link>
                                <button onClick={handleLogout} className="btn-logout">
                                    Salir
                                </button>
                            </div>
                        ) : (
                            <div className="auth-buttons">
                                <Link to="/login" className="btn-login">Iniciar Sesión</Link>
                                <Link to="/register" className="btn-register">Registrarse</Link>
                            </div>
                        )}
                    </div>
                </div>
            </header>

            <main className="main-content">
                {children}
            </main>

            <footer className="footer">
                <p>© 2026 Inku - Manga Reader</p>
            </footer>
        </div>
    );
};

export default Layout;
