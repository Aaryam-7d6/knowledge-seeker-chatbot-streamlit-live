# Knowledge Seeker — Live

> Production deployment of the Knowledge Seeker RAG chatbot.  
> Upload documents. Ask questions. Get answers from your own content.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit-FF4B4B?logo=streamlit)](https://knowledge-seeker-chatbot-app-live.streamlit.app/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://python.org)

---

## [→ Try the Live App](https://knowledge-seeker-chatbot-app-live.streamlit.app/)

---

## What It Does

Knowledge Seeker is a RAG-based conversational AI that lets you query
your own documents through natural language. Upload PDFs, text files,
Word docs, or Markdown — and ask anything.

The system retrieves relevant chunks from your documents using vector
similarity search, passes them as context to an LLM, and returns
grounded, accurate answers.

---

## Architecture

```
User Upload (PDF / TXT / DOCX / MD)
↓
Parsing & Chunking
(LlamaIndex — indexing.py)
↓
HuggingFace Embeddings
(embed.py)
↓
Qdrant Cloud Vector Storage
(qdb.py)
↓
Query → Hybrid Retrieval
(search.py + rag_eng.py)
↓
Gemini LLM Generation
(llm.py)
↓
Streamlit Chat Interface
(app.py)
```
---

## Module Overview

| File | Responsibility |
|---|---|
| `app.py` | Main Streamlit app — UI and session management |
| `embed.py` | HuggingFace embedding model integration |
| `indexing.py` | Document parsing and LlamaIndex indexing |
| `llm.py` | Gemini LLM integration + auto model switching |
| `qdb.py` | Qdrant Cloud connection and collection management |
| `rag_eng.py` | Core RAG retrieval and generation engine |
| `search.py` | Search and retrieval logic |
| `summary_eng.py` | Document summarization engine |
| `logger.py` | Logging utilities |
| `config.py` | Centralised configuration |

---

## Stack

| Layer | Technology |
|---|---|
| Language | Python |
| RAG Framework | LlamaIndex |
| Vector DB | Qdrant Cloud |
| Embeddings | HuggingFace (`sentence-transformers`) |
| LLM | Gemini 2.5 Flash / Flash-Lite |
| Frontend | Streamlit |
| Deployment | Streamlit Cloud |

---

## Features

- Multi-turn conversational memory — ask follow-up questions naturally
- Auto model switching — falls back automatically when rate limit is hit
- User-selectable LLM model
- File hashing — prevents redundant re-indexing of the same document
- Auto-scroll to latest message
- Supports PDF, TXT, DOCX, and Markdown files

---

## Local Setup

```bash
# Clone the repo
git clone https://github.com/Aaryam-7d6/knowledge-seeker-chatbot-streamlit-live.git
cd knowledge-seeker-chatbot-streamlit-live

# Install dependencies
pip install -r requirements.txt
```

Create a `.env` or set the following environment variables:

```
GEMINI_API_KEY=your_key_here
QDRANT_URL=your_qdrant_cloud_url
QDRANT_API_KEY=your_qdrant_api_key
```
```bash
# Run the app
streamlit run app.py
```

### Optional: build a project knowledge graph

If you want a codebase-level knowledge graph for AI exploration and navigation:

```bash
# Generates graphify-out/graph.json and the report locally
/graphify .
```

If you do not have a Gemini key configured, use the code-only mode:

```bash
/graphify . --code-only #or graphify . --code-only
```

---

## Development Repo

This is the production version. For the full milestone-by-milestone
development journey and internship artifacts:

**→ [Development Repo](https://github.com/Aaryam-7d6/knowledge-seeker-chatbot)**

---

## License

MIT — see [LICENSE](LICENSE)

---

*Built by [Aarya R. Thakar](https://www.linkedin.com/in/aaryamthakar)*
