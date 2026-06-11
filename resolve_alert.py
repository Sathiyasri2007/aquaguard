import requests
import json

def resolve_alert(alert_id, notes="Alert acknowledged and resolved"):
    """Resolve a specific alert"""
    url = "http://localhost:5000/api/alerts/resolve/" + alert_id
    
    data = {
        "notes": notes
    }
    
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Alert {alert_id} resolved successfully")
            print(f"Status: {result['alert']['status']}")
            print(f"Resolved at: {result['alert']['resolved_at']}")
        else:
            print(f"❌ Error resolving alert: {response.json()}")
    except requests.exceptions.ConnectionError:
        print("❌ Backend server not running. Start with: python backend/app.py")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == '__main__':
    # Resolve the specific alert
    resolve_alert("ALT20260305210746", "Water contamination issue addressed by health department")