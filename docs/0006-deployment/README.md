# Deployment Documentation

Welcome to comprehensive deployment documentation for FSL Continuum.

## 🌊 Navigation

### 🚀 Deployment Overview
Learn about different deployment options for FSL Continuum.

1. [Production Deployment](0001-production-deployment.md)
   - [Overview](0001-production-deployment/0001-overview.md)
   - [Self-Hosted Setup](0001-production-deployment/0002-self-hosted.md)
   - [Cloud Deployment](0001-production-deployment/0003-cloud-deployment.md)
   - [Container Deployment](0001-production-deployment/0004-container-deployment.md)

2. [Development Deployment](0002-development-deployment.md)
   - [Overview](0002-development-deployment/0001-overview.md)
   - [Local Setup](0002-development-deployment/0002-local-setup.md)
   - [Docker Development](0002-development-deployment/0003-docker-development.md)
   - [CI/CD Integration](0002-development-deployment/0004-cicd-integration.md)

3. [Enterprise Deployment](0003-enterprise-deployment.md)
   - [Overview](0003-enterprise-deployment/0001-overview.md)
   - [SSO Integration](0003-enterprise-deployment/0002-sso-integration.md)
   - [Security Configuration](0003-enterprise-deployment/0003-security-configuration.md)
   - [Performance Optimization](0003-enterprise-deployment/0004-performance-optimization.md)

4. [Configuration Management](0004-configuration-management.md)
   - [Overview](0004-configuration-management/0001-overview.md)
   - [Environment Variables](0004-configuration-management/0002-environment-variables.md)
   - [Secret Management](0004-configuration-management/0003-secret-management.md)
   - [Configuration Validation](0004-configuration-management/0004-configuration-validation.md)

5. [Monitoring and Observability](0005-monitoring-observability.md)
   - [Overview](0005-monitoring-observability/0001-overview.md)
   - [Metrics Collection](0005-monitoring-observability/0002-metrics-collection.md)
   - [Log Management](0005-monitoring-observability/0003-log-management.md)
   - [Alert Configuration](0005-monitoring-observability/0004-alert-configuration.md)

6. [Scaling and Load Balancing](0006-scaling-load-balancing.md)
   - [Overview](0006-scaling-load-balancing/0001-overview.md)
   - [Horizontal Scaling](0006-scaling-load-balancing/0002-horizontal-scaling.md)
   - [Vertical Scaling](0006-scaling-load-balancing/0003-vertical-scaling.md)
   - [Load Balancer Configuration](0006-scaling-load-balancing/0004-load-balancer-configuration.md)

7. [Backup and Disaster Recovery](0007-backup-disaster-recovery.md)
   - [Overview](0007-backup-disaster-recovery/0001-overview.md)
   - [Backup Strategies](0007-backup-disaster-recovery/0002-backup-strategies.md)
   - [Recovery Procedures](0007-backup-disaster-recovery/0003-recovery-procedures.md)
   - [Business Continuity](0007-backup-disaster-recovery/0004-business-continuity.md)

---

## 🚀 Quick Start

### Production Deployment

```bash
# 1. Clone repository
git clone https://github.com/your-org/fsl-continuum.git
cd fsl-continuum

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env with your settings

# 4. Deploy
docker-compose up -d
```

### Development Deployment

```bash
# 1. Set up development environment
python -m venv venv
source venv/bin/activate

# 2. Install development dependencies
pip install -r requirements-dev.txt

# 3. Run in development mode
python -m fsl_continuum --dev
```

### Container Deployment

```bash
# 1. Build container
docker build -t fsl-continuum .

# 2. Run container
docker run -d \
  --name fsl-continuum \
  -p 8080:8080 \
  -v $(pwd)/config:/app/config \
  -v $(pwd)/data:/app/data \
  fsl-continuum
```

---

## 📋 Deployment Prerequisites

### System Requirements

- **Python**: 3.9 or higher
- **Memory**: 4GB RAM minimum, 8GB recommended
- **Storage**: 10GB free space minimum, 50GB recommended
- **Network**: 1Gbps connection recommended for production

