# ============================================================
# Legal Judgment Prediction System - Configuration
# ============================================================

import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import List

# ── Root paths ────────────────────────────────────────────────
ROOT_DIR = Path(__file__).resolve().parent

@dataclass
class PathConfig:
    """All filesystem paths used across the project."""
    root:             Path = ROOT_DIR
    data_dir:         Path = ROOT_DIR / "data"
    models_dir:       Path = ROOT_DIR / "models"
    embeddings_dir:   Path = ROOT_DIR / "embeddings"
    retrieval_dir:    Path = ROOT_DIR / "retrieval"
    logs_dir:         Path = ROOT_DIR / "logs"
    cache_dir:        Path = ROOT_DIR / ".cache"

    # Key files
    cases_csv:        Path = ROOT_DIR / "data"     / "cases.csv"
    model_pkl:        Path = ROOT_DIR / "models"   / "logistic_model.pkl"
    label_encoder:    Path = ROOT_DIR / "models"   / "label_encoder.pkl"
    scaler_pkl:       Path = ROOT_DIR / "models"   / "scaler.pkl"
    embeddings_npy:   Path = ROOT_DIR / "embeddings" / "case_embeddings.npy"
    case_ids_npy:     Path = ROOT_DIR / "embeddings" / "case_ids.npy"
    processed_csv:    Path = ROOT_DIR / "data"     / "processed_cases.csv"
    faiss_index:      Path = ROOT_DIR / "retrieval"  / "faiss_index.bin"
    metrics_json:     Path = ROOT_DIR / "models"   / "metrics.json"

    def make_dirs(self):
        """Create all directories if they do not exist."""
        for attr in vars(self).values():
            if isinstance(attr, Path) and not attr.suffix:
                attr.mkdir(parents=True, exist_ok=True)


@dataclass
class ModelConfig:
    """Embedding and prediction model settings."""
    # Legal Longformer for domain-specific legal text embeddings
    embedding_model:   str  = "sentence-transformers/all-MiniLM-L6-v2"
    # Fallback model (lighter / faster for CPU-only environments)
    fallback_model:    str  = "lexlms/legal-longformer-base"
    # Max token length for the transformer
    max_length:        int  = 512
    # Dimensionality of the embedding vector
    embedding_dim:     int  = 384
    # Batch size for encoding multiple texts
    batch_size:        int  = 32
    # Use GPU if available
    device:            str  = "auto"   # "cpu" | "cuda" | "auto"


@dataclass
class RetrievalConfig:
    """FAISS similarity search settings."""
    top_k:            int   = 5          # Number of similar cases to return
    similarity_metric: str  = "cosine"   # "cosine" or "l2"
    # FAISS index type: "flat" (exact) or "ivf" (approximate, faster for large corpora)
    index_type:       str   = "flat"
    nlist:            int   = 10         # IVF number of clusters (used when index_type="ivf")
    nprobe:           int   = 5          # IVF probe count at query time


@dataclass
class PredictionConfig:
    """Logistic Regression classifier settings."""
    C:                float = 0.5        # Inverse regularisation strength
    max_iter:         int   = 2500
    solver:           str   = "liblinear"
    class_weight:     str   = "balanced" # Handle imbalanced labels
    test_size:        float = 0.2
    random_state:     int   = 123


@dataclass
class RAGConfig:
    """Retrieval-Augmented Generation settings."""
    # Number of retrieved cases to include in the reasoning prompt
    context_cases:    int   = 3
    # Maximum characters from each retrieved case to include
    max_case_chars:   int   = 400
    # Anthropic model used for generation (swapped in the API call)
    llm_model:        str   = "claude-sonnet-4-20250514"
    max_tokens:       int   = 800
    temperature:      float = 0.3


@dataclass
class APIConfig:
    """FastAPI server settings."""
    host:             str   = os.getenv("API_HOST", "0.0.0.0")
    port:             int   = int(os.getenv("PORT", os.getenv("API_PORT", "8000")))
    reload:           bool  = os.getenv("API_RELOAD", "false").lower() == "true"
    workers:          int   = int(os.getenv("API_WORKERS", "1"))
    log_level:        str   = os.getenv("API_LOG_LEVEL", "info")
    cors_origins:     List[str] = field(default_factory=lambda: ["*"])


@dataclass
class PreprocessConfig:
    """Text cleaning settings."""
    remove_stopwords: bool  = True
    lemmatize:        bool  = False
    min_text_length:  int   = 20         # Drop rows shorter than this (chars)
    # Extra legal stopwords that add no signal
    legal_stopwords:  List[str] = field(default_factory=lambda: [
        "court", "plaintiff", "defendant", "case", "judge",
        "ruling", "honor", "hereby", "therein", "thereof",
        "pursuant", "whereas", "aforementioned",
    ])


# ── Singleton instances ───────────────────────────────────────
PATHS      = PathConfig()
MODELS     = ModelConfig()
RETRIEVAL  = RetrievalConfig()
PREDICTION = PredictionConfig()
RAG        = RAGConfig()
API        = APIConfig()
PREPROCESS = PreprocessConfig()

# Ensure all directories exist when this module is first imported
PATHS.make_dirs()
