# Production Deployment

## Overview

Production deployment of FSL Continuum requires careful planning, security configuration, and monitoring setup. This guide covers enterprise-grade production deployment with high availability, security, and performance optimization.

### Production Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Load Balancer  │    │   FSL Continuum  │    │  Database       │
│  (HAProxy/Nginx)│────│   (App Servers) │────│  (PostgreSQL)   │
│  SSL/TLS      │    │   (Multiple)    │    │  (Primary/Replica)│
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  CDN/Static    │    │     Redis       │    │   Monitoring    │
│  (CloudFlare)  │────│   (Cluster)     │────│  (Prometheus)   │
│  Cache         │    │   (Multiple)    │    │  (Grafana)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Prerequisites

### Infrastructure Requirements

#### Hardware Requirements

| Component | Minimum | Recommended | Production |
|-----------|----------|-------------|------------|
| CPU | 4 cores | 8 cores | 16+ cores |
| Memory | 8GB | 16GB | 32GB+ |
| Storage | 100GB SSD | 500GB SSD | 1TB+ NVMe |
| Network | 1Gbps | 10Gbps | 10Gbps+ |

#### Software Requirements

- **Operating System**: Ubuntu 20.04+, CentOS 8+, RHEL 8+
- **Container Runtime**: Docker 20.10+ or Podman 3.4+
- **Orchestration**: Kubernetes 1.24+ (optional)
- **Reverse Proxy**: Nginx 1.20+ or HAProxy 2.4+

#### External Services

- **Domain**: Custom domain with SSL certificate
- **Email**: SMTP server for notifications
- **Monitoring**: Optional external monitoring service
- **Backup**: Offsite backup storage

## Installation

### Step 1: Server Preparation

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Install Nginx
sudo apt install nginx -y

# Install SSL (Let's Encrypt)
sudo apt install certbot python3-certbot-nginx -y
```

### Step 2: Clone and Configure

```bash
# Clone repository
git clone https://github.com/your-org/fsl-continuum.git
cd fsl-continuum

# Switch to production branch
git checkout production

# Create production environment
cp .env.example .env.production

# Edit production configuration
nano .env.production
```

### Step 3: Configure Environment

```bash
# .env.production
# Core Settings
FSL_ENV=production
FSL_DEBUG=false
FSL_LOG_LEVEL=info
FSL_SECRET_KEY=$(openssl rand -hex 32)

# Database Settings
FSL_DB_HOST=postgres-primary
FSL_DB_PORT=5432
FSL_DB_NAME=fsl_continuum_prod
FSL_DB_USER=fsl_prod
FSL_DB_PASSWORD=secure_database_password

# Redis Settings
FSL_REDIS_HOST=redis-cluster
FSL_REDIS_PORT=6379
FSL_REDIS_DB=0

# Security Settings
FSL_SSL_CERT_PATH=/etc/letsencrypt/live/your-domain.com/fullchain.pem
FSL_SSL_KEY_PATH=/etc/letsencrypt/live/your-domain.com/privkey.pem

# AI Integration
OPENAI_API_KEY=your_openai_production_key
ANTHROPIC_API_KEY=your_anthropic_production_key

# Monitoring Settings
PROMETHEUS_ENABLED=true
GRAFANA_ENABLED=true
SENTRY_DSN=your_sentry_dsn

