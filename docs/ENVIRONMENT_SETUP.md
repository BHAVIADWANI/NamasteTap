# ONE3TAP - Environment Variables Setup Guide

## Method 1: .env File (Recommended) ✅
Your project is already configured! Just edit the .env file:
`c:\Users\BHAVESH\OneDrive\Documents\ONE3TAP\.env`

## Method 2: Windows Command Prompt (Temporary)
```cmd
# Set for current session only
set DEBUG=False
set SECRET_KEY=your-secret-key
set ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Run Django
python manage.py runserver
```

## Method 3: Windows PowerShell (Temporary)
```powershell
# Set for current session only
$env:DEBUG="False"
$env:SECRET_KEY="your-secret-key"
$env:ALLOWED_HOSTS="yourdomain.com,www.yourdomain.com"

# Run Django
python manage.py runserver
```

## Method 4: Windows System Environment Variables (Permanent)
1. Right-click "This PC" → Properties
2. Click "Advanced system settings"
3. Click "Environment Variables"
4. Under "User variables" click "New"
5. Add variables:
   - Variable name: DEBUG
   - Variable value: False
   - Repeat for SECRET_KEY, ALLOWED_HOSTS, etc.

## Method 5: Production Deployment

### For VPS/Server:
```bash
# Add to ~/.bashrc or ~/.profile
export DEBUG=False
export SECRET_KEY="your-production-secret-key"
export ALLOWED_HOSTS="yourdomain.com,www.yourdomain.com"
export DATABASE_URL="postgresql://user:pass@localhost/db"
```

### For Docker:
```dockerfile
ENV DEBUG=False
ENV SECRET_KEY=your-secret-key
ENV ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

### For Heroku:
```bash
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=your-secret-key
heroku config:set ALLOWED_HOSTS=yourapp.herokuapp.com
```

### For Railway/Vercel:
Add environment variables in the dashboard:
- DEBUG=False
- SECRET_KEY=your-secret-key
- ALLOWED_HOSTS=yourdomain.com

## 🔐 Important Environment Variables for ONE3TAP:

### Required:
- `SECRET_KEY`: Django secret key (minimum 50 characters)
- `DEBUG`: True for development, False for production
- `ALLOWED_HOSTS`: Comma-separated list of allowed domains

### Optional:
- `DATABASE_URL`: PostgreSQL connection string for production
- `EMAIL_HOST_USER`: Email for sending notifications
- `EMAIL_HOST_PASSWORD`: Email app password
- `REDIS_URL`: Redis cache URL for production

## 🚀 Quick Start:
1. Edit your .env file with actual values
2. Keep DEBUG=True for development
3. Set DEBUG=False only for production deployment
4. Generate a new SECRET_KEY for production

## 🔍 Testing Environment Variables:
```bash
python manage.py check --deploy
```

## ✅ Your .env file is already set up and working!
Just update the values in: c:\Users\BHAVESH\OneDrive\Documents\ONE3TAP\.env
