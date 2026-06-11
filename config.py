# System Configuration

# Geographic Settings
DEFAULT_LOCATION = {
    'center': [26.2006, 92.9376],  # Assam, Northeast India
    'zoom': 8
}

# Alert System Settings
ALERT_CONFIG = {
    'response_time_limit_hours': 24,
    'escalation_enabled': True,
    'notification_channels': ['email', 'sms']
}

# Email Configuration (Optional - Configure for production)
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'sender_email': 'your-email@example.com',
    'sender_password': 'your-app-password',
    'enabled': False  # Set to True when configured
}

# SMS Configuration (Optional - Configure for production)
SMS_CONFIG = {
    'provider': 'twilio',
    'account_sid': 'your_account_sid',
    'auth_token': 'your_auth_token',
    'from_number': '+1234567890',
    'enabled': False  # Set to True when configured
}

# Model Settings
MODEL_CONFIG = {
    'image_size': (224, 224),
    'confidence_threshold': 0.6,
    'batch_size': 32
}

# Risk Analysis Settings
RISK_CONFIG = {
    'high_risk_threshold': 2.0,
    'medium_risk_threshold': 1.0,
    'analysis_window_days': 30
}

# Disease Database
DISEASE_SEVERITY = {
    'Critical': ['Cholera'],
    'High': ['Typhoid', 'Dysentery', 'Hepatitis A'],
    'Medium': ['Diarrhea', 'Gastroenteritis']
}

# Water Quality Thresholds
WATER_QUALITY_THRESHOLDS = {
    'turbidity_high': 100,
    'blue_ratio_normal': 0.3,
    'floating_objects_threshold': 50,
    'oil_layer_ratio': 0.1,
    'algae_ratio': 0.15
}

# API Settings
API_CONFIG = {
    'host': '0.0.0.0',
    'port': 5000,
    'debug': True,
    'upload_folder': 'uploads',
    'max_file_size_mb': 10
}

# Frontend Settings
FRONTEND_CONFIG = {
    'api_url': 'http://localhost:5000/api',
    'map_refresh_interval_seconds': 300,
    'auto_refresh_enabled': True
}
