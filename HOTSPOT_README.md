# Water Contamination Hotspot Analysis

## Overview
The hotspot analysis system processes historical water quality data to identify and classify contamination risk zones across India. It uses the provided `hotspot.csv` dataset to create interactive risk maps with high, medium, and low risk classifications.

## Features

### 🎯 Risk Classification
- **High Risk**: Locations with severe water quality issues (Risk Score ≥ 8)
- **Medium Risk**: Locations with moderate contamination (Risk Score 4-7)  
- **Low Risk**: Locations with acceptable water quality (Risk Score < 4)

### 📊 Risk Scoring Parameters
The system evaluates multiple water quality parameters:
- **pH levels** (ideal range: 6.5-8.5)
- **BOD (Biochemical Oxygen Demand)** (lower is better)
- **Fecal Coliform** (bacterial contamination indicator)
- **Total Coliform** (general bacterial contamination)
- **Conductivity** (dissolved solids indicator)

### 🗺️ Interactive Mapping
- Color-coded markers (🔴 High, 🟡 Medium, 🟢 Low)
- Detailed popups with water quality parameters
- Filtering by risk levels
- Geographic distribution across Indian states

## Files Structure

```
data/
├── hotspot_locations.py    # Main hotspot analyzer
└── hotspot.csv            # Water quality dataset

utils/
└── geo_mapper.py          # Enhanced with hotspot integration

backend/
└── app.py                 # API endpoints for hotspot data

frontend/
└── index.html             # UI with hotspot filtering

static/
├── hotspot_risk_map.html  # Generated risk map
└── high_risk_only_map.html # Filtered high-risk map
```

## API Endpoints

### GET /api/risk-map
Returns interactive map with all hotspot locations

### GET /api/hotspot-summary  
Returns risk distribution statistics:
```json
{
  "high_risk": 157,
  "medium_risk": 698, 
  "low_risk": 1136,
  "total_locations": 1991
}
```

### GET /api/hotspot-locations/{risk_level}
Returns locations filtered by risk level (High Risk, Medium Risk, Low Risk)

### GET /api/filtered-risk-map?risk_levels=High Risk
Returns map filtered by specified risk levels

## Usage

### 1. Run Hotspot Analysis
```bash
python test_hotspot.py
```

### 2. Start Backend Server
```bash
python backend/app.py
```

### 3. Open Frontend
Navigate to `frontend/index.html` and click "Risk Map" tab

### 4. Use Filtering
- Select risk levels from dropdown
- View summary statistics
- Click markers for detailed information

## Data Processing

The system automatically:
1. Loads water quality data from CSV
2. Handles encoding issues (tries multiple encodings)
3. Calculates risk scores based on parameter thresholds
4. Assigns geographic coordinates to Indian states/regions
5. Generates interactive maps with Folium

## Risk Score Calculation

Each parameter contributes to the total risk score (0-12):

- **pH**: +3 (very acidic/basic), +2 (moderately off), +0 (normal)
- **BOD**: +3 (>10 mg/l), +2 (5-10 mg/l), +1 (3-5 mg/l)
- **Fecal Coliform**: +3 (>1000), +2 (100-1000), +1 (10-100)
- **Total Coliform**: +3 (>5000), +2 (1000-5000), +1 (100-1000)  
- **Conductivity**: +3 (>10000), +2 (5000-10000), +1 (2000-5000)

## Current Dataset Statistics
- **Total Locations**: 1,991 water monitoring stations
- **High Risk**: 157 locations (7.9%)
- **Medium Risk**: 698 locations (35.1%) 
- **Low Risk**: 1,136 locations (57.0%)
- **Coverage**: Multiple Indian states from 2003-2014

## Integration with Main System

The hotspot data integrates seamlessly with:
- Real-time water analysis
- Disease prediction engine
- Alert system for high-risk areas
- NGO response coordination

This provides a comprehensive view combining historical contamination patterns with current analysis results.