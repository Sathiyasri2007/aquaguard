class DiseasePredictionEngine:
    def __init__(self):
        self.disease_db = {
            'Cholera': {
                'risk_factors': ['high_turbidity', 'floating_waste', 'color_abnormal'],
                'symptoms': ['Severe diarrhea', 'Vomiting', 'Dehydration', 'Muscle cramps'],
                'prevention': ['Boil water before drinking', 'Use water purification tablets', 'Maintain hygiene'],
                'severity': 'Critical'
            },
            'Typhoid': {
                'risk_factors': ['contaminated', 'floating_waste'],
                'symptoms': ['High fever', 'Headache', 'Stomach pain', 'Weakness'],
                'prevention': ['Drink only boiled/filtered water', 'Wash hands frequently', 'Avoid raw food'],
                'severity': 'High'
            },
            'Diarrhea': {
                'risk_factors': ['possibly_contaminated', 'turbidity'],
                'symptoms': ['Loose stools', 'Stomach cramps', 'Nausea', 'Dehydration'],
                'prevention': ['Use clean water', 'Maintain food hygiene', 'ORS solution'],
                'severity': 'Medium'
            },
            'Dysentery': {
                'risk_factors': ['contaminated', 'algae', 'floating_waste'],
                'symptoms': ['Bloody diarrhea', 'Fever', 'Abdominal pain', 'Cramping'],
                'prevention': ['Boil drinking water', 'Proper sanitation', 'Hand washing'],
                'severity': 'High'
            },
            'Hepatitis A': {
                'risk_factors': ['contaminated', 'floating_waste', 'oil_layer'],
                'symptoms': ['Jaundice', 'Fatigue', 'Nausea', 'Abdominal pain', 'Dark urine'],
                'prevention': ['Vaccination', 'Boil water', 'Avoid contaminated food/water'],
                'severity': 'High'
            },
            'Gastroenteritis': {
                'risk_factors': ['possibly_contaminated', 'turbidity', 'color_abnormal'],
                'symptoms': ['Diarrhea', 'Vomiting', 'Stomach pain', 'Fever'],
                'prevention': ['Clean water consumption', 'Hand hygiene', 'Food safety'],
                'severity': 'Medium'
            }
        }
    
    def predict_diseases(self, contamination_result):
        classification = contamination_result['classification'].lower()
        
        # If water is classified as clean, return no diseases
        if 'clean' in classification or 'safe' in classification:
            return []
        
        indicators = contamination_result['indicators']
        
        risk_factors = [classification.replace('-', '_')]
        if indicators['turbidity'] == 'High':
            risk_factors.append('high_turbidity')
        if indicators['floating_waste'] == 'Detected':
            risk_factors.append('floating_waste')
        if indicators['color_change'] == 'Abnormal':
            risk_factors.append('color_abnormal')
        if indicators['algae'] == 'Detected':
            risk_factors.append('algae')
        if indicators['oil_layer'] == 'Detected':
            risk_factors.append('oil_layer')
        
        predicted_diseases = []
        for disease, info in self.disease_db.items():
            match_count = sum(1 for rf in info['risk_factors'] if rf in risk_factors)
            if match_count > 0:
                predicted_diseases.append({
                    'disease': disease,
                    'risk_score': match_count / len(info['risk_factors']),
                    'symptoms': info['symptoms'],
                    'prevention': info['prevention'],
                    'severity': info['severity']
                })
        
        predicted_diseases.sort(key=lambda x: x['risk_score'], reverse=True)
        return predicted_diseases
    
    def get_water_quality_status(self, contamination_result):
        classification = contamination_result['classification'].lower()
        confidence = contamination_result['confidence']
        
        if 'clean' in classification or 'safe' in classification:
            return 'Pure'
        elif 'dirty' in classification or 'contaminated' in classification:
            return 'Highly Contaminated'
        else:
            return 'Moderately Unsafe'
