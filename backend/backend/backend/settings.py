"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import json
import dj_database_url
from os import environ, path

from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-m139&@m^3l-5-w54teh))^e=ow*-12m2%n&tixzvw*jebn28gh'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    "*", 
    "http://carcaraqsar.com.br",
    "http://www.carcaraqsar.com.br",
]


# Application definition

INSTALLED_APPS = [
    'user',
    'api',
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'project_management',
    'database',
    'training',
    'variables_selection',
    'prevision',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

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

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases




# Definir uma variável de ambiente no código?

if "DATABASE_SECRET" in environ:
    print("DATABASE_SECRET is on ENVIRON")
    database_secret = environ.get("DATABASE_SECRET")
    if database_secret != None:
        db_url = json.loads(database_secret)["DATABASE_URL"]
        DATABASES = {"default": dj_database_url.parse(db_url)}
else:
    print("DATABASE_SECRET is not on ENVIRON")
    DATABASES = {"default": dj_database_url.parse("sqlite:///db.sqlite3")}

# configuration_postgres = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'django',
#         'USER': 'postgres',
#         'PASSWORD': 'postgres',
#         'HOST': 'django-builder-db.c18m40gqukp8.us-east-2.rds.amazonaws.com',
#         'PORT': '5432',
#     }
# }

# configuration_postgres = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'condominio',
#         'USER': 'user',
#         'PASSWORD': 'password',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }

# DATABASES = configuration_postgres

# configuration_sqlite = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
# DATABASES = configuration_sqlite


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# STATICFILES_DIRS files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=90),
    "ROTATE_REFRESH_TOKENS":True,
    "BLACKLIST_AFTER_ROTATION":True,
    "UPDATE_LAST_LOGIN":False,

    "ALGORITHM": "HS256",

    "VERIFYING_KEY": "",
    "AUDIENCE":None,
    "ISSUER":None,
    "JSON_ENCODER":None,
    "JWK_URL":None,
    "LEEWAY": 0,

    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    "JTI_CLAIM": "jti",

    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),

    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}

# Mudança de usuário principal
AUTH_USER_MODEL = 'user.User'

# Permissões de acesso
# Permitir todas as origens
CORS_ALLOW_ALL_ORIGINS = True
# Configurações para permitir cookies de autenticação
# Permite credenciais em solicitações cross-origin
CORS_ALLOW_CREDENTIALS = True

# Permitir origens específicas
X_FRAME_OPTIONS = 'ALLOW-FROM https://carcaraqsar.com.br'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

CSRF_TRUSTED_ORIGINS = [
    'http://backend.carcaraqsar.com.br:3000',
    'http://www.backend.carcaraqsar.com.br:3000',
    'http://carcaraqsar.com.br',
    'http://www.carcaraqsar.com.br',
]

# Configurações básicas de segurança
CSRF_COOKIE_SECURE = False  # True se usar HTTPS
SESSION_COOKIE_SECURE = False  # True se usar HTTPS
CSRF_USE_SESSIONS = False
CSRF_COOKIE_HTTPONLY = False
SESSION_COOKIE_HTTPONLY = False

# Configurações do JWT
# Nome do cookie JWT, se personalizado
JWT_AUTH_COOKIE = 'jwt_tokens'

# Configurações de mídia
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"

# Configurações do Celery
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
# URL do broker de mensagens
CELERY_BROKER_URL = 'redis://redis:6379/0'

# URL para resultados das tarefas (opcional)
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'

# Outras configurações do Celery, se necessário
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'