/**
 * Environment Configuration
 * 
 * This module validates environment variables and provides typed access.
 * Vite exposes env vars via import.meta.env with VITE_ prefix.
 */

// ============================================
// Environment Variable Validation
// ============================================

interface EnvConfig {
    // API URLs
    apiBaseUrl: string;
    authApiUrl: string;
    listApiUrl: string;

    // Firebase
    firebase: {
        apiKey: string;
        authDomain: string;
        projectId: string;
        storageBucket: string;
        messagingSenderId: string;
        appId: string;
    };

    // Validation status
    isValid: boolean;
    missingVars: string[];
}

// Required Firebase variables
const REQUIRED_FIREBASE_VARS = [
    'VITE_FIREBASE_API_KEY',
    'VITE_FIREBASE_PROJECT_ID',
] as const;

// Check for placeholder values that indicate unconfigured vars
const PLACEHOLDER_VALUES = [
    'your-firebase-api-key',
    'your-api-key',
    'your-api-key-here',
    'your-project-id',
    undefined,
    '',
];

function isPlaceholder(value: string | undefined): boolean {
    return PLACEHOLDER_VALUES.includes(value as string);
}

function validateEnv(): EnvConfig {
    const env = import.meta.env;

    // Check for missing or placeholder Firebase vars
    const missingVars: string[] = [];

    for (const key of REQUIRED_FIREBASE_VARS) {
        const value = env[key];
        if (!value || isPlaceholder(value)) {
            missingVars.push(key);
        }
    }

    // Additional check: API key shouldn't be a test/example value
    const apiKey = env.VITE_FIREBASE_API_KEY;
    if (apiKey && (apiKey.includes('example') || apiKey.length < 20)) {
        if (!missingVars.includes('VITE_FIREBASE_API_KEY')) {
            missingVars.push('VITE_FIREBASE_API_KEY (invalid format)');
        }
    }

    return {
        // API URLs - empty string for same-origin in production
        apiBaseUrl: env.VITE_API_BASE_URL ?? '',
        authApiUrl: env.VITE_AUTH_API_URL ?? '',
        listApiUrl: env.VITE_LIST_API_URL ?? '',

        // Firebase config
        firebase: {
            apiKey: env.VITE_FIREBASE_API_KEY ?? '',
            authDomain: env.VITE_FIREBASE_AUTH_DOMAIN ?? '',
            projectId: env.VITE_FIREBASE_PROJECT_ID ?? '',
            storageBucket: env.VITE_FIREBASE_STORAGE_BUCKET ?? '',
            messagingSenderId: env.VITE_FIREBASE_MESSAGING_SENDER_ID ?? '',
            appId: env.VITE_FIREBASE_APP_ID ?? '',
        },

        isValid: missingVars.length === 0,
        missingVars,
    };
}

// Export validated config
export const env = validateEnv();

// ============================================
// Helper Functions
// ============================================

/**
 * Check if Firebase is properly configured
 */
export function isFirebaseConfigured(): boolean {
    return env.isValid;
}

/**
 * Get user-friendly error message for missing config
 */
export function getConfigErrorMessage(): string | null {
    if (env.isValid) return null;

    const isDev = import.meta.env.DEV;
    const envFile = isDev ? '.env.local' : '.env.production';

    return `Faltan variables de entorno en ${envFile}: ${env.missingVars.join(', ')}. ` +
        'Copia .env.example y configura tus credenciales de Firebase.';
}

/**
 * Log configuration status (for debugging)
 */
export function logConfigStatus(): void {
    if (import.meta.env.DEV) {
        console.group('🔧 Inku Environment Config');
        console.log('Mode:', import.meta.env.MODE);
        console.log('API Base URL:', env.apiBaseUrl || '(same-origin)');
        console.log('Firebase Project:', env.firebase.projectId || '(not configured)');
        console.log('Config Valid:', env.isValid);
        if (!env.isValid) {
            console.warn('Missing:', env.missingVars);
        }
        console.groupEnd();
    }
}

// Log on module load in development
logConfigStatus();
