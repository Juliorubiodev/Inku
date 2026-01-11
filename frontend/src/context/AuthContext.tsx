import React, { createContext, useContext, useEffect, useState } from 'react';
import {
    auth,
    onAuthStateChanged,
    login as firebaseLogin,
    register as firebaseRegister,
    logout as firebaseLogout,
    updateUserProfile,
    isFirebaseConfigured,
    getFirebaseError,
    type User,
} from '../lib/firebase';
import type { AuthUser } from '../types';

interface AuthContextType {
    user: AuthUser | null;
    loading: boolean;
    isConfigured: boolean;
    configError: string | null;
    login: (email: string, password: string) => Promise<void>;
    register: (email: string, password: string) => Promise<void>;
    logout: () => Promise<void>;
    updateProfile: (displayName: string) => Promise<void>;
}

const AuthContext = createContext<AuthContextType | null>(null);

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within AuthProvider');
    }
    return context;
};

const mapFirebaseUser = (user: User | null): AuthUser | null => {
    if (!user) return null;
    return {
        uid: user.uid,
        email: user.email,
        displayName: user.displayName,
        photoURL: user.photoURL,
    };
};

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [user, setUser] = useState<AuthUser | null>(null);
    const [loading, setLoading] = useState(true);

    // Check if Firebase is configured
    const isConfigured = isFirebaseConfigured();
    const configError = getFirebaseError();

    useEffect(() => {
        // If Firebase is not configured, stop loading immediately
        if (!isConfigured || !auth) {
            setLoading(false);
            return;
        }

        const unsubscribe = onAuthStateChanged(auth, (firebaseUser) => {
            setUser(mapFirebaseUser(firebaseUser));
            setLoading(false);
        });
        return unsubscribe;
    }, [isConfigured]);

    const handleLogin = async (email: string, password: string) => {
        const result = await firebaseLogin(email, password);
        setUser(mapFirebaseUser(result.user));
    };

    const handleRegister = async (email: string, password: string) => {
        const result = await firebaseRegister(email, password);
        setUser(mapFirebaseUser(result.user));
    };

    const handleLogout = async () => {
        await firebaseLogout();
        setUser(null);
    };

    const handleUpdateProfile = async (displayName: string) => {
        await updateUserProfile(displayName);
        if (auth?.currentUser) {
            setUser(mapFirebaseUser(auth.currentUser));
        }
    };

    return (
        <AuthContext.Provider
            value={{
                user,
                loading,
                isConfigured,
                configError,
                login: handleLogin,
                register: handleRegister,
                logout: handleLogout,
                updateProfile: handleUpdateProfile,
            }}
        >
            {children}
        </AuthContext.Provider>
    );
};
