# TapOne3 - Production Deployment Guide

## Environment Setup

1. **Environment Variables** (create .env file):
```bash
DEBUG=False
SECRET_KEY=your-super-secret-key-here-at-least-50-characters-long
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://username:password@localhost:5432/tapone3_db
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
REDIS_URL=redis://127.0.0.1:6379/1
```

2. **Database Migration**:
```bash
python manage.py migrate
python manage.py createsuperuser
```

3. **Static Files**:
```bash
python manage.py collectstatic
```

4. **Production Server** (using Gunicorn):
```bash
gunicorn namaste_tap.wsgi:application --bind 0.0.0.0:8000
```

## Security Checklist

- ✅ SECRET_KEY is secure and unique
- ✅ DEBUG=False in production
- ✅ HTTPS enforced (SECURE_SSL_REDIRECT=True)
- ✅ HSTS enabled (SECURE_HSTS_SECONDS=31536000)
- ✅ Secure cookies enabled
- ✅ Content security headers configured
- ✅ Database credentials secured
- ✅ Static files properly configured

## Performance Optimization

- Redis caching enabled
- Static files served via CDN (recommended)
- Database connection pooling
- Compressed static files
- Optimized images

## Monitoring

- Logging configured (logs/django.log)
- Error tracking (configure Sentry in production)
- Performance monitoring
- Health checks
