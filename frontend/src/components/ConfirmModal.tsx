import React, { useEffect, useRef } from 'react';
import './ConfirmModal.css';

interface ConfirmModalProps {
    isOpen: boolean;
    title: string;
    message: string;
    confirmText?: string;
    cancelText?: string;
    onConfirm: () => void;
    onCancel: () => void;
    isLoading?: boolean;
}

const ConfirmModal: React.FC<ConfirmModalProps> = ({
    isOpen,
    title,
    message,
    confirmText = 'Eliminar',
    cancelText = 'Cancelar',
    onConfirm,
    onCancel,
    isLoading = false,
}) => {
    const confirmButtonRef = useRef<HTMLButtonElement>(null);

    useEffect(() => {
        if (isOpen) {
            // Focus on confirm button when modal opens for accessibility
            confirmButtonRef.current?.focus();

            // Handle ESC key to close modal
            const handleEsc = (e: KeyboardEvent) => {
                if (e.key === 'Escape' && !isLoading) {
                    onCancel();
                }
            };
            document.addEventListener('keydown', handleEsc);
            return () => document.removeEventListener('keydown', handleEsc);
        }
    }, [isOpen, isLoading, onCancel]);

    if (!isOpen) return null;

    return (
        <div className="confirm-modal-overlay" onClick={!isLoading ? onCancel : undefined}>
            <div className="confirm-modal" onClick={(e) => e.stopPropagation()}>
                <button
                    className="confirm-modal-close"
                    onClick={onCancel}
                    disabled={isLoading}
                    aria-label="Cerrar"
                >
                    ✕
                </button>

                <div className="confirm-modal-content">
                    <h2 className="confirm-modal-title">{title}</h2>
                    <p className="confirm-modal-message">{message}</p>

                    <div className="confirm-modal-actions">
                        <button
                            className="confirm-modal-btn confirm-modal-btn-cancel"
                            onClick={onCancel}
                            disabled={isLoading}
                        >
                            {cancelText}
                        </button>
                        <button
                            ref={confirmButtonRef}
                            className="confirm-modal-btn confirm-modal-btn-confirm"
                            onClick={onConfirm}
                            disabled={isLoading}
                        >
                            {isLoading ? 'Eliminando...' : confirmText}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ConfirmModal;
