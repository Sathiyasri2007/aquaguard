# Smart Community Health Monitoring and Early Warning System

## Overview
AI-powered system for detecting water contamination and providing early health warnings for water-borne diseases in Rural Northeast India.

## Features

### ✅ Implemented Features

1. **Water Image Analysis**
   - AI/Computer Vision-based water sample analysis
   - Classification: Contaminated / Possibly Contaminated / Safe
   - Visual indicator detection:
     - Color changes
     - Turbidity levels
     - Floating waste
     - Oil layers
     - Algae growth

2. **Disease Prediction**
   - Predicts 6 water-borne diseases:
     - Cholera
     - Typhoid
     - Diarrhea
     - Dysentery
     - Hepatitis A
     - Gastroenteritis
   - Provides symptoms, prevention measures, and health advice

3. **Water Quality Status**
   - Categories: Pure / Moderately Unsafe / Highly Contaminated
   - Confidence scoring

4. **Dataset-Based Risk Analysis**
   - Historical pattern analysis
   - High-risk location identification
   - Contamination trend tracking

5. **Geographic Risk Mapping**
   - Interactive map with color-coded risk zones:
     - 🔴 High Risk
     - 🟡 Medium Risk
     - 🟢 Low Risk
   - Auto-updates based on analysis results

6. **Alert System**
   - Automatic alerts to NGOs and health departments
   - Multi-channel notifications (Email, SMS simulation)
   - Alert tracking and management

7. **NGO Response Monitoring**
   - Response time tracking
   - Action status monitoring
   - Alert escalation for non-response
   - Response statistics dashboard

## Technology Stack

### AI/ML Models
- **CNN (Convolutional Neural Network)** - Water contamination classification
- **Random Forest** - Risk pattern analysis
- **Computer Vision** - OpenCV for visual indicator detection

### Backend
- **Flask** - REST API server
- **TensorFlow/Keras** - Deep learning framework
- **scikit-learn** - Machine learning utilities
- **Pandas** - Data analysis

### Frontend
- **HTML5/CSS3/JavaScript** - Web interface
- **Folium** - Interactive map visualization
- **Responsive Design** - Mobile-friendly interface

### Computer Vision Techniques
- **HSV Color Space Analysis** - Color anomaly detection
- **Edge Detection (Canny)** - Floating object detection
- **Laplacian Variance** - Turbidity measurement
- **Color Masking** - Oil layer and algae detection

### Alert System Architecture
- **Multi-channel Notifications** - Email + SMS
- **Queue-based Dispatch** - Asynchronous alert delivery
- **Response Tracking** - Time-stamped action logging
- **Escalation Engine** - Auto-escalation for delayed responses

## Installation

### Prerequisites
- Python 3.8+
- pip package manager

### Setup Steps

1. **Clone/Navigate to Project Directory**
```bash
cd c:\Users\suvet\OneDrive\Documents\DT
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Generate Sample Dataset**
```bash
python data/generate_dataset.py
```

4. **Start Backend Server**
```bash
python backend/app.py
```

5. **Open Frontend**
Open `frontend/index.html` in your web browser or serve it:
```bash
cd frontend
python -m http.server 8000
```
Then visit: http://localhost:8000

## Usage Guide

### 1. Water Analysis
- Upload water sample image
- Enter location and coordinates
- Click "Analyze Water Sample"
- View contamination results and disease predictions

### 2. Risk Map
- Navigate to "Risk Map" tab
- View geographic distribution of risk zones
- Click markers for detailed information
- Refresh to see latest data

### 3. Alert Dashboard
- Monitor alert statistics
- View alert history
- Track response rates
- Identify pending/escalated alerts

### 4. NGO Management
- Register NGOs with contact details
- Record responses to alerts
- Track response times

## API Endpoints

### Analysis
- `POST /api/analyze` - Analyze water sample image
  - Form data: image, location, latitude, longitude
  - Returns: contamination results, diseases, risk level, alert info

### Risk Mapping
- `GET /api/risk-map` - Get interactive risk map HTML
- `GET /api/patterns` - Get contamination patterns and high-risk locations

### Alert Management
- `GET /api/alerts/history` - Get all alerts
- `GET /api/alerts/pending` - Get pending/overdue alerts
- `GET /api/alerts/statistics` - Get response statistics

### NGO Management
- `POST /api/ngo/register` - Register new NGO
  - JSON: {name, email, phone, region}
- `POST /api/ngo/respond` - Record NGO response
  - JSON: {alert_id, ngo_id, action_taken}

## Project Structure

```
DT/
├── backend/
│   └── app.py                 # Flask API server
├── models/
│   ├── water_model.py         # CNN water contamination model
│   ├── disease_predictor.py   # Disease prediction engine
│   └── risk_analyzer.py       # Risk analysis module
├── utils/
│   ├── geo_mapper.py          # Geographic mapping
│   └── alert_system.py        # Alert and notification system
├── data/
│   └── generate_dataset.py    # Sample data generator
├── frontend/
│   └── index.html             # Web dashboard
└── requirements.txt           # Python dependencies
```

## Datasets Recommended

### Water Quality Datasets
1. **India Water Quality Dataset** - Central Pollution Control Board (CPCB)
2. **WHO Water Quality Database**
3. **Kaggle Water Quality Dataset**
4. **Custom Northeast India Water Samples** (collect locally)

### Disease Datasets
1. **IDSP (Integrated Disease Surveillance Programme) India**
2. **WHO Disease Outbreak Database**
3. **State Health Department Records**

## Model Training (Future Enhancement)

To train the CNN model with real data:

```python
from models.water_model import WaterContaminationModel

model = WaterContaminationModel()

# Prepare your dataset
# X_train: images (224x224x3)
# y_train: labels (0=Safe, 1=Possibly Contaminated, 2=Contaminated)

model.model.fit(X_train, y_train, epochs=50, validation_split=0.2)
model.model.save('trained_water_model.h5')
```

## Configuration

### Email Alerts (Optional)
Edit `utils/alert_system.py` to configure SMTP:
```python
smtp_server = "smtp.gmail.com"
smtp_port = 587
sender_email = "your-email@gmail.com"
sender_password = "your-app-password"
```

### SMS Alerts (Optional)
Configure Twilio credentials in `utils/alert_system.py`:
```python
account_sid = "your_account_sid"
auth_token = "your_auth_token"
twilio_phone = "your_twilio_phone"
```

## Performance Optimization

- **Image Preprocessing**: Resize to 224x224 for faster inference
- **Batch Processing**: Analyze multiple samples simultaneously
- **Caching**: Store recent analysis results
- **Database**: Use PostgreSQL/MongoDB for production

## Security Considerations

- Implement authentication for API endpoints
- Use HTTPS in production
- Sanitize file uploads
- Rate limiting for API calls
- Secure NGO credentials

## Future Enhancements

1. Mobile app (Android/iOS)
2. Real-time water sensor integration
3. Machine learning model retraining pipeline
4. Multi-language support
5. WhatsApp integration for alerts
6. Predictive analytics for outbreak forecasting
7. Integration with government health systems

## Contributing

This is a community health project. Contributions welcome:
- Improve ML models
- Add more disease databases
- Enhance UI/UX
- Add regional language support

## License

Open source for community health initiatives.

## Contact & Support

For issues, suggestions, or collaboration:
- Create GitHub issues
- Contact local health departments
- Reach out to NGO partners

## Acknowledgments

- Northeast India Health Departments
- Local NGOs and Community Health Workers
- Open source community

---

**Note**: This system is designed to assist health monitoring but should not replace professional medical diagnosis. Always consult healthcare professionals for medical decisions.