# Backup Settings
BACKUP_ENABLED=true
BACKUP_S3_BUCKET=your-backup-bucket
BACKUP_S3_ACCESS_KEY=your_s3_access_key
BACKUP_S3_SECRET_KEY=your_s3_secret_key
```

### Step 4: Docker Production Setup

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  # PostgreSQL Primary
  postgres-primary:
    image: postgres:15-alpine
    container_name: postgres-primary
    environment:
      POSTGRES_DB: ${FSL_DB_NAME}
      POSTGRES_USER: ${FSL_DB_USER}
      POSTGRES_PASSWORD: ${FSL_DB_PASSWORD}
    volumes:
      - postgres_primary_data:/var/lib/postgresql/data
      - ./config/postgres/primary.conf:/etc/postgresql/postgresql.conf
    networks:
      - fsl-network
    restart: unless-stopped
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 4G
        reservations:
          cpus: '1.0'
          memory: 2G

  # PostgreSQL Replica
  postgres-replica:
    image: postgres:15-alpine
    container_name: postgres-replica
    environment:
      POSTGRES_DB: ${FSL_DB_NAME}
      POSTGRES_USER: ${FSL_DB_USER}
      POSTGRES_PASSWORD: ${FSL_DB_PASSWORD}
      PGUSER: ${FSL_DB_USER}
      POSTGRES_MASTER_SERVICE: postgres-primary
      POSTGRES_REPLICATION_MODE: replica
      POSTGRES_REPLICATION_USER: replicator
      POSTGRES_REPLICATION_PASSWORD: replication_password
    volumes:
      - postgres_replica_data:/var/lib/postgresql/data
    networks:
      - fsl-network
    restart: unless-stopped
    depends_on:
      - postgres-primary

  # Redis Cluster
  redis-master:
    image: redis:7-alpine
    container_name: redis-master
    command: redis-server --cluster-enabled yes --cluster-config-file /redis/cluster.conf
    volumes:
      - redis_master_data:/data
      - ./config/redis/cluster.conf:/redis/cluster.conf
    networks:
      - fsl-network
    restart: unless-stopped
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 2G
        reservations:
          cpus: '0.5'
          memory: 1G

  redis-slave:
    image: redis:7-alpine
    container_name: redis-slave
    command: redis-server --slaveof redis-master 6379
    volumes:
      - redis_slave_data:/data
    networks:
      - fsl-network
    restart: unless-stopped
    depends_on:
      - redis-master

  # FSL Continuum App (Multiple instances)
  fsl-app-1:
    image: fsl-continuum:latest
    container_name: fsl-app-1
    environment:
      - FSL_ENV=production
      - FSL_DB_HOST=postgres-primary
      - FSL_REDIS_HOST=redis-master
    volumes:
      - ./logs:/app/logs
      - ./config:/app/config
    networks:
      - fsl-network
    restart: unless-stopped
    depends_on:
      - postgres-primary
      - redis-master
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 4G
        reservations:
          cpus: '1.0'
          memory: 2G

  fsl-app-2:
    image: fsl-continuum:latest
    container_name: fsl-app-2
    environment:
      - FSL_ENV=production
      - FSL_DB_HOST=postgres-primary
      - FSL_REDIS_HOST=redis-master
    volumes:
      - ./logs:/app/logs
      - ./config:/app/config
    networks:
      - fsl-network
    restart: unless-stopped
    depends_on:
      - postgres-primary
      - redis-master
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 4G
        reservations:
          cpus: '1.0'
          memory: 2G

  # Nginx Load Balancer
  nginx:
    image: nginx:alpine
    container_name: nginx-lb
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./config/nginx/nginx.conf:/etc/nginx/nginx.conf
      - ${FSL_SSL_CERT_PATH}:/etc/ssl/cert.pem:ro
      - ${FSL_SSL_KEY_PATH}:/etc/ssl/key.pem:ro
    networks:
      - fsl-network
    restart: unless-stopped
    depends_on:
      - fsl-app-1
      - fsl-app-2

  # Prometheus Monitoring
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
    volumes:
      - ./config/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    networks:
      - fsl-network
    restart: unless-stopped
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 2G
        reservations:
          cpus: '0.5'
          memory: 1G

  # Grafana Dashboard
  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=secure_grafana_password
      - GF_INSTALL_PLUGINS=grafana-clock-panel,grafana-simple-json-datasource
    volumes:
      - grafana_data:/var/lib/grafana
      - ./config/grafana/provisioning:/etc/grafana/provisioning
    networks:
      - fsl-network
    restart: unless-stopped
    depends_on:
      - prometheus

volumes:
  postgres_primary_data:
  postgres_replica_data:
  redis_master_data:
  redis_slave_data:
  prometheus_data:
  grafana_data:

networks:
  fsl-network:
    driver: bridge
```

### Step 5: SSL/TLS Configuration

```bash
# Obtain SSL certificate
sudo certbot --nginx -d your-domain.com --email admin@your-domain.com --agree-tos --no-eff-email

# Configure Nginx for SSL
sudo nano /etc/nginx/sites-available/fsl-continuum
```

```nginx
# /etc/nginx/sites-available/fsl-continuum
upstream fsl_backend {
    server fsl-app-1:8080;
    server fsl-app-2:8080;
}

server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;

    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # FSL Continuum proxy
    location / {
        proxy_pass http://fsl_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # WebSocket support
    location /ws {
        proxy_pass http://fsl_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }

    # Static files
    location /static/ {
        alias /var/www/fsl-continuum/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

### Step 6: Deploy

```bash
# Enable production configuration
ln -sf .env.production .env

# Start production services
docker-compose -f docker-compose.prod.yml up -d

# Verify services are running
docker-compose -f docker-compose.prod.yml ps

