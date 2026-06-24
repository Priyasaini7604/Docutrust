# 🛡️ DocuTrust — Enterprise RAG Platform with Self-Correction & Citations

> An intelligent document Q&A platform that retrieves answers from uploaded PDFs with **automated self-correction**, **relevance grading**, and **strict source citations** — eliminating AI hallucinations.

![Tech Stack](https://img.shields.io/badge/React-Vite-blue?style=flat-square&logo=react)
![FastAPI](https://img.shields.io/badge/FastAPI-Python-green?style=flat-square&logo=fastapi)
![LangGraph](https://img.shields.io/badge/LangGraph-CRAG-purple?style=flat-square)
![MongoDB](https://img.shields.io/badge/MongoDB-Database-brightgreen?style=flat-square&logo=mongodb)
![ChromaDB](https://img.shields.io/badge/ChromaDB-VectorStore-orange?style=flat-square)

---

## 🚀 What is DocuTrust?

Most AI document tools suffer from **hallucinations** — they confidently give wrong answers with no sources. DocuTrust solves this by implementing a **Corrective RAG (CRAG)** pipeline:

- ✅ Retrieves relevant document chunks
- ✅ **Grades** retrieved chunks for relevance before answering
- ✅ **Rewrites** the query and searches the web if chunks are irrelevant
- ✅ Always outputs answers with **page-level citations**

---

## ✨ Features

- 📄 **PDF Upload** — Drag & drop multi-page PDF documents
- 🤖 **Real-time Agent Logs** — Watch AI think step by step
- 🔍 **CRAG Pipeline** — Self-correcting retrieval with relevance grading
- 📎 **Source Citations** — Every answer linked to exact document pages
- 🌐 **Web Fallback** — If document lacks info, agent searches the web
- 🎨 **Dark Corporate UI** — Professional split-pane interface

---

## 🏗️ Architecture

```
PDF Upload
    ↓
Chunking → HuggingFace Embeddings → ChromaDB
    ↓
User Question
    ↓
Retrieve Chunks (ChromaDB)
    ↓
Grade Relevance (LangGraph Agent)
    ↓
Relevant? ✅ → Generate Answer + Citations
Not Relevant? ❌ → Rewrite Query → Web Search → Answer
    ↓
FastAPI → React Frontend
```

---

## 🛠️ Tech Stack

### Frontend
| Technology | Purpose |
|------------|---------|
| React + Vite | UI Framework |
| react-dropzone | PDF drag & drop |
| lucide-react | Icons |
| axios | API calls |

### Backend
| Technology | Purpose |
|------------|---------|
| FastAPI | REST API |
| LangGraph | CRAG agent pipeline |
| Groq (Llama 3) | LLM inference |
| HuggingFace Embeddings | Text → vectors |
| ChromaDB | Vector store |
| MongoDB | Chat history & metadata |

---

## 📁 Project Structure

```
docutrust/
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── PDFUploader.jsx    # Drag & drop PDF
│   │   │   ├── AgentLogs.jsx      # Real-time agent steps
│   │   │   └── ChatPanel.jsx      # Q&A + citations
│   │   ├── services/
│   │   │   └── api.js             # Backend API calls
│   │   └── App.jsx
│   └── package.json
│
└── backend/
    ├── core/
    │   ├── config.py              # Environment variables
    │   └── database.py            # MongoDB connection
    ├── rag/
    │   ├── ingestion.py           # PDF → chunks → ChromaDB
    │   ├── retriever.py           # Fetch relevant chunks
    │   ├── grader.py              # Relevance grading agent
    │   ├── rewriter.py            # Query rewriter agent
    │   └── graph.py               # LangGraph CRAG flow
    ├── api/
    │   └── routes.py              # FastAPI endpoints
    ├── main.py
    └── requirements.txt
```

---

## ⚙️ Setup Instructions

### Prerequisites
- Python 3.10+
- Node.js 18+
- MongoDB running locally
- Groq API key (free at [console.groq.com](https://console.groq.com))

### Backend Setup

```bash
# Clone the repo
git clone https://github.com/Priyasaini7604/docutrust.git
cd docutrust/backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Fill in your GROQ_API_KEY in .env

# Run backend
uvicorn main:app --reload
```

### Frontend Setup

```bash
cd docutrust/frontend

# Install dependencies
npm install

# Run frontend
npm run dev
```

Open `http://localhost:5173` in your browser! 🎉

---

## 🔑 Environment Variables

Create `backend/.env` file:

```env
GROQ_API_KEY=your_groq_api_key_here
MONGO_URI=mongodb://localhost:27017
DB_NAME=docutrust
```

---

## 🎯 How It Works

1. **Upload PDF** — Drop any PDF document into the uploader
2. **Ask a Question** — Type your question in the chat panel
3. **Watch the Agent** — See real-time logs as the AI:
   - Retrieves relevant chunks from your document
   - Grades whether chunks actually answer your question
   - Rewrites query & searches web if needed
4. **Get Cited Answer** — Receive answer with exact page references

---

## 🚧 Future Improvements

- [ ] Multi-document support
- [ ] User authentication
- [ ] Docker containerization
- [ ] Deploy on Railway + Vercel
- [ ] Support for DOCX and TXT files
- [ ] Export chat history as PDF

---

## 👩‍💻 Author

**Priya Saini**
B.Tech Computer Science — Sitare University

[![GitHub](https://img.shields.io/badge/GitHub-Priyasaini7604-black?style=flat-square&logo=github)](https://github.com/Priyasaini7604)

---

## 📄 License

MIT License — feel free to use this project for learning!