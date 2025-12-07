import styles from './Spinner.module.css';

export function Spinner() {
  return (
    <div className={styles.spinner} role="status" aria-label="Loading">
      <div className={styles.spinnerCircle}></div>
    </div>
  );
}