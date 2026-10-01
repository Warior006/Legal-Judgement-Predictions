# ⚖️ Legal Judgment Prediction System

> **AI-powered legal case outcome prediction** using Legal Longformer embeddings,
> FAISS similarity search, Logistic Regression, and RAG-based legal reasoning.

---

## Architecture Overview

```
User Input (Case Text)
        │
        ▼
┌─────────────────────┐
│  1. Preprocessing   │  Lowercase, strip special chars,
│  (src/preprocessing)│  remove stopwords, lemmatize
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  2. Legal Longformer│  lexlms/legal-longformer-base
│  Embedding          │  768-dimensional dense vector
│  (src/embedding)    │  Mean-pool + L2-normalise
└────────┬────────────┘
         │
         ├──────────────────────────────┐
         ▼                              ▼
┌─────────────────────┐    ┌────────────────────────┐
│  3. FAISS Retrieval │    │  4. Logistic Regression│
│  (src/retrieval)    │    │  Prediction            │
│  Top-5 similar past │    │  (src/prediction)      │
│  cases by cosine    │    │  Label + probability   │
│  similarity         │    │  scores                │
└────────┬────────────┘    └───────────┬────────────┘
         │                             │
         └──────────┬──────────────────┘
                    ▼
         ┌─────────────────────┐
         │  5. RAG Reasoning   │  Retrieved cases as context
         │  (src/rag_reasoning)│  → LLM generates legal
         │                     │    reasoning explanation
         └──────────┬──────────┘
                    │
                    ▼
         ┌─────────────────────┐
         │  6. FastAPI + UI    │  REST API + Streamlit
         │  (api/ frontend/)   │  dashboard
         └─────────────────────┘
```

---

## Project Structure

```
legal_judgment_prediction_system/
│
├── config.py                    # Centralised configuration
│
├── data/
│   ├── cases.csv                # Raw dataset (40 sample cases)
│   └── processed_cases.csv      # Auto-generated after build
│
├── models/
│   ├── logistic_model.pkl       # Trained classifier
│   ├── label_encoder.pkl        # Label ↔ integer mapping
│   ├── scaler.pkl               # Feature scaler
│   └── metrics.json             # Evaluation metrics
│
├── embeddings/
│   ├── case_embeddings.npy      # Cached embedding matrix
│   └── case_ids.npy             # Matching case IDs
│
├── retrieval/
│   └── faiss_index.bin          # FAISS binary index
│
├── src/
│   ├── __init__.py
│   ├── logger.py                # Loguru logging setup
│   ├── preprocessing.py         # Text cleaning pipeline
│   ├── embedding.py             # Legal Longformer encoder + cache
│   ├── retrieval.py             # FAISS similarity search
│   ├── prediction.py            # LR training + inference
│   └── rag_reasoning.py         # RAG prompt + LLM call
│
├── api/
│   ├── __init__.py
│   └── main.py                  # FastAPI backend (3 endpoints)
│
├── frontend/
│   └── app.py                   # Streamlit UI
│
├── scripts/
│   └── build_index.py           # One-command bootstrap script
│
├── tests/
│   └── test_pipeline.py         # Pytest test suite
│
├── logs/                        # Rotating daily log files
├── requirements.txt
└── README.md
```

---

## Quick Start

### 1. Prerequisites

- Python 3.10 or 3.11
- 4 GB RAM minimum (16 GB recommended for Legal Longformer)
- Internet connection (first run downloads model weights ~400 MB)

### 2. Install Dependencies

```bash
# Clone / download the project
cd legal_judgment_prediction_system

# Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate          # Linux / macOS
# .venv\Scripts\activate           # Windows

# Install all packages
pip install -r requirements.txt

# Download spaCy English model (used by NLTK fallback)
python -m spacy download en_core_web_sm
```

### 3. (Optional) Set Anthropic API Key for LLM Reasoning

```bash
export ANTHROPIC_API_KEY="sk-ant-..."   # Linux / macOS
# set ANTHROPIC_API_KEY=sk-ant-...      # Windows CMD
```

> Without the key the system falls back to template-based reasoning.

### 4. Build the Index — One Command

```bash
python scripts/build_index.py
```

