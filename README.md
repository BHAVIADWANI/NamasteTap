# NamasteTap Django Project

A Django web application project.

## Setup Instructions

1. **Install Python dependencies:**
   ```
   pip install -r requirements.txt
   ```

2. **Run database migrations:**
   ```
   python manage.py migrate
   ```

3. **Start the development server:**
   ```
   python manage.py runserver
   ```

4. **Access the application:**
   Open your browser and navigate to `http://127.0.0.1:8000/`

## Project Structure

- `namaste_tap/` - Main Django project configuration
- `main/` - Main Django application
- `manage.py` - Django management script
- `requirements.txt` - Python dependencies
- `db.sqlite3` - SQLite database file

## Development

### Creating a new Django app
```
python manage.py startapp app_name
```

### Creating database migrations
```
python manage.py makemigrations
python manage.py migrate
```

### Creating a superuser
```
python manage.py createsuperuser
```

## Django Admin

Access the Django admin interface at `http://127.0.0.1:8000/admin/` after creating a superuser account.
