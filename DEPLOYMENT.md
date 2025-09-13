# Deployment Guide

This guide covers how to deploy the Resume Optimization Backend System in different environments.

## Local Development Setup

### Prerequisites
- Python 3.8 or higher
- Google Gemini API key

### Quick Start
1. **Clone the project and navigate to directory**
   ```bash
   cd /path/to/resume-optimization-backend
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env and add your GEMINI_API_KEY
   ```

5. **Test the system**
   ```bash
   python3 test_system.py
   ```

6. **Start the server**
   ```bash
   python3 start_server.py
   # Or directly: python3 main.py
   ```

7. **Test the API**
   ```bash
   # In another terminal
   python3 example_client.py
   ```

## Production Deployment

### Option 1: Docker Deployment (Recommended)

Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  resume-optimizer:
    build: .
    ports:
      - "8000:8000"
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    volumes:
      - ./logs:/app/logs
```

Deploy with Docker Compose:
```bash
# Set your API key
export GEMINI_API_KEY="your_api_key_here"

# Build and start
docker-compose up -d

# Check logs
docker-compose logs -f

# Stop
docker-compose down
```

### Option 2: Traditional Server Deployment

#### Using systemd (Ubuntu/CentOS)

1. **Prepare the application**
   ```bash
   sudo mkdir -p /opt/resume-optimizer
   sudo cp -r * /opt/resume-optimizer/
   cd /opt/resume-optimizer
   sudo python3 -m venv venv
   sudo venv/bin/pip install -r requirements.txt
   ```

2. **Create systemd service file**
   ```bash
   sudo nano /etc/systemd/system/resume-optimizer.service
   ```

   ```ini
   [Unit]
   Description=Resume Optimization Backend
   After=network.target

   [Service]
   Type=simple
   User=www-data
   WorkingDirectory=/opt/resume-optimizer
   Environment=PATH=/opt/resume-optimizer/venv/bin
   Environment=GEMINI_API_KEY=your_api_key_here
   ExecStart=/opt/resume-optimizer/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
   Restart=always
   RestartSec=3

   [Install]
   WantedBy=multi-user.target
   ```

3. **Start the service**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable resume-optimizer
   sudo systemctl start resume-optimizer
   sudo systemctl status resume-optimizer
   ```

#### Using Nginx as Reverse Proxy

1. **Install Nginx**
   ```bash
   sudo apt install nginx
   ```

2. **Create Nginx configuration**
   ```bash
   sudo nano /etc/nginx/sites-available/resume-optimizer
   ```

   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       client_max_body_size 10M;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
           proxy_read_timeout 300s;
           proxy_connect_timeout 75s;
       }

       location /health {
           proxy_pass http://127.0.0.1:8000/health;
           access_log off;
       }
   }
   ```

3. **Enable the site**
   ```bash
   sudo ln -s /etc/nginx/sites-available/resume-optimizer /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

### Option 3: Cloud Platform Deployment

#### Heroku

1. **Create `Procfile`**
   ```
   web: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

2. **Deploy**
   ```bash
   heroku create your-app-name
   heroku config:set GEMINI_API_KEY="your_api_key_here"
   git push heroku main
   ```

#### AWS EC2

1. **Launch EC2 instance** (Ubuntu 20.04 LTS recommended)
2. **Install dependencies**
   ```bash
   sudo apt update
   sudo apt install -y python3 python3-venv python3-pip nginx
   ```
3. **Follow traditional server deployment steps above**
4. **Configure security groups** to allow HTTP (port 80) and HTTPS (port 443)

#### Google Cloud Platform

1. **Create `app.yaml` for App Engine**
   ```yaml
   runtime: python311

   env_variables:
     GEMINI_API_KEY: "your_api_key_here"

   automatic_scaling:
     min_instances: 1
     max_instances: 10
   ```

2. **Deploy**
   ```bash
   gcloud app deploy
   ```

## Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `GEMINI_API_KEY` | Google Gemini API key | Yes | None |
| `MAX_FILE_SIZE` | Maximum file size in bytes | No | 10485760 (10MB) |
| `LOG_LEVEL` | Logging level | No | INFO |
| `HOST` | Server host | No | 0.0.0.0 |
| `PORT` | Server port | No | 8000 |

## Security Considerations

### API Security
- **Rate Limiting**: Implement rate limiting to prevent abuse
- **Input Validation**: All inputs are validated and sanitized
- **File Size Limits**: Maximum file size is enforced
- **CORS**: Configure CORS appropriately for your frontend domain

### Production Security
```python
# Add to main.py for production
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=["your-domain.com", "*.your-domain.com"]
)
```

### SSL/HTTPS
For production, always use HTTPS:
```bash
# Using Certbot for free SSL
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

## Monitoring and Logging

### Application Logs
```python
# Configure structured logging
import logging
import json

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            'timestamp': self.formatTime(record),
            'level': record.levelname,
            'message': record.getMessage(),
            'module': record.module
        }
        return json.dumps(log_entry)

# Use in main.py
logging.basicConfig(
    level=logging.INFO,
    handlers=[logging.FileHandler('app.log')],
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Health Monitoring
- Use the `/health` endpoint for health checks
- Monitor API response times and error rates
- Set up alerts for API failures

### Resource Monitoring
- Monitor CPU, memory, and disk usage
- Track API request volumes and patterns
- Monitor Gemini API usage and costs

## Scaling Considerations

### Horizontal Scaling
- Use a load balancer (nginx, HAProxy, or cloud load balancer)
- Deploy multiple instances of the application
- Consider using container orchestration (Kubernetes, Docker Swarm)

### Performance Optimization
- Implement caching for frequently processed resumes
- Use async processing for long-running operations
- Consider adding a task queue (Celery, RQ) for background processing

### Database Integration (Optional)
For tracking and analytics:
```python
# Example database models
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ProcessingLog(Base):
    __tablename__ = "processing_logs"
    
    id = Column(Integer, primary_key=True)
    filename = Column(String(255))
    file_size = Column(Integer)
    processing_time = Column(Integer)  # in seconds
    status = Column(String(50))
    created_at = Column(DateTime)
```

## Troubleshooting

### Common Issues

1. **"GEMINI_API_KEY environment variable is required"**
   - Ensure the API key is set in your environment
   - Check that the .env file is in the correct location

2. **"Failed to parse PDF file"**
   - Ensure the PDF contains extractable text (not just images)
   - Try converting the PDF to a different format

3. **API timeout errors**
   - Increase timeout values in your client
   - Check Gemini API rate limits and quotas

4. **High memory usage**
   - Monitor file sizes being processed
   - Implement file size limits
   - Consider processing files in chunks

### Debugging
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG

# Run with verbose output
uvicorn main:app --host 0.0.0.0 --port 8000 --log-level debug

# Check system resources
htop
df -h
```

## Backup and Recovery

### Application Backup
```bash
# Backup application and configuration
tar -czf resume-optimizer-backup-$(date +%Y%m%d).tar.gz \
    /opt/resume-optimizer \
    /etc/nginx/sites-available/resume-optimizer \
    /etc/systemd/system/resume-optimizer.service
```

### Disaster Recovery
1. Keep configuration files in version control
2. Document your deployment process
3. Test recovery procedures regularly
4. Consider using infrastructure as code (Terraform, Ansible)

## Support and Maintenance

### Regular Maintenance
- Update dependencies regularly
- Monitor security advisories
- Review and rotate API keys
- Clean up temporary files and logs

### Updates and Releases
```bash
# Update process
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart resume-optimizer
```

For questions or issues, check the logs and refer to the main README.md file.