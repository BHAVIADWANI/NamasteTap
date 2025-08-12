#!/bin/bash

# entrypoint.sh - Docker entrypoint script for ONE3TAP Django application

set -e

# Function to wait for database
wait_for_db() {
    echo "Waiting for PostgreSQL..."
    
    # Extract database connection details from DATABASE_URL
    if [ -n "$DATABASE_URL" ]; then
        # Parse DATABASE_URL - format: postgresql://user:pass@host:port/db
        DB_HOST=$(echo $DATABASE_URL | sed -n 's/.*@\([^:]*\):.*/\1/p')
        DB_PORT=$(echo $DATABASE_URL | sed -n 's/.*:\([0-9]*\)\/.*/\1/p')
        
        if [ -n "$DB_HOST" ] && [ -n "$DB_PORT" ]; then
            while ! nc -z $DB_HOST $DB_PORT; do
                echo "PostgreSQL is unavailable - sleeping"
                sleep 1
            done
            echo "PostgreSQL is up - continuing..."
        fi
    fi
}

# Function to wait for Redis (if configured)
wait_for_redis() {
    if [ -n "$REDIS_URL" ]; then
        echo "Waiting for Redis..."
        REDIS_HOST=$(echo $REDIS_URL | sed -n 's/redis:\/\/\([^:]*\):.*/\1/p')
        REDIS_PORT=$(echo $REDIS_URL | sed -n 's/.*:\([0-9]*\)\/.*/\1/p')
        
        if [ -n "$REDIS_HOST" ] && [ -n "$REDIS_PORT" ]; then
            while ! nc -z $REDIS_HOST $REDIS_PORT; do
                echo "Redis is unavailable - sleeping"
                sleep 1
            done
            echo "Redis is up - continuing..."
        fi
    fi
}

# Function to run Django setup
django_setup() {
    echo "Running Django setup..."
    
    # Create logs directory if it doesn't exist
    mkdir -p /app/logs
    
    # Run database migrations
    echo "Running database migrations..."
    python manage.py migrate --noinput
    
    # Create company templates
    echo "Creating default company templates..."
    python manage.py create_templates || echo "Templates already exist or command failed"
    
    # Collect static files
    echo "Collecting static files..."
    python manage.py collectstatic --noinput --clear
    
    # Create superuser if specified
    if [ "$DJANGO_SUPERUSER_USERNAME" ] && [ "$DJANGO_SUPERUSER_EMAIL" ] && [ "$DJANGO_SUPERUSER_PASSWORD" ]; then
        echo "Creating superuser..."
        python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists():
    User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD')
    print('Superuser created successfully')
else:
    print('Superuser already exists')
EOF
    fi
}

# Main execution
echo "Starting ONE3TAP application..."

# Wait for dependencies
wait_for_db
wait_for_redis

# Run Django setup
django_setup

echo "Setup complete. Starting application with: $@"

# Execute the main command
exec "$@"
