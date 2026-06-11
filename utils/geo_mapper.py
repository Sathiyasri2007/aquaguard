import folium
import pandas as pd
import os

class HotspotAnalyzer:
    def __init__(self):
        self.risk_locations = []
        self._load_hotspot_data()

    def _load_hotspot_data(self):
        csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'hotspot.csv')
        if not os.path.exists(csv_path):
            return
        try:
            df = pd.read_csv(csv_path, encoding='latin-1')
            for _, row in df.iterrows():
                self.risk_locations.append({
                    'location': str(row.get('location', '')),
                    'state': str(row.get('state', '')),
                    'latitude': float(row.get('latitude', 0)),
                    'longitude': float(row.get('longitude', 0)),
                    'risk_level': str(row.get('risk_level', 'Low Risk')),
                    'risk_score': int(row.get('risk_score', 0)),
                    'ph': str(row.get('ph', 'N/A')),
                    'bod': str(row.get('bod', 'N/A')),
                    'fecal_coliform': str(row.get('fecal_coliform', 'N/A')),
                    'total_coliform': str(row.get('total_coliform', 'N/A')),
                    'year': str(row.get('year', 'N/A'))
                })
        except Exception as e:
            print(f"Error loading hotspot data: {e}")

    def get_risk_summary(self):
        summary = {'high_risk': 0, 'medium_risk': 0, 'low_risk': 0, 'total_locations': len(self.risk_locations)}
        for loc in self.risk_locations:
            rl = loc.get('risk_level', '')
            if rl == 'High Risk': summary['high_risk'] += 1
            elif rl == 'Medium Risk': summary['medium_risk'] += 1
            else: summary['low_risk'] += 1
        return summary


class GeographicMapper:
    def __init__(self):
        self.hotspot_analyzer = HotspotAnalyzer()
        self.color_map = {'High Risk': 'red', 'Medium Risk': 'orange', 'Low Risk': 'green'}

    def create_risk_map(self):
        m = folium.Map(location=[22.0, 82.0], zoom_start=5)
        for loc in self.hotspot_analyzer.risk_locations:
            color = self.color_map.get(loc['risk_level'], 'blue')
            folium.CircleMarker(
                location=[loc['latitude'], loc['longitude']],
                radius=6,
                color=color,
                fill=True,
                fill_color=color,
                popup=f"{loc['location']} - {loc['risk_level']}"
            ).add_to(m)
        return m

    def create_filtered_risk_map(self, risk_levels):
        m = folium.Map(location=[22.0, 82.0], zoom_start=5)
        for loc in self.hotspot_analyzer.risk_locations:
            if loc['risk_level'] in risk_levels:
                color = self.color_map.get(loc['risk_level'], 'blue')
                folium.CircleMarker(
                    location=[loc['latitude'], loc['longitude']],
                    radius=6,
                    color=color,
                    fill=True,
                    fill_color=color,
                    popup=f"{loc['location']} - {loc['risk_level']}"
                ).add_to(m)
        return m

    def get_hotspot_locations_by_risk(self, risk_level):
        return [loc for loc in self.hotspot_analyzer.risk_locations if loc['risk_level'] == risk_level]
