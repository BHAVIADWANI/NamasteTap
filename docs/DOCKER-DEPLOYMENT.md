# ONE3TAP Docker Deployment Guide

## Overview
This guide covers deploying the ONE3TAP Django application using Docker and Docker Compose for both development and production environments.

## Prerequisites

### Required Software
- Docker Engine 20.10+
- Docker Compose 2.0+
- Git (for cloning the repository)

### System Requirements
- **Memory**: Minimum 2GB RAM (4GB+ recommended for production)
- **Storage**: Minimum 10GB free space
- **CPU**: 2+ cores recommended

## Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/BHAVIADWANI/ONE3TAP.git
cd ONE3TAP
```

### 2. Environment Configuration
Copy and customize the environment file:
```bash
cp .env.example .env
# Edit .env with your specific configuration
```

### 3. Development Deployment
```bash
# Start development environment
docker-compose -f docker-compose.dev.yml up --build

# Access the application at: http://localhost:8000
```

### 4. Production Deployment
```bash
# Start production environment
docker-compose up --build -d

# Access the application at: http://localhost (via Nginx)
```

## Detailed Configuration

### Environment Variables (.env)

#### Required Variables
```bash
# Django Core
SECRET_KEY=your-super-secret-key-here-50-characters-minimum
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,localhost

# Database
DATABASE_URL=postgresql://username:password@db:5432/database_name

# Security (Production Only)
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

#### Optional Variables
```bash
# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password

# Redis Cache
REDIS_URL=redis://redis:6379/1

# Superuser Creation (Optional)
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@yourdomain.com
DJANGO_SUPERUSER_PASSWORD=secure_password
```

## Deployment Options

### Option 1: Development Environment
Best for: Local development, testing, debugging

```bash
# Start development environment
docker-compose -f docker-compose.dev.yml up --build

# Features:
# - Hot reload for code changes
# - Debug mode enabled
# - SQLite database (optional)
# - Direct Django development server
```

### Option 2: Production Environment
Best for: Production deployment, staging

```bash
# Start production environment
docker-compose up --build -d

# Features:
# - Nginx reverse proxy
# - PostgreSQL database
# - Redis caching
# - Gunicorn WSGI server
# - SSL/HTTPS support (configurable)
```

### Option 3: Production with SSL
For HTTPS deployment:

1. **Obtain SSL certificates**:
   ```bash
   # Using Let's Encrypt (example)
   certbot certonly --webroot -w /var/www/html -d yourdomain.com
   ```

2. **Place certificates**:
   ```bash
   mkdir ssl
   cp /path/to/your/certificate.crt ssl/
   cp /path/to/your/private.key ssl/
   ```

3. **Update nginx.conf**: Uncomment HTTPS server block

4. **Deploy**:
   ```bash
   docker-compose up --build -d
   ```

## Docker Commands

### Basic Operations
```bash
# Build and start all services
docker-compose up --build

# Start in background (detached mode)
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f web

# Execute commands in container
docker-compose exec web python manage.py shell
```

### Database Operations
```bash
# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Create templates
docker-compose exec web python manage.py create_templates

# Collect static files
docker-compose exec web python manage.py collectstatic --noinput
```

### Backup and Restore
```bash
# Backup database
docker-compose exec db pg_dump -U one3tap_user one3tap_db > backup.sql

# Restore database
docker-compose exec -T db psql -U one3tap_user one3tap_db < backup.sql

# Backup volumes
docker run --rm -v one3tap_postgres_data:/data -v $(pwd):/backup alpine tar czf /backup/postgres_backup.tar.gz -C /data .
```

## Monitoring and Maintenance

### Health Checks
```bash
# Check service status
docker-compose ps

# Check application health
curl -f http://localhost:8000/ || echo "Application is down"

# Database connection test
docker-compose exec web python manage.py dbshell
```

### Logs Management
```bash
# View application logs
docker-compose logs -f web

# View database logs
docker-compose logs -f db

# View Nginx logs
docker-compose logs -f nginx

# View all logs
docker-compose logs -f
```

