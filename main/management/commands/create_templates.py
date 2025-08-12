from django.core.management.base import BaseCommand
from main.models import CompanyTemplate


class Command(BaseCommand):
    help = 'Create default company templates'

    def handle(self, *args, **options):
        # Corporate Template
        corporate_html = '''{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ card.display_name }} - {{ card.company_name|default:"Professional" }} Digital Card</title>
    
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    
    <!-- Company Template CSS -->
    <link rel="stylesheet" href="{% static css_path %}">
    
    <style>
        :root {
            --primary-color: {{ primary_color|default:"#0088FF" }};
            --secondary-color: {{ secondary_color|default:"#00D4FF" }};
            --font-family: {{ font_family|default:"Inter, sans-serif" }};
        }
        
        body {
            font-family: var(--font-family);
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            margin: 0;
            padding: 20px;
        }
    </style>
</head>
<body>
    <div class="container-fluid">
        <div class="row justify-content-center">
            <div class="col-lg-5 col-md-7 col-sm-9">
                <div class="corporate-card">
                    <!-- Card content here -->
                    <div class="card-header-section">
                        <div class="company-logo-section">
                            {% if card.profile_image %}
                                <img src="{{ card.profile_image.url }}" alt="{{ card.display_name }}" class="profile-image">
                            {% else %}
                                <div class="profile-placeholder">
                                    <i class="fas fa-user"></i>
                                </div>
                            {% endif %}
                        </div>
                        
                        <div class="card-info">
                            <h1 class="person-name">{{ card.display_name }}</h1>
                            {% if card.job_title %}
                                <p class="job-title">{{ card.job_title }}</p>
                            {% endif %}
                            {% if card.company_name %}
                                <p class="company-name">
                                    <i class="fas fa-building"></i>
                                    {{ card.company_name }}
                                </p>
                            {% endif %}
                        </div>
                    </div>
                    
                    <!-- Rest of the template content -->
                    <!-- Contact Information, Bio, Social Links, etc. -->
                </div>
            </div>
        </div>
    </div>
    
    <!-- Scripts -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="{% static js_path %}"></script>
    
    <script>
        window.cardData = {
            name: "{{ card.display_name|escapejs }}",
            title: "{{ card.job_title|escapejs }}",
            company: "{{ card.company_name|escapejs }}",
            email: "{{ card.email|escapejs }}",
            phone: "{{ card.phone|escapejs }}",
            website: "{{ card.website|escapejs }}",
            location: "{{ card.location|escapejs }}",
            url: "{{ request.build_absolute_uri }}"
        };
    </script>
</body>
</html>'''

        corporate_css = '''/* Corporate Template Styles - Simplified for command */
.corporate-card {
    background: linear-gradient(145deg, #ffffff 0%, #f8f9fc 100%);
    border-radius: 20px;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    overflow: hidden;
    max-width: 500px;
    margin: 0 auto;
    position: relative;
}

.corporate-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
}

.card-header-section {
    text-align: center;
    padding: 40px 30px 20px;
    background: linear-gradient(135deg, var(--primary-color)0a, var(--secondary-color)0a);
}

.profile-image {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    object-fit: cover;
    border: 4px solid var(--primary-color);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    margin-bottom: 20px;
}

.profile-placeholder {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 20px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.person-name {
    font-size: 28px;
    font-weight: 700;
    color: #2c3e50;
    margin-bottom: 8px;
    letter-spacing: -0.5px;
}'''

        corporate_js = '''// Corporate Template JavaScript - Simplified
function saveContact() {
    alert('Save contact functionality');
}

function shareCard() {
    if (navigator.share) {
        navigator.share({
            title: document.title,
            url: window.location.href
        });
    } else {
        alert('Share functionality');
    }
}

function generateQR() {
    alert('QR Code functionality');
}'''

        # Create Corporate Template
        corporate_template, created = CompanyTemplate.objects.get_or_create(
            name='Corporate Professional',
            defaults={
                'slug': 'corporate',
                'template_type': 'corporate',
                'html_template': corporate_html,
                'css_content': corporate_css,
                'js_content': corporate_js,
                'primary_color': '#0088FF',
                'secondary_color': '#00D4FF',
                'font_family': 'Inter, sans-serif',
                'description': 'Professional corporate template with clean design',
                'is_active': True,
                'is_premium': False,
            }
        )

        if created:
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created Corporate template')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'Corporate template already exists')
            )

        # Create more templates...
        self.create_creative_template()
        self.create_minimal_template()

    def create_creative_template(self):
        """Create creative template"""
        creative_template, created = CompanyTemplate.objects.get_or_create(
            name='Creative Designer',
            defaults={
                'slug': 'creative',
                'template_type': 'creative',
                'html_template': '<!-- Creative HTML Template -->',
                'css_content': '/* Creative CSS */\nbody { background: linear-gradient(45deg, #ff6b6b, #4ecdc4); }',
                'js_content': '// Creative JS',
                'primary_color': '#FF6B6B',
                'secondary_color': '#4ECDC4',
                'font_family': 'Poppins, sans-serif',
                'description': 'Creative template for designers and artists',
                'is_active': True,
                'is_premium': True,
            }
        )

        if created:
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created Creative template')
            )

    def create_minimal_template(self):
        """Create minimal template"""
        minimal_template, created = CompanyTemplate.objects.get_or_create(
            name='Minimal Clean',
            defaults={
                'slug': 'minimal',
                'template_type': 'minimal',
                'html_template': '<!-- Minimal HTML Template -->',
                'css_content': '/* Minimal CSS */\nbody { background: #f8f9fa; color: #333; }',
                'js_content': '// Minimal JS',
                'primary_color': '#333333',
                'secondary_color': '#666666',
                'font_family': 'Source Sans Pro, sans-serif',
                'description': 'Clean minimal template for professionals',
                'is_active': True,
                'is_premium': False,
            }
        )

        if created:
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created Minimal template')
            )
