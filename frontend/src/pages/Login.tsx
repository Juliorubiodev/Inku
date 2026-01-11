import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './Auth.css';

const Login: React.FC = () => {
    const { login, isConfigured, configError } = useAuth();
    const navigate = useNavigate();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [showPassword, setShowPassword] = useState(false);
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');

        // Check if Firebase is configured
        if (!isConfigured) {
            setError(configError || 'Firebase no está configurado. Verifica las variables de entorno.');
            return;
        }

        setLoading(true);

        try {
            await login(email, password);
            navigate('/');
        } catch (err: unknown) {
            const message = err instanceof Error ? err.message : 'Error al iniciar sesión';

            // Make Firebase errors more user-friendly
            if (message.includes('api-key-not-valid') || message.includes('invalid-api-key')) {
                setError('Error de configuración: API Key de Firebase inválida. Verifica las variables de entorno.');
            } else if (message.includes('user-not-found')) {
                setError('Usuario no encontrado. ¿Deseas registrarte?');
            } else if (message.includes('wrong-password') || message.includes('invalid-credential')) {
                setError('Contraseña incorrecta.');
            } else if (message.includes('too-many-requests')) {
                setError('Demasiados intentos fallidos. Intenta más tarde.');
            } else if (message.includes('network')) {
                setError('Error de conexión. Verifica tu internet.');
            } else {
                setError(message);
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="auth-page">
            <div className="auth-card">
                <h1>Iniciar Sesión</h1>
                <p className="auth-subtitle">Bienvenido de vuelta a Inku</p>

                {/* Config error banner */}
                {!isConfigured && (
                    <div className="auth-error config-error">
                        ⚠️ {configError || 'Firebase no configurado. Crea .env.local con las credenciales.'}
                    </div>
                )}

                {error && <div className="auth-error">{error}</div>}

                <form onSubmit={handleSubmit} className="auth-form">
                    <div className="form-group">
                        <label htmlFor="email">Email</label>
                        <input
                            type="email"
                            id="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            placeholder="tu@email.com"
                            required
                            autoComplete="email"
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="password">Contraseña</label>
                        <div className="password-wrapper">
                            <input
                                type={showPassword ? 'text' : 'password'}
                                id="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                placeholder="••••••••"
                                required
                                autoComplete="current-password"
                            />
                            <button
                                type="button"
                                className="password-toggle"
                                onClick={() => setShowPassword(!showPassword)}
                                aria-label={showPassword ? 'Ocultar contraseña' : 'Mostrar contraseña'}
                                title={showPassword ? 'Ocultar contraseña' : 'Mostrar contraseña'}
                            >
                                {showPassword ? '👁️' : '👁️‍🗨️'}
                            </button>
                        </div>
                    </div>

                    <button
                        type="submit"
                        className="btn-primary"
                        disabled={loading || !isConfigured}
                    >
                        {loading ? 'Cargando...' : 'Iniciar Sesión'}
                    </button>
                </form>

                <p className="auth-link">
                    ¿No tienes cuenta? <Link to="/register">Regístrate</Link>
                </p>
            </div>
        </div>
    );
};

export default Login;
