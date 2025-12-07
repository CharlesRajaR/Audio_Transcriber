import { AlertCircle, X } from 'lucide-react';
import styles from './ErrorMessage.module.css';
import type { ErrorMessageProps } from '../types';

export function ErrorMessage({ message, onDismiss }: ErrorMessageProps) {
  return (
    <div className={styles.container} role="alert">
      <div className={styles.content}>
        <AlertCircle className={styles.icon} />
        <p className={styles.message}>{message}</p>
      </div>
      <button
        onClick={onDismiss}
        className={styles.closeButton}
        aria-label="Dismiss error"
      >
        <X className={styles.closeIcon} />
      </button>
    </div>
  );
}