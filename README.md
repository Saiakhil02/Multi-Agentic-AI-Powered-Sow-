# 🧠 Agentic SOW Drafting

A full-stack AI-powered tool to dynamically generate Statements of Work (SOW) using agentic workflows and memory-based retrieval.

## 🚀 Tech Stack

- **Frontend**: React  
- **Backend**: Python, Flask  
- **AI Orchestration**: LangGraph  
- **Vector DB**: pgvector (PostgreSQL)  
- **Embedding & Memory**: LangChain-compatible memory with pgvector

## 🖥️ Frontend Setup (React)

```bash
cd frontend
yarn install
yarn run dev
```

Make sure to update the API_BASE_URL in `frontend\src\components\SOWGenerator.tsx` with the url backend is running at.


## 🧠 Backend Setup (Python + Flask + LangGraph)

```bash
cd backend
pip install -r requirements.txt
```

### 1. Setup Environment Variables

Create a `.env` file in the root of `/backend` based on `.env-example`:

```bash
cp .env-example .env
```

Update the required keys (e.g., OpenAI API Key, DB connection string).

### 2. Setup PostgreSQL with pgvector

Ensure your PostgreSQL instance has the `pgvector` extension enabled:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

Create necessary tables using your preferred method or provided migrations (if any).

### 3. Run vector migrations

```bash
python generate_sample_embeddings.py
```

### 4. Run the Backend

```bash
python app.py
```

The Flask server will start and handle LangGraph-based multi-agent interactions and vector DB retrieval.

---

## ⚠️ Notes

- Ensure both front and backend servers are running simultaneously.  
- You may need to allow CORS depending on deployment.  
- This project assumes access to OpenAI or Hugging Face for LLM calls.  