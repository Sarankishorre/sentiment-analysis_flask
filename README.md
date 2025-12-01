# Sentiment Analysis Flask API

A production-ready Flask API for sentiment analysis powered by machine learning. Predicts whether text is **Positive**, **Negative**, or **Neutral** with ~75% accuracy using an ensemble of tree-based classifiers.

## 📊 Project Overview

This project deploys a sentiment classification model trained on Twitter sentiment data. It provides:
- **REST API endpoint** for real-time sentiment predictions
- **Interactive web interface** with visual confidence scores
- **High-accuracy ensemble model** (75% accuracy on test data)
- **Production-ready architecture** with easy deployment

## 🎯 Model Performance

| Metric | Score |
|--------|-------|
| **Overall Accuracy** | **74.96%** |
| **Precision (Weighted)** | 0.7183 |
| **Recall (Weighted)** | 0.6993 |
| **F1 Score (Weighted)** | 0.6982 |

### Per-Class Performance
```
Class        Precision  Recall  F1-Score  Support
─────────────────────────────────────────────────
Negative       0.79     0.56     0.65     1,556
Neutral        0.62     0.80     0.70     2,224
Positive       0.78     0.70     0.74     1,717
─────────────────────────────────────────────────
Average        0.72     0.70     0.70     5,497
```

## 🏗️ Model Architecture

The sentiment classifier uses a **Voting Ensemble** combining three tree-based models for robust predictions:

### 1. Random Forest (200 trees)
- max_depth=20, max_features='sqrt'
- class_weight='balanced' for handling imbalanced data
- Good at capturing non-linear patterns

### 2. Gradient Boosting (150 trees)
- learning_rate=0.1, max_depth=7
- Iteratively improves weak learners
- Excellent for sequential error correction

### 3. Extra Trees (200 trees)
- max_depth=20, max_features='sqrt'
- Adds randomness for better generalization
- Reduces overfitting via randomization

**Combination Strategy**: All three models vote with **soft probabilities** (averaging predicted probabilities) for final predictions, combining their strengths.

## 📚 Training Data & Pipeline

### Dataset Information
- **Source**: Twitter Sentiment Analysis Dataset
- **Total Samples**: 27,481 tweets
- **Train/Test Split**: 80% training (21,984), 20% testing (5,497)
- **Split Type**: Stratified (preserves class distribution)
- **Labels**: 3 classes (negative, neutral, positive)

### Class Distribution
```
Neutral   : 11,118 samples (40.4%)
Positive  :  8,582 samples (31.2%)
Negative  :  7,781 samples (28.3%)
```

### Data Processing Pipeline

```
┌─────────────────────────────────────────┐
│       Raw Text Input from User          │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│        Text Preprocessing Stage         │
├─────────────────────────────────────────┤
│ 1. Convert to lowercase                 │
│ 2. Remove URLs and emails               │
│ 3. Remove special characters            │
│ 4. Expand contractions                  │
│    (don't → do not, i'm → i am)        │
│ 5. Tokenization (split into words)      │
│ 6. Remove stopwords (keeping "not")     │
│ 7. Apply Porter Stemmer normalization   │
│    (loving → love, running → run)       │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│   TF-IDF Vectorization Stage            │
├─────────────────────────────────────────┤
│ • Max Features: 4,000 dimensions        │
│ • N-grams: (1,2) - single & bigrams     │
│ • Min document frequency: 2             │
│ • Max document frequency: 85%           │
│ • Sublinear TF scaling: True            │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│     Ensemble Prediction Stage           │
├─────────────────────────────────────────┤
│ ┌────────────────────────────────────┐  │
│ │ Random Forest Prediction           │  │
│ │ [prob_neg, prob_neu, prob_pos]     │  │
│ └────────────────────────────────────┘  │
│ ┌────────────────────────────────────┐  │
│ │ Gradient Boosting Prediction       │  │
│ │ [prob_neg, prob_neu, prob_pos]     │  │
│ └────────────────────────────────────┘  │
│ ┌────────────────────────────────────┐  │
│ │ Extra Trees Prediction             │  │
│ │ [prob_neg, prob_neu, prob_pos]     │  │
│ └────────────────────────────────────┘  │
│         ↓ Soft Voting ↓                │
│   Average all 3 predictions             │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│    Output: Sentiment + Confidence       │
│                                         │
│ Sentiment: POSITIVE                     │
│ Positive:  78.5%                        │
│ Neutral:   15.3%                        │
│ Negative:   6.2%                        │
└─────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### Installation (Windows PowerShell)

1. **Clone the repository**
```powershell
git clone https://github.com/Sarankishorre/sentiment-analysis_flask.git
cd sentiment-analysis_flask
```

2. **Create virtual environment**
```powershell
python -m venv .venv
. .\.venv\Scripts\Activate.ps1
```

3. **Install dependencies**
```powershell
pip install -r requirements.txt
```

4. **Run the Flask server**
```powershell
python app.py
```

The API will start on `http://localhost:5000`

### Installation (Linux/Mac)

```bash
git clone https://github.com/Sarankishorre/sentiment-analysis_flask.git
cd sentiment-analysis_flask
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

## 🌐 API Endpoints

### 1. **GET /** - Interactive Web Interface
Visit `http://localhost:5000` in your browser

**Features:**
- User-friendly text input form
- Real-time sentiment prediction
- Color-coded sentiment display (🟢 Positive, 🔴 Negative, 🟡 Neutral)
- Confidence percentage bars for all 3 classes
- Smooth animations and modern UI

### 2. **GET /health** - Health Check