This script will:
1. Preprocess `data/cases.csv` → `data/processed_cases.csv`
2. Generate Legal Longformer embeddings → `embeddings/case_embeddings.npy`
3. Build the FAISS index → `retrieval/faiss_index.bin`
4. Train the Logistic Regression → `models/logistic_model.pkl`
5. Print evaluation metrics

Expected output:
```
[1/4] Preprocessing dataset …          40 cases ready
[2/4] Generating / loading embeddings … Embeddings shape: (40, 768)
[3/4] Building FAISS index …           Saved → retrieval/faiss_index.bin
[4/4] Training Logistic Regression …
      Accuracy:    0.8750
      F1 (macro):  0.8720
      ROC-AUC:     0.9200
      CV Accuracy: 0.8500 ± 0.0412
```

### 5. Start the FastAPI Backend

```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

Interactive API docs: **http://localhost:8000/docs**

### 6. Start the Streamlit Frontend

```bash
# In a new terminal
streamlit run frontend/app.py
```

UI opens at: **http://localhost:8501**

### 7. Run Tests

```bash
pytest tests/ -v
```

---

## API Reference

### `POST /predict`

Full pipeline — predict + retrieve + reason.

**Request body:**
```json
{
  "case_text": "The defendant was charged with aggravated assault ...",
  "top_k": 5,
  "use_llm": true
}
```

**Response:**
```json
{
  "predicted_label": "guilty",
  "confidence": 0.8734,
  "probabilities": {"guilty": 0.8734, "not_guilty": 0.1266},
  "similar_cases": [
    {
      "rank": 1,
      "case_id": "CASE001",
      "label": "guilty",
      "similarity_score": 0.9412,
      "case_text": "..."
    }
  ],
  "reasoning": "## Legal Analysis\n...",
  "cleaned_text": "defendant charged aggravated assault ..."
}
```

---

### `POST /similar_cases`

Retrieve only — no prediction, no reasoning.

```json
{ "case_text": "...", "top_k": 5 }
```

---

### `POST /reasoning`

Generate reasoning for a pre-computed prediction.

```json
{
  "case_text": "...",
  "predicted_label": "guilty",
  "confidence": 0.87,
  "retrieved_cases": [...],
  "use_llm": true
}
```

---

### `GET /health`

```json
{
  "status": "ok",
  "predictor_loaded": true,
  "retriever_loaded": true
}
```

---

### `GET /metrics`

Returns the JSON metrics from the last training run.

---

## Configuration

All settings are in `config.py`:

| Config class | Key settings |
|---|---|
| `ModelConfig` | `embedding_model`, `max_length`, `batch_size` |
| `RetrievalConfig` | `top_k`, `index_type` (`flat`/`ivf`) |
| `PredictionConfig` | `C`, `max_iter`, `test_size` |
| `RAGConfig` | `context_cases`, `llm_model`, `max_tokens` |
| `PreprocessConfig` | `remove_stopwords`, `lemmatize`, `min_text_length` |

---

## Dataset Format

`data/cases.csv` must have these three columns:

| Column | Type | Description |
|---|---|---|
| `case_id` | string | Unique case identifier |
| `case_text` | string | Full case description text |
| `label` | string | `guilty` or `not_guilty` |

---

## Evaluation Metrics

After running `build_index.py` check `models/metrics.json`:

```json
{
  "accuracy": 0.875,
  "f1_macro": 0.872,
  "f1_weighted": 0.874,
  "roc_auc": 0.920,
  "cv_accuracy_mean": 0.850,
  "cv_accuracy_std": 0.041,
  "n_train": 32,
  "n_test": 8,
  "classes": ["guilty", "not_guilty"]
}
```

---

## Technology Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| Embedding Model | `lexlms/legal-longformer-base` (HuggingFace) |
| ML Framework | PyTorch, scikit-learn |
| Vector DB | FAISS (`faiss-cpu`) |
| Classifier | Logistic Regression |
| Reasoning LLM | Anthropic Claude (via RAG) |
| Backend API | FastAPI + Uvicorn |
| Frontend | Streamlit + Plotly |
| Caching | diskcache |
| Logging | Loguru |

---

## Disclaimer

This system is a research prototype for educational purposes.
It does **not** constitute legal advice. Always consult a
qualified attorney for real legal matters.