# Check logs
docker-compose -f docker-compose.prod.yml logs -f fsl-app-1
```

## Configuration

### Production Configuration

```yaml
# config/production.yaml
server:
  host: "0.0.0.0"
  port: 8080
  workers: 4
  worker_class: "uvicorn.workers.UvicornWorker"
  
database:
  host: "${FSL_DB_HOST}"
  port: "${FSL_DB_PORT}"
  name: "${FSL_DB_NAME}"
  user: "${FSL_DB_USER}"
  password: "${FSL_DB_PASSWORD}"
  pool_size: 20
  max_overflow: 30
  pool_timeout: 30
  pool_recycle: 3600
  
redis:
  host: "${FSL_REDIS_HOST}"
  port: "${FSL_REDIS_PORT}"
  db: "${FSL_REDIS_DB}"
  password: "${FSL_REDIS_PASSWORD}"
  max_connections: 100
  socket_timeout: 5
  socket_connect_timeout: 5

security:
  secret_key: "${FSL_SECRET_KEY}"
  ssl_cert_path: "${FSL_SSL_CERT_PATH}"
  ssl_key_path: "${FSL_SSL_KEY_PATH}"
  csrf_protection: true
  rate_limiting: true
  
logging:
  level: "info"
  format: "json"
  file: "/app/logs/fsl_continuum.log"
  max_size: "100MB"
  backup_count: 10
  handlers:
    - name: "file"
      enabled: true
    - name: "syslog"
      enabled: true
    - name: "prometheus"
      enabled: true

ai_integration:
  enabled: true
  timeout: 30
  retry_attempts: 3
  models:
    openai:
      model: "gpt-4"
      max_tokens: 4096
      temperature: 0.7
    anthropic:
      model: "claude-3-sonnet-20240229"
      max_tokens: 4096
      temperature: 0.7

monitoring:
  prometheus:
    enabled: true
    port: 9090
    metrics_path: "/metrics"
  grafana:
    enabled: true
    url: "http://grafana:3000"
  health_check:
    enabled: true
    interval: 30
    timeout: 10
```

### Environment Variables

```bash
# Critical production variables
export FSL_ENV=production
export FSL_DEBUG=false
export FSL_LOG_LEVEL=info
export FSL_SECRET_KEY=$(openssl rand -hex 32)

# Database configuration
export FSL_DB_HOST=postgres-primary
export FSL_DB_PORT=5432
export FSL_DB_NAME=fsl_continuum_prod
export FSL_DB_USER=fsl_prod
export FSL_DB_PASSWORD="secure_database_password"

# Redis configuration
export FSL_REDIS_HOST=redis-master
export FSL_REDIS_PORT=6379
export FSL_REDIS_DB=0

# SSL configuration
export FSL_SSL_CERT_PATH=/etc/letsencrypt/live/your-domain.com/fullchain.pem
export FSL_SSL_KEY_PATH=/etc/letsencrypt/live/your-domain.com/privkey.pem

# AI integration
export OPENAI_API_KEY="your_openai_production_key"
export ANTHROPIC_API_KEY="your_anthropic_production_key"

# Monitoring
export PROMETHEUS_ENABLED=true
export GRAFANA_ENABLED=true
export SENTRY_DSN="your_sentry_dsn"
```

## Security

### SSL/TLS Security

```bash
# Verify SSL certificate
sudo certbot certificates

# Test SSL configuration
openssl s_client -connect your-domain.com:443 -servername your-domain.com

# Set up automatic renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

### Firewall Configuration

```bash
# UFW configuration
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable

# Fail2Ban configuration
sudo apt install fail2ban -y
sudo nano /etc/fail2ban/jail.local
```

### Security Headers

```nginx
# Additional security headers
add_header Referrer-Policy "strict-origin-when-cross-origin";
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';";
add_header Permissions-Policy "camera=(), microphone=(), geolocation=()";
```

## Monitoring

### Health Checks

```bash
# Application health check
curl http://localhost:8080/health

# Database health check
docker exec postgres-primary pg_isready -U fsl_prod -d fsl_continuum_prod

# Redis health check
docker exec redis-master redis-cli ping

# Load balancer health check
curl http://localhost/nginx_health
```

### Metrics Collection

```yaml
# config/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "alert_rules.yml"

scrape_configs:
  - job_name: 'fsl-continuum'
    static_configs:
      - targets: ['fsl-app-1:9090', 'fsl-app-2:9090']
    metrics_path: '/metrics'
    scrape_interval: 5s

  - job_name: 'nginx'
    static_configs:
      - targets: ['nginx:9113']
    scrape_interval: 5s

  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres-exporter:9187']
    scrape_interval: 5s

  - job_name: 'redis'
    static_configs:
      - targets: ['redis-exporter:9121']
    scrape_interval: 5s
```

