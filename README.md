# TapOne3 - Smart NFC Business Cards Platform

🚀 **One Tap, Three Connections** - The Future of Business Networking

A Django web application for managing NFC-enabled digital business cards with role-based access control and comprehensive user management.

## ✨ Features

### 🔐 **User Management**
- Custom user model with Admin/Standard user types
- Secure authentication with email/username login
- Profile management with contact information
- User dashboard with analytics

### 🎨 **Smart Interface**
- Modern, responsive design with TapOne3 branding
- Role-based dashboards (Admin vs Standard users)
- Real-time form validation
- Mobile-friendly NFC-focused UI

### 👨‍💼 **Admin Features**
- User management and monitoring
- Detailed user profiles and statistics
- Pagination and search functionality
- Admin dashboard with insights

### 🎯 **NFC Integration Ready**
- Built for NFC business card functionality
- Three profile system (Professional/Personal/Creative)
- Analytics tracking foundation
- Custom design capabilities

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- pip
- Git

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/BHAVIADWANI/NamasteTap.git
   cd NamasteTap
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Run database migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

7. **Access the application:**
   Open your browser and navigate to `http://127.0.0.1:8000/`

## 📁 Project Structure

```
TapOne3/
├── namaste_tap/          # Main Django project configuration
│   ├── settings.py       # Django settings with environment support
│   ├── urls.py          # URL routing
│   └── wsgi.py          # WSGI configuration
├── main/                # Main Django application
│   ├── models.py        # CustomUser and UserProfile models
│   ├── views.py         # Authentication and dashboard views
│   ├── forms.py         # Custom forms with validation
│   ├── admin.py         # Admin interface configuration
│   ├── urls.py          # App URL patterns
│   └── tests.py         # Comprehensive test suite
├── templates/           # HTML templates
│   ├── base.html        # Base template with TapOne3 branding
│   ├── home.html        # Landing page
│   ├── about.html       # About page
│   ├── services.html    # Services page
│   ├── contact.html     # Contact page
│   ├── auth/           # Authentication templates
│   │   ├── login.html
│   │   └── signup.html
│   └── dashboard/      # Dashboard templates
│       ├── admin_dashboard.html
│       ├── user_dashboard.html
│       ├── profile.html
│       ├── manage_users.html
│       └── user_detail.html
├── static/             # Static files
│   ├── css/
│   │   └── style.css   # TapOne3 styling with NFC theme
│   ├── js/
│   │   └── main.js     # Interactive JavaScript
│   └── images/         # Image assets
├── manage.py           # Django management script
├── requirements.txt    # Python dependencies
├── .env.example       # Environment variables template
└── README.md          # This file
```

## 🎨 Design & Branding

### Color Scheme
- **Primary**: Deep Blue (#1E3A8A) - Trust, Technology
- **Secondary**: Electric Green (#10B981) - Innovation, Action  
- **Accent**: Silver (#94A3B8) - Premium, Tech

### Typography
- **Font**: Poppins (Google Fonts)
- **Style**: Modern, clean, tech-forward

### Icons
- **NFC Symbol**: WiFi icon with pulse animation
- **FontAwesome**: Comprehensive icon library

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Run all tests
python manage.py test

# Run specific test categories
python manage.py test main.tests.CustomUserModelTests
python manage.py test main.tests.ViewsTests
python manage.py test main.tests.IntegrationTests

# Run with coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

## 🔧 Development

### Creating a new Django app
```bash
python manage.py startapp app_name
```

### Creating database migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Collecting static files
```bash
python manage.py collectstatic
```

### Running development server with different settings
```bash
python manage.py runserver --settings=namaste_tap.settings_dev
```

## 🚢 Production Deployment

### Environment Setup
1. Set `DEBUG=False` in production
2. Configure proper `SECRET_KEY`
3. Set up PostgreSQL database
4. Configure static file serving (WhiteNoise or S3)
5. Set up proper logging and monitoring

### Dependencies for Production
```bash
pip install gunicorn psycopg2-binary whitenoise
```

### Sample Production Commands
```bash
# Database setup
python manage.py migrate --settings=namaste_tap.settings_prod

# Static files
python manage.py collectstatic --settings=namaste_tap.settings_prod

# Run with Gunicorn
gunicorn namaste_tap.wsgi:application
```

## 🔮 Future Features

### 🏷️ **TapOne3 Pro**
- Physical NFC card integration
- Custom card design studio
- Advanced analytics dashboard
- CRM integrations

### 🏢 **TapOne3 Teams**
- Corporate account management
- Team member management
- Bulk card ordering
- Company branding

### 📊 **TapOne3 Analytics**
- Contact interaction tracking
- Networking insights
- ROI analytics
- Export capabilities

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

- **Documentation**: [Coming Soon]
- **Issues**: [GitHub Issues](https://github.com/BHAVIADWANI/NamasteTap/issues)
- **Email**: support@tapone3.com

## 🎯 Vision

**TapOne3** aims to revolutionize business networking by making it as simple as a single tap. Our platform bridges the physical and digital worlds, creating meaningful connections in the age of NFC technology.

---

**Built with ❤️ for the future of networking**

*TapOne3 - One Tap, Three Connections*

## Django Admin

Access the Django admin interface at `http://127.0.0.1:8000/admin/` after creating a superuser account.
