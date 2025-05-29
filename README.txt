# 💰 Karthick’s AI Finance Assistant

A multi-agent financial assistant that answers spoken or typed market questions, processes PDFs, and summarizes financial data using real-time sources, RAG pipelines, and language models — all within a sleek Streamlit app.

---

## 🧠 Use Case

> “What’s our risk exposure in Asia tech stocks today, and highlight any earnings surprises?”

### ✅ Sample Response:
> *Today, your Asia tech allocation is 22% of AUM, up from 18% yesterday. TSMC beat estimates by 4%, Samsung missed by 2%. Regional sentiment is neutral with a cautionary tilt due to rising yields.*

---

## 🏗️ Architecture Overview

```mermaid
flowchart TD
    A[User Input] -->|Voice/Text| B[Streamlit UI]
    B --> C[Voice Agent (STT)]
    B --> D[PDF Upload]
    C --> E[Orchestrator]
    D --> E
    E -->|If PDF| F[Retriever Agent (FAISS)]
    E -->|If market data| G[API Agent (Yahoo Finance)]
    E -->|If headlines| H[Scraping Agent (BeautifulSoup)]
    E --> I[Language Agent (ChatGroq)]
    I --> J[TTS via pyttsx3]
    J --> K[Audio Output]
    I --> L[Streamlit Text Output]
```

---

## 🧩 Agent Breakdown

| Agent              | Role                                                                 |
|-------------------|----------------------------------------------------------------------|
| **API Agent**      | Pulls stock and market data via `yfinance`.                         |
| **Scraping Agent**| Scrapes real-time headlines from Yahoo Finance.                     |
| **Retriever Agent**| Indexes and retrieves top chunks from PDFs using FAISS.            |
| **Language Agent**| Synthesizes summaries using LLM (`ChatGroq` from `langchain-groq`). |
| **Voice Agent**    | Handles voice input (Whisper STT) and output (pyttsx3 TTS).         |
| **Orchestrator**   | Routes input to correct agents and assembles final response.       |

---

## 🧪 Features

- ✅ Voice & Text input
- ✅ PDF upload and retrieval
- ✅ Financial summarization via LLM
- ✅ Headline scraping
- ✅ Spoken output via TTS
- ✅ Modular, agent-based design

---

## ⚙️ Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/your-username/finance-agent.git
cd finance-agent
```

### 2. Create a Virtual Environment (Python 3.10 recommended)

```bash
python -m venv venv
.
env\Scripts ctivate  # Windows
```

### 3. Install Requirements

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Add Your API Keys

Create a `.env` file:

```env
groq_api=your_groq_api_key
huggingface_api=your_huggingface_key
langchain_api=your_langchain_key
langsmith_api=your_langsmith_key
```

### 5. Run Locally

```bash
streamlit run app.py
```

---

## 🚀 Deploy on Streamlit Cloud

1. Push your repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo and set:
   - Main file: `app.py`
   - Secrets: paste `.env` values into Streamlit’s **Secrets Manager**

✅ Share the URL once live!

---

## 📁 Project Structure

```
AI_Finance_Assistant/
├── app.py
├── orchestrator.py
├── AI_AGENTS.py
├── requirements.txt
├── .env
├── agents/
│   ├── __init__.py
│   ├── language_agent.py
│   ├── retriver_agent.py
│   ├── scraping_agent.py
│   └── voice_agent.py
└── docs/
    └── ai_tool_usage.md
```

---

## 🧠 AI Tooling Log

See [`docs/ai_tool_usage.md`](docs/ai_tool_usage.md) for detailed prompts and LLM usage.

---

## 🏁 Credits

- Built by **Karthick**
- Powered by Streamlit, LangChain, Groq, Whisper, FAISS


---

## 🛠️ Manual Contributions (What I Built Myself)

This project was built through a combination of custom coding, toolkit integration, and prompt engineering. Here's what was done manually:

### ✅ Architecture & Agents
- Designed modular architecture with clearly separated agents
- Wrote orchestration logic from scratch in `orchestrator.py`
- Created custom `VoiceAgent` with Whisper and `pyttsx3`
- Implemented PDF-to-FAISS pipeline manually in `retriver_agent.py`

### ✅ Prompt & LLM Engineering
- Wrote prompts to guide ChatGroq for summarizing finance context
- Configured fallback behavior to general-purpose agent when no clear route

### ✅ Data & Tools Integration
- Manually integrated Yahoo Finance via `yfinance`
- Used BeautifulSoup to scrape headlines
- Connected FAISS and Ollama embeddings for retrieval
- Setup `.env` manually with Groq, LangChain, and Hugging Face keys

---

## 🧠 AI Assistance Usage

| Task                          | How AI Helped                          |
|------------------------------|----------------------------------------|
| Folder structuring           | Used GPT to suggest modular layout     |
| LangChain integration        | Got syntax and structure suggestions   |
| Streamlit layout             | Refined input/output flow with GPT     |
| Prompt writing               | Iterated summaries for ChatGroq        |
| Requirements cleanup         | Suggested lighter versions to avoid memory errors |

See detailed log in `docs/ai_tool_usage.md` (to be added).

---

## 💡 Lessons Learned

- Running large LLMs locally requires memory-aware pip installs
- Streamlit + LangChain + Whisper + FAISS work best modularized
- GPT can help scaffold but custom logic is always needed
- Groq LLMs are very fast for low-latency RAG-based systems

--