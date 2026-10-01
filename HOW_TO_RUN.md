# 🚀 How to Run the Legal Judgment Prediction System

## Quick Start (System Already Running)

Your system is currently running with:
- ✅ **Frontend**: http://localhost:8501 (Streamlit)
- ✅ **API**: http://localhost:8000 (FastAPI)
- 🔄 **Training**: Building models with 32,406 cases

---

## 1️⃣ **Start the Entire System**

### On Windows (PowerShell):

```powershell
# Navigate to project directory
cd 'c:\Users\Raj Kumar\Downloads\legal_judgment_prediction_system\legal_judgment_prediction_system'

# Terminal 1: Start FastAPI Backend
& '.venv\Scripts\uvicorn.exe' api.main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2: Start Streamlit Frontend
& '.venv\Scripts\streamlit.exe' run frontend/app.py
```

### On Linux/Mac:

```bash
cd legal_judgment_prediction_system

# Terminal 1: Backend
source .venv/bin/activate
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2: Frontend
streamlit run frontend/app.py
```

---

## 2️⃣ **Import New Dataset**

### Import complete dataset:
```powershell
cd 'path\to\legal_judgment_prediction_system'
& '.venv\Scripts\python.exe' scripts/import_new_dataset.py 'D:\case_files_total.csv.xlsx'
```

### Import sample (faster for testing):
```powershell
& '.venv\Scripts\python.exe' scripts/import_new_dataset.py 'D:\case_files_total.csv.xlsx' --sample 100
```

### Validate without importing:
```powershell
& '.venv\Scripts\python.exe' scripts/import_new_dataset.py 'D:\my_dataset.csv' --validate-only
```

### Replace entire dataset:
```powershell
& '.venv\Scripts\python.exe' scripts/import_new_dataset.py 'D:\new_cases.xlsx' --replace
```

**Arguments**:
- `--sample N`: Import only N random cases
- `--replace`: Replace existing dataset instead of appending
- `--validate-only`: Check format without importing

---

## 3️⃣ **Build/Train ML Models**

### Full rebuild (with new dataset):
```powershell
& '.venv\Scripts\python.exe' scripts/build_index.py --force
```

### Normal build (load cached embeddings if available):
```powershell
& '.venv\Scripts\python.exe' scripts/build_index.py
```

**What it does**:
1. Preprocessing - cleans & normalizes text
2. Embedding - generates Legal Longformer vectors
3. FAISS Index - builds search index
4. Logistic Regression - trains classifier
5. Metrics - evaluates performance

**Time**: 45-90 minutes for full dataset (depends on CPU)

---

## 4️⃣ **Run Performance Tests**

### Full performance test suite:
```powershell
& '.venv\Scripts\python.exe' tests/performance_test.py
```

### Check single endpoint:
```powershell
& '.venv\Scripts\python.exe' -c "
import httpx
r = httpx.get('http://localhost:8000/health', timeout=5)
print(f'API Status: {r.status_code}')
print(r.json())
"
```

---

## 5️⃣ **Run Tests**

### Full test suite:
```powershell
pytest tests/ -v
```

### Test specific file:
```powershell
pytest tests/test_pipeline.py -v
```

### With coverage report:
```powershell
pytest tests/ --cov=src --cov-report=html
```

---

## 6️⃣ **API Direct Commands**

### Health check:
```powershell
curl http://localhost:8000/health
```

### Get metrics:
```powershell
curl http://localhost:8000/metrics
```

### Make prediction (POST):
```powershell
$body = @{
    case_text = "The defendant was charged with assault..."
} | ConvertTo-Json

curl -X POST http://localhost:8000/predict `
  -ContentType "application/json" `
  -Body $body
```

---

## 7️⃣ **Check Dataset Status**

### Count cases:
```powershell
cd 'legal_judgment_prediction_system'
& '.venv\Scripts\python.exe' -c "
import pandas as pd
df = pd.read_csv('data/cases.csv')
print(f'Total cases: {len(df)}')
print(f'Guilty: {(df.label == \"guilty\").sum()}')
print(f'Not Guilty: {(df.label == \"not_guilty\").sum()}')
"
```

---

## 8️⃣ **View Logs**

### Latest log file:
```powershell
ls src/logs/ | Sort-Object LastWriteTime -Descending | Select-Object -First 1 | % { cat $_.FullName -Tail 50 }
```

### Watch logs in real-time:
```powershell
Get-Content src/logs/latest.log -Wait
```

---

## 9️⃣ **Environment Setup**

### Install dependencies:
```powershell
pip install -r requirements.txt
pip install streamlit
```

### Check Python version:
```powershell
python --version
```

### Activate virtual environment:
```powershell
# Windows
.venv\Scripts\Activate.ps1

# Linux/Mac
source .venv/bin/activate
```

---

## 🔟 **Working with Configuration**

### View/Edit config:
```powershell
cat config.py
```

### Update settings:
Edit `config.py` directly:
```python
# Model settings
EMBEDDING_MODEL = "distiluse-base-multilingual-cased-v2"  # Switch models here

# API settings
API_HOST = "0.0.0.0"
API_PORT = 8000

# Paths
PATHS.EMBEDDINGS_DIR = Path("embeddings")
PATHS.MODELS_DIR = Path("models")
```

---

## 📊 **Complete Workflow**

```
1. Import Dataset
   └─ python scripts/import_new_dataset.py <file>

2. Build Models
   └─ python scripts/build_index.py --force

3. Start Backend
   └─ uvicorn api.main:app --reload

4. Start Frontend
   └─ streamlit run frontend/app.py

5. Open Browser
   └─ http://localhost:8501

6. Test Performance
   └─ python tests/performance_test.py

7. View Results
   └─ API: http://localhost:8000/metrics
   └─ Logs: src/logs/
```

---

## 🆘 Troubleshooting

### Port already in use:
```powershell
# Change port in api/main.py or use:
uvicorn api.main:app --port 9000
```

### API not responding:
```powershell
# Check if running:
Get-NetTCPConnection -LocalPort 8000 -State Listen

# Restart:
# Kill process and run again
```

### Streamlit cache issues:
```powershell
streamlit cache clear
```

### Out of memory (large dataset):
```powershell
# Use --sample during import
python scripts/import_new_dataset.py data.xlsx --sample 1000
```

---

## 📝 Quick Reference

| Task | Command |
|------|---------|
| Import data | `python scripts/import_new_dataset.py <file>` |
| Train model | `python scripts/build_index.py --force` |
| Start API | `uvicorn api.main:app --reload` |
| Start UI | `streamlit run frontend/app.py` |
| Test API | `python tests/performance_test.py` |
| Check metrics | `curl http://localhost:8000/metrics` |
| View config | `cat config.py` |

