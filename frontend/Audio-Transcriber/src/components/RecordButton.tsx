import { Mic, Square, Loader2 } from 'lucide-react';
import styles from './RecordButton.module.css';
import type { RecordButtonProps } from '../types';

export function RecordButton({
  isRecording,
  isProcessing,
  onStartRecording,
  onStopRecording,
}: RecordButtonProps) {
  const handleClick = () => {
    if (isProcessing) return;
    if (isRecording) {
      onStopRecording();
    } else {
      void onStartRecording();
    }
  };

  const getButtonContent = () => {
    if (isProcessing) {
      return (
        <>
          <Loader2 className={styles.icon} />
          <span>Processing...</span>
        </>
      );
    }

    if (isRecording) {
      return (
        <>
          <Square className={styles.icon} />
          <span>Stop Recording</span>
        </>
      );
    }

    return (
      <>
        <Mic className={styles.icon} />
        <span>Start Recording</span>
      </>
    );
  };

  const buttonClass = `${styles.button} ${isRecording ? styles.recording : ''} ${isProcessing ? styles.processing : ''}`;

  return (
    <div className={styles.container}>
      <button
        onClick={handleClick}
        disabled={isProcessing}
        className={buttonClass}
        aria-label={
          isProcessing
            ? 'Processing audio'
            : isRecording
              ? 'Stop recording'
              : 'Start recording'
        }
      >
        {getButtonContent()}
      </button>
      <p className={styles.hint}>Hold &quot;V&quot; key to record</p>
    </div>
  );
}