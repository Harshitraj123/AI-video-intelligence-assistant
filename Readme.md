# 🎬 AI Video Intelligence Assistant

> Transform long-form video and local media into structured, searchable knowledge using speech-to-text, LLM-powered analysis, and Retrieval-Augmented Generation (RAG).

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.64%2B-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![LangChain](https://img.shields.io/badge/LangChain-1.x-1C3C3C)](https://www.langchain.com/)
[![ChromaDB](https://img.shields.io/badge/Vector%20DB-ChromaDB-FF6F00)](https://www.trychroma.com/)
[![Whisper](https://img.shields.io/badge/Speech--to--Text-Whisper-412991)](https://github.com/openai/whisper)

---

## 📌 Overview

**AI Video Intelligence Assistant** is an end-to-end AI application that converts video or audio content into actionable, searchable information.

The system accepts either a **YouTube URL** or a **local media file**, extracts and processes the audio, transcribes the content with **OpenAI Whisper**, and uses an LLM to generate a professional title, summary, action items, key decisions, and unresolved questions.

The generated transcript is then indexed in **ChromaDB** with local **Hugging Face embeddings**, enabling users to ask natural-language questions about the analyzed video through a **RAG-powered chat interface**.

### Core workflow

```text
YouTube URL / Local Media
          │
          ▼
    Audio Extraction
          │
          ▼
   WAV Conversion + Chunking
          │
          ▼
    Whisper Transcription
          │
          ▼
      LLM Analysis
     ┌────┼───────────┐
     ▼    ▼           ▼
   Title Summary   Structured Insights
                     ├── Action Items
                     ├── Key Decisions
                     └── Open Questions
          │
          ▼
   Transcript Chunking
          │
          ▼
   Hugging Face Embeddings
          │
          ▼
       ChromaDB
          │
          ▼
     Similarity Retrieval
          │
          ▼
      LLM-powered Q&A
```

---

## ✨ Key Features

### 🎥 Flexible Video Input
- Accepts **YouTube URLs**
- Accepts **local video/audio file paths**
- Automatically detects the input type

### 🎙️ Local Speech-to-Text
- Uses **OpenAI Whisper** for transcription
- Processes long recordings in manageable audio chunks
- Supports English transcription
- Includes a Hinglish input option using Whisper translation mode

### 🧠 AI-Powered Meeting Intelligence
Automatically generates:
- **Professional title**
- **Concise summary**
- **Action items**
- **Responsible owners and deadlines** when available
- **Key decisions**
- **Open questions / follow-up topics**

### 🔎 RAG-Powered Video Q&A
- Splits transcripts into semantic chunks
- Generates embeddings locally with **all-MiniLM-L6-v2**
- Stores vectors in **ChromaDB**
- Retrieves the most relevant transcript context
- Answers questions using only the retrieved transcript context

### 💬 Interactive Streamlit Interface
- Dark, responsive UI
- Pipeline status indicators
- Full transcript viewer
- Structured result cards
- Conversational Q&A interface
- Chat history with clear-chat support

---

## 🏗️ Architecture

The project is organized as a modular pipeline rather than a single monolithic script.

```text
AI-video-intelligence-assistant/
│
├── app.py                    # Streamlit application and UI
├── main.py                   # CLI pipeline entry point
├── test.py                   # Basic transcription test
├── requirements.txt          # Python dependencies
├── .gitignore
│
├── core/
│   ├── extractor.py          # Action items, decisions, questions
│   ├── rag_engine.py         # RAG chain and Q&A
│   ├── summarizer.py         # Title generation and summarization
│   ├── transcriber.py        # Whisper transcription
│   └── vector_store.py       # ChromaDB + embeddings
│
├── utils/
│   └── audio_processor.py    # Download, conversion and chunking
│
└── vector_db/                # ChromaDB persistence directory
```

---

## 🔧 Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| UI | Streamlit |
| Video / Audio Ingestion | yt-dlp, pydub, FFmpeg |
| Speech-to-Text | OpenAI Whisper |
| LLM Orchestration | LangChain |
| LLM Provider | Groq |
| LLM Model | `openai/gpt-oss-20b` |
| Text Splitting | RecursiveCharacterTextSplitter |
| Embeddings | Hugging Face `all-MiniLM-L6-v2` |
| Vector Database | ChromaDB |
| Environment Management | python-dotenv |
| Deep Learning Runtime | PyTorch / TorchAudio |

---

## ⚙️ How It Works

### 1. Input Processing

When a user submits a source:

- A YouTube URL is downloaded using **yt-dlp**
- A local media file is converted to WAV using **pydub**
- Audio is normalized to **mono, 16 kHz WAV**
- The audio is split into **10-minute chunks**

This prevents long recordings from becoming a single oversized transcription job.

### 2. Transcription

Each audio chunk is transcribed using **OpenAI Whisper**.

The Whisper model is loaded lazily and can be selected through the `WHISPER_MODEL` environment variable. The default configured model is:

```text
small
```

### 3. Intelligent Summarization

The transcript is split into smaller sections and processed using a map-and-combine summarization flow.

The system produces:
- A short professional title
- A consolidated meeting summary

### 4. Information Extraction

The transcript is analyzed for structured meeting information:

```text
Action Items
├── Task
├── Owner
└── Deadline

Key Decisions
└── Important decisions made during the discussion

Open Questions
└── Unresolved issues requiring follow-up
```

### 5. Vectorization

For semantic retrieval, the transcript is divided into smaller chunks.

Each chunk is embedded with:

```text
all-MiniLM-L6-v2
```

The resulting embeddings are stored in **ChromaDB** with chunk metadata.

### 6. Retrieval-Augmented Generation

For every user question:

1. The question is embedded.
2. Similar transcript chunks are retrieved.
3. The top **4** relevant chunks are passed as context.
4. The Groq-hosted LLM generates the answer.
5. The prompt explicitly constrains the assistant to answer from the transcript context.

When relevant information is not present, the system is instructed to state that it could not find the information in the transcript.

---

## 🚀 Getting Started

### Prerequisites

Install the following before running the project:

- Python **3.10+**
- **FFmpeg**
- Git
- A Groq API key

> **Note:** Whisper and PyTorch can require substantial CPU/RAM resources. Processing time depends on the recording length and available hardware.

### 1. Clone the repository

```bash
git clone https://github.com/Harshitraj123/AI-video-intelligence-assistant.git
cd AI-video-intelligence-assistant
```

### 2. Create a virtual environment

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
WHISPER_MODEL=small
```

Do not commit your API key to GitHub.

### 5. Start the Streamlit application

```bash
streamlit run app.py
```

Then open the local Streamlit URL shown in your terminal.

---

## 🖥️ Usage

### From the Streamlit UI

1. Enter a **YouTube URL** or **local file path** in the sidebar.
2. Select the language option.
3. Click **Analyse Video**.
4. Wait for the processing pipeline to complete.
5. Review the generated:
   - Title
   - Summary
   - Transcript
   - Action Items
   - Key Decisions
   - Open Questions
6. Ask follow-up questions in **Chat with your Video**.

### CLI mode

The project also includes a command-line pipeline through `main.py`:

```bash
python main.py
```

You will be prompted for:
- YouTube URL or local file path
- Language

---

## 📊 Example Output

After analysis, the application presents:

```text
📌 Session Title
Professional meeting title

📋 Summary
• Main discussion point
• Important conclusions
• Key outcomes

✅ Action Items
1. Task — Owner — Deadline

🔑 Key Decisions
1. Decision made during the discussion

❓ Open Questions
1. Follow-up topic requiring clarification

💬 Chat with your Video
User: What were the main decisions?
Assistant: ...
```

---

## 🧪 Testing

A small transcription test is provided in `test.py`.

Run:

```bash
python test.py
```

The test downloads audio from the configured YouTube example, processes the audio chunks, and prints the beginning of the generated transcript.

---

## 🔐 Environment & Security

The project expects API credentials to be supplied through environment variables.

Recommended practice:

```text
.env
   │
   ├── GROQ_API_KEY
   └── WHISPER_MODEL
```

The API key should never be hard-coded in source code or committed to version control.

---

## 📁 Project Design Principles

The codebase separates major responsibilities into independent modules:

- **Input processing** handles acquisition and audio preparation.
- **Transcription** handles speech-to-text.
- **Summarization** handles title and summary generation.
- **Extraction** handles structured meeting intelligence.
- **Vector storage** handles embedding and persistence.
- **RAG engine** handles retrieval and question answering.
- **Streamlit UI** handles user interaction and presentation.

This separation makes the project easier to test, maintain, and extend.

---

## 🔮 Future Improvements

Potential extensions include:

- Timestamp-aware answers and citations
- Speaker diarization
- Automatic topic segmentation
- Multi-video knowledge bases
- Conversation memory across sessions
- Better retrieval with hybrid search
- Background processing for long recordings
- GPU acceleration for Whisper
- Authentication and user-specific workspaces
- Export of summaries and insights to PDF/Markdown
- Deployment with Docker and cloud infrastructure

---

## 🧑‍💻 Author

**Harshit Raj**

Computer Science & Engineering Student  
BMS Institute of Technology and Management

GitHub: https://github.com/Harshitraj123  
LinkedIn: https://linkedin.com/in/harshitraj010204

---

## ⭐ Project Highlights

This project demonstrates practical experience with:

- End-to-end **AI application development**
- **Speech-to-text** pipelines
- **LLM application development**
- **Retrieval-Augmented Generation**
- **Vector databases**
- **Semantic search**
- **Modular Python architecture**
- **Streamlit application development**
- Integration of local models with hosted LLM APIs

---

## 📜 License

Add an appropriate open-source license before publicly distributing the project.

---

<p align="center">
  Built with Python, Whisper, LangChain, ChromaDB, Groq and Streamlit.
</p>
