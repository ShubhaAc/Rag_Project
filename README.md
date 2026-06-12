# RAG API Project

A backend API that lets you upload documents and chat with them. Built with FastAPI, it uses Groq's LLaMA model for answering questions and Pinecone for storing and searching document chunks. It also supports booking interviews through natural conversation.

---

## What it does

- Upload a PDF or TXT file
- The file gets split into chunks, converted into embeddings, and stored in Pinecone
- You can then ask questions about the document in a chat-style API
- It remembers your conversation history using Redis
- If you mention booking an interview (with name, email, date, time), it automatically saves the booking to the database

---

## Tech Stack

| Purpose | Tool |
|---|---|
| API Framework | FastAPI |
| LLM | Groq (llama-3.1-8b-instant) |
| Embeddings | HuggingFace sentence-transformers |
| Vector Database | Pinecone |
| Chat Memory | Upstash Redis |
| Database | PostgreSQL |
| Document Parsing | pypdf |

---

## Project Structure

```
ragProject/
├── app/
│   ├── main.py                  # App entry point
│   ├── core/
│   │   └── config.py            # Loads environment variables
│   ├── db/
│   │   ├── database.py          # DB connection and session
│   │   └── models.py            # Document and Booking tables
│   ├── api/
│   │   └── routes/
│   │       ├── ingestion.py     # Upload endpoint
│   │       └── rag.py           # Chat endpoint
│   └── services/
│       ├── embedding.py         # HuggingFace embeddings
│       ├── chunking.py          # Two chunking strategies
│       ├── ingestion.py         # Handles file upload logic
│       ├── pinecone_service.py  # Vector store operations
│       ├── redis_service.py     # Chat history via Redis
│       ├── rag.py               # RAG pipeline with Groq
│       └── booking.py          # Interview booking logic
├── .env                        # API keys 
└── requirements.txt
```

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/ShubhaAc/Rag_Project.git
cd Rag_Project
```

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file in the root folder

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.1-8b-instant

PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=rag-index

DATABASE_URL=postgresql+asyncpg://postgres:your_password@localhost:5432/your_db_name

UPSTASH_REDIS_REST_URL=your_upstash_redis_url
UPSTASH_REDIS_REST_TOKEN=your_upstash_redis_token

EMBEDDING_MODEL=sentence-transformers/all-mpnet-base-v2
```

### 5. Run the server

```bash
uvicorn app.main:app --reload
```

---

## API Endpoints

Two endpoints are available :
`POST /api/v1/ingest/upload` and
`POST /api/v1/rag/chat`

![Swagger UI](screenshots/Screenshot%202026-06-12%20083544.png)

### Upload a Document
Upload a PDF or TXT file and choose a chunking strategy — `recursive` or `token`.
**Recursive chunking:**


![Recursive strategy](screenshots/Screenshot%202026-06-12%20083646.png)
![Recursive response](screenshots/Screenshot%202026-06-12%20083720.png)

**Token chunking:**

![Token strategy](screenshots/Screenshot%202026-06-12%20083755.png)
![Token response](screenshots/Screenshot%202026-06-12%20083814.png)

---

### Chat with the Document
`POST /api/v1/rag/chat`

Ask questions about the uploaded document. Use the same `session_id` to maintain conversation history across turns.

![Chat question](screenshots/Screenshot%202026-06-12%20084048.png)
![Chat response](screenshots/Screenshot%202026-06-12%20084104.png)

**Multi-turn memory — follow up question in the same session:**

![Follow-up question](screenshots/Screenshot%202026-06-12%20084416.png)
![Follow-up response](screenshots/Screenshot%202026-06-12%20084426.png)

---

### Book an Interview

Just mention the booking details in the chat. The LLM detects it and saves it to the database automatically.

![Booking request](screenshots/Screenshot%202026-06-12%20084559.png)
![Booking response](screenshots/Screenshot%202026-06-12%20084829.png)

---

## Database

PostgreSQL tables are created automatically on server startup.

**Documents table** — stores metadata for every uploaded file:

![Documents table](screenshots/Screenshot%202026-06-12%20085148.png)

**Bookings table** — stores interview bookings detected from chat:

![Bookings table](screenshots/Screenshot%202026-06-12%20085251.png)

---

## Chunking Strategies

Two strategies are available when uploading a document:

- **recursive** — splits by paragraphs, sentences, and words. Good for general text like reports or articles.
- **token** — splits by token count. More precise, good for technical documents.

---

## Notes

- The embedding model (`all-mpnet-base-v2`) downloads automatically on first run and gets cached locally.
- Make sure your Pinecone index is created with **768 dimensions** and **cosine** metric before running.
- PostgreSQL tables are created automatically on server startup.