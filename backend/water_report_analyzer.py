import cv2
import numpy as np
import re
import joblib
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
import os

# Try to use pytesseract if available, otherwise use PIL
tesseract_available = False
try:
    import pytesseract
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    pytesseract.get_tesseract_version()
    tesseract_available = True
    print('Tesseract found and ready.')
except Exception:
    try:
        from PIL import Image
        import struct
        print('Tesseract not found. Using PIL fallback OCR.')
    except Exception:
        print('Using basic fallback mode.')

app = Flask(__name__)
CORS(app)

PARAMS = ['ph', 'Hardness', 'Solids', 'Chloramines', 'Sulfate',
          'Conductivity', 'Organic_carbon', 'Trihalomethanes', 'Turbidity']

MODEL_PATH = 'water_quality_model.pkl'

def train_model():
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'archive (6)', 'water_potability.csv')
    df = pd.read_csv(csv_path)
    X = df[PARAMS]
    y = df['Potability']
    pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='mean')),
        ('model', RandomForestClassifier(n_estimators=100, random_state=42))
    ])
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    pipeline.fit(X_train, y_train)
    acc = pipeline.score(X_test, y_test)
    print(f"Model trained. Accuracy: {acc:.2f}")
    joblib.dump(pipeline, MODEL_PATH)
    return pipeline

def load_model():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    return train_model()

model = load_model()

def preprocess_image(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh

def extract_text(image_path):
    if tesseract_available:
        processed = preprocess_image(image_path)
        config = '--oem 3 --psm 6'
        return pytesseract.image_to_string(processed, config=config)
    else:
        # Fallback: try to read filename or return empty so manual entry is used
        return ''

def parse_parameters(text):
    extracted = {}
    patterns = {
        'ph':              r'ph[\s:=]+([0-9]+\.?[0-9]*)',
        'Hardness':        r'hardness[\s:=]+([0-9]+\.?[0-9]*)',
        'Solids':          r'solids[\s:=]+([0-9]+\.?[0-9]*)',
        'Chloramines':     r'chloramines[\s:=]+([0-9]+\.?[0-9]*)',
        'Sulfate':         r'sulfate[\s:=]+([0-9]+\.?[0-9]*)',
        'Conductivity':    r'conductivity[\s:=]+([0-9]+\.?[0-9]*)',
        'Organic_carbon':  r'organic[\s_]?carbon[\s:=]+([0-9]+\.?[0-9]*)',
        'Trihalomethanes': r'trihalomethanes[\s:=]+([0-9]+\.?[0-9]*)',
        'Turbidity':       r'turbidity[\s:=]+([0-9]+\.?[0-9]*)',
    }
    text_lower = text.lower()
    for param, pattern in patterns.items():
        match = re.search(pattern, text_lower)
        if match:
            extracted[param] = float(match.group(1))
    return extracted

def predict_potability(params):
    row = {p: params.get(p, np.nan) for p in PARAMS}
    df = pd.DataFrame([row])
    prediction = model.predict(df)[0]
    proba = model.predict_proba(df)[0]
    return int(prediction), float(max(proba))

@app.route('/api/analyze-report', methods=['POST'])
def analyze_report():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    file = request.files['image']
    filepath = os.path.join('uploads', file.filename)
    os.makedirs('uploads', exist_ok=True)
    file.save(filepath)

    try:
        text = extract_text(filepath)
        params = parse_parameters(text)

        # If OCR not available or no params found, use default mean values
        # so prediction still works
        if not tesseract_available:
            return jsonify({
                'error': 'Tesseract OCR not installed',
                'tip': 'Install Tesseract from https://github.com/UB-Mannheim/tesseract/wiki then restart the server.',
                'install_url': 'https://github.com/UB-Mannheim/tesseract/wiki',
                'raw_text': ''
            }), 422

        if not params:
            return jsonify({
                'error': 'Could not extract parameters from image',
                'raw_text': text,
                'tip': 'Ensure the image contains labeled water quality parameters like: pH: 7.2, Turbidity: 3.5'
            }), 422

        prediction, confidence = predict_potability(params)

        return jsonify({
            'prediction': prediction,
            'result': 'Water is Safe ✅' if prediction == 1 else 'Water is Contaminated ❌',
            'confidence': round(confidence * 100, 2),
            'extracted_parameters': params,
            'missing_parameters': [p for p in PARAMS if p not in params],
            'raw_text': text
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/tesseract-status', methods=['GET'])
def tesseract_status():
    return jsonify({
        'available': tesseract_available,
        'message': 'Tesseract is ready' if tesseract_available else 'Tesseract not installed. Download from https://github.com/UB-Mannheim/tesseract/wiki'
    })

@app.route('/api/predict-manual', methods=['POST'])
def predict_manual():
    data = request.json
    try:
        params = {p: float(data[p]) for p in PARAMS if p in data}
        prediction, confidence = predict_potability(params)
        return jsonify({
            'prediction': prediction,
            'result': 'Water is Safe ✅' if prediction == 1 else 'Water is Contaminated ❌',
            'confidence': round(confidence * 100, 2),
            'parameters_used': params
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
