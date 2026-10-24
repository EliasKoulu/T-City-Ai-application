# Project name

### Oikotie.fi Asuntoesitteiden Vertailukone (Oikotie.fi Property Listing Comparison Tool)

## Team members

- Ari Mononen ari.mononen@student.hamk.fi
- Elias Rosenberg elias.rosenberg@student.hamk.fi
- Kim Erwe kim.erwe@student.hamk.fi
- Riku Turunen riku.turunen@student.hamk.fi


## Problem

### Intended users
Who are the primary target users of this application?
- The primary target users for this application are mostly real estate agents who frequently analyze and compare two property listings. In addition the app can be used by everyday people to make a quick comparison between two apartments.

### Problem statement
What specific problem does this application solve for those users?
- Comparing two documents manually is time consuming and it can be prone to errors. This application provides thorough comparison between documents and summarizes key differences and similarities by saving users time.

### Why AI is appropriate
Why does this problem require AI / LLM capabilities rather than traditional deterministic software?
- Deterministic softwares follow a strict pattern which has been determined and doesn't have the necessary capabilities to process the documents how the user prefers / wants. This problem can be solved with a document analyzer which has been trained with an LLM and/or uses AI.

## Solution

Briefly describe your application, its primary value proposition, and how it addresses the problem statement above.
- Our application of choice will be a document comparison tool designed to analyze two property listing documents from www.oikotie.fi and summarize key differences. It's primary value comes from saving time and automating redundant repetitive tasks. It's for minimizing mistakes which come from repetitiveness and compares the documents on user input/preference.

## Main user workflow

1. **User Input:** The user uploads two PDF-documents containing the specs of the two properties to compare. The user can then specify and tell the program which key points and areas to focus on. The specification box can also be left totally blank and the program will give a generic comparison of the most important features.

2. **Processing & Guardrails:** The processing pipeline handles PDF text extraction via PyPDF, text chunking and vector storage in ChromaDB and sending the retrieved context to Ollama language model. 

3. **Model Response:** The model generates a structured analysis containing a side-by-side comparison of the two documents. After that it is presented to the user as a clear visual comparison table.

## Architecture

Below is the initial starter architecture. As your project evolves with additional capabilities, replace or extend this diagram in [`docs/architecture.md`](docs/architecture.md).

```text
User (Uploading the PDF-files and query)
  ↓
Gradio UI (app/ui.py). The user interface layer that receives the uploaded PDF-files and optional user queries.
  ↓
Application / AI Service (src/services/ai_service.py)
  |--> RAG (src/capabilities/rag.py)
  |      |---> PyPDF (PDF text extraction)
  |      |---> Splitting text into chunks
  |      |---> SentenceTransformer
  |      |---> ChromaDB
  |
Model Client (src/models/model_client.py)
  ↓
Ollama (Local LLM  - Qwen3:8b)
```

> **Core Architectural Rule:** The user interface must NEVER communicate directly with the model client or Ollama. All interactions must pass through the service layer (`ai_service.py`).

## Model

- **Model used:** qwen3:8b
- **Selection rationale:** We chose qwen 3:8b for our model. We wanted the model to be able to handle long text documents as cost effective as possible. Qwen3 supports context lengths of up to 32 thousand tokens and can be extended to 131 thousand using yarn method. It also has support for over 100+ languages and dialects.

## Additional AI capability

Select at least one additional capability to implement for your final project:

- [X] RAG (Retrieval-Augmented Generation)
- [ ] Tools / External API integration
- [ ] Model Context Protocol (MCP)
- [ ] Agentic workflow (Model-selected actions based on observations)
- [ ] Memory / Persistent state
- [ ] Multimodal interaction (Text + Images)
- [ ] Other: ______________________

### Capability justification
Explain why the selected capability is useful and necessary for your application's user problem.
- RAG (Retrieval-Augmented Generation) allow the application to retrieve information from the uploaded PDF-files. Property listings from www.oikotie.fi are solely downloadable in PDF-format and RAG fits perfectly in our application.

## Setup

### 1. Create the Conda environment
- Make sure that Anaconda has been installed on your machine. Create a new python-environment by running this command in root directory

```bash
conda env create -f environment.yml
```

### 2. Activate the environment
- Activate the environment we just created with this command

```bash
conda activate dev-ai-project
```

### 3. Configure environment variables

The directory contains a file `.env.example`. To create your local `.env` configuration file run this command:

On Linux / macOS:
```bash
cp .env.example .env
```

On Windows (Command Prompt / PowerShell):
```powershell
copy .env.example .env
```

Make sure `.env` now contains the following: 
```env
OLLAMA_BASE_URL=http://localhost:11434
MODEL_NAME=qwen3:8b
```

### 4. Start Ollama

Make sure Ollama is installed and running locally, then pull your configured model:

```bash
ollama run qwen3:8b
```

### 5. Run the application

Run the application from the root directory of the project:

```bash
python -m app.main
```

Then open your browser at `http://localhost:7860`.

### 6. Run automated tests

```bash
pytest
```

## Evaluation

Describe your evaluation methodology and summarize key results. Starter test cases can be found in [`evaluation/test_cases.json`](evaluation/test_cases.json).

Refer to [`evaluation/README.md`](evaluation/README.md) for guidelines on defining success, edge cases, and failure scenarios.

## Known limitations

- Using a model with a context length of 32k tokens can be limiting when comparing two very long documents. The model may not be able to process the entire content of both documents at once, which could lead to incomplete or inaccurate comparisons.
- Current implementation only supports PDF.
- The model may not always provide accurate or relevant comparisons, especially if the documents contain complex or ambiguous information.
- The prompt has  to be thought carefully, two similar kind of questions can give different answers.


## Future improvements

- [ ] More support for different filetypes, now the tool can only handle PDF.
- [x] Improvements to the general quality of answers.