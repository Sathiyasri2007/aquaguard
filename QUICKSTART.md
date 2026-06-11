# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Test the System
```bash
python test_system.py
```

This will:
- Initialize all components
- Create a test water sample
- Analyze contamination
- Predict diseases
- Generate risk map
- Send test alerts

### Step 3: Start the Backend
```bash
python backend/app.py
```

Server will start at: http://localhost:5000

### Step 4: Open the Dashboard
Open `frontend/index.html` in your browser

OR serve it with:
```bash
cd frontend
python -m http.server 8000
```
Then visit: http://localhost:8000

## 📋 Quick Test Workflow

1. **Upload Image**: Click upload area and select a water image
2. **Enter Location**: Type location name (e.g., "Guwahati Well")
3. **Add Coordinates**: Enter latitude and longitude
4. **Analyze**: Click "Analyze Water Sample"
5. **View Results**: See contamination level, diseases, and risk
6. **Check Map**: Go to "Risk Map" tab to see geographic visualization
7. **Monitor Alerts**: Check "Alert Dashboard" for notifications

## 🧪 Sample Test Data

### Test Locations (Northeast India)
- Guwahati: 26.1445, 91.7362
- Dibrugarh: 27.4728, 94.9120
- Jorhat: 26.7509, 94.2037
- Tezpur: 26.6338, 92.8000
- Silchar: 24.8333, 92.7789

### Register Test NGO
1. Go to "NGO Management" tab
2. Fill in:
   - Name: Test Health NGO
   - Email: test@ngo.org
   - Phone: +91-9876543210
   - Region: Guwahati
3. Click "Register NGO"
4. Note the NGO ID returned

## 🔍 What to Expect

### Water Analysis Output
- Classification (Safe/Possibly Contaminated/Contaminated)
- Confidence percentage
- Visual indicators (turbidity, color, waste, oil, algae)
- Water quality status
- Risk level

### Disease Predictions
- List of potential diseases
- Risk scores
- Symptoms
- Prevention measures
- Severity levels

### Risk Map
- Interactive map with colored markers
- 🔴 High Risk locations
- 🟡 Medium Risk locations
- 🟢 Low Risk locations
- Click markers for details

### Alerts
- Automatic alert generation for contaminated water
- Email and SMS notifications (simulated in console)
- Alert tracking and history
- Response monitoring

## 📊 Dashboard Features

### Tab 1: Water Analysis
- Upload and analyze water samples
- View detailed results
- See disease predictions

### Tab 2: Risk Map
- Geographic visualization
- Risk patterns
- High-risk location identification

### Tab 3: Alert Dashboard
- Alert statistics
- Response rates
- Alert history
- Pending alerts

### Tab 4: NGO Management
- Register NGOs
- Record responses
- Track actions

## 🛠️ Troubleshooting

### Issue: Module not found
```bash
pip install -r requirements.txt
```

### Issue: Port already in use
Change port in backend/app.py:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Issue: Image upload fails
- Check file size (< 10MB)
- Use JPG or PNG format
- Ensure uploads/ folder exists

### Issue: Map not loading
- Check if backend is running
- Refresh the map
- Check browser console for errors

## 📝 API Testing with cURL

### Analyze Water (with image)
```bash
curl -X POST http://localhost:5000/api/analyze \
  -F "image=@path/to/water_image.jpg" \
  -F "location=Test Location" \
  -F "latitude=26.2006" \
  -F "longitude=92.9376"
```

### Get Risk Patterns
```bash
curl http://localhost:5000/api/patterns
```

### Get Alert Statistics
```bash
curl http://localhost:5000/api/alerts/statistics
```

### Register NGO
```bash
curl -X POST http://localhost:5000/api/ngo/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Test NGO","email":"test@ngo.org","phone":"+919876543210","region":"Guwahati"}'
```

## 🎯 Next Steps

1. **Collect Real Data**: Gather actual water sample images
2. **Train Model**: Use real data to train the CNN model
3. **Configure Alerts**: Set up real email/SMS credentials
4. **Deploy**: Host on cloud platform (AWS, Azure, GCP)
5. **Mobile App**: Develop mobile version for field workers
6. **Integration**: Connect with government health systems

## 💡 Tips

- Use clear, well-lit water sample photos
- Include GPS coordinates for accurate mapping
- Register multiple NGOs for better coverage
- Monitor response times regularly
- Update risk patterns weekly
- Back up historical data

## 📞 Support

For issues or questions:
- Check README.md for detailed documentation
- Review code comments
- Test with sample data first
- Verify all dependencies are installed

---

**Ready to make a difference in community health! 🌊💙**
