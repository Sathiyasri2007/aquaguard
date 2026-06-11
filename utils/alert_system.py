from datetime import datetime

class AlertSystem:
    def __init__(self):
        self.ngo_contacts = []
        self.alert_history = []

    def register_ngo(self, name, email, phone, region):
        ngo_id = len(self.ngo_contacts) + 1
        self.ngo_contacts.append({
            'ngo_id': ngo_id, 'name': name,
            'email': email, 'phone': phone, 'region': region
        })
        return ngo_id

    def create_alert(self, location, risk_level, water_quality, diseases, latitude, longitude):
        alert = {
            'alert_id': f'ALT-{len(self.alert_history)+1}-{int(datetime.now().timestamp())}',
            'location': location,
            'risk_level': risk_level,
            'water_quality': water_quality,
            'diseases': [d['disease'] for d in diseases] if diseases else [],
            'latitude': latitude,
            'longitude': longitude,
            'timestamp': datetime.now(),
            'status': 'Pending',
            'responses': []
        }
        self.alert_history.append(alert)
        return alert

    def dispatch_alerts(self, alert):
        print(f"Alert dispatched: {alert['alert_id']} for {alert['location']}")

    def record_response(self, alert_id, ngo_id, action_taken):
        response = {
            'ngo_id': ngo_id,
            'action_taken': action_taken,
            'timestamp': datetime.now()
        }
        for alert in self.alert_history:
            if alert['alert_id'] == alert_id:
                alert['responses'].append(response)
                alert['status'] = 'Responded'
        return response

    def check_pending_alerts(self):
        return [a for a in self.alert_history if a['status'] == 'Pending']

    def get_response_statistics(self):
        total = len(self.alert_history)
        responded = sum(1 for a in self.alert_history if a['status'] == 'Responded')
        pending = sum(1 for a in self.alert_history if a['status'] == 'Pending')
        return {'total': total, 'responded': responded, 'pending': pending}
