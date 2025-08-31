#!/bin/bash

# ONE3TAP Deployment Script
# This script sets up the necessary directories and runs Django commands

echo "🚀 Starting ONE3TAP deployment..."

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p logs
mkdir -p media
mkdir -p static
mkdir -p staticfiles

# Set proper permissions
echo "🔒 Setting permissions..."
chmod 755 logs media static staticfiles

# Install/update dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Run Django management commands
echo "🔄 Running Django migrations..."
python manage.py migrate

echo "📊 Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser if it doesn't exist
echo "👤 Creating superuser..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
import os
User = get_user_model()
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@one3tap.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f'Superuser {username} created successfully!')
else:
    print(f'Superuser {username} already exists.')
"

echo "✅ Deployment completed successfully!"
echo "🌐 Your ONE3TAP application is ready to run!"
echo ""
echo "To start the server:"
echo "  Development: python manage.py runserver 0.0.0.0:8000"
echo "  Production:  gunicorn one3tap.wsgi:application --bind 0.0.0.0:8000"
echo ""
echo "Admin panel: http://your-server:8000/admin/"
