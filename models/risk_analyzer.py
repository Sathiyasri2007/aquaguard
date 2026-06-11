import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from datetime import datetime, timedelta

class RiskAnalysisEngine:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.historical_data = []
        
    def add_analysis_record(self, location, lat, lon, contamination_level, diseases):
        record = {
            'timestamp': datetime.now(),
            'location': location,
            'latitude': lat,
            'longitude': lon,
            'contamination_level': contamination_level,
            'disease_count': len(diseases),
            'high_severity_count': sum(1 for d in diseases if d['severity'] in ['High', 'Critical'])
        }
        self.historical_data.append(record)
    
    def analyze_patterns(self):
        if len(self.historical_data) < 5:
            return {'status': 'Insufficient data', 'patterns': []}
        
        df = pd.DataFrame(self.historical_data)
        
        location_risk = df.groupby('location').agg({
            'contamination_level': lambda x: (x == 'Highly Contaminated').sum(),
            'disease_count': 'mean',
            'high_severity_count': 'sum'
        }).reset_index()
        
        location_risk['risk_score'] = (
            location_risk['contamination_level'] * 0.4 +
            location_risk['disease_count'] * 0.3 +
            location_risk['high_severity_count'] * 0.3
        )
        
        patterns = []
        for _, row in location_risk.iterrows():
            patterns.append({
                'location': row['location'],
                'risk_score': float(row['risk_score']),
                'contamination_incidents': int(row['contamination_level']),
                'avg_diseases': float(row['disease_count'])
            })
        
        return {'status': 'Success', 'patterns': sorted(patterns, key=lambda x: x['risk_score'], reverse=True)}
    
    def identify_high_risk_locations(self, threshold=2.0):
        patterns = self.analyze_patterns()
        if patterns['status'] != 'Success':
            return []
        
        return [p for p in patterns['patterns'] if p['risk_score'] >= threshold]
    
    def get_location_risk_level(self, location):
        recent_data = [r for r in self.historical_data if r['location'] == location]
        
        if not recent_data:
            return 'Low Risk'
        
        recent_30_days = [r for r in recent_data if (datetime.now() - r['timestamp']).days <= 30]
        
        if not recent_30_days:
            return 'Low Risk'
        
        contaminated_count = sum(1 for r in recent_30_days if r['contamination_level'] == 'Highly Contaminated')
        avg_diseases = np.mean([r['disease_count'] for r in recent_30_days])
        
        if contaminated_count >= 3 or avg_diseases >= 4:
            return 'High Risk'
        elif contaminated_count >= 1 or avg_diseases >= 2:
            return 'Medium Risk'
        else:
            return 'Low Risk'
