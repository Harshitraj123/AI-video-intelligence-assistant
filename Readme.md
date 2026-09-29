# 🎬 AI Video Intelligence Assistant

> An end-to-end AI application that converts long-form videos and local media into structured, searchable knowledge using speech-to-text, Large Language Models, and Retrieval-Augmented Generation (RAG).

## 🚀 Overview

The **AI Video Intelligence Assistant** transforms long videos into useful, structured information.

Users can provide a **YouTube URL or local media file**, and the system automatically:

- Extracts and processes audio
- Converts speech into text using **OpenAI Whisper**
- Generates a professional title
- Produces an AI-generated summary
- Extracts action items
- Identifies key decisions
- Detects unresolved questions
- Builds a searchable vector database
- Enables natural-language Q&A over the transcript using **RAG**

The application provides an interactive **Streamlit dashboard** for video analysis and transcript-based question answering.

---

## ✨ Key Features

### 🎥 Video & Audio Processing

- Supports YouTube URLs
- Supports local video/audio files
- Automatically detects the input source
- Downloads YouTube audio using `yt-dlp`
- Converts media to mono 16 kHz WAV
- Splits long recordings into 10-minute audio chunks

### 🎙️ Speech-to-Text

- Uses **OpenAI Whisper** for local transcription
- Supports configurable Whisper models
- Processes audio chunk-by-chunk
- Supports English transcription
- Includes a Hinglish option using Whisper translation mode

### 🧠 AI-Powered Video Analysis

The system automatically generates:

- 📌 Professional title
- 📋 Video/meeting summary
- ✅ Action items
- 🔑 Key decisions
- ❓ Open questions

For action items, the system attempts to identify:

- Task description
- Responsible owner
- Deadline, when mentioned

---

## 🔎 Retrieval-Augmented Generation

The transcript is transformed into a searchable knowledge base using:

- **RecursiveCharacterTextSplitter**
- **Hugging Face `all-MiniLM-L6-v2` embeddings**
- **ChromaDB**
- **Similarity retrieval**
- **Groq LLM**

The system retrieves the most relevant transcript sections and uses them as context for question answering.

### RAG Pipeline

```text
Transcript
    │
    ▼
Text Chunking
    │
    ▼
Hugging Face Embeddings
    │
    ▼
ChromaDB Vector Store
    │
    ▼
Similarity Search
    │
    ▼
Relevant Transcript Context
    │
    ▼
Groq LLM
    │
    ▼
Answer
```

---

## 🏗️ System Architecture

```text
                    ┌─────────────────────────┐
                    │ YouTube URL / Local File │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │    Audio Processing    │
                    │     yt-dlp / pydub     │
                    └────────────┬───────────┘
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │     Audio Chunking     │
                    │       10 min chunks    │
                    └────────────┬───────────┘
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │     Whisper STT        │
                    │      Speech → Text     │
                    └────────────┬───────────┘
                                 │
                                 ▼
                  ┌─────────────────────────────┐
                  │      Transcript Analysis   │
                  ├─────────────┬───────────────┤
                  │             │               │
                  ▼             ▼               ▼
               Title         Summary      Information
                                           Extraction
                                            │
                                  ┌─────────┼──────────┐
                                  ▼         ▼          ▼
                              Action Items Decisions Open Questions

                                 │
                                 ▼
                    ┌────────────────────────┐
                    │    Transcript Chunks   │
                    └────────────┬───────────┘
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │ Hugging Face Embeddings │
                    │   all-MiniLM-L6-v2      │
                    └────────────┬───────────┘
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │       ChromaDB          │
                    │     Vector Database     │
                    └────────────┬───────────┘
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │    Similarity Search   │
                    └────────────┬───────────┘
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │       Groq LLM         │
                    │    Context + Query     │
                    └────────────┬───────────┘
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │       Video Q&A         │
                    └────────────────────────┘
```

---

