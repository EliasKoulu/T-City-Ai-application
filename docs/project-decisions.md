# Project decisions

## Decision 1 — Model selection

**Decision:**
- Qwen3:8b (via ollama)

**Alternatives considered:**
- We briefly considered to use Qwen2.5:3b due to it being smaller in size. However most of us didn't have a powerful enough laptop to test the app (even with qwen3:8b) that fast so we decided to just stick with the one model we already decided. Also smaller models struggle to consistently adhere the very strict markdown formatting without generating extra, unwanted content.

**Why we chose this:**
- We wanted the model to be able to handle long text documents as cost effective as possible. Qwen3:8b supports context lengths of up to 32 thousand tokens and can be extended to 131 thousand using yarn method. It also has support for over 100+ languages and dialects.

When ollama is ran locally it eliminates api latency, costs and data privacy risks.

---

## Decision 2 — Additional AI capability

**Decision:**
- RAG (Retrieval-augmented generation)

**Why it is needed:**
- RAG is required in this application to extract and retrieve specific context directly from PDF property listings. This grounds the AI model's responses in data from the documents since pdf about apartments are usually long, unstructured text / picture files and multi column tables at times. Passing this all information directly into the LLM context  may lead to model hallucinations or details missing.

**Alternatives considered:**
- First we considered to use Multimodal Interaction. However after few meetings, learing more about the course chapters and getting familiar with the project we decided that RAG is the best choice for this specific application since text base rag uses pypdf is faster and less computationally demanding plus reliable for structured data extraction.

RAG doesnt compare pictures at all, so it does not create unwanted comparison of photos in the apartments ads. That might lead to misreading the users input and hallucinations. 

---

## Decision 3 — Architecture

**Decision:**
```text
User (Uploading the PDF-files and query)
  ↓
Gradio UI (app/ui.py). The user interface layer that receives the uploaded PDF-files and optional user queries.
  ↓
Application / AI Service (src/services/ai_service.py)
  |--> RAG (src/capabilities/rag.py)
  |      |---> PyPDF (PDF text extraction)
  |      |---> Splitting text into chunks (400 chars / 100 overlap)
  |      |---> SentenceTransformer (paraphrase-multilingual-MiniLM-L12-v2)
  |      |---> ChromaDB (filtered by asunto 1 / asunto 2 = forced to create two seperate balanced queries)
  |
Model Client (src/models/model_client.py)
  ↓
Ollama (Local LLM  - Qwen3:8b)
```

**Why:**
- First of all, we wanted to isolate ui (app + ui.py) from backed (ai_service.py). Thats how we ensure that ui modifications never break the logic or model.
- Dual document retrieving setup ensures we force two seperate queries (chromadb asunto 1 and asunto 2). This guarantees that both of the apartment listings get equal search representation even though the PDF have different lenghts and characteristics.
- Chunk size 400 and overlap 100 make sure that we prevent key metrics (like: " Velaton hinta 150 000€) from cutting mid way during chunking.
- This setup is running locally, so it eliminates costs and keeps document processing 100% private.