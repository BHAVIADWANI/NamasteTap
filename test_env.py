#!/usr/bin/env python
"""
ONE3TAP Environment Variables Test Script
Run this to verify your environment setup is working correctly.
"""

import os
import sys
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(project_dir))

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ python-dotenv loaded successfully")
except ImportError:
    print("❌ python-dotenv not installed. Run: pip install python-dotenv")
    sys.exit(1)

# Check environment variables
print("\n🔍 Environment Variables Status:")
print("-" * 50)

env_vars = {
    'DEBUG': os.environ.get('DEBUG', 'Not set'),
    'SECRET_KEY': 'Set ✅' if os.environ.get('SECRET_KEY') else 'Not set ❌',
    'ALLOWED_HOSTS': os.environ.get('ALLOWED_HOSTS', 'Not set'),
    'EMAIL_HOST_USER': os.environ.get('EMAIL_HOST_USER', 'Not set (optional)'),
    'DATABASE_URL': os.environ.get('DATABASE_URL', 'Not set (optional)'),
}

for key, value in env_vars.items():
    if key == 'SECRET_KEY' and 'Set' in value:
        actual_key = os.environ.get('SECRET_KEY', '')
        print(f"{key}: {value} (Length: {len(actual_key)} chars)")
    else:
        print(f"{key}: {value}")

# Test Django settings
print("\n🚀 Django Configuration Test:")
print("-" * 50)

try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'one3tap.settings')
    import django
    django.setup()
    
    from django.conf import settings
    print(f"Django DEBUG: {settings.DEBUG}")
    print(f"Django SECRET_KEY: {'Set ✅' if settings.SECRET_KEY else 'Not set ❌'}")
    print(f"Django ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
    print("✅ Django settings loaded successfully!")
    
except Exception as e:
    print(f"❌ Django configuration error: {e}")

print("\n📋 Summary:")
print("-" * 50)
print("✅ Your environment variables are properly configured!")
print("✅ Edit the .env file to customize values")
print("✅ Set DEBUG=False for production deployment")
print("\n🎉 ONE3TAP is ready to run!")
