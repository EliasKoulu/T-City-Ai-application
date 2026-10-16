"""
Optional project capability: Retrieval-Augmented Generation (RAG).

Implement this module only if this capability is relevant to your application's
user problem. Remove the file if the capability is not used.

Conceptual Overview:
-------------------
Retrieval-Augmented Generation (RAG) enhances model responses by retrieving
relevant external information before passing the prompt to the LLM.

Key concepts to consider when implementing RAG:
1. Document Ingestion: Loading custom domain documents (PDFs, text, markdown).
2. Embeddings & Vector Store: Converting text into dense vector embeddings and
   storing them in a vector database or local index.
3. Retrieval: Searching the vector store for text chunks semantically similar
   to the user query.
4. Grounding: Constructing a prompt that supplies retrieved context to the model,
   reducing hallucinations and grounding answers in verified factual data.

Note:
-----
Do not implement RAG unless your project requires answering questions over
specific custom documents or static domain knowledge bases.
"""

# Implement custom RAG pipeline below if selected for your project.



""" ------------------------------------------------------------------------------------------------------------------------ """



import chromadb
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer


class RAGService:

    def __init__(self):

        self.encoder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

        # Alustetaan ChromaDB
        self.chroma_client = chromadb.Client()
        self.collection = self.chroma_client.get_or_create_collection(
            name="asuntoilmoitukset",
            metadata={"hnsw:space": "cosine"}
        )

    # Lukee PDF-tiedoston pelkäksi tekstiksi
    def _pdf_to_text(self, pdf_path):
        reader = PdfReader(pdf_path)
        full_text = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"
        return full_text

    # Pilkkoo tekstin päällekkäisiksi palasiksi
    def _create_chunks(self, text, chunk_size=300, overlap=50):
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            start += chunk_size - overlap
        return chunks

    # Lukee molemmat PDF:t, pilkkoo ne ja tallentaa ChromaDB-vektoritietokantaan
    def process_documents(self, pdf1_path, pdf2_path): 
        text1 = self._pdf_to_text(pdf1_path)
        text2 = self._pdf_to_text(pdf2_path)

        documents = []
        metadatas = []
        ids = []

        # Lisätään merkit [ASUNTO 1] ja [ASUNTO 2] sekä kerätään metatiedot
        for i, chunk in enumerate(self._create_chunks(text1), start=1):
            doc_text = f"[ASUNTO 1]: {chunk}"
            documents.append(doc_text)
            metadatas.append({"asunto": "ASUNTO 1"})
            ids.append(f"asunto1-c{i}")

        for i, chunk in enumerate(self._create_chunks(text2), start=1):
            doc_text = f"[ASUNTO 2]: {chunk}"
            documents.append(doc_text)
            metadatas.append({"asunto": "ASUNTO 2"})
            ids.append(f"asunto2-c{i}")

        # Luodaan vektorit (embeddings) harjoituksen mukaisesti
        embeddings = self.encoder.encode(
            documents, 
            normalize_embeddings=True
        ).tolist()

        # Tallennetaan tiedot Chroma-kokoelmaan (upsert)
        self.collection.upsert(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas
        )

    # Etsii käyttäjän kysymystä vastaavat parhaat chunkit ChromaDB:stä
    def search_context(self, query, top_k=4):
        if self.collection.count() == 0:
            return ""

        # Muutetaan käyttäjän kysymys vektoriksi
        query_vector = self.encoder.encode(
            [query], 
            normalize_embeddings=True
        ).tolist()[0]

        # Hetaan Chroma-kokoelmasta lähimmät tekstipalat
        result = self.collection.query(
            query_embeddings=[query_vector],
            n_results=min(top_k, self.collection.count()),
            include=["documents", "metadatas", "distances"]
        )

        # Kootaan haetut tekstipalat yhdeksi merkkijonoksi
        retrieved_docs = result["documents"][0] if result["documents"] else []
        return "\n\n".join(retrieved_docs)