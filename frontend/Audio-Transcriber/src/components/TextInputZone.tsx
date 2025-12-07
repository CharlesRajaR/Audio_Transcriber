import { FileText } from 'lucide-react';
import { useState } from 'react';
import styles from './TextInputZone.module.css';
import type { TextInputZoneProps } from '../types';
import { TextBox } from './TextBox';
import { Box } from './Box';

export function TextInputZone({
  isProcessing,
  onTextSubmit,
}: TextInputZoneProps) {
  const [inputText, setInputText] = useState('');

  const handleSubmit = async () => {
    if (!inputText.trim() || isProcessing) {
      return;
    }

    await onTextSubmit(inputText.trim());
    setInputText(''); // Clear after successful submission
  };

  const isDisabled = isProcessing || !inputText.trim();

  return (
    <div className={styles.container}>
      <div className={styles.divider}>
        <span>OR</span>
      </div>

      <Box header="Paste Text Transcript" icon={FileText}>
        <TextBox
          mode="input"
          variant="default"
          value={inputText}
          onChange={setInputText}
          placeholder="Paste your transcript here..."
          isDisabled={isProcessing}
          rows={3}
          ariaLabel="Text transcript input"
        />

        <button
          className={`${styles.button} ${isDisabled ? styles.disabled : ''}`}
          onClick={handleSubmit}
          disabled={isDisabled}
          type="button"
        >
          {isProcessing ? 'Processing...' : 'Process Text'}
        </button>
      </Box>
    </div>
  );
}