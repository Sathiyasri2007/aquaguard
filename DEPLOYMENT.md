# Production Deployment Guide

## 🚀 Deployment Options

### Option 1: AWS Deployment

#### EC2 Setup
```bash
# Launch EC2 instance (Ubuntu 20.04 LTS)
# t2.medium or larger recommended

# SSH into instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3-pip python3-venv nginx -y

# Clone/upload project
git clone your-repo-url
cd DT

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 backend.app:app
```

#### Configure Nginx
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        root /path/to/DT/frontend;
        index index.html;
    }

    location /api {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### S3 for Image Storage
```python
import boto3

s3_client = boto3.client('s3',
    aws_access_key_id='YOUR_KEY',
    aws_secret_access_key='YOUR_SECRET'
)

# Upload image
s3_client.upload_file('local_image.jpg', 'your-bucket', 'images/image.jpg')
```

### Option 2: Heroku Deployment

#### Create Procfile
```
web: gunicorn backend.app:app
```

#### Create runtime.txt
```
python-3.9.16
```

#### Deploy
```bash
heroku login
heroku create your-app-name
git push heroku main
```

### Option 3: Docker Deployment

#### Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "backend/app.py"]
```

#### docker-compose.yml
```yaml
version: '3.8'
services:
  backend:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./uploads:/app/uploads
      - ./data:/app/data
    environment:
      - FLASK_ENV=production
  
  frontend:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./frontend:/usr/share/nginx/html
```

#### Deploy
```bash
docker-compose up -d
```

## 🔒 Security Configuration

### 1. Environment Variables
Create `.env` file:
```
FLASK_SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:pass@host:5432/db
EMAIL_PASSWORD=your-email-password
SMS_AUTH_TOKEN=your-sms-token
AWS_ACCESS_KEY=your-aws-key
AWS_SECRET_KEY=your-aws-secret
```

### 2. Enable HTTPS
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d your-domain.com
```

### 3. API Authentication
Add to backend/app.py:
```python
from functools import wraps
from flask import request

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if api_key != os.getenv('API_KEY'):
            return jsonify({'error': 'Invalid API key'}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/api/analyze', methods=['POST'])
@require_api_key
def analyze_water():
    # ... existing code
```

## 📊 Database Setup (Production)

### PostgreSQL Setup
```bash
# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Create database
sudo -u postgres psql
CREATE DATABASE water_monitoring;
CREATE USER admin WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE water_monitoring TO admin;
```

### Update backend to use PostgreSQL
```python
import psycopg2
from psycopg2.extras import RealDictCursor

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
```

## 📧 Email Configuration (Production)

### Using Gmail
```python
import smtplib
from email.mime.text import MIMEText

def send_email(to_email, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = os.getenv('EMAIL_USER')
    msg['To'] = to_email
    
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(os.getenv('EMAIL_USER'), os.getenv('EMAIL_PASSWORD'))
        server.send_message(msg)
```

### Using AWS SES
```python
import boto3

ses_client = boto3.client('ses',
    region_name='us-east-1',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('AWS_SECRET_KEY')
)

def send_email_ses(to_email, subject, body):
    ses_client.send_email(
        Source='noreply@yourdomain.com',
        Destination={'ToAddresses': [to_email]},
        Message={
            'Subject': {'Data': subject},
            'Body': {'Text': {'Data': body}}
        }
    )
```

## 📱 SMS Configuration (Production)

### Using Twilio
```python
from twilio.rest import Client

def send_sms(to_phone, message):
    client = Client(
        os.getenv('TWILIO_ACCOUNT_SID'),
        os.getenv('TWILIO_AUTH_TOKEN')
    )
    
    client.messages.create(
        body=message,
        from_=os.getenv('TWILIO_PHONE'),
        to=to_phone
    )
```

### Using AWS SNS
```python
import boto3

sns_client = boto3.client('sns',
    region_name='ap-south-1',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('AWS_SECRET_KEY')
)

def send_sms_sns(to_phone, message):
    sns_client.publish(
        PhoneNumber=to_phone,
        Message=message
    )
```

## 🔄 Continuous Deployment

### GitHub Actions Workflow
Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Deploy to EC2
      uses: appleboy/ssh-action@master
      with:
        host: ${{ secrets.EC2_HOST }}
        username: ubuntu
        key: ${{ secrets.EC2_KEY }}
        script: |
          cd /path/to/DT
          git pull
          source venv/bin/activate
          pip install -r requirements.txt
          sudo systemctl restart water-monitoring
```

## 📈 Monitoring & Logging

### Setup Logging
```python
import logging
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler('app.log', maxBytes=10000000, backupCount=5)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
app.logger.addHandler(handler)
```

### CloudWatch Integration
```python
import watchtower

app.logger.addHandler(watchtower.CloudWatchLogHandler(
    log_group='water-monitoring',
    stream_name='production'
))
```

## 🔧 Performance Optimization

### 1. Caching with Redis
```python
import redis
from functools import wraps

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def cache_result(timeout=300):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            cache_key = f"{f.__name__}:{str(args)}:{str(kwargs)}"
            cached = redis_client.get(cache_key)
            if cached:
                return json.loads(cached)
            result = f(*args, **kwargs)
            redis_client.setex(cache_key, timeout, json.dumps(result))
            return result
        return decorated_function
    return decorator
```

### 2. Load Balancing
Use AWS ELB or Nginx load balancer for multiple instances

### 3. CDN for Static Files
Use CloudFront or Cloudflare for frontend assets

## 🧪 Testing in Production

### Health Check Endpoint
```python
@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })
```

### Monitoring Script
```bash
#!/bin/bash
while true; do
    response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/health)
    if [ $response != "200" ]; then
        echo "Service down! Restarting..."
        sudo systemctl restart water-monitoring
    fi
    sleep 60
done
```

## 📋 Pre-Deployment Checklist

- [ ] Environment variables configured
- [ ] Database setup and migrated
- [ ] SSL certificate installed
- [ ] Email/SMS credentials configured
- [ ] API authentication enabled
- [ ] Logging configured
- [ ] Backup strategy in place
- [ ] Monitoring setup
- [ ] Load testing completed
- [ ] Security audit done
- [ ] Documentation updated
- [ ] Team trained

## 🆘 Rollback Plan

```bash
# Keep previous version
cp -r DT DT_backup_$(date +%Y%m%d)

# If issues occur, rollback
sudo systemctl stop water-monitoring
rm -rf DT
mv DT_backup_YYYYMMDD DT
sudo systemctl start water-monitoring
```

## 📞 Support & Maintenance

- Monitor logs daily
- Review alert statistics weekly
- Update ML models monthly
- Security patches as needed
- Database backups daily
- Performance optimization quarterly

---

**Production deployment requires careful planning and testing. Always test in staging environment first!**
