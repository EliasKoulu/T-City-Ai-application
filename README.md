# Project name

### Oikotie.fi Asuntoesitteiden Vertailukone (Oikotie.fi Property Listing Comparison Tool)

## Team members

- Ari Mononen ari.mononen@student.hamk.fi
- Elias Rosenberg elias.rosenberg@student.hamk.fi
- Kim Erwe kim.erwe@student.hamk.fi
- Riku Turunen riku.turunen@student.hamk.fi

Video presentation link: https://drive.google.com/file/d/1OaCfn1OD-6Qu98VW8tW1EeeZF7reX1z8/view?usp=drive_link


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

3. **Model Response:** The model generates a structured analysis containing a side-by-side comparison of the two documents. After that it is presented to the user as a clear visual comparison table. With a short summary below the table.

## Architecture

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
- [/] Multimodal interaction (Text + Images) -> Tested but not chosen.
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

For evaluation we used manual evaluation method. Different style of prompts were chosen to test the programs capabilities.

1. First test was a standard, well structured prompt.
2. Second test contained a long, unorganized but still understandable prompt.
3. Third test was an empty prompt.
4. Fourth test had a prompt with totally random string of charcters.
5. Fifth test had a prompt which was malicious prompt, trying to role hijack.

Every test came out passing, the program worked as it should and returned the expected answers. You can find clearer information about the testing conducted and photos of the tests in [evaluation_results.md].

## Known limitations

- Using a model with a context length of 32k tokens can be limiting when comparing two very long documents. The model may not be able to process the entire content of both documents at once, which could lead to incomplete or inaccurate comparisons.
- Current implementation only supports PDF.
- The model may not always provide accurate or relevant comparisons, especially if the documents contain complex or ambiguous information.
- The prompt has  to be thought carefully, two similar kind of questions can give different answers.


## Future improvements

- [ ] More support for different filetypes, now the tool can only handle PDF.
- [x] Improvements to the general quality of answers.