### Performance Monitoring
```bash
# Container resource usage
docker stats

# View container processes
docker-compose top

# Database performance
docker-compose exec db psql -U one3tap_user -d one3tap_db -c "SELECT * FROM pg_stat_activity;"
```

## Scaling and Performance

### Horizontal Scaling
```yaml
# docker-compose.yml
services:
  web:
    deploy:
      replicas: 3
    # ... other configuration
```

### Load Balancing with Nginx
```nginx
upstream django {
    server web_1:8000;
    server web_2:8000;
    server web_3:8000;
}
```

### Database Optimization
```bash
# Increase PostgreSQL performance
docker-compose exec db psql -U one3tap_user -d one3tap_db -c "
    ALTER SYSTEM SET shared_buffers = '256MB';
    ALTER SYSTEM SET effective_cache_size = '1GB';
    SELECT pg_reload_conf();
"
```

## Security Best Practices

### 1. Environment Security
- Never commit `.env` file to version control
- Use strong, unique passwords
- Regularly rotate secrets
- Use environment-specific configurations

### 2. Container Security
```bash
# Run containers as non-root user (already configured)
# Limit container capabilities
# Use read-only filesystems where possible
# Regular security updates
```

### 3. Network Security
```bash
# Use internal networks
# Limit exposed ports
# Implement rate limiting
# Use HTTPS in production
```

## Troubleshooting

### Common Issues

#### 1. Database Connection Errors
```bash
# Check database status
docker-compose exec db pg_isready -U one3tap_user

# Reset database
docker-compose down -v
docker-compose up -d db
docker-compose exec web python manage.py migrate
```

#### 2. Static Files Not Loading
```bash
# Collect static files
docker-compose exec web python manage.py collectstatic --clear --noinput

# Check volume mounts
docker-compose exec nginx ls -la /app/staticfiles/
```

#### 3. Permission Issues
```bash
# Fix file permissions
docker-compose exec web chown -R appuser:appuser /app
```

#### 4. Memory Issues
```bash
# Check container memory usage
docker stats

# Increase memory limits in docker-compose.yml
services:
  web:
    deploy:
      resources:
        limits:
          memory: 1G
```

### Debug Mode
```bash
# Enable debug mode temporarily
docker-compose exec web python manage.py shell
# In shell: settings.DEBUG = True

# View detailed error logs
docker-compose logs --tail=100 web
```

## Backup Strategy

### Automated Backups
```bash
#!/bin/bash
# backup.sh - Automated backup script

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/one3tap"

# Create backup directory
mkdir -p $BACKUP_DIR

# Database backup
docker-compose exec -T db pg_dump -U one3tap_user one3tap_db > $BACKUP_DIR/db_$DATE.sql

# Media files backup
docker run --rm -v one3tap_media_volume:/data -v $BACKUP_DIR:/backup alpine tar czf /backup/media_$DATE.tar.gz -C /data .

# Cleanup old backups (keep last 7 days)
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
```

### Restore Procedure
```bash
# Stop application
docker-compose down

# Restore database
docker-compose up -d db
docker-compose exec -T db psql -U one3tap_user one3tap_db < backup/db_20240812_120000.sql

# Restore media files
docker run --rm -v one3tap_media_volume:/data -v $(pwd)/backup:/backup alpine tar xzf /backup/media_20240812_120000.tar.gz -C /data

# Start application
docker-compose up -d
```

## Production Deployment Checklist

- [ ] Environment variables configured
- [ ] SSL certificates installed
- [ ] Database properly configured
- [ ] Static files serving configured
- [ ] Backup strategy implemented
- [ ] Monitoring setup
- [ ] Security headers configured
- [ ] Rate limiting enabled
- [ ] Log rotation configured
- [ ] Health checks implemented

## Support and Maintenance

### Regular Maintenance Tasks
1. **Weekly**: Check logs, monitor performance
2. **Monthly**: Update dependencies, security patches
3. **Quarterly**: Full system backup, disaster recovery test

### Updates and Patches
```bash
# Update application
git pull origin main
docker-compose down
docker-compose up --build -d

# Update base images
docker-compose pull
docker-compose up --build -d
```

This comprehensive Docker deployment setup provides a robust, scalable, and secure foundation for hosting the ONE3TAP Django application.
