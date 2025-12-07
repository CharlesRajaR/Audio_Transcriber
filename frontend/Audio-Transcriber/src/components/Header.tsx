import styles from './Header.module.css';
import type { HeaderProps } from '../types';

export function Header(_props: HeaderProps) {
  return (
    <header className={styles.header}>
      <h1 className={styles.title}>Super AI Transcript</h1>
      <p className={styles.subtitle}>
        Record audio or upload a file to transcribe with AI
      </p>
    </header>
  );
}