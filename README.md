# Flask ML model API

This repository contains a minimal Flask API to serve a scikit-learn model.

Quick start (PowerShell on Windows):

```powershell
python -m venv .venv
. .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python train_model.py    # creates models/model.joblib
python app.py            # starts server on port 5000
```

Endpoints:
- `GET /` - basic message
- `GET /health` - health check and whether model loaded
- `POST /predict` - get predictions

Predict request examples:

Single sample (Iris features):

```bash
curl -X POST http://localhost:5000/predict -H "Content-Type: application/json" -d "{\"input\":[5.1,3.5,1.4,0.2]}"
```

Batch samples:

```bash
curl -X POST http://localhost:5000/predict -H "Content-Type: application/json" -d "{\"input\": [[5.1,3.5,1.4,0.2],[6.2,3.4,5.4,2.3]]}"
```

If you need the API to load your own model, replace `models/model.joblib` with your serialized scikit-learn estimator.
