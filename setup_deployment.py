#!/usr/bin/env python3
"""
ONE3TAP Deployment Setup Script
This script creates necessary directories and prepares the Django application for deployment.
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"⏳ {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def create_directories():
    """Create necessary directories for the Django application."""
    directories = ['logs', 'media', 'static', 'staticfiles']
    print("📁 Creating directories...")
    
    for directory in directories:
        dir_path = Path(directory)
        dir_path.mkdir(exist_ok=True)
        print(f"   ✓ {directory}/")
    
    # Create subdirectories in static if needed
    static_subdirs = ['css', 'js', 'images', 'company_templates']
    static_path = Path('static')
    for subdir in static_subdirs:
        subdir_path = static_path / subdir
        subdir_path.mkdir(exist_ok=True)
        print(f"   ✓ static/{subdir}/")
    
    print("✅ Directories created successfully")

def set_permissions():
    """Set proper permissions for directories (Unix/Linux only)."""
    if os.name != 'nt':  # Not Windows
        directories = ['logs', 'media', 'static', 'staticfiles']
        print("🔒 Setting permissions...")
        
        for directory in directories:
            if Path(directory).exists():
                os.chmod(directory, 0o755)
                print(f"   ✓ {directory}/ - 755")
        
        print("✅ Permissions set successfully")
    else:
        print("ℹ️  Skipping permission setting on Windows")

def main():
    """Main deployment setup function."""
    print("🚀 ONE3TAP Deployment Setup")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not Path('manage.py').exists():
        print("❌ Error: manage.py not found. Please run this script from the Django project root.")
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Set permissions (Unix/Linux only)
    set_permissions()
    
    # Install dependencies
    if Path('requirements.txt').exists():
        run_command('pip install -r requirements.txt', 'Installing dependencies')
    
    # Run migrations
    run_command('python manage.py migrate', 'Running database migrations')
    
    # Collect static files
    run_command('python manage.py collectstatic --noinput', 'Collecting static files')
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Update your .env file with production settings")
    print("2. Configure your web server (Nginx/Apache)")
    print("3. Start your Django application:")
    print("   Development: python manage.py runserver 0.0.0.0:8000")
    print("   Production:  gunicorn one3tap.wsgi:application --bind 0.0.0.0:8000")
    print("\n🌐 Access your application:")
    print("   Frontend: http://your-server:8000/")
    print("   Admin:    http://your-server:8000/admin/")

if __name__ == '__main__':
    main()
