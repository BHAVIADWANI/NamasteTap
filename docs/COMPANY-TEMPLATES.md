# Company Template System Documentation

## Overview
The ONE3TAP platform now supports dynamic company-specific digital visiting card templates. Each company can have unique HTML, CSS, and JavaScript files organized in separate folders, allowing for complete customization of the digital card appearance and functionality.

## Architecture

### 1. Database Model: CompanyTemplate
- **Purpose**: Stores template metadata and content
- **Key Fields**:
  - `name`: Template display name
  - `slug`: URL-friendly identifier (auto-generated)
  - `template_type`: Category (corporate, creative, minimal, etc.)
  - `html_template`: Complete HTML template content
  - `css_content`: CSS styling content
  - `js_content`: JavaScript functionality
  - `primary_color`, `secondary_color`: Brand colors
  - `font_family`: Typography settings
  - `is_active`, `is_premium`: Status flags

### 2. File Organization
```
templates/
└── company_cards/
    ├── corporate/
    │   └── card_template.html
    ├── creative/
    │   └── card_template.html
    └── minimal/
        └── card_template.html

static/
└── company_templates/
    ├── corporate/
    │   ├── css/
    │   │   └── style.css
    │   └── js/
    │       └── script.js
    ├── creative/
    │   ├── css/
    │   └── js/
    └── minimal/
        ├── css/
        └── js/
```

### 3. Digital Card Integration
- **DigitalCard Model**: Added `company_template` foreign key
- **Template Selection**: Users can choose templates for their cards
- **Dynamic Rendering**: Cards render using selected template or default

## Features Implemented

### 1. Template Management
- **Admin Interface**: Full CRUD operations for templates
- **Template Creation**: Automatic file generation when saving
- **Preview System**: Live preview with sample data
- **Gallery View**: Browse all available templates

### 2. User Interface
- **Template Selection**: User-friendly template picker
- **Live Preview**: See templates before applying
- **Template Gallery**: Browse all available options
- **Color Customization**: Visual color indicators

### 3. Template Types
- **Corporate**: Professional business design
- **Creative**: Artistic and colorful design
- **Minimal**: Clean and simple design
- **Custom**: Fully customizable templates

### 4. Advanced Features
- **Responsive Design**: All templates mobile-friendly
- **Social Integration**: Built-in social media links
- **Analytics Tracking**: View counting and user analytics
- **vCard Export**: Contact information download
- **QR Code Generation**: Dynamic QR codes
- **Share Functionality**: Native and fallback sharing

## Usage Guide

### For Administrators

#### Creating New Templates
```bash
# Access Django Admin
python manage.py createsuperuser
# Navigate to /admin/main/companytemplate/

# Or use management command
python manage.py create_templates
```

#### Template Structure
```html
<!-- HTML Template Structure -->
{% load static %}
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="{% static css_path %}">
    <style>
        :root {
            --primary-color: {{ primary_color }};
            --secondary-color: {{ secondary_color }};
            --font-family: {{ font_family }};
        }
    </style>
</head>
<body>
    <!-- Template content using card data -->
    <h1>{{ card.display_name }}</h1>
    <p>{{ card.job_title }}</p>
    <!-- ... -->
    <script src="{% static js_path %}"></script>
</body>
</html>
```

### For Users

#### Selecting Templates
1. Navigate to card dashboard
2. Click "Select Template" for any card
3. Preview templates before applying
4. Choose and apply desired template

#### Available Template Variables
```javascript
// Card data available in templates
{
    card: {
        display_name, job_title, company_name,
        email, phone, website, location, bio,
        profile_image, social links, etc.
    },
    template: {
        name, description, colors, etc.
    },
    primary_color, secondary_color, font_family,
    css_path, js_path, social_links
}
```

## API Endpoints

### Template Management
- `GET /templates/gallery/` - Browse all templates
- `GET /templates/preview/{id}/` - Preview template
- `POST /card/{slug}/select-template/` - Apply template
- `GET /api/template/{id}/` - Get template info (AJAX)

### Card Rendering
- `GET /card/{slug}/` - View digital card (uses template)

## Development

### Adding New Template Types
1. Add to `TEMPLATE_TYPE_CHOICES` in models.py
2. Create template files in appropriate directories
3. Add template data via admin or management command

### Customizing Templates
```python
# Create template via code
template = CompanyTemplate.objects.create(
    name='Tech Startup',
    template_type='startup',
    html_template='<!-- HTML content -->',
    css_content='/* CSS styles */',
    js_content='// JavaScript code',
    primary_color='#FF6B35',
    secondary_color='#F7931E'
)
```

### Template Variables Reference
```django
<!-- Available in all templates -->
{{ card.display_name }}        <!-- Person's name -->
{{ card.job_title }}          <!-- Job position -->
{{ card.company_name }}       <!-- Company name -->
{{ card.email }}              <!-- Email address -->
{{ card.phone }}              <!-- Phone number -->
{{ card.website }}            <!-- Website URL -->
{{ card.location }}           <!-- Location/address -->
{{ card.bio }}                <!-- Biography -->
{{ card.profile_image.url }}  <!-- Profile image -->
{{ social_links }}            <!-- Social media links -->
{{ primary_color }}           <!-- Template primary color -->
{{ secondary_color }}         <!-- Template secondary color -->
{{ font_family }}             <!-- Template font -->
{{ css_path }}                <!-- CSS file path -->
{{ js_path }}                 <!-- JS file path -->
```

## Deployment Considerations

### Docker Support
- Dockerfile included for containerization
- Static file collection handled automatically
- Template files created on container startup

### File Permissions
- Ensure write permissions for template directories
- Static files properly collected and served
- Media uploads configured correctly

### Performance
- Templates cached after first load
- Static files served via CDN in production
- Database queries optimized with select_related

## Future Enhancements

### Planned Features
1. **Template Marketplace**: User-submitted templates
2. **Theme Customizer**: Real-time color/font editing
3. **Template Analytics**: Usage statistics and performance
4. **Bulk Template Management**: Apply templates to multiple cards
5. **Template Versioning**: Track template changes over time
6. **Company Branding**: Automatic company-specific templates
7. **Integration APIs**: Third-party template sources

### Technical Improvements
1. **Template Caching**: Redis-based template caching
2. **CDN Integration**: Template assets via CDN
3. **Progressive Loading**: Lazy-load template assets
4. **Template Validation**: Automated template testing
5. **Backup System**: Template content backup and restore

## Troubleshooting

### Common Issues
1. **Template Not Loading**: Check file paths and permissions
2. **CSS Not Applied**: Verify static file collection
3. **JavaScript Errors**: Check console for syntax errors
4. **Template Selection**: Ensure template is active and accessible

### Debug Mode
```python
# Enable debug logging for templates
LOGGING = {
    'loggers': {
        'main.template_views': {
            'level': 'DEBUG',
            'handlers': ['console'],
        }
    }
}
```

This system provides a robust foundation for company-specific digital visiting card templates while maintaining flexibility for future enhancements.
