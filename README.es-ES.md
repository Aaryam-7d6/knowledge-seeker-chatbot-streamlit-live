

# Knowledge Seeker — Live

> Despliegue en producción del chatbot RAG Knowledge Seeker.  
> Sube documentos. Haz preguntas. Obtén respuestas a partir de tu propio contenido.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit-FF4B4B?logo=streamlit)](https://knowledge-seeker-chatbot-app-live.streamlit.app/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://python.org)

---

## [→ Prueba la aplicación en vivo](https://knowledge-seeker-chatbot-app-live.streamlit.app/)

---

## ¿Qué hace?

Knowledge Seeker es una IA conversacional basada en RAG que te permite consultar
tus propios documentos mediante lenguaje natural. Sube archivos PDF, de texto,
de Word o Markdown, y pregunta lo que necesites.

El sistema recupera fragmentos relevantes de tus documentos mediante búsqueda
de similitud vectorial, los pasa como contexto a un LLM y devuelve
respuestas fundamentadas y precisas.

---

## Arquitectura

```
Carga de usuario (PDF / TXT / DOCX / MD)
↓
Análisis y segmentación
(LlamaIndex — indexing.py)
↓
Embeddings de HuggingFace
(embed.py)
↓
Almacenamiento vectorial en Qdrant Cloud
(qdb.py)
↓
Consulta → Recuperación híbrida
(search.py + rag_eng.py)
↓
Generación con LLM Gemini
(llm.py)
↓
Interfaz de chat en Streamlit
(app.py)
```
---

## Descripción de módulos

| Archivo | Responsabilidad |
|---|---|
| `app.py` | Aplicación principal de Streamlit: interfaz de usuario y gestión de sesiones |
| `embed.py` | Integración del modelo de embeddings de HuggingFace |
| `indexing.py` | Análisis de documentos e indexación con LlamaIndex |
| `llm.py` | Integración del LLM Gemini + cambio automático de modelos |
| `qdb.py` | Conexión a Qdrant Cloud y gestión de colecciones |
| `rag_eng.py` | Motor principal de recuperación y generación RAG |
| `search.py` | Lógica de búsqueda y recuperación |
| `summary_eng.py` | Motor de resumen de documentos |
| `logger.py` | Utilidades de registro (logging) |
| `config.py` | Configuración centralizada |

---

## Stack

| Capa | Tecnología |
|---|---|
| Lenguaje | Python |
| Framework RAG | LlamaIndex |
| Base de datos vectorial | Qdrant Cloud |
| Embeddings | HuggingFace (`sentence-transformers`) |
| LLM | Gemini 2.5 Flash / Flash-Lite |
| Frontend | Streamlit |
| Despliegue | Streamlit Cloud |

---

## Características

- Memoria conversacional multironda: haz preguntas de seguimiento de forma natural
- Cambio automático de modelo: cambia automáticamente cuando se alcanza el límite de tasa (rate limit)
- Modelo de LLM seleccionable por el usuario
- Hash de archivos: evita la reindexación redundante del mismo documento
- Desplazamiento automático al último mensaje
- Compatible con archivos PDF, TXT, DOCX y Markdown

---

## Configuración local

```bash
# Clone the repo
git clone https://github.com/Aaryam-7d6/knowledge-seeker-chatbot-streamlit-live.git
cd knowledge-seeker-chatbot-streamlit-live

# Install dependencies
pip install -r requirements.txt
```

Crea un `.env` o establece las siguientes variables de entorno:

```
GEMINI_API_KEY=your_key_here
QDRANT_URL=your_qdrant_cloud_url
QDRANT_API_KEY=your_qdrant_api_key
```
```bash
# Run the app
streamlit run app.py
```

---

## Repositorio de desarrollo

Esta es la versión de producción. Para el recorrido de desarrollo completo
paso a paso y los artefactos de la pasantía:

**→ [Development Repo](https://github.com/Aaryam-7d6/knowledge-seeker-chatbot)**

---

## Licencia

MIT: consulta [LICENSE](LICENSE)

---

*Desarrollado por [Aarya R. Thakar](https://www.linkedin.com/in/aaryamthakar)*
