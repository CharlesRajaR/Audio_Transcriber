from pathlib import Path
from faster_whisper import WhisperModel
from google import genai
from google.genai import types

PROMPT_FILE = Path(__file__).parent/"system_prompt.txt"
SYSTEM_PROMPT = PROMPT_FILE.read_text().strip()

class TranscriptionService:
    "Uses faster whisper for transcription and gemini api for cleaning"

    def __init__(self, whisper_model:str, llm_api_key:str, llm_model:str):
        self.whisper = WhisperModel(whisper_model, device="auto", compute_type="int8")

        try:
           self.llm_client = genai.Client(api_key=llm_api_key)
           self.llm_model = llm_model

           self.llm_client.models.list()

        except Exception as e:
            print("Could not connect to gemini llm")
    
    def transcribe(self, audio_file):
        segments, info = self.whisper.transcribe(audio_file, 
                                                 beam_size=5,
                                                 language="en",
                                                 condition_on_previous_text=False)
        text = "".join([segment.text for segment in segments]).strip()

        return text
    
    def get_default_system_prompt(self):
       return SYSTEM_PROMPT
    
    def clean_with_llm(self, text, system_prompt = None):
        if not text:
            return ""
        
        prompt_to_use = system_prompt if system_prompt else SYSTEM_PROMPT

        try:

            config = types.GenerateContentConfig(system_instruction=prompt_to_use,
                                             temperature=0.3,
                                             max_output_tokens=200)
            response = self.llm_client.models.generate_content(
            model=self.llm_model,
            contents=[text],
            config=config
            )
   
            cleaned = response.text.strip()

            return cleaned

        except Exception as e:
            return text
        
    def transcribe_file(self, audio_file_path: str, use_llm: bool = True):

        raw_text = self.transcribe(audio_file=audio_file_path)

        result = {"raw_text": raw_text}

        if use_llm and raw_text:
            cleaned_text = self.clean_with_llm(raw_text)

            result["cleaned_text"] = cleaned_text

        else:
            result["cleaned_text"] = raw_text

        return result
    



# if __name__ == "__main__":
#     print(SYSTEM_PROMPT)