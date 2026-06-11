import pandas as pd
import numpy as np
import os

class HotspotAnalyzer:
    def __init__(self, csv_path=None):
        if csv_path is None:
            # Use relative path from current file location
            current_dir = os.path.dirname(os.path.abspath(__file__))
            csv_path = os.path.join(os.path.dirname(current_dir), 'hotspot.csv')
        self.csv_path = csv_path
        self.hotspot_data = self.load_and_process_data()
        self.risk_locations = self.classify_risk_zones()
    
    def load_and_process_data(self):
        """Load and clean the hotspot CSV data"""
        try:
            # Try different encodings
            encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
            df = None
            
            for encoding in encodings:
                try:
                    df = pd.read_csv(self.csv_path, encoding=encoding)
                    print(f"Successfully loaded data with {encoding} encoding")
                    break
                except UnicodeDecodeError:
                    continue
            
            if df is None:
                print("Could not load CSV with any encoding, creating sample data")
                return self.create_sample_data()
            
            # Clean column names
            df.columns = df.columns.str.strip()
            
            # Convert numeric columns
            numeric_cols = ['Temp', 'D.O. (mg/l)', 'PH', 'CONDUCTIVITY (mhos/cm)', 
                          'B.O.D. (mg/l)', 'NITRATENAN N+ NITRITENANN (mg/l)', 
                          'FECAL COLIFORM (MPN/100ml)', 'TOTAL COLIFORM (MPN/100ml)Mean']
            
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Remove rows with all NaN values
            df = df.dropna(how='all')
            
            return df
        except Exception as e:
            print(f"Error loading data: {e}")
            return self.create_sample_data()
    
    def create_sample_data(self):
        """Create sample data if CSV loading fails"""
        sample_data = {
            'STATION CODE': [1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009, 1010],
            'LOCATIONS': [
                'Guwahati Water Source',
                'Shillong Lake', 
                'Imphal River',
                'Aizawl Stream',
                'Agartala Pond',
                'Dibrugarh Well',
                'Jorhat Canal',
                'Silchar River',
                'Kohima Spring',
                'Itanagar Creek'
            ],
            'STATE': [
                'ASSAM', 'MEGHALAYA', 'MANIPUR', 'MIZORAM', 'TRIPURA',
                'ASSAM', 'ASSAM', 'ASSAM', 'NAGALAND', 'ARUNACHAL PRADESH'
            ],
            'PH': [7.2, 6.8, 7.5, 6.9, 7.1, 7.3, 6.7, 7.0, 6.8, 7.2],
            'B.O.D. (mg/l)': [4.2, 2.1, 8.5, 3.2, 5.1, 12.3, 6.8, 15.2, 3.5, 7.8],
            'FECAL COLIFORM (MPN/100ml)': [890, 450, 2500, 680, 1200, 5500, 1800, 8200, 520, 3100],
            'TOTAL COLIFORM (MPN/100ml)Mean': [1500, 800, 4500, 1100, 2200, 9500, 3200, 14000, 950, 5500],
            'CONDUCTIVITY (mhos/cm)': [350, 280, 820, 310, 450, 1500, 680, 2200, 290, 950],
            'year': [2024] * 10
        }
        return pd.DataFrame(sample_data)
    
    def classify_risk_zones(self):
        """Classify locations into High, Medium, Low risk based on water quality parameters"""
        if self.hotspot_data.empty:
            return []
        
        risk_locations = []
        
        for _, row in self.hotspot_data.iterrows():
            location = row.get('LOCATIONS', 'Unknown Location')
            state = row.get('STATE', 'Unknown State')
            
            # Risk scoring based on multiple parameters
            risk_score = 0
            
            # pH risk (ideal range 6.5-8.5)
            ph = row.get('PH', 7)
            if not pd.isna(ph):
                if ph < 6 or ph > 9:
                    risk_score += 3
                elif ph < 6.5 or ph > 8.5:
                    risk_score += 2
                else:
                    risk_score += 0
            
            # BOD risk (higher BOD = more pollution)
            bod = row.get('B.O.D. (mg/l)', 0)
            if not pd.isna(bod):
                if bod > 10:
                    risk_score += 3
                elif bod > 5:
                    risk_score += 2
                elif bod > 3:
                    risk_score += 1
            
            # Fecal Coliform risk
            fecal = row.get('FECAL COLIFORM (MPN/100ml)', 0)
            if not pd.isna(fecal):
                if fecal > 1000:
                    risk_score += 3
                elif fecal > 100:
                    risk_score += 2
                elif fecal > 10:
                    risk_score += 1
            
            # Total Coliform risk
            total_col = row.get('TOTAL COLIFORM (MPN/100ml)Mean', 0)
            if not pd.isna(total_col):
                if total_col > 5000:
                    risk_score += 3
                elif total_col > 1000:
                    risk_score += 2
                elif total_col > 100:
                    risk_score += 1
            
            # Conductivity risk (very high conductivity indicates pollution)
            conductivity = row.get('CONDUCTIVITY (mhos/cm)', 0)
            if not pd.isna(conductivity):
                if conductivity > 10000:
                    risk_score += 3
                elif conductivity > 5000:
                    risk_score += 2
                elif conductivity > 2000:
                    risk_score += 1
            
            # Classify risk level
            if risk_score >= 8:
                risk_level = 'High Risk'
            elif risk_score >= 4:
                risk_level = 'Medium Risk'
            else:
                risk_level = 'Low Risk'
            
            # Generate approximate coordinates for Indian states/regions
            lat, lon = self.get_approximate_coordinates(state, location)
            
            risk_locations.append({
                'location': location,
                'state': state,
                'latitude': lat,
                'longitude': lon,
                'risk_level': risk_level,
                'risk_score': risk_score,
                'ph': ph,
                'bod': bod,
                'fecal_coliform': fecal,
                'total_coliform': total_col,
                'conductivity': conductivity,
                'year': row.get('year', 2014)
            })
        
        return risk_locations
    
    def get_approximate_coordinates(self, state, location):
        """Get approximate coordinates for Indian states and regions"""
        # Approximate coordinates for Indian states (center points)
        state_coords = {
            'ASSAM': (26.2006, 92.9376),
            'MEGHALAYA': (25.4670, 91.3662),
            'MANIPUR': (24.6637, 93.9063),
            'MIZORAM': (23.1645, 92.9376),
            'TRIPURA': (23.9408, 91.9882),
            'NAGALAND': (26.1584, 94.5624),
            'ARUNACHAL PRADESH': (28.2180, 94.7278),
            'GOA': (15.2993, 74.1240),
            'GUJARAT': (23.0225, 72.5714),
            'MAHARASHTRA': (19.7515, 75.7139),
            'KERALA': (10.8505, 76.2711),
            'KARNATAKA': (15.3173, 75.7139),
            'ANDHRA PRADESH': (15.9129, 79.7400),
            'ORISSA': (20.9517, 85.0985),
            'ODISHA': (20.9517, 85.0985),
            'PONDICHERRY': (11.9416, 79.8083),
            'TAMIL NADU': (11.1271, 78.6569),
            'TAMILNADU': (11.1271, 78.6569),
            'PUNJAB': (31.1471, 75.3412),
            'HARYANA': (29.0588, 76.0856),
            'HIMACHAL PRADESH': (31.1048, 77.1734),
            'RAJASTHAN': (27.0238, 74.2179),
            'MADHYA PRADESH': (22.9734, 78.6569),
            'DAMAN & DIU': (20.4283, 72.8397),
            'DADRA AND NAGAR HAVELI': (20.1809, 73.0169),
            'CHANDIGARH': (30.7333, 76.7794),
            'DELHI': (28.7041, 77.1025),
            'UTTAR PRADESH': (26.8467, 80.9462),
            'WEST BENGAL': (22.9868, 87.8550)
        }
        
        base_lat, base_lon = state_coords.get(state.upper(), (26.2006, 92.9376))  # Default to Guwahati
        
        # Add small random offset for different locations within same state
        lat_offset = np.random.uniform(-0.5, 0.5)
        lon_offset = np.random.uniform(-0.5, 0.5)
        
        return base_lat + lat_offset, base_lon + lon_offset
    
    def get_high_risk_locations(self):
        """Get only high risk locations"""
        return [loc for loc in self.risk_locations if loc['risk_level'] == 'High Risk']
    
    def get_medium_risk_locations(self):
        """Get only medium risk locations"""
        return [loc for loc in self.risk_locations if loc['risk_level'] == 'Medium Risk']
    
    def get_low_risk_locations(self):
        """Get only low risk locations"""
        return [loc for loc in self.risk_locations if loc['risk_level'] == 'Low Risk']
    
    def get_risk_summary(self):
        """Get summary of risk distribution"""
        high_count = len(self.get_high_risk_locations())
        medium_count = len(self.get_medium_risk_locations())
        low_count = len(self.get_low_risk_locations())
        
        return {
            'high_risk': high_count,
            'medium_risk': medium_count,
            'low_risk': low_count,
            'total_locations': len(self.risk_locations)
        }

if __name__ == "__main__":
    # Test the hotspot analyzer
    analyzer = HotspotAnalyzer()
    summary = analyzer.get_risk_summary()
    print(f"Risk Summary: {summary}")
    
    # Print sample high risk locations
    high_risk = analyzer.get_high_risk_locations()[:5]
    print(f"\nSample High Risk Locations:")
    for loc in high_risk:
        print(f"- {loc['location']}, {loc['state']} (Score: {loc['risk_score']})")