```bash
curl http://localhost:5000/health
```

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "timestamp": "2025-12-01T10:30:00"
}
```

### 3. **POST /predict** - Sentiment Prediction

```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "I absolutely love this product!"}'
```

**Request:**
```json
{
  "text": "Your text to analyze"
}
```

**Response:**
```json
{
  "predictions": [
    {
      "sentiment": "positive",
      "confidence": {
        "positive": 0.785,
        "neutral": 0.153,
        "negative": 0.062
      }
    }
  ],
  "success": true
}
```

## 💻 Usage Examples

### Python
```python
import requests

url = "http://localhost:5000/predict"
text = "This movie was absolutely amazing! Best film ever."

response = requests.post(url, json={"text": text})
result = response.json()

sentiment = result['predictions'][0]['sentiment']
confidence = result['predictions'][0]['confidence']

print(f"Sentiment: {sentiment.upper()}")
print(f"Confidence Scores:")
print(f"  Positive: {confidence['positive']*100:.1f}%")
print(f"  Neutral:  {confidence['neutral']*100:.1f}%")
print(f"  Negative: {confidence['negative']*100:.1f}%")
```

### JavaScript/Fetch
```javascript
const analyzeText = async (text) => {
  const response = await fetch('http://localhost:5000/predict', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text: text })
  });
  
  const data = await response.json();
  const pred = data.predictions[0];
  
  console.log(`Sentiment: ${pred.sentiment}`);
  console.log(`Confidence: ${JSON.stringify(pred.confidence)}`);
};

analyzeText("I'm so happy today!");
```

### cURL
```bash
# Positive sentiment
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"text":"I love this! Absolutely fantastic!"}'

# Negative sentiment
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"text":"This is terrible and disappointing."}'

# Neutral sentiment
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"text":"The weather is cloudy today."}'
```

## 📁 Project Structure

```
sentiment-analysis_flask/
│
├── app.py                          # Main Flask application & API routes
├── requirements.txt                # Python package dependencies
├── README.md                       # This documentation file
│
├── 📁 models/
│   ├── model.joblib               # Trained voting ensemble (20MB)
│   └── vectorizer.joblib          # TF-IDF vectorizer (146KB)
│
├── 📁 sentiment-analysis/
│   ├── train.csv                  # Training dataset (27,481 tweets)
│   ├── README.md                  # Dataset details
│   └── sentiment_analysis.ipynb   # Jupyter notebook with EDA
│
├── 📄 HOW_IT_WORKS.md             # Technical deep-dive
├── 📄 COMMANDS.md                 # Useful CLI commands
├── 📄 INDEX.md                    # Project index
│
├── 📁 .venv/                      # Virtual environment (local, not in repo)
└── 📁 __pycache__/                # Python cache (local, not in repo)
```

## ⚙️ Technical Details

### Dependencies
```
Flask==2.0.0+              # Web framework
scikit-learn==1.0.0+       # Machine learning library
joblib==1.0.0+            # Model serialization
numpy==1.21.0+            # Numerical computing
pandas==1.3.0+            # Data manipulation
nltk==3.5.0+              # Natural language processing
```

Full list in `requirements.txt`

### Model Files
- **model.joblib** (20 MB): Serialized voting ensemble classifier
- **vectorizer.joblib** (146 KB): Fitted TF-IDF vectorizer

### Preprocessing Features
- Lowercase normalization
- URL/email removal
- Special character cleaning
- Contraction expansion (don't → do not)
- Tokenization and stopword removal
- Porter Stemmer normalization
- TF-IDF vectorization with bigrams

## 🔧 Configuration

### Model Hyperparameters
Edit `sentiment-analysis/train_voting_ensemble.py` to adjust:
- Number of trees in classifiers
- Max depth and other tree parameters
- TF-IDF feature count and n-grams
- Train/test split ratio

### API Settings
Edit `app.py` to modify:
- Port number (line: `app.run(port=5000)`)
- Debug mode (for development)
- CORS headers
- Preprocessing functions

## 📖 Additional Documentation

- **[HOW_IT_WORKS.md](HOW_IT_WORKS.md)** - Deep technical documentation
- **[COMMANDS.md](COMMANDS.md)** - Useful command line tools
- **[INDEX.md](INDEX.md)** - Project file index

## 🚀 Deployment

### Local Development
```powershell
python app.py
```

### Production with Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker Deployment
```bash
docker build -t sentiment-api .
docker run -p 5000:5000 sentiment-api
```

## ✅ Limitations & Improvements

### Current Limitations
- Trained on Twitter data (may not work well on other domains)
- Limited to English text
- Doesn't capture sarcasm well
- Accuracy limited to ~75% due to dataset characteristics

### Potential Improvements
- Use BERT/DistilBERT for 80-85% accuracy
- Add custom training data for your domain
- Implement sarcasm detection
- Add multilingual support
- Implement keyword boosting for emotional terms

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Commit: `git commit -m 'Add amazing feature'`
5. Push: `git push origin feature/amazing-feature`
6. Open a Pull Request

## 📝 License

Open source - MIT License

## 👤 Author

**Saran Kishore**
- GitHub: [@Sarankishorre](https://github.com/Sarankishorre)
- Project: [sentiment-analysis_flask](https://github.com/Sarankishorre/sentiment-analysis_flask)

## 📞 Support & Contact

For issues, questions, or suggestions:
- Open an issue on [GitHub Issues](https://github.com/Sarankishorre/sentiment-analysis_flask/issues)
- Check documentation in [HOW_IT_WORKS.md](HOW_IT_WORKS.md)
- Review this README for common questions

---

**Project Status**: ✅ Production Ready  
**Last Updated**: December 1, 2025  
**Model Accuracy**: 74.96%  
**Training Dataset**: 27,481 Twitter sentiment tweets  
**Ensemble Models**: Random Forest + Gradient Boosting + Extra Trees
