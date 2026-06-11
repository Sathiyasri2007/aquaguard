import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_sample_dataset():
    locations = [
        ('Guwahati Village Well', 26.1445, 91.7362),
        ('Dibrugarh River Point', 27.4728, 94.9120),
        ('Jorhat Pond', 26.7509, 94.2037),
        ('Tezpur Community Tank', 26.6338, 92.8000),
        ('Silchar Water Source', 24.8333, 92.7789),
        ('Imphal Lake', 24.8170, 93.9368),
        ('Shillong Spring', 25.5788, 91.8933),
        ('Kohima Village Well', 25.6747, 94.1086)
    ]
    
    contamination_levels = ['Pure', 'Moderately Unsafe', 'Highly Contaminated']
    diseases = ['Cholera', 'Typhoid', 'Diarrhea', 'Dysentery', 'Hepatitis A', 'Gastroenteritis']
    
    data = []
    start_date = datetime.now() - timedelta(days=90)
    
    for i in range(200):
        location, lat, lon = locations[np.random.randint(0, len(locations))]
        date = start_date + timedelta(days=np.random.randint(0, 90))
        
        contamination = np.random.choice(contamination_levels, p=[0.4, 0.35, 0.25])
        
        if contamination == 'Highly Contaminated':
            disease_count = np.random.randint(2, 5)
        elif contamination == 'Moderately Unsafe':
            disease_count = np.random.randint(1, 3)
        else:
            disease_count = 0
        
        detected_diseases = np.random.choice(diseases, size=min(disease_count, len(diseases)), replace=False).tolist() if disease_count > 0 else []
        
        data.append({
            'date': date.strftime('%Y-%m-%d'),
            'location': location,
            'latitude': lat,
            'longitude': lon,
            'contamination_level': contamination,
            'turbidity': np.random.choice(['Low', 'High'], p=[0.6, 0.4]),
            'color': np.random.choice(['Normal', 'Abnormal'], p=[0.7, 0.3]),
            'floating_waste': np.random.choice(['None', 'Detected'], p=[0.75, 0.25]),
            'oil_layer': np.random.choice(['None', 'Detected'], p=[0.85, 0.15]),
            'algae': np.random.choice(['None', 'Detected'], p=[0.8, 0.2]),
            'diseases_detected': ', '.join(detected_diseases),
            'disease_count': disease_count
        })
    
    df = pd.DataFrame(data)
    df.to_csv('data/water_quality_dataset.csv', index=False)
    print(f"Generated {len(data)} sample records")
    return df

if __name__ == '__main__':
    generate_sample_dataset()
