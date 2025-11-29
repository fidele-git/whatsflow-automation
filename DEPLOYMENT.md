# WhatsFlow Automation - Production Deployment Guide

This guide provides detailed instructions for deploying WhatsFlow Automation to a production server.

## Table of Contents

1. [Server Requirements](#server-requirements)
2. [Initial Server Setup](#initial-server-setup)
3. [Installation Methods](#installation-methods)
4. [Database Setup](#database-setup)
5. [SSL/HTTPS Configuration](#sslhttps-configuration)
6. [Environment Configuration](#environment-configuration)
7. [Running the Application](#running-the-application)
8. [Maintenance](#maintenance)
9. [Troubleshooting](#troubleshooting)

## Server Requirements

### Minimum Requirements
- **OS**: Ubuntu 20.04 LTS or later (or any Linux distribution)
- **RAM**: 1GB minimum, 2GB recommended
- **CPU**: 1 core minimum, 2 cores recommended
- **Storage**: 10GB minimum
- **Python**: 3.11 or later

### Recommended Cloud Providers
- DigitalOcean (Droplet)
- AWS (EC2)
- Google Cloud Platform (Compute Engine)
- Linode
- Vultr

## Initial Server Setup

### 1. Update System
```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Install Required Packages
```bash
sudo apt install -y python3.11 python3.11-venv python3-pip git nginx certbot python3-certbot-nginx
```

### 3. Create Application User
```bash
sudo adduser whatsflow
sudo usermod -aG sudo whatsflow
su - whatsflow
```

### 4. Install Docker (Optional but Recommended)
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker whatsflow
sudo apt install -y docker-compose
```

## Installation Methods

### Method 1: Docker Deployment (Recommended)

1. **Clone Repository**
   ```bash
   cd /home/whatsflow
   git clone https://github.com/fidele-git/whatsflow-automation.git
   cd whatsflow-automation
   ```

2. **Configure Environment**
   ```bash
   cp .env.example .env
   nano .env  # Edit with your configuration
   ```

3. **Build and Run**
   ```bash
   docker-compose up -d
   ```

4. **Initialize Database**
   ```bash
   docker-compose exec web python init_pricing.py
   docker-compose exec web python scripts/create_admin.py
   ```

### Method 2: Traditional Deployment

1. **Clone Repository**
   ```bash
   cd /home/whatsflow
   git clone https://github.com/fidele-git/whatsflow-automation.git
   cd whatsflow-automation
   ```

2. **Create Virtual Environment**
   ```bash
   python3.11 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install gunicorn
   ```

4. **Configure Environment**
   ```bash
   cp .env.example .env
   nano .env  # Edit with your configuration
   ```

5. **Initialize Database**
   ```bash
   python init_pricing.py
   python scripts/create_admin.py
   ```

6. **Create Systemd Service**
   ```bash
   sudo nano /etc/systemd/system/whatsflow.service
   ```

   Add the following content:
   ```ini
   [Unit]
   Description=WhatsFlow Automation
   After=network.target

   [Service]
   User=whatsflow
   WorkingDirectory=/home/whatsflow/whatsflow-automation
   Environment="PATH=/home/whatsflow/whatsflow-automation/.venv/bin"
   ExecStart=/home/whatsflow/whatsflow-automation/.venv/bin/gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 120 app:app
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

7. **Start Service**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable whatsflow
   sudo systemctl start whatsflow
   sudo systemctl status whatsflow
   ```

## Database Setup

### SQLite (Default - Development/Small Scale)
- Already configured in `.env`
- Database file: `instance/whatsflow.db`
- Automatic backups recommended

### PostgreSQL (Recommended for Production)

1. **Install PostgreSQL**
   ```bash
   sudo apt install -y postgresql postgresql-contrib
   ```

2. **Create Database and User**
   ```bash
   sudo -u postgres psql
   ```
   ```sql
   CREATE DATABASE whatsflow;
   CREATE USER whatsflow WITH PASSWORD 'your-secure-password';
   GRANT ALL PRIVILEGES ON DATABASE whatsflow TO whatsflow;
   \q
   ```

3. **Update .env**
   ```env
   DATABASE_URL=postgresql://whatsflow:your-secure-password@localhost/whatsflow
   ```

4. **Install PostgreSQL Driver**
   ```bash
   pip install psycopg2-binary
   ```

## SSL/HTTPS Configuration

### Using Nginx and Let's Encrypt

1. **Configure Nginx**
   ```bash
   sudo nano /etc/nginx/sites-available/whatsflow
   ```

   Add the following:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com www.your-domain.com;

       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }

       client_max_body_size 10M;
   }
   ```

2. **Enable Site**
   ```bash
   sudo ln -s /etc/nginx/sites-available/whatsflow /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

3. **Obtain SSL Certificate**
   ```bash
   sudo certbot --nginx -d your-domain.com -d www.your-domain.com
   ```

4. **Auto-Renewal**
   ```bash
   sudo certbot renew --dry-run
   ```

## Environment Configuration

### Required Environment Variables

```env
# Security
SECRET_KEY=your-very-long-random-secret-key-here

# Database
DATABASE_URL=sqlite:///whatsflow.db  # or PostgreSQL URL

# Email (Gmail Example)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-specific-password
MAIL_DEFAULT_SENDER=your-email@gmail.com
```

### Generating Secure SECRET_KEY
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Gmail App Password
1. Enable 2-Factor Authentication on your Google account
2. Go to https://myaccount.google.com/apppasswords
3. Generate an app password for "Mail"
4. Use this password in `MAIL_PASSWORD`

## Running the Application

### Check Status
```bash
# Docker
docker-compose ps
docker-compose logs -f

# Systemd
sudo systemctl status whatsflow
sudo journalctl -u whatsflow -f
```

### Restart Application
```bash
# Docker
docker-compose restart

# Systemd
sudo systemctl restart whatsflow
```

### Update Application
```bash
cd /home/whatsflow/whatsflow-automation
git pull origin main

# Docker
docker-compose down
docker-compose build
docker-compose up -d

# Systemd
source .venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart whatsflow
```

## Maintenance

### Database Backups

**SQLite:**
```bash
# Backup
cp instance/whatsflow.db instance/whatsflow.db.backup-$(date +%Y%m%d)

# Automated daily backups
echo "0 2 * * * cp /home/whatsflow/whatsflow-automation/instance/whatsflow.db /home/whatsflow/backups/whatsflow.db.backup-\$(date +\%Y\%m\%d)" | crontab -
```

**PostgreSQL:**
```bash
# Backup
pg_dump whatsflow > whatsflow_backup_$(date +%Y%m%d).sql

# Restore
psql whatsflow < whatsflow_backup_20250129.sql
```

### Log Rotation
```bash
sudo nano /etc/logrotate.d/whatsflow
```

Add:
```
/home/whatsflow/whatsflow-automation/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 whatsflow whatsflow
}
```

### Monitoring
- Set up monitoring with tools like:
  - Uptime Robot (uptime monitoring)
  - Sentry (error tracking)
  - Prometheus + Grafana (metrics)

## Troubleshooting

### Application Won't Start
```bash
# Check logs
docker-compose logs web  # Docker
sudo journalctl -u whatsflow -n 50  # Systemd

# Check if port is in use
sudo lsof -i :5000

# Check file permissions
ls -la /home/whatsflow/whatsflow-automation
```

### Database Connection Issues
```bash
# Check database file exists
ls -la instance/

# Check PostgreSQL is running
sudo systemctl status postgresql

# Test database connection
python -c "from app import app, db; app.app_context().push(); print(db.engine.url)"
```

### Email Not Sending
```bash
# Test email configuration
python -c "from flask_mail import Mail, Message; from app import app, mail; app.app_context().push(); msg = Message('Test', recipients=['test@example.com']); mail.send(msg)"

# Check SMTP credentials
# Verify Gmail app password is correct
# Check firewall allows outbound SMTP
```

### Performance Issues
- Increase Gunicorn workers: `--workers 8`
- Use PostgreSQL instead of SQLite
- Add Redis for caching
- Use CDN for static files
- Enable Nginx caching

## Security Best Practices

1. **Keep system updated**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. **Use strong passwords**
   - Generate with: `openssl rand -base64 32`

3. **Enable firewall**
   ```bash
   sudo ufw allow 22/tcp
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   sudo ufw enable
   ```

4. **Regular backups**
   - Database daily
   - Application files weekly

5. **Monitor logs**
   - Check for suspicious activity
   - Set up alerts for errors

6. **Keep dependencies updated**
   ```bash
   pip list --outdated
   pip install --upgrade -r requirements.txt
   ```

## Support

For deployment assistance, contact: whatsappautomationbusiness@gmail.com