### Platform Support

- **Operating Systems**: Linux (Ubuntu 20.04+, CentOS 8+), macOS 10.15+, Windows 10+
- **Container Platforms**: Docker 20.10+, Kubernetes 1.24+
- **Cloud Platforms**: AWS, Azure, Google Cloud, DigitalOcean

### Dependencies

- **Core**: Redis 6+, PostgreSQL 13+, Git 2.30+
- **Optional**: MongoDB 5+, Elasticsearch 8+, Prometheus
- **Development**: Node.js 16+, Docker 20+, Make 4+

---

## 🏗️ Deployment Architecture

### Production Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Load Balancer  │    │   FSL Continuum  │    │  Database       │
│  (Nginx/HAProxy)│────│   (App Servers) │────│  (PostgreSQL)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Static Assets  │    │     Redis       │    │   Monitoring    │
│  (CDN/S3)      │────│   (Cache)       │────│  (Prometheus)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Development Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Dev Server     │    │   Hot Reload    │    │  Test Database  │
│  (uvicorn)     │────│  (watchdog)     │────│  (PostgreSQL)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Dev Tools      │    │   Debug UI      │    │   Dev Logs     │
│  (pre-commit)  │────│   (debugger)    │────│  (file logs)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

---

## 🔧 Configuration

### Environment Variables

```bash
# Core Settings
FSL_ENV=production
FSL_DEBUG=false
FSL_LOG_LEVEL=info

# Database Settings
FSL_DB_HOST=localhost
FSL_DB_PORT=5432
FSL_DB_NAME=fsl_continuum
FSL_DB_USER=fsl_user
FSL_DB_PASSWORD=secure_password

# Redis Settings
FSL_REDIS_HOST=localhost
FSL_REDIS_PORT=6379
FSL_REDIS_DB=0

# Security Settings
FSL_SECRET_KEY=your_secret_key_here
FSL_API_TOKEN=your_api_token_here
FSL_ENCRYPTION_KEY=your_encryption_key_here

# AI Integration
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
```

### Configuration Files

```yaml
# config/production.yaml
server:
  host: "0.0.0.0"
  port: 8080
  workers: 4

database:
  host: "${FSL_DB_HOST}"
  port: "${FSL_DB_PORT}"
  name: "${FSL_DB_NAME}"
  user: "${FSL_DB_USER}"
  password: "${FSL_DB_PASSWORD}"

ai_integration:
  enabled: true
  models:
    openai: "${OPENAI_API_KEY}"
    anthropic: "${ANTHROPIC_API_KEY}"

logging:
  level: "info"
  file: "logs/fsl_continuum.log"
  max_size: "100MB"
  backup_count: 10
```

---

## 🔐 Security Configuration

### SSL/TLS Setup

```nginx
# nginx.conf
server {
    listen 443 ssl;
    server_name fsl-continuum.your-domain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    
    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Firewall Configuration

```bash
# Allow web traffic
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Allow SSH (if needed)
sudo ufw allow 22/tcp

# Enable firewall
sudo ufw enable
```

### Authentication Setup

```yaml
# config/security.yaml
authentication:
  enabled: true
  type: "oauth"
  providers:
    - name: "github"
      client_id: "${GITHUB_CLIENT_ID}"
      client_secret: "${GITHUB_CLIENT_SECRET}"
    - name: "google"
      client_id: "${GOOGLE_CLIENT_ID}"
      client_secret: "${GOOGLE_CLIENT_SECRET}"
  
authorization:
  roles:
    - name: "admin"
      permissions: ["read", "write", "delete"]
    - name: "user"
      permissions: ["read", "write"]
    - name: "viewer"
      permissions: ["read"]
```

---

## 📊 Monitoring

### Metrics Collection

```yaml
# config/monitoring.yaml
prometheus:
  enabled: true
  port: 9090
  metrics_path: "/metrics"
  
  collect:
    - name: "http_requests_total"
      type: "counter"
    - name: "http_request_duration_seconds"
      type: "histogram"
    - name: "ai_processing_time"
      type: "gauge"
    - name: "cache_hit_rate"
      type: "gauge"

