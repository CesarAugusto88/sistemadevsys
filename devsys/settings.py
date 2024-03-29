# Usando Django==2.0
"""
Django settings for agenda project.
Generated by 'django-admin startproject' using Django 3.0.2.
For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from decouple import config

from dj_database_url import parse as dburl


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = [
    config("SITE1"),
    config("SITE2"),
    config("LOCAL1"),
    config("LOCAL2"),
    config("IP"),
]

INTERNAL_IPS = ['127.0.0.1']

ADMINS = [('Cesar', 'cesar@devsys.com.br')]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    
    "core",

    "crispy_forms",

    "account",
    'bootstrapform',
    'auditlog',
    'django.contrib.sitemaps',
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'auditlog.middleware.AuditlogMiddleware',
]

ROOT_URLCONF = "devsys.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "devsys.wsgi.application"


# default_dburl = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
# DATABASES = { 'default': config('DATABASE_URL', default=default_dburl, cast=dburl), }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "db_devsys",
        "USER": "cesar",
        "PASSWORD": "Ads_12345",
        "HOST": "localhost",
        "PORT": "3306",
        "OPTIONS": {"init_command": "SET sql_mode='STRICT_TRANS_TABLES'",},
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = "America/Sao_Paulo"  #'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# DATE_FORMAT = 'd/m/Y'

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

STATIC_TMP = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"

os.makedirs(STATIC_TMP, exist_ok=True)
os.makedirs(STATIC_ROOT, exist_ok=True)

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

MEDIA_ROOT = os.path.join(BASE_DIR, "media")

MEDIA_URL = "/media/"

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login'
LOGIN_URL = '/devsys/'

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
#STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

#Configurations e-mail
# EMAIL_HOST = 'http://mail.devsys.com.br'
# EMAIL_PORT = 465
# EMAIL_HOST_USER = config("EMAIL_HOST_USER")
# EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
# EMAIL_USE_TLS = False
# EMAIL_USE_SSL = True

# Recuperação de senha do usuário
# cursos.alura.com.br/forum/topico-recuperacao-de-senha-do-usuario-131150
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
####
EMAIL_USE_TLS = True
EMAIL_HOST = 'mail.devsys.com.br'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'cesar@devsys.com.br'
EMAIL_HOST_PASSWORD = config('SECRET_EMAIL')