### Alert Configuration

```yaml
# alert_rules.yml
groups:
  - name: fsl_continuum_alerts
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value }} for the last 5 minutes"

      - alert: HighMemoryUsage
        expr: process_resident_memory_bytes / 1024 / 1024 > 4000
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "High memory usage detected"
          description: "Memory usage is {{ $value }}MB"

      - alert: DatabaseDown
        expr: up{job="postgres"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Database is down"
          description: "PostgreSQL database is not responding"
```

## Backup and Recovery

### Database Backup

```bash
#!/bin/bash
# backup_database.sh

BACKUP_DIR="/backups/database"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="fsl_continuum_prod"

# Create backup
docker exec postgres-primary pg_dump -U fsl_prod -d $DB_NAME | gzip > $BACKUP_DIR/fsl_backup_$DATE.sql.gz

# Upload to S3
aws s3 cp $BACKUP_DIR/fsl_backup_$DATE.sql.gz s3://your-backup-bucket/database/

# Clean old backups (keep 7 days)
find $BACKUP_DIR -name "fsl_backup_*.sql.gz" -mtime +7 -delete
```

### Application Backup

```bash
#!/bin/bash
# backup_application.sh

BACKUP_DIR="/backups/application"
DATE=$(date +%Y%m%d_%H%M%S)

# Backup configuration
tar -czf $BACKUP_DIR/config_$DATE.tar.gz config/

# Backup logs
tar -czf $BACKUP_DIR/logs_$DATE.tar.gz logs/

# Upload to S3
aws s3 cp $BACKUP_DIR/config_$DATE.tar.gz s3://your-backup-bucket/application/
aws s3 cp $BACKUP_DIR/logs_$DATE.tar.gz s3://your-backup-bucket/application/
```

### Recovery Procedures

```bash
#!/bin/bash
# recovery_database.sh

BACKUP_FILE=$1
TEMP_DIR="/tmp/recovery"

# Create recovery environment
mkdir -p $TEMP_DIR
cd $TEMP_DIR

# Download backup from S3
aws s3 cp s3://your-backup-bucket/database/$BACKUP_FILE $BACKUP_FILE

# Restore database
gunzip -c $BACKUP_FILE | docker exec -i postgres-primary psql -U fsl_prod -d fsl_continuum_prod

# Clean up
rm -rf $TEMP_DIR
```

## Performance Optimization

### Database Optimization

```sql
-- PostgreSQL optimization
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET maintenance_work_mem = '64MB';
ALTER SYSTEM SET checkpoint_completion_target = 0.9;
ALTER SYSTEM SET wal_buffers = '16MB';
SELECT pg_reload_conf();
```

### Application Optimization

```yaml
# config/production.yaml
performance:
  connection_pooling: true
  connection_pool_size: 20
  connection_max_overflow: 30
  request_timeout: 30
  response_timeout: 30
  
caching:
  enabled: true
  redis_cache: true
  cache_timeout: 300
  cache_max_size: 1000
  
compression:
  enabled: true
  compression_level: 6
  min_compress_length: 1024
```

### Nginx Optimization

```nginx
# Nginx performance optimization
worker_processes auto;
worker_connections 1024;

events {
    worker_connections 1024;
    multi_accept on;
}

http {
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    
    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
    
    # Client cache
    location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

## Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Check database credentials in .env
   - Verify database is running: `docker exec postgres-primary pg_isready`
   - Check network connectivity: `docker network ls`

2. **SSL Certificate Issues**
   - Verify domain ownership: `nslookup your-domain.com`
   - Check certificate: `openssl s_client -connect your-domain.com:443`
   - Renew certificate: `sudo certbot renew`

3. **High Memory Usage**
   - Monitor memory: `docker stats`
   - Optimize database settings
   - Increase memory limits in docker-compose.yml

4. **Performance Issues**
   - Check load balancer: `curl http://localhost/nginx_status`
   - Monitor application: `curl http://localhost:8080/metrics`
   - Analyze logs: `docker-compose logs -f fsl-app-1`

### Debug Mode

```bash
# Enable debug logging
export FSL_DEBUG=true
export FSL_LOG_LEVEL=debug

# Restart with debug
docker-compose -f docker-compose.prod.yml restart fsl-app-1

# Monitor debug logs
docker-compose -f docker-compose.prod.yml logs -f fsl-app-1
```

---

*Production deployment guide for FSL Continuum - enabling terminal velocity with enterprise-grade deployment.*
