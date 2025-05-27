from pathlib import Path
import os
from google.oauth2 import service_account

# Diretório base do projeto (raiz)
BASE_DIR = Path(__file__).resolve().parent.parent

CERTIFICADOS_DIR = BASE_DIR / 'certificados'

# Caminho para os certificados
SSL_CERT_PATH = CERTIFICADOS_DIR / 'client-cert.pem'
SSL_KEY_PATH = CERTIFICADOS_DIR / 'client-key.pem'
SSL_ROOTCERT_PATH = CERTIFICADOS_DIR / 'server-ca.pem'

WSGI_APPLICATION = 'diarioautista.wsgi.application'

AUTH_USER_MODEL = 'accounts.CustomUser'

ROOT_URLCONF = 'diarioautista.urls'

GS_BUCKET_NAME = 'bucket-diario-autista'
GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
    str(CERTIFICADOS_DIR / 'chave-servico.json')
)

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ACCOUNT_LOGIN_METHODS = ['email'] 
ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*']
AUTH_USER_MODEL = 'accounts.CustomUser'
ACCOUNT_USER_MODEL_USERNAME_FIELD = None

LOGIN_URL = 'accounts/login/'
LOGIN_REDIRECT_URL = 'accounts/perfil/'
ACCOUNT_LOGOUT_REDIRECT_URL = 'accounts/login/'
STATIC_URL = f'https://storage.googleapis.com/{GS_BUCKET_NAME}/static/'

SITE_ID = 1

SECRET_KEY = 'django-insecure-h^c5tf2z)t9co_3a++&bmn@+k*d@*%(v#_bu&-tt&l#!*k1%w_'

DEBUG = True

ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = [
    'https://projeto-integrador-iii-d7e19.web.app',
    'https://projeto-integrador-iii-d7e19.firebaseapp.com',
    'https://diariodoautista.app',
    'https://diario-virtual-1065315166413.southamerica-east1.run.app',
    'https://127.0.0.1'
]

CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = 'None'

SESSION_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = 'None'

CORS_ALLOWED_ORIGINS = [
    'https://diario-virtual-1065315166413.southamerica-east1.run.app',
    'https://127.0.0.1'
]

CORS_ALLOW_CREDENTIALS = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'accounts',
    'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'autista-db',
        'USER': 'app-user',
        'PASSWORD': 'f}PI;Gp6ngVJ%0mt**',
        'HOST': '35.198.55.132',
        'PORT': '5432',
        'OPTIONS': {
            'sslmode': 'require',
            'sslcert': str(SSL_CERT_PATH),
            'sslkey': str(SSL_KEY_PATH),
            'sslrootcert': str(SSL_ROOTCERT_PATH), 
    }
}
}

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

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.gcloud.GoogleCloudStorage",
        "OPTIONS": {
            "project_id": "diario0autista",
            "bucket_name": "bucket-diario-autista",
            "credentials": GS_CREDENTIALS,
        },
    },
    "staticfiles": {
        "BACKEND": "storages.backends.gcloud.GoogleCloudStorage",
        "OPTIONS": {
            "project_id": "diario0autista",
            "bucket_name": "bucket-diario-autista",
        },
    },
}

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)
