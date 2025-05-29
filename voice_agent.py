#!/usr/bin/env python
# coding: utf-8

# In[1]:


# agents/voice_agent.py

import whisper
import pyttsx3


class VoiceAgent:
    def __init__(self, whisper_model_size="base"):
        self.stt_model = whisper.load_model(whisper_model_size)
        self.tts_engine = pyttsx3.init()

    def transcribe_audio(self, file_path: str) -> str:
        """
        Converts audio speech to text using Whisper.
        Args:
            file_path (str): Path to the audio file.
        Returns:
            str: Transcribed text.
        """
        try:
            result = self.stt_model.transcribe(file_path)
            return result["text"]
        except Exception as e:
            return f"[STT Error]: {e}"

    def synthesize_speech(self, text: str):
        """
        Converts text to speech using pyttsx3.
        Args:
            text (str): Text to be spoken aloud.
        """
        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            print(f"[TTS Error]: {e}")

