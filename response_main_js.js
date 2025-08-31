// TapOne3 - Futuristic NFC Business Cards Platform
// Enhanced JavaScript Functionality

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initAnimations();
    initFormEnhancements();
    initNavigation();
    initParticleEffects();
    initScrollEffects();
    initMessaging();
    initModalEffects();
    initThemeToggle();
    
    console.log('🚀 TapOne3 Platform Initialized');
});

// Smooth Animations and Transitions
function initAnimations() {
    // Add intersection observer for scroll animations
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-up');
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });

    // Observe elements for animation
    document.querySelectorAll('.card, .feature-card, .dashboard-card').forEach(el => {
        observer.observe(el);
    });

    // Add hover effects to buttons
    document.querySelectorAll('.btn').forEach(btn => {
        btn.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-3px)';
        });
        
        btn.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
}

// Enhanced Form Functionality
function initFormEnhancements() {
    // Floating label effects (works with .form-group > label + .form-control)
    document.querySelectorAll('.form-group .form-control').forEach(input => {
        const group = input.closest('.form-group');
        const label = group ? group.querySelector('label') : input.previousElementSibling;

        function applyFocus() {
            if (group) group.classList.add('focused');
            if (label) label.style.transform = 'translateY(-18px) scale(0.85)';
        }

        function removeFocus() {
            if (!input.value.trim()) {
                if (group) group.classList.remove('focused');
                if (label) label.style.transform = 'translateY(0) scale(1)';
            }
        }

        input.addEventListener('focus', applyFocus);
        input.addEventListener('blur', removeFocus);

        // Initialize state
        if (input.value && input.value.trim()) applyFocus();
    });

    // Real-time form validation
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(this)) {
                e.preventDefault();
                showNotification('Please fill in all required fields correctly.', 'error');
            }
        });
    });

    // Add loading states to submit buttons
    document.querySelectorAll('button[type="submit"]').forEach(btn => {
        btn.addEventListener('click', function() {
            this.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
            this.disabled = true;
        });
    });
}

// Theme toggle: persists to localStorage and updates UI
function initThemeToggle() {
    const btn = document.getElementById('themeToggle');
    if (!btn) return;

    const root = document.documentElement || document.body;
    const saved = localStorage.getItem('one3tap:theme');

    function applyTheme(theme) {
        document.body.setAttribute('data-theme', theme);
        localStorage.setItem('one3tap:theme', theme);
        // update icon
        btn.innerHTML = theme === 'light' ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';
    }

    // Initialize
    if (saved) applyTheme(saved);
    else {
        // default from body attr
        const defaultTheme = document.body.getAttribute('data-theme') || 'dark';
        applyTheme(defaultTheme);
    }

    btn.addEventListener('click', function() {
        const current = document.body.getAttribute('data-theme') || 'dark';
        const next = current === 'dark' ? 'light' : 'dark';
        applyTheme(next);
    });
}