## 🛠️ Tech Stack

| Category | Technology |
|---|---|
| Programming Language | Python 3.10+ |
| User Interface | Streamlit |
| Video / Audio Download | yt-dlp |
| Audio Processing | pydub |
| Multimedia Processing | FFmpeg |
| Speech-to-Text | OpenAI Whisper |
| LLM Framework | LangChain |
| LLM Provider | Groq |
| LLM Model | `openai/gpt-oss-20b` |
| Text Splitting | RecursiveCharacterTextSplitter |
| Embeddings | Hugging Face `all-MiniLM-L6-v2` |
| Vector Database | ChromaDB |
| Deep Learning | PyTorch, TorchAudio |
| Environment Management | python-dotenv |

---

## 📂 Project Structure

```text
AI-video-intelligence-assistant/
│
├── app.py
├── main.py
├── test.py
├── requirements.txt
├── .gitignore
│
├── core/
│   ├── __init__.py
│   ├── extractor.py
│   ├── rag_engine.py
│   ├── summarizer.py
│   ├── transcriber.py
│   └── vector_store.py
│
├── utils/
│   ├── __init__.py
│   └── audio_processor.py
│
├── .streamlit/
│   └── config.toml
│
└── vector_db/
    └── ChromaDB persistent data
```

---

## 🔄 Application Workflow

### 1. Input Processing

The application accepts:

```text
YouTube URL
      OR
Local Media File
```

For YouTube URLs, `yt-dlp` downloads the best available audio.

For local media files, `pydub` converts the input into WAV format.

The audio is normalized to:

```text
Mono
16 kHz
WAV
```

### 2. Audio Chunking

Long recordings are divided into **10-minute chunks**.

This allows the transcription pipeline to process long-form recordings incrementally rather than handling the complete recording as one large input.

### 3. Whisper Transcription

Each audio chunk is processed using **OpenAI Whisper**.

The default configured model is:

```text
small
```

The model can be changed using:

```env
WHISPER_MODEL=small
```

### 4. AI Title Generation

The transcript is passed to the Groq-hosted LLM to generate a concise professional title.

Configured model:

```text
openai/gpt-oss-20b
```

### 5. Transcript Summarization

The transcript is split into smaller sections.

Each section is summarized independently, after which the partial summaries are combined into a final professional summary.

```text
Transcript
    │
    ├── Chunk 1 → Summary 1
    ├── Chunk 2 → Summary 2
    ├── Chunk 3 → Summary 3
    └── ...
           │
           ▼
     Final Summary
```

### 6. Information Extraction

The system separately extracts:

```text
Action Items
Key Decisions
Open Questions
```

Action items attempt to capture:

```text
Task
Owner
Deadline
```

when such information is available in the transcript.

### 7. Vector Store Creation

The transcript is split using:

```text
Chunk Size: 500
Chunk Overlap: 50
```

Each chunk is converted into an embedding using:

```text
all-MiniLM-L6-v2
```

The embeddings are stored in **ChromaDB** for semantic retrieval.

### 8. RAG-Based Question Answering

When a user asks a question:

```text
User Question
      │
      ▼
Similarity Search
      │
      ▼
Top 4 Relevant Transcript Chunks
      │
      ▼
Context + Question
      │
      ▼
Groq LLM
      │
      ▼
Final Answer
```

The retriever is configured to return the top **4 relevant chunks**.

The RAG prompt instructs the assistant to answer using the provided transcript context and return a fallback response when the requested information cannot be found.

---

## 💬 Example Use Cases

The application can be used for:

- Meeting analysis
- Lecture summarization
- Technical video understanding
- Interview analysis
- Webinar processing
- Educational content analysis
- Research discussions
- Knowledge extraction from long-form videos
- Searching through recorded meetings

### Example Questions

```text
What were the main decisions?

What tasks were assigned?

Who was responsible for the implementation?

What unresolved issues were discussed?

What was the main conclusion?

What did the speaker say about the deployment process?
```

