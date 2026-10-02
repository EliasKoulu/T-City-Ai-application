# Project name

Compare-and-analyze AI

## Team members

- Ari Mononen ari.mononen@student.hamk.fi
- Elias Rosenberg elias.rosenberg@student.hamk.fi
- Kim Erwe kim.erwe@student.hamk.fi
- Riku Turunen riku.turunen@student.hamk.fi


## Problem

### Intended users
Who are the primary target users of this application?
- The primary target users of this application is mostly workers who frequently analyze, evaluate and compare complex documents. Specifically analysts conducting analysis on products specs or legal team reviewing contracts and policies. In addition the app can be used by everyday people to compare different items to purchase. 

### Problem statement
What specific problem does this application solve for those users?
- Comparing documents manually is time consuming and it can be prone to errors. This application provides thorough comparison between documents and summarizes key differences and similarities by saving users time and preventing high costs.

### Why AI is appropriate
Why does this problem require AI / LLM capabilities rather than traditional deterministic software?
- Deterministic softwares follow a strict pattern which has been determined and doesn't have the necessary capabilities to process the documents how the user prefers / wants. This problem can be solved with a document analyzer which has been trained with an LLM and/or uses AI.

## Solution

Briefly describe your application, its primary value proposition, and how it addresses the problem statement above.
- Our application of choice will be a document comparison tool designed to analyze two documents and summarize key differences. It's primary value comes from saving time and automating redundant repetitive tasks. It's for minimizing mistakes which come from repetitiveness and compares the documents on user input/preference.

## Main user workflow

1. **User Input:** The user uploads two documents (PDF or word document) containing product specs or contracts to compare. In addition the details can be also copy-pasted in plain text format. The user then specifies and tells the program which key points and areas to focus on.
2. **Processing & Guardrails:** The application checks for supported file formats and size limit of the documents to be uploaded. The app focuses on raw text and pictures ignoring the layout of the document.
3. **Model Response:** The model generates a structured analysis containing a side-by-side comparison of the two documents. After that it is presented to the user as a clear visual comparison table.

## Architecture

Below is the initial starter architecture. As your project evolves with additional capabilities, replace or extend this diagram in [`docs/architecture.md`](docs/architecture.md).

```text
User
  ↓
Gradio UI (app/ui.py)
  ↓
Application / AI Service (src/services/ai_service.py)
  ↓
Model Client (src/models/model_client.py)
  ↓
Ollama (Local LLM Server)
```

> **Core Architectural Rule:** The user interface must NEVER communicate directly with the model client or Ollama. All interactions must pass through the service layer (`ai_service.py`).

## Model

- **Model used:** qwen3:8b
- **Selection rationale:** We chose qwen 3:8b for our model. We wanted the model to be able to handle long text documents as cost effective as possible. Qwen3 supports context lengths of up to 32 thousand tokens and can be extended to 131 thousand using yarn method. It also has support for over 100+ languages and dialects.

## Additional AI capability

Select at least one additional capability to implement for your final project:

- [ ] RAG (Retrieval-Augmented Generation)
- [ ] Tools / External API integration
- [ ] Model Context Protocol (MCP)
- [ ] Agentic workflow (Model-selected actions based on observations)
- [ ] Memory / Persistent state
- [X] Multimodal interaction (Text + Images)
- [ ] Other: ______________________

### Capability justification
Explain why the selected capability is useful and necessary for your application's user problem.
- Multimodal interaction allows the application to process text and visual elements simultaneously. Real world documents often rely on diagrams and embedded images so this will give a thorough and more accurate analysis of the documents rather than just focusing on raw text.

## Setup

### 1. Create the Conda environment

```bash
conda env create -f environment.yml
```

### 2. Activate the environment

```bash
conda activate dev-ai-project
```

### 3. Configure environment variables

Copy `.env.example` to create your local `.env` configuration file:

On Linux / macOS:
```bash
cp .env.example .env
```

On Windows (Command Prompt / PowerShell):
```powershell
copy .env.example .env
```

Ensure `.env` contains valid values for `OLLAMA_BASE_URL` and `MODEL_NAME`:
```env
OLLAMA_BASE_URL=http://localhost:11434
MODEL_NAME=llama3.2
```

### 4. Start Ollama

Make sure Ollama is installed and running locally, then pull your configured model:

```bash
ollama run llama3.2
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

- Highlight known system limitations, unhandled edge cases, or boundaries of current capabilities.

## Future improvements

- List planned feature enhancements, architectural refactorings, or future capabilities.
