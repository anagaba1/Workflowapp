import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
#BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'django-insecure-9#*=1hk7gudhqql=8w)^pwq)sele)ry=#)5yvld0ph4phbwhxs'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'workflowapp',
    'feedbackapp',
    'schoolapp',
    'fliteracyapp',
    'feedback2024',
    'suspenseapp',
    #'bootstrap4',
    #'crispy_bootstrap4',
    'django_fsm',
    'django_fsm_log',
    'crispy_forms',
]

#CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap4'

CRISPY_TEMPLATE_PACK = 'bootstrap4'
#CRISPY_TEMPLATE_PACK = 'bootstrap4'



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'workflows.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'workflows.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'business_db2',
        'USER': 'postgres',
        #'PASSWORD': 'ismi@311',
        # 'PASSWORD': 'twib@311',
        'PASSWORD': 'new_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Email Settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # Use SMTP email backend
EMAIL_HOST = 'webmail.nssfug.org'  # SMTP server address
#EMAIL_HOST = 'https://webmail.nssfug.org/owa/'  # SMTP server address
EMAIL_PORT = 587  # SMTP server port
EMAIL_HOST_USER = 'nssfbiu@nssfug.org'  # SMTP username (your email address)
EMAIL_HOST_PASSWORD = '2X^te8U4Gb64F8e!'  # SMTP password
EMAIL_USE_TLS = True  # Use TLS encryption
# From email address (optional)
DEFAULT_FROM_EMAIL = 'nssfbiu@nssfug.org'

# The email address where password reset links will be sent from
# You can use the same email address as DEFAULT_FROM_EMAIL or a different one
PASSWORD_RESET_FROM_EMAIL = 'nssfbiu@nssfug.org'



INITIAL_PASSWORD = 'Password2023'

# Internationalization
LANGUAGE_CODE = 'en-us'

#TIME_ZONE = 'UTC'
TIME_ZONE = 'Africa/Nairobi'

USE_I18N = True

USE_TZ = True

# Static files
STATIC_URL = '/static/'
#STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, 'workflows', 'static'))
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'workflowapp', 'static'),
]


# Media files
#MEDIA_URL = '/media/'

"""
MEDIA_ROOT = {
    'workflowapp': os.path.join(BASE_DIR, 'workflowapp', 'media'),
    'fliteracyapp': os.path.join(BASE_DIR, 'fliteracyapp', 'media'),
}
"""
# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
#MEDIA_ROOT = os.path.join(BASE_DIR, 'workflowapp', 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Login URL
LOGIN_URL = 'login'

DATE_FORMAT = 'dd-mm-yyyy'  # Example format, adjust as needed