// Navigation Enhancements
function initNavigation() {
    const navbar = document.querySelector('.navbar');
    let lastScrollTop = 0;
    
    // Navbar scroll effects
    window.addEventListener('scroll', function() {
        let scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        if (scrollTop > lastScrollTop && scrollTop > 100) {
            // Scrolling down
            navbar.style.transform = 'translateY(-100%)';
        } else {
            // Scrolling up
            navbar.style.transform = 'translateY(0)';
        }
        
        // Add blur effect when scrolling
        if (scrollTop > 50) {
            navbar.style.background = 'rgba(12, 12, 12, 0.98)';
            navbar.style.backdropFilter = 'blur(30px)';
        } else {
            navbar.style.background = 'rgba(12, 12, 12, 0.95)';
            navbar.style.backdropFilter = 'blur(20px)';
        }
        
        lastScrollTop = scrollTop;
    });

    // Mobile navigation toggle
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    if (navbarToggler) {
        navbarToggler.addEventListener('click', function() {
            navbarCollapse.classList.toggle('show');
        });
    }

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Particle Effects for Hero Section
function initParticleEffects() {
    const heroSection = document.querySelector('.hero-section');
    if (!heroSection) return;

    // Create floating particles
    for (let i = 0; i < 20; i++) {
        createParticle(heroSection);
    }
}

function createParticle(container) {
    const particle = document.createElement('div');
    particle.className = 'particle';
    particle.style.cssText = `
        position: absolute;
        width: 4px;
        height: 4px;
        background: linear-gradient(45deg, #4facfe, #00f2fe);
        border-radius: 50%;
        pointer-events: none;
        opacity: 0.6;
        animation: float ${Math.random() * 10 + 5}s infinite linear;
        left: ${Math.random() * 100}%;
        top: ${Math.random() * 100}%;
        z-index: 1;
    `;
    
    container.appendChild(particle);
    
    // Remove particle after animation
    setTimeout(() => {
        if (particle.parentNode) {
            particle.parentNode.removeChild(particle);
        }
    }, 15000);
}

// Scroll Effects
function initScrollEffects() {
    // Parallax effect for hero section
    window.addEventListener('scroll', function() {
        const scrolled = window.pageYOffset;
        const heroImage = document.querySelector('.hero-image');
        
        if (heroImage) {
            heroImage.style.transform = `translateY(${scrolled * 0.3}px)`;
        }
    });

    // Progress indicator
    const progressBar = document.createElement('div');
    progressBar.className = 'scroll-progress';
    progressBar.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        height: 3px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        z-index: 9999;
        transition: width 0.1s ease;
    `;
    document.body.appendChild(progressBar);

    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset;
        const docHeight = document.documentElement.scrollHeight - window.innerHeight;
        const scrollPercent = (scrollTop / docHeight) * 100;
        progressBar.style.width = scrollPercent + '%';
    });
}

// Enhanced Messaging System
function initMessaging() {
    // Auto-hide alerts after 5 seconds
    document.querySelectorAll('.alert').forEach(alert => {
        setTimeout(() => {
            fadeOut(alert);
        }, 5000);
    });
}

// Modal Effects
function initModalEffects() {
    // Add backdrop blur when modals open
    document.querySelectorAll('[data-bs-toggle="modal"]').forEach(trigger => {
        trigger.addEventListener('click', function() {
            document.body.style.backdropFilter = 'blur(5px)';
        });
    });

    // Remove backdrop blur when modals close
    document.querySelectorAll('.modal').forEach(modal => {
        modal.addEventListener('hidden.bs.modal', function() {
            document.body.style.backdropFilter = 'none';
        });
    });
}

// Utility Functions
function validateForm(form) {
    let isValid = true;
    const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.classList.add('is-invalid');
            isValid = false;
        } else {
            input.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = `
        top: 20px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    `;
    
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        fadeOut(notification);
    }, 5000);
}

function fadeOut(element) {
    element.style.opacity = '0';
    element.style.transform = 'translateX(100px)';
    setTimeout(() => {
        if (element.parentNode) {
            element.parentNode.removeChild(element);
        }
    }, 300);
}

// NFC Card Animations
function animateNFCCard(cardElement) {
    cardElement.style.transform = 'scale(1.05) rotateY(5deg)';
    cardElement.style.boxShadow = '0 20px 40px rgba(79, 172, 254, 0.4)';
    
    setTimeout(() => {
        cardElement.style.transform = 'scale(1) rotateY(0deg)';
        cardElement.style.boxShadow = '0 8px 32px rgba(0, 0, 0, 0.3)';
    }, 300);
}

// Initialize NFC card interactions
document.addEventListener('click', function(e) {
    if (e.target.closest('.nfc-card')) {
        animateNFCCard(e.target.closest('.nfc-card'));
    }
});

// Add floating animation keyframes to CSS
const style = document.createElement('style');
style.textContent = `
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); opacity: 0.6; }
        25% { transform: translateY(-20px) rotate(90deg); opacity: 1; }
        50% { transform: translateY(-40px) rotate(180deg); opacity: 0.8; }
        75% { transform: translateY(-20px) rotate(270deg); opacity: 1; }
    }
    
    .particle {
        animation: float linear infinite;
    }
    
    .scroll-progress {
        transition: width 0.1s ease !important;
    }
    
    .navbar {
        transition: transform 0.3s ease, background 0.3s ease, backdrop-filter 0.3s ease !important;
    }
    
    .form-control.is-invalid {
        border-color: #ef4444;
        box-shadow: 0 0 0 0.2rem rgba(239, 68, 68, 0.25);
    }
`;
document.head.appendChild(style);

// Performance optimization
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Apply debouncing to scroll events
window.addEventListener('scroll', debounce(function() {
    // Debounced scroll events
}, 10));

console.log('✨ TapOne3 Enhanced UI System Loaded');
