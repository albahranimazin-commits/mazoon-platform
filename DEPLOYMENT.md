# Deployment Guide | دليل النشر
# Mazoon Platform Deployment

This guide covers deploying Mazoon to various platforms.

---

## 📋 Table of Contents

- [Local Development](#local-development)
- [Heroku](#heroku-deployment)
- [DigitalOcean](#digitalocean-deployment)
- [AWS](#aws-deployment)
- [Docker](#docker-deployment)
- [Production Checklist](#production-checklist)

---

## 🏠 Local Development

### Quick Setup

```bash
# Clone repository
git clone https://github.com/mazoon-platform/mazoon.git
cd mazoon

# Install dependencies
pip install -r requirements.txt

# Initialize database
python init_database.py

# Start server
python api.py
```

Access at: `http://localhost:5000`

---

## 🚀 Heroku Deployment

### Prerequisites
- Heroku account
- Heroku CLI installed

### Step 1: Prepare Files

Create `Procfile`:
```
web: gunicorn api:app
```

Create `runtime.txt`:
```
python-3.11.0
```

Update `requirements.txt`:
```bash
pip freeze > requirements.txt
```

### Step 2: Deploy

```bash
# Login to Heroku
heroku login

# Create app
heroku create mazoon-platform

# Add PostgreSQL (recommended for production)
heroku addons:create heroku-postgresql:mini

# Deploy
git push heroku main

# Open app
heroku open
```

### Step 3: Initialize Database

```bash
heroku run python init_database.py
```

### Environment Variables

```bash
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=your-secret-key
```

---

## 🌊 DigitalOcean Deployment

### Using Droplet

#### Step 1: Create Droplet
- Choose Ubuntu 22.04
- Minimum: 1GB RAM, 1 vCPU
- Add SSH key

#### Step 2: Connect and Setup

```bash
# Connect to droplet
ssh root@your-droplet-ip

# Update system
apt update && apt upgrade -y

# Install Python and dependencies
apt install python3-pip python3-venv nginx -y

# Create app directory
mkdir -p /var/www/mazoon
cd /var/www/mazoon

# Clone repository
git clone https://github.com/mazoon-platform/mazoon.git .

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn

# Initialize database
python init_database.py
```

#### Step 3: Setup Gunicorn

Create `/etc/systemd/system/mazoon.service`:

```ini
[Unit]
Description=Mazoon API
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/mazoon
Environment="PATH=/var/www/mazoon/venv/bin"
ExecStart=/var/www/mazoon/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 api:app

[Install]
WantedBy=multi-user.target
```

Start service:
```bash
systemctl start mazoon
systemctl enable mazoon
systemctl status mazoon
```

#### Step 4: Setup Nginx

Create `/etc/nginx/sites-available/mazoon`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

Enable site:
```bash
ln -s /etc/nginx/sites-available/mazoon /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

#### Step 5: SSL with Let's Encrypt

```bash
apt install certbot python3-certbot-nginx -y
certbot --nginx -d your-domain.com
```

---

## ☁️ AWS Deployment

### Using EC2

#### Step 1: Launch EC2 Instance
- AMI: Ubuntu 22.04
- Instance Type: t2.micro (free tier)
- Security Group: Allow HTTP (80), HTTPS (443), SSH (22)

#### Step 2: Setup (Similar to DigitalOcean)
Follow DigitalOcean steps above

### Using Elastic Beanstalk

#### Step 1: Install EB CLI

```bash
pip install awsebcli
```

#### Step 2: Initialize

```bash
eb init -p python-3.11 mazoon-platform
```

#### Step 3: Create Environment

```bash
eb create mazoon-production
```

#### Step 4: Deploy

```bash
eb deploy
```

### Using AWS Lambda (Serverless)

Use Zappa for serverless deployment:

```bash
pip install zappa

# Initialize
zappa init

# Deploy
zappa deploy production

# Update
zappa update production
```

---

## 🐳 Docker Deployment

### Step 1: Create Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Initialize database
RUN python init_database.py

# Expose port
EXPOSE 5000

# Run application
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "api:app"]
```

### Step 2: Create docker-compose.yml

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - DATABASE_URL=sqlite:///mazoon.db
    volumes:
      - ./data:/app/data
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - api
    restart: unless-stopped
```

### Step 3: Build and Run

```bash
# Build
docker-compose build

# Run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

---

## ✅ Production Checklist

### Security
- [ ] Change default SECRET_KEY
- [ ] Enable HTTPS/SSL
- [ ] Set up firewall (UFW)
- [ ] Configure CORS properly
- [ ] Add rate limiting
- [ ] Implement authentication
- [ ] Sanitize user inputs
- [ ] Enable security headers

### Database
- [ ] Use PostgreSQL/MySQL (not SQLite)
- [ ] Set up regular backups
- [ ] Enable connection pooling
- [ ] Add database indexes
- [ ] Configure replication

### Performance
- [ ] Enable caching (Redis)
- [ ] Set up CDN
- [ ] Enable gzip compression
- [ ] Optimize database queries
- [ ] Add monitoring (New Relic, Datadog)
- [ ] Configure load balancer

### Monitoring
- [ ] Set up error logging (Sentry)
- [ ] Configure uptime monitoring
- [ ] Add performance metrics
- [ ] Set up alerts
- [ ] Enable access logs

### Backup
- [ ] Database backups (daily)
- [ ] File backups
- [ ] Off-site backup storage
- [ ] Test restore procedures
- [ ] Document backup process

---

## 🔧 Environment Variables

### Required

```bash
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:pass@localhost/mazoon
```

### Optional

```bash
REDIS_URL=redis://localhost:6379
CORS_ORIGINS=https://mazoon.om,https://www.mazoon.om
MAX_CONTENT_LENGTH=16777216
UPLOAD_FOLDER=/var/uploads
```

---

## 📊 Performance Optimization

### 1. Database

```python
# Use connection pooling
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20
)
```

### 2. Caching

```python
# Add Redis caching
from flask_caching import Cache

cache = Cache(app, config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': os.environ.get('REDIS_URL')
})

@cache.cached(timeout=300)
def get_news():
    # Your code here
    pass
```

### 3. Gunicorn Configuration

```bash
gunicorn \
  --workers 4 \
  --threads 2 \
  --worker-class gthread \
  --timeout 30 \
  --keep-alive 5 \
  --max-requests 1000 \
  --max-requests-jitter 50 \
  -b 0.0.0.0:5000 \
  api:app
```

---

## 🔍 Monitoring Setup

### Application Monitoring (Sentry)

```python
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0
)
```

### Server Monitoring

```bash
# Install monitoring tools
apt install htop iotop nethogs

# View processes
htop

# View disk I/O
iotop

# View network usage
nethogs
```

---

## 🐛 Troubleshooting

### Common Issues

**Issue: Database locked**
```bash
# Solution: Use PostgreSQL instead of SQLite in production
```

**Issue: Port already in use**
```bash
# Find process using port 5000
lsof -i :5000

# Kill process
kill -9 PID
```

**Issue: Permission denied**
```bash
# Fix file permissions
chown -R www-data:www-data /var/www/mazoon
chmod -R 755 /var/www/mazoon
```

---

## 📞 Support

Need help with deployment?
- 📧 Email: support@mazoon.om
- 💬 Discord: [Join our server]
- 📚 Docs: https://docs.mazoon.om

---

**Made with ♥ in Oman | صُنع بكل ♥ في عُمان**
