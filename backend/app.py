from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import sys
from datetime import datetime, timedelta
import jwt
import hashlib

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.water_model import WaterContaminationModel
from models.disease_predictor import DiseasePredictionEngine
from models.risk_analyzer import RiskAnalysisEngine
from utils.geo_mapper import GeographicMapper
from utils.alert_system import AlertSystem
from utils.lab_report_extractor import LabReportExtractor

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

SECRET_KEY = 'your-secret-key-change-in-production'
users_db = {}  # In production, use a real database

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load trained model if available, otherwise use base model
trained_model_path = 'trained_water_model.h5'
water_model = WaterContaminationModel(trained_model_path if os.path.exists(trained_model_path) else None)
disease_engine = DiseasePredictionEngine()
risk_analyzer = RiskAnalysisEngine()
geo_mapper = GeographicMapper()
alert_system = AlertSystem()
lab_extractor = LabReportExtractor()

# Register default NGOs if none exist
if not alert_system.ngo_contacts:
    alert_system.register_ngo(
        "Northeast Health Department", 
        "health@northeast.gov.in", 
        "+91-9876543210", 
        "Northeast India"
    )
    alert_system.register_ngo(
        "Community Health NGO", 
        "alerts@communityhealth.org", 
        "+91-9876543211", 
        "Assam"
    )

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    except:
        return None

@app.route('/api/auth/signup', methods=['POST'])
def signup():
    data = request.json
    email = data.get('email')
    
    if email in users_db:
        return jsonify({'error': 'Email already exists'}), 400
    
    users_db[email] = {
        'name': data.get('name'),
        'email': email,
        'password': hash_password(data.get('password')),
        'role': data.get('role', 'user')
    }
    
    return jsonify({'message': 'Account created successfully'})

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = hash_password(data.get('password'))
    
    if email not in users_db or users_db[email]['password'] != password:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    token = jwt.encode({
        'email': email,
        'exp': datetime.utcnow() + timedelta(days=7)
    }, SECRET_KEY, algorithm='HS256')
    
    return jsonify({
        'token': token,
        'user': {'name': users_db[email]['name'], 'email': email, 'role': users_db[email]['role']}
    })

@app.route('/api/extract-lab-report', methods=['POST'])
def extract_lab_report():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    try:
        file = request.files['file']
        ext = os.path.splitext(file.filename)[1].lower()
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        if ext == '.pdf':
            result = lab_extractor.extract_from_pdf(filepath)
        elif ext in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']:
            result = lab_extractor.extract_from_image(filepath)
        else:
            return jsonify({'error': 'Unsupported file type. Use PDF, JPG, or PNG'}), 400

        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def analyze_water():
    if request.method == 'OPTIONS':
        return '', 204
    
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    try:
        file = request.files['image']
        location = request.form.get('location', 'Unknown')
        latitude = float(request.form.get('latitude', 26.2006))
        longitude = float(request.form.get('longitude', 92.9376))
        
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        
        contamination_result = water_model.predict(filepath)
        diseases = disease_engine.predict_diseases(contamination_result)
        water_quality = disease_engine.get_water_quality_status(contamination_result)
        
        risk_analyzer.add_analysis_record(
            location, latitude, longitude, water_quality, diseases
        )
        
        risk_level = risk_analyzer.get_location_risk_level(location)
        
        alert = None
        if water_quality in ['Moderately Unsafe', 'Highly Contaminated']:
            alert = alert_system.create_alert(
                location, risk_level, water_quality, diseases, latitude, longitude
            )
            alert_system.dispatch_alerts(alert)
        
        return jsonify({
            'contamination': contamination_result,
            'water_quality': water_quality,
            'diseases': diseases,
            'risk_level': risk_level,
            'alert': {
                'alert_id': alert['alert_id'],
                'status': alert['status']
            } if alert else None
        })
    except Exception as e:
        print(f"Error in analyze: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/risk-map', methods=['GET'])
def get_risk_map():
    try:
        risk_map = geo_mapper.create_risk_map()
        map_html = risk_map._repr_html_()
        return map_html
    except Exception as e:
        print(f"Error creating risk map: {e}")
        # Return a simple fallback map
        import folium
        fallback_map = folium.Map(location=[26.2006, 92.9376], zoom_start=5)
        folium.Marker([26.2006, 92.9376], popup='Guwahati, Assam').add_to(fallback_map)
        return fallback_map._repr_html_()

@app.route('/api/hotspot-summary', methods=['GET'])
def get_hotspot_summary():
    try:
        summary = geo_mapper.hotspot_analyzer.get_risk_summary()
        return jsonify(summary)
    except Exception as e:
        print(f"Error getting hotspot summary: {e}")
        return jsonify({'high_risk': 0, 'medium_risk': 0, 'low_risk': 0, 'total_locations': 0})

@app.route('/api/hotspot-locations', methods=['GET'])
def get_hotspot_locations():
    """Get all hotspot locations, optionally filtered by risk level"""
    risk_level = request.args.get('risk_level', 'all')
    if risk_level == 'all':
        locations = geo_mapper.hotspot_analyzer.risk_locations
    else:
        locations = geo_mapper.get_hotspot_locations_by_risk(risk_level)
    
    # Serialize for JSON (convert any non-serializable types)
    serialized = []
    for loc in locations:
        serialized.append({
            'location': str(loc.get('location', '')),
            'state': str(loc.get('state', '')),
            'latitude': float(loc.get('latitude', 0)),
            'longitude': float(loc.get('longitude', 0)),
            'risk_level': str(loc.get('risk_level', 'Low Risk')),
            'risk_score': int(loc.get('risk_score', 0)),
            'ph': str(loc.get('ph', 'N/A')),
            'bod': str(loc.get('bod', 'N/A')),
            'fecal_coliform': str(loc.get('fecal_coliform', 'N/A')),
            'total_coliform': str(loc.get('total_coliform', 'N/A')),
            'year': str(loc.get('year', 'N/A'))
        })
    return jsonify({'locations': serialized, 'total': len(serialized)})

@app.route('/api/filtered-risk-map', methods=['GET'])
def get_filtered_risk_map():
    try:
        risk_levels = request.args.getlist('risk_levels')
        if not risk_levels:
            risk_levels = ['High Risk', 'Medium Risk', 'Low Risk']
        
        risk_map = geo_mapper.create_filtered_risk_map(risk_levels)
        map_html = risk_map._repr_html_()
        return map_html
    except Exception as e:
        print(f"Error creating filtered map: {e}")
        import folium
        fallback_map = folium.Map(location=[26.2006, 92.9376], zoom_start=5)
        return fallback_map._repr_html_()

@app.route('/api/patterns', methods=['GET'])
def get_patterns():
    patterns = risk_analyzer.analyze_patterns()
    high_risk = risk_analyzer.identify_high_risk_locations()
    return jsonify({
        'patterns': patterns,
        'high_risk_locations': high_risk
    })

@app.route('/api/ngo/register', methods=['POST'])
def register_ngo():
    data = request.json
    ngo_id = alert_system.register_ngo(
        data['name'], data['email'], data['phone'], data['region']
    )
    return jsonify({'ngo_id': ngo_id, 'status': 'registered'})

@app.route('/api/ngo/respond', methods=['POST'])
def ngo_respond():
    data = request.json
    response = alert_system.record_response(
        data['alert_id'], data['ngo_id'], data['action_taken']
    )
    return jsonify({'status': 'recorded', 'response': response})

@app.route('/api/alerts/pending', methods=['GET'])
def get_pending_alerts():
    pending = alert_system.check_pending_alerts()
    return jsonify({'pending_alerts': pending})

@app.route('/api/alerts/statistics', methods=['GET'])
def get_alert_statistics():
    stats = alert_system.get_response_statistics()
    return jsonify(stats)

@app.route('/api/alerts/resolve/<alert_id>', methods=['POST'])
def resolve_alert(alert_id):
    """Resolve/acknowledge an alert"""
    data = request.json or {}
    resolution_notes = data.get('notes', 'Alert resolved')
    
    for alert in alert_system.alert_history:
        if alert['alert_id'] == alert_id:
            alert['status'] = 'Resolved'
            alert['resolved_at'] = datetime.now()
            alert['resolution_notes'] = resolution_notes
            
            return jsonify({
                'status': 'success',
                'message': f'Alert {alert_id} resolved successfully',
                'alert': {
                    'alert_id': alert['alert_id'],
                    'status': alert['status'],
                    'resolved_at': alert['resolved_at'].strftime('%Y-%m-%d %H:%M:%S')
                }
            })
    
    return jsonify({'error': f'Alert {alert_id} not found'}), 404

@app.route('/api/alerts/history', methods=['GET'])
def get_alert_history():
    history = [{
        'alert_id': a['alert_id'],
        'location': a['location'],
        'timestamp': a['timestamp'].strftime('%Y-%m-%d %H:%M:%S'),
        'risk_level': a['risk_level'],
        'status': a['status'],
        'diseases': a['diseases']
    } for a in alert_system.alert_history]
    return jsonify({'alerts': history})

# In-memory store for doctor appointments
doctor_appointments = []

@app.route('/api/doctor/book', methods=['POST'])
def book_doctor_appointment():
    data = request.json
    data['server_timestamp'] = datetime.now().isoformat()
    doctor_appointments.append(data)
    return jsonify({'status': 'success', 'appointment_id': data.get('id')})

@app.route('/api/doctor/appointments', methods=['GET'])
def get_doctor_appointments():
    return jsonify({'appointments': doctor_appointments})

@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    data = request.json
    feedback = {
        'name': data.get('name'),
        'email': data.get('email'),
        'rating': data.get('rating'),
        'message': data.get('message'),
        'timestamp': datetime.now()
    }
    print(f"Feedback received: {feedback}")
    return jsonify({'status': 'success', 'message': 'Thank you for your feedback!'})

@app.route('/api/chatbot', methods=['POST'])
def chatbot():
    data = request.json
    message = data.get('message', '').lower()
    
    responses = {
        'hello': 'Hello! How can I help you with water quality monitoring today?',
        'hi': 'Hi there! I can help you with water analysis, disease information, or system features.',
        'help': 'I can assist with: water analysis, disease predictions, risk mapping, alerts, and NGO coordination. What would you like to know?',
        'water': 'To analyze water, upload a sample image in the Water Analysis tab. Our AI will detect contamination instantly.',
        'disease': 'We predict 6 water-borne diseases: Cholera, Typhoid, Diarrhea, Dysentery, Hepatitis A, and Gastroenteritis.',
        'alert': 'Alerts are automatically sent to NGOs and health departments when contamination is detected.',
        'map': 'The Risk Map shows contamination hotspots across Northeast India with color-coded risk zones.',
        'how': 'Upload a water sample image → AI analyzes it → Get results with disease predictions → Alerts sent if needed.',
        'contact': 'You can reach us at support@aquaguard.org or call +91-9876543210.',
    }
    
    for key in responses:
        if key in message:
            return jsonify({'response': responses[key]})
    
    return jsonify({'response': 'I can help with water analysis, diseases, alerts, and more. Try asking about "water", "disease", or "help"!'})

if __name__ == '__main__':
    os.makedirs('static', exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)
