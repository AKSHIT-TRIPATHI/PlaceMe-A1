"""
Django settings for PlaceMe_AI project.
"""

from pathlib import Path
import os
import dj_database_url

# ---------------------------------------------------------------------------
# Base directory
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# Security
# ---------------------------------------------------------------------------
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-change-me-in-production')

DEBUG = False

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')

# Render terminates TLS at the proxy layer and forwards the original scheme.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = False          # Render handles the redirect itself


# ---------------------------------------------------------------------------
# Application definition
# ---------------------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'placeme',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',   # ← serve static files efficiently
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'PlaceMe_AI.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'PlaceMe_AI.wsgi.application'


# ---------------------------------------------------------------------------
# Database
# Render provides a DATABASE_URL env var when a Postgres instance is attached.
# Falls back to local SQLite for development.
# ---------------------------------------------------------------------------
_DATABASE_URL = os.environ.get('DATABASE_URL', '').strip()

if _DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(
            _DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# ---------------------------------------------------------------------------
# Password validation
# ---------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ---------------------------------------------------------------------------
# Internationalisation
# ---------------------------------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# ---------------------------------------------------------------------------
# Static files
# WhiteNoise compresses and caches static files in production.
# ---------------------------------------------------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ---------------------------------------------------------------------------
# Media files (user-uploaded resumes, profile pics)
# NOTE: Render's disk is ephemeral on the free tier.
# For persistent uploads, swap MEDIA_ROOT for an S3/Cloudinary backend.
# ---------------------------------------------------------------------------
MEDIA_URL  = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ---------------------------------------------------------------------------
# Default primary key
# ---------------------------------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ---------------------------------------------------------------------------
# Authentication backends — email OR username login
# ---------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = [
    'placeme.backends.EmailOrUsernameBackend',
    'django.contrib.auth.backends.ModelBackend',
]


# ---------------------------------------------------------------------------
# Email — Brevo (formerly Sendinblue) HTTP API
# Render's free tier blocks outbound SMTP (port 587), so we use Brevo's
# transactional REST API over HTTPS (port 443) instead.
# Set BREVO_API_KEY, BREVO_SENDER_EMAIL, BREVO_SENDER_NAME in Render's
# environment variables dashboard.
# ---------------------------------------------------------------------------
BREVO_API_KEY      = os.environ.get('BREVO_API_KEY', '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')
BREVO_SENDER_EMAIL = os.environ.get('BREVO_SENDER_EMAIL', 'placeme143@gmail.com')
BREVO_SENDER_NAME  = os.environ.get('BREVO_SENDER_NAME', 'PlaceMe AI')

# Keep Django's email backend set (unused on Render, harmless to leave)
EMAIL_BACKEND       = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST          = 'smtp.gmail.com'
EMAIL_PORT          = 587
EMAIL_USE_TLS       = True
EMAIL_HOST_USER     = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL  = BREVO_SENDER_EMAIL


# ---------------------------------------------------------------------------
# AI API keys
# ---------------------------------------------------------------------------
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')
GROQ_API_KEY   = os.environ.get('GROQ_API_KEY', '')
