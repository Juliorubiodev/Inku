import { initializeApp } from 'firebase/app';
import type { FirebaseApp } from 'firebase/app';
import {
    getAuth,
    signInWithEmailAndPassword,
    createUserWithEmailAndPassword,
    signOut,
    onAuthStateChanged,
    updateProfile,
} from 'firebase/auth';
import type { User, Auth } from 'firebase/auth';
import { env, isFirebaseConfigured, getConfigErrorMessage } from '../config/env';

// Firebase configuration from validated env
const firebaseConfig = {
    apiKey: env.firebase.apiKey,
    authDomain: env.firebase.authDomain,
    projectId: env.firebase.projectId,
    storageBucket: env.firebase.storageBucket,
    messagingSenderId: env.firebase.messagingSenderId,
    appId: env.firebase.appId,
};

// Initialize Firebase only if configured
let app: FirebaseApp | null = null;
let auth: Auth | null = null;
let initError: string | null = null;

if (isFirebaseConfigured()) {
    try {
        app = initializeApp(firebaseConfig);
        auth = getAuth(app);
    } catch (error) {
        console.error('❌ Firebase initialization failed:', error);
        initError = error instanceof Error ? error.message : 'Unknown error';
    }
} else {
    initError = getConfigErrorMessage();
    console.error('❌ Firebase not configured:', initError);
}

// Export auth (may be null if not configured)
export { auth };

// Re-export config check
export { isFirebaseConfigured };

/**
 * Get initialization error if any
 */
export function getFirebaseError(): string | null {
    return initError;
}

// ============================================
// Auth Functions
// ============================================

export const login = async (email: string, password: string) => {
    if (!auth) {
        throw new Error(initError || 'Firebase no está configurado. Verifica las variables de entorno.');
    }
    return signInWithEmailAndPassword(auth, email, password);
};

export const register = async (email: string, password: string) => {
    if (!auth) {
        throw new Error(initError || 'Firebase no está configurado. Verifica las variables de entorno.');
    }
    return createUserWithEmailAndPassword(auth, email, password);
};

export const logout = async () => {
    if (!auth) {
        throw new Error('No auth instance available');
    }
    return signOut(auth);
};

export const updateUserProfile = async (displayName: string) => {
    if (!auth?.currentUser) {
        throw new Error('No user logged in');
    }
    return updateProfile(auth.currentUser, { displayName });
};

export const getIdToken = async (forceRefresh = false): Promise<string | null> => {
    if (!auth?.currentUser) return null;
    return auth.currentUser.getIdToken(forceRefresh);
};

export { onAuthStateChanged, type User };
