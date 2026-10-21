# Project decisions

Use this decision log to document significant technical and architectural choices made by your team during development.

## Decision 1 — Model selection

**Decision:**
- Qwen3:8b

**Alternatives considered:**
- We briefly considered to use Qwen2.5:3b due to it being smaller in size. However most of us didn't have a powerful enough laptop to test the app that fast so we decided to just stick with the one model we already decided.

**Why we chose this:**
- We wanted the model to be able to handle long text documents as cost effective as possible. Qwen3 supports context lengths of up to 32 thousand tokens and can be extended to 131 thousand using yarn method. It also has support for over 100+ languages and dialects.

---

## Decision 2 — Additional AI capability

**Decision:**
- RAG (Retrieval-augmented generation)

**Why it is needed:**
- RAG is required in this application to extract and retrieve specific context directly from PDF property listings. This grounds the AI model's responses in data from the documents.

**Alternatives considered:**
- First we considered to use Multimodal Interaction. However after few meetings, learing more about the course chapters and getting familiar with the project we decided that RAG is the best choice for this specific application.

---

## Decision 3 — Architecture

**Decision:**
- asdasd

**Why:**
- The way our architecture was built was the most sensible choice for this application.