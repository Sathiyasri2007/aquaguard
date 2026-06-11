import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.water_model import WaterContaminationModel
from models.disease_predictor import DiseasePredictionEngine
from models.risk_analyzer import RiskAnalysisEngine
from utils.geo_mapper import GeographicMapper
from utils.alert_system import AlertSystem
import numpy as np
from PIL import Image

def create_test_image():
    """Create a test water sample image"""
    img = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
    img[:, :, 2] = img[:, :, 2] * 0.5  # Reduce blue channel to simulate contamination
    img[:, :, 1] = img[:, :, 1] * 1.2  # Increase green for algae
    
    os.makedirs('test_images', exist_ok=True)
    Image.fromarray(img).save('test_images/sample_water.jpg')
    return 'test_images/sample_water.jpg'

def test_system():
    print("=" * 60)
    print("SMART COMMUNITY HEALTH MONITORING SYSTEM - TEST")
    print("=" * 60)
    
    # Initialize components
    print("\n1. Initializing System Components...")
    water_model = WaterContaminationModel()
    disease_engine = DiseasePredictionEngine()
    risk_analyzer = RiskAnalysisEngine()
    geo_mapper = GeographicMapper()
    alert_system = AlertSystem()
    print("✓ All components initialized")
    
    # Register NGOs
    print("\n2. Registering NGOs...")
    ngo1 = alert_system.register_ngo("Health First NGO", "health@ngo.org", "+91-9876543210", "Guwahati")
    ngo2 = alert_system.register_ngo("Clean Water Initiative", "water@ngo.org", "+91-9876543211", "Dibrugarh")
    print(f"✓ Registered {len(alert_system.ngo_contacts)} NGOs")
    
    # Create test image
    print("\n3. Creating Test Water Sample Image...")
    test_image = create_test_image()
    print(f"✓ Test image created: {test_image}")
    
    # Analyze water sample
    print("\n4. Analyzing Water Sample...")
    contamination_result = water_model.predict(test_image)
    print(f"   Classification: {contamination_result['classification']}")
    print(f"   Confidence: {contamination_result['confidence']:.2%}")
    print(f"   Visual Indicators:")
    for indicator, value in contamination_result['indicators'].items():
        print(f"     - {indicator.replace('_', ' ').title()}: {value}")
    
    # Predict diseases
    print("\n5. Predicting Diseases...")
    diseases = disease_engine.predict_diseases(contamination_result)
    water_quality = disease_engine.get_water_quality_status(contamination_result)
    print(f"   Water Quality Status: {water_quality}")
    print(f"   Diseases Predicted: {len(diseases)}")
    for disease in diseases[:3]:
        print(f"\n   • {disease['disease']} (Risk: {disease['risk_score']:.1%})")
        print(f"     Severity: {disease['severity']}")
        print(f"     Symptoms: {', '.join(disease['symptoms'][:3])}")
    
    # Add to risk analysis
    print("\n6. Adding to Risk Analysis Database...")
    locations = [
        ("Guwahati Village Well", 26.1445, 91.7362),
        ("Dibrugarh River Point", 27.4728, 94.9120),
        ("Jorhat Pond", 26.7509, 94.2037)
    ]
    
    for location, lat, lon in locations:
        risk_analyzer.add_analysis_record(location, lat, lon, water_quality, diseases)
    print(f"✓ Added {len(locations)} location records")
    
    # Analyze patterns
    print("\n7. Analyzing Contamination Patterns...")
    patterns = risk_analyzer.analyze_patterns()
    if patterns['status'] == 'Success':
        print(f"   Found {len(patterns['patterns'])} location patterns")
        for pattern in patterns['patterns'][:3]:
            print(f"   • {pattern['location']}: Risk Score {pattern['risk_score']:.2f}")
    
    # Create risk map
    print("\n8. Generating Geographic Risk Map...")
    locations_data = []
    for location, lat, lon in locations:
        risk_level = risk_analyzer.get_location_risk_level(location)
        locations_data.append({
            'location': location,
            'latitude': lat,
            'longitude': lon,
            'risk_level': risk_level,
            'water_quality': water_quality,
            'disease_count': len(diseases),
            'timestamp': 'Just now'
        })
    
    risk_map = geo_mapper.create_risk_map(locations_data)
    map_file = geo_mapper.save_map(risk_map, 'test_risk_map.html')
    print(f"✓ Risk map saved: {map_file}")
    
    # Create and dispatch alert
    print("\n9. Creating and Dispatching Alerts...")
    if water_quality in ['Moderately Unsafe', 'Highly Contaminated']:
        alert = alert_system.create_alert(
            locations[0][0], 
            risk_analyzer.get_location_risk_level(locations[0][0]),
            water_quality, 
            diseases, 
            locations[0][1], 
            locations[0][2]
        )
        print(f"   Alert ID: {alert['alert_id']}")
        print(f"   Location: {alert['location']}")
        print(f"   Risk Level: {alert['risk_level']}")
        
        dispatched = alert_system.dispatch_alerts(alert)
        print(f"✓ Alert dispatched to {len(dispatched)} NGOs")
    
    # Check alert statistics
    print("\n10. Alert System Statistics...")
    stats = alert_system.get_response_statistics()
    print(f"   Total Alerts: {stats['total_alerts']}")
    print(f"   Responded: {stats['responded']}")
    print(f"   Pending: {stats['pending']}")
    print(f"   Response Rate: {stats['response_rate']:.1f}%")
    
    # Simulate NGO response
    print("\n11. Simulating NGO Response...")
    if alert_system.alert_history:
        response = alert_system.record_response(
            alert_system.alert_history[0]['alert_id'],
            ngo1,
            "Water purification tablets distributed. Community warned. Medical team dispatched."
        )
        print(f"✓ Response recorded from NGO {ngo1}")
        print(f"   Response Time: {response['time_taken_hours']:.2f} hours")
    
    print("\n" + "=" * 60)
    print("SYSTEM TEST COMPLETED SUCCESSFULLY")
    print("=" * 60)
    print("\nNext Steps:")
    print("1. Start the backend server: python backend/app.py")
    print("2. Open frontend/index.html in your browser")
    print("3. Upload water sample images for analysis")
    print("4. View the risk map: test_risk_map.html")
    print("\n")

if __name__ == '__main__':
    test_system()
