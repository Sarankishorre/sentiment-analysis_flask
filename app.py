from flask import Flask, request, jsonify
import os
import joblib
import numpy as np
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

app = Flask(__name__)

# Try to load model from `models/model.joblib` if available
MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")
MODEL_PATH = os.path.join(MODEL_DIR, "model.joblib")
VECT_PATH = os.path.join(MODEL_DIR, "vectorizer.joblib")

model = None
vectorizer = None
if os.path.exists(MODEL_PATH) and os.path.exists(VECT_PATH):
    try:
        model = joblib.load(MODEL_PATH)
        vectorizer = joblib.load(VECT_PATH)
    except Exception:
        model = None
        vectorizer = None


@app.route('/')
def hello_world():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Sentiment Analysis API</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 900px; margin: 50px auto; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
            .container { background: white; padding: 40px; border-radius: 12px; box-shadow: 0 8px 32px rgba(0,0,0,0.1); }
            h1 { color: #333; text-align: center; margin-bottom: 10px; }
            .subtitle { text-align: center; color: #666; margin-bottom: 30px; }
            .form-group { margin: 25px 0; }
            label { display: block; margin-bottom: 8px; font-weight: bold; color: #555; font-size: 14px; }
            textarea { width: 100%; padding: 12px; border: 2px solid #ddd; border-radius: 6px; font-size: 14px; font-family: Arial; resize: vertical; }
            textarea:focus { outline: none; border-color: #667eea; box-shadow: 0 0 8px rgba(102, 126, 234, 0.3); }
            button { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 12px 30px; border: none; border-radius: 6px; cursor: pointer; font-size: 16px; font-weight: bold; width: 100%; }
            button:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4); }
            button:active { transform: translateY(0); }
            .result { margin-top: 30px; padding: 25px; background: #f9f9f9; border-radius: 8px; display: none; }
            .result.show { display: block; }
            
            .sentiment-header { font-size: 28px; font-weight: bold; margin-bottom: 20px; padding-bottom: 15px; border-bottom: 3px solid #ddd; }
            .sentiment-positive { color: #28a745; }
            .sentiment-negative { color: #dc3545; }
            .sentiment-neutral { color: #ffc107; }
            
            .confidence-bars { margin-top: 20px; }
            .confidence-item { margin: 15px 0; }
            .confidence-label { display: flex; justify-content: space-between; margin-bottom: 6px; font-weight: bold; font-size: 14px; }
            .confidence-label-name { color: #555; }
            .confidence-label-value { color: #667eea; font-size: 16px; }
            .bar-background { background: #e9ecef; border-radius: 8px; height: 28px; overflow: hidden; position: relative; }
            .bar-fill { height: 100%; display: flex; align-items: center; justify-content: flex-end; padding-right: 10px; color: white; font-weight: bold; transition: width 0.5s ease; font-size: 12px; }
            .bar-positive { background: linear-gradient(90deg, #28a745, #20c997); }
            .bar-negative { background: linear-gradient(90deg, #dc3545, #fd7e14); }
            .bar-neutral { background: linear-gradient(90deg, #ffc107, #fd7e14); }
            
            .loading { display: none; text-align: center; color: #667eea; font-weight: bold; }
            .spinner { display: inline-block; width: 20px; height: 20px; border: 3px solid #e9ecef; border-top: 3px solid #667eea; border-radius: 50%; animation: spin 0.8s linear infinite; margin-right: 10px; }
            @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
            
            .error { background: #f8d7da; border: 2px solid #f5c6cb; color: #721c24; padding: 15px; border-radius: 6px; margin-top: 20px; }
            .endpoint-info { background: linear-gradient(135deg, #e7f3ff, #f0f7ff); padding: 18px; border-left: 4px solid #667eea; border-radius: 6px; margin-top: 30px; font-size: 13px; }
            .endpoint-info strong { color: #667eea; }
            .endpoint-info code { background: white; padding: 2px 6px; border-radius: 3px; font-family: monospace; }
            .meter-container { display: flex; gap: 15px; justify-content: space-around; margin-top: 20px; }
            .meter { text-align: center; flex: 1; }
            .meter-label { font-size: 12px; color: #666; margin-bottom: 5px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎯 Sentiment Analysis API</h1>
            <p class="subtitle">Powered by Machine Learning • Real-time Analysis</p>
            
            <div class="form-group">
                <label for="text">Enter Your Text:</label>
                <textarea id="text" rows="5" placeholder="Example: I absolutely love this product! It's amazing and works perfectly."></textarea>
            </div>
            
            <button onclick="predictSentiment()">🚀 Analyze Sentiment</button>
            <div class="loading" id="loading"><span class="spinner"></span>Analyzing sentiment...</div>
            
            <div class="result" id="result"></div>
            
            <div class="endpoint-info">
                <strong>📡 API Endpoints:</strong><br>
                • <code>POST /predict</code> - Get sentiment with confidence scores<br>
                • <code>GET /health</code> - Check server health<br>
                <strong>Request Format:</strong> <code>{"text": "your text"}</code> or <code>{"texts": ["text1", "text2"]}</code>
            </div>
        </div>
        
        <script>
            async function predictSentiment() {
                const text = document.getElementById('text').value.trim();
                if (!text) { 
                    alert('Please enter some text to analyze'); 
                    return; 
                }
                
                document.getElementById('loading').style.display = 'block';
                document.getElementById('result').classList.remove('show');
                
                try {
                    const response = await fetch('/predict', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ text: text })
                    });
                    
                    const data = await response.json();
                    const resultDiv = document.getElementById('result');
                    
                    if (response.ok) {
                        const result = data.predictions[0];
                        const sentiment = result.sentiment;
                        const confidence = result.confidence;
                        
                        let sentimentClass = 'sentiment-' + sentiment;
                        let html = `<div class="sentiment-header ${sentimentClass}">
                                        🎭 Sentiment: ${sentiment.toUpperCase()}
                                    </div>`;
                        
                        html += '<div class="confidence-bars">';
                        html += '<div style="color: #666; font-size: 13px; margin-bottom: 15px; font-weight: bold;">Confidence Scores:</div>';
                        
                        // Sort by value descending to show highest first
                        const sorted = Object.entries(confidence).sort((a, b) => b[1] - a[1]);
                        
                        sorted.forEach(([label, score]) => {
                            const barClass = 'bar-' + label;
                            const displayLabel = label.charAt(0).toUpperCase() + label.slice(1);
                            html += `
                                <div class="confidence-item">
                                    <div class="confidence-label">
                                        <span class="confidence-label-name">${displayLabel}</span>
                                        <span class="confidence-label-value">${score.toFixed(2)}%</span>
                                    </div>
                                    <div class="bar-background">
                                        <div class="bar-fill ${barClass}" style="width: ${score}%">${score > 15 ? score.toFixed(1) + '%' : ''}</div>
                                    </div>
                                </div>
                            `;
                        });
                        
                        html += '</div>';
                        resultDiv.innerHTML = html;
                        resultDiv.classList.add('show');
                    } else {
                        resultDiv.innerHTML = `<div class="error"><strong>Error:</strong> ${data.error}</div>`;
                        resultDiv.classList.add('show');
                    }
                } catch (error) {
                    document.getElementById('result').innerHTML = `<div class="error"><strong>Error:</strong> ${error.message}</div>`;
                    document.getElementById('result').classList.add('show');
                } finally {
                    document.getElementById('loading').style.display = 'none';
                }
            }
            
            // Allow Ctrl+Enter to submit
            document.getElementById('text').addEventListener('keypress', function(e) {
                if (e.key === 'Enter' && e.ctrlKey) predictSentiment();
            });
        </script>
    </body>
    </html>
    '''


@app.route('/health')
def health():
    return {"message": "ok", "model_loaded": bool(model), "text_model": bool(vectorizer)}


def _clean_text(text):
    try:
        sw = set(stopwords.words('english'))
        sw.discard('not')
    except Exception:
        sw = set()
    ps = PorterStemmer()
    text = re.sub('[^a-zA-Z]', ' ', str(text))
    tokens = text.lower().split()
    return ' '.join(ps.stem(t) for t in tokens if t not in sw)


@app.route('/predict', methods=['POST'])
def predict():
    """POST /predict

    - If JSON contains `text` (string) or `texts` (list of strings), returns sentiment.
    - Else falls back to numeric `input` array handling.
    """
    data = request.get_json(force=True)
    if not data:
        return jsonify({"error": "Empty JSON body."}), 400

    # Text-based sentiment prediction
    if 'text' in data or 'texts' in data:
        if model is None or vectorizer is None:
            return jsonify({"error": "Text model not loaded. Run export_model.py to create model and vectorizer."}), 500

        texts = data.get('texts') or [data.get('text')]
        if isinstance(texts, str):
            texts = [texts]

        cleaned = [_clean_text(t) for t in texts]
        X = vectorizer.transform(cleaned)
        try:
            preds = model.predict(X).tolist()
            # Get confidence scores (probabilities)
            probs = model.predict_proba(X)
            classes = model.classes_.tolist()
            
            # Build response with confidence scores
            results = []
            for i, pred in enumerate(preds):
                confidence_dict = {}
                for j, cls in enumerate(classes):
                    confidence_dict[cls] = round(float(probs[i][j]) * 100, 2)
                results.append({
                    "sentiment": pred,
                    "confidence": confidence_dict
                })
            
            return jsonify({"predictions": results})
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    # Numeric/predict fallback (old behavior)
    if model is None:
        return jsonify({"error": "Model not loaded. Run the training script to create `models/model.joblib`."}), 500

    if 'input' not in data:
        return jsonify({"error": "Missing 'input' in JSON body."}), 400

    X = data['input']
    if isinstance(X, list) and (len(X) == 0 or not isinstance(X[0], list)):
        X = [X]

    try:
        X_arr = np.array(X)
        preds = model.predict(X_arr).tolist()
        return jsonify({"predictions": preds})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