---

## 🖥️ User Interface

### Sidebar

The sidebar provides:

- YouTube URL / local file input
- Language selection
- Analyse Video button
- Pipeline status indicators

### Results Dashboard

After processing, the application displays:

- Generated title
- AI summary
- Full transcript
- Action items
- Key decisions
- Open questions

### Interactive Q&A

Users can ask follow-up questions about the analyzed video through the built-in chat interface.

---

## ⚙️ Installation

### Prerequisites

Make sure the following are installed:

- Python 3.10+
- FFmpeg
- Git
- Groq API key

### 1. Clone the Repository

```bash
git clone https://github.com/Harshitraj123/AI-video-intelligence-assistant.git
cd AI-video-intelligence-assistant
```

### 2. Create Virtual Environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
WHISPER_MODEL=small
```

> ⚠️ Never commit API keys or other secrets to GitHub.

---

## ▶️ Run the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your browser.

---

## 🧪 CLI Mode

The project also includes a command-line implementation.

Run:

```bash
python main.py
```

The CLI asks for:

```text
YouTube URL or local file path
Language
```

It then executes:

```text
Audio Processing
      ↓
Transcription
      ↓
Title Generation
      ↓
Summarization
      ↓
Information Extraction
      ↓
RAG Creation
      ↓
Interactive Q&A
```

---

## 🧪 Testing

A basic transcription test is available in:

```text
test.py
```

Run:

```bash
python test.py
```

This tests the audio-processing and Whisper transcription pipeline.

---

## 📈 Technical Highlights

This project demonstrates practical implementation of:

- Speech-to-text pipelines
- Large Language Model integration
- Prompt engineering
- Retrieval-Augmented Generation
- Semantic search
- Vector databases
- Text chunking
- Embeddings
- Information extraction
- Modular Python architecture
- Streamlit application development
- API integration
- Local model inference

---

## 🧩 Design Approach

The project follows a modular architecture where each major responsibility is separated into its own component.

```text
utils/
    └── Audio Processing

core/
    ├── Transcription
    ├── Summarization
    ├── Information Extraction
    ├── Vector Storage
    └── RAG Engine

app.py
    └── Streamlit User Interface
```

This separation improves maintainability, testing, and future extensibility.

---

## 🔮 Future Improvements

Potential extensions include:

- Timestamp-based transcript citations
- Speaker diarization
- Automatic topic segmentation
- Multi-video knowledge bases
- Persistent conversation memory
- Hybrid keyword + semantic retrieval
- Improved retrieval ranking
- GPU acceleration for Whisper
- Background processing for long videos
- PDF / Markdown export
- User authentication
- Cloud deployment
- Docker-based deployment
- RAG evaluation and observability

---

## 🎯 Resume Project Description

**AI Video Intelligence Assistant**  
*Python, Whisper, LangChain, Groq, ChromaDB, Hugging Face, Streamlit*

- Built an end-to-end AI system that processes YouTube and local media, performs Whisper-based speech-to-text transcription, and generates structured summaries, action items, key decisions, and open questions.
- Implemented a **Retrieval-Augmented Generation (RAG)** pipeline using Hugging Face embeddings and ChromaDB for semantic transcript retrieval and context-aware video Q&A.
- Developed a modular Streamlit interface with pipeline status tracking, transcript visualization, structured insights, and interactive question answering.

---

## 👨‍💻 Author

**Harshit Raj**

Computer Science & Engineering Student  
BMS Institute of Technology and Management, Bengaluru

GitHub: https://github.com/Harshitraj123

LinkedIn: https://linkedin.com/in/harshitraj010204

---

## ⭐ Repository

https://github.com/Harshitraj123/AI-video-intelligence-assistant

---

<p align="center">
  Built with Python, Whisper, LangChain, Groq, ChromaDB, Hugging Face and Streamlit.
</p>
