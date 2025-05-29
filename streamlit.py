#!/usr/bin/env python
# coding: utf-8

# In[1]:


# streamlit.py
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import tempfile
import os
import time
import base64
from orchestrator import Orchestrator
from AI_AGENTS import finance_agent_executor
from agents.voice_agent import VoiceAgent 

# Initialize orchestrator and voice agent
orchestrator = Orchestrator(agent_executor=finance_agent_executor)
voice_agent = VoiceAgent()

# --- Page setup ---
st.set_page_config(page_title="Karthick’s AI Finance Assistant", layout="centered")
st.title("💰 Karthick’s AI Finance Assistant")
st.markdown("Ask a financial question by typing, speaking, or uploading a financial PDF.")

# --- Input section ---
st.subheader("1. Enter your question")

query = st.text_input("💬 Type your question:", placeholder="e.g., What’s our exposure to Asia tech?")
st.markdown("Or record your voice:")

# --- Voice recording widget ---
audio_file = st.file_uploader("🎤 Upload a voice file (.wav, .mp3)", type=["wav", "mp3"])

# --- PDF Upload ---
uploaded_pdf = st.file_uploader("📄 Optional: Upload a financial PDF", type=["pdf"])

# --- Process Button ---
if st.button("🧠 Get Answer"):
    if not query and not audio_file:
        st.warning("⚠️ Please type a question or upload a voice recording.")
    else:
        if audio_file and not query:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_audio:
                tmp_audio.write(audio_file.read())
                tmp_audio_path = tmp_audio.name

            with st.spinner("🗣️ Transcribing your question..."):
                query = voice_agent.transcribe_audio(tmp_audio_path)

            st.success(f"✅ Transcribed: {query}")

        with st.spinner("🔍 Processing your query..."):
            if uploaded_pdf:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
                    tmp_pdf.write(uploaded_pdf.read())
                    result = orchestrator.process_query(query, pdf_path=tmp_pdf.name)
            else:
                result = orchestrator.process_query(query)

        st.success("✅ Answer:")
        st.write(result)

        # --- Voice Output ---
        st.markdown("🔊 Playing answer aloud...")
        voice_agent.synthesize_speech(result)

        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.save_to_file(result, "output.mp3")
            engine.runAndWait()
            audio_bytes = open("output.mp3", "rb").read()
            st.audio(audio_bytes, format="audio/mp3")
        except Exception as e:
            st.warning(f"Audio playback failed: {e}")

# --- Footer ---
st.markdown("---")
st.caption("Built with LangChain, Groq, Whisper, and 💙 by **Karthick**")

