"""
Django settings for pcr project.

Generated by 'django-admin startproject' using Django 3.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-7ig@-zml5v$k*yk+70wfp*i-g3&+krxxm^4_ezx52x(g6=e6aq'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['raihandev.com']


# Application definition

INSTALLED_APPS = [

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'post',
    'user',
    'hostel',
    'collegeSystem',
    'semesterSystem',
    'dashboard',

]



X_FRAME_OPTIONS = 'SAMEORIGIN'
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pcr.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
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

WSGI_APPLICATION = 'pcr.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases


"""For Cpanel """

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'raihande_test_database',
        'HOST': 'localhost',
        'PORT': '3306',
        'USER': 'raihande_joy',
        'PASSWORD': 'kmr2303200@'
    }
}

AUTH_USER_MODEL = 'user.User'


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Dhaka'

USE_I18N = True

USE_L10N = True

USE_TZ = True




"""Settings for deployment """

STATIC_URL = '/static/'
STATIC_ROOT = 'static'
# STATICFILES_DIRS = [
#     BASE_DIR / 'static',
# ]
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.raihandev.com'

EMAIL_HOST_USER = 'test_sys@raihandev.com'#os.environ.get('USER_EMAIL')
EMAIL_HOST_PASSWORD = 'kmr2303200@'#os.environ.get('PASSWORD')
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True

COLLEGE_NAME = os.environ.get('COLLEGE_NAME')
CLG_ADDRESS = os.environ.get('COLLEGE_ADDRESS')
CLG_CODE = os.environ.get('COLLEGE_CODE')
SEMESTER_FEE = int(os.environ.get('SEMESTER_FEE'))
HOSTEL_FEE = int(os.environ.get('HOSTEL_FEE'))
EMAIL_PORT = 465

LOGIN_URL = '/login/'
# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


MEDIA_URL = '/media/' 
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
SECURE_SSL_REDIRECT = True  


EMAIL_LOGO_PATH = '/home2/raihande/public_html/static/post/images'