grafana:
  enabled: true
  url: "http://localhost:3000"
  dashboard: "fsl-continuum"
  
  alerts:
    - name: "high_error_rate"
      condition: "error_rate > 0.05"
      severity: "critical"
    - name: "slow_ai_processing"
      condition: "ai_processing_time > 5.0"
      severity: "warning"
```

### Log Management

```yaml
# config/logging.yaml
logging:
  level: "info"
  format: "json"
  
  handlers:
    - type: "file"
      filename: "logs/fsl_continuum.log"
      max_size: "100MB"
      backup_count: 10
    - type: "syslog"
      facility: "daemon"
    - type: "elasticsearch"
      hosts: ["localhost:9200"]
      index: "fsl-continuum"
  
  loggers:
    - name: "fsl_continuum"
      level: "info"
    - name: "ai_integration"
      level: "debug"
    - name: "security"
      level: "warning"
```

---

## 🔄 Scaling

### Horizontal Scaling

```yaml
# docker-compose.production.yml
version: "3.8"
services:
  app:
    image: fsl-continuum:latest
    replicas: 3
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: "1.0"
          memory: "1G"
        reservations:
          cpus: "0.5"
          memory: "512M"
    
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - app
  
  redis:
    image: redis:alpine
    deploy:
      replicas: 2
  
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: fsl_continuum
      POSTGRES_USER: fsl_user
      POSTGRES_PASSWORD: secure_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
```

### Kubernetes Scaling

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fsl-continuum
spec:
  replicas: 3
  selector:
    matchLabels:
      app: fsl-continuum
  template:
    metadata:
      labels:
        app: fsl-continuum
    spec:
      containers:
        - name: fsl-continuum
          image: fsl-continuum:latest
          ports:
            - containerPort: 8080
          env:
            - name: FSL_DB_HOST
              value: "postgres-service"
          resources:
            requests:
              cpu: "500m"
              memory: "512Mi"
            limits:
              cpu: "1.0"
              memory: "1Gi"
---
apiVersion: v1
kind: Service
metadata:
  name: fsl-continuum-service
spec:
  selector:
    app: fsl-continuum
  ports:
    - port: 80
      targetPort: 8080
  type: LoadBalancer
```

---

## 🚨 Troubleshooting

### Common Deployment Issues

1. **Database Connection Errors**
   - Check database credentials in .env
   - Verify database is running and accessible
   - Check network connectivity

2. **Port Already in Use**
   - Check if port 8080 is occupied
   - Kill conflicting processes
   - Use different port if needed

3. **Permission Errors**
   - Check file permissions for data directories
   - Verify user has proper permissions
   - Check SELinux/AppArmor policies

4. **Memory Issues**
   - Monitor memory usage with `htop`
   - Increase memory if needed
   - Check for memory leaks in application

### Debug Mode

```bash
# Enable debug mode
export FSL_DEBUG=true
export FSL_LOG_LEVEL=debug

# Run with debug logs
python -m fsl_continuum --debug
```

### Health Checks

```bash
# Check application health
curl http://localhost:8080/health

# Check database connection
python -c "
from fsl_continuum import Database
db = Database()
if db.ping():
    print('Database is healthy')
else:
    print('Database connection failed')
"

# Check Redis connection
redis-cli ping
```

---

## 📚 Additional Resources

### Documentation
- [Production Deployment Guide](0001-production-deployment.md)
- [Development Setup Guide](0002-development-deployment.md)
- [Enterprise Deployment Guide](0003-enterprise-deployment.md)

### Tools and Scripts
- [Deployment Scripts](scripts/deployment/)
- [Configuration Templates](config/templates/)
- [Monitoring Dashboards](monitoring/dashboards/)

### Community and Support
- [GitHub Discussions](https://github.com/your-org/fsl-continuum/discussions)
- [Discord Community](https://discord.gg/fsl-continuum)
- [Documentation Issues](https://github.com/your-org/fsl-continuum/issues)

---

*FSL Continuum deployment documentation - enabling terminal velocity with reliable deployment.*
