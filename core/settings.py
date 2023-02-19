import os
import sys
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-%x508#=mrw*_c)5#2cup5k22j3b)ci)3b3g*5=n_j=0_t-uoi!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['http://127.0.0.1', "http://10.0.2.2", 'localhost', '192.168.1.154', 'https://inmansdj.herokuapp.com', 'https://euronature.com' ]

#insta_image_url = 'instaggy.com'


LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
    )


INSTALLED_APPS = [
    # app -> api 
    'api',
    'channels',
    'daphne',
    'rest_framework.authtoken',
    ####
    'django_filters',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'user',
    'services',
    'custom_admin',
    'root',
    'dj_rest_auth',
    'crispy_forms',
    'django_cleanup',
    'rest_framework',
    'ckeditor',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware', # Localization
]

ROOT_URLCONF = 'core.urls'

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
                'custom_admin.context_processors.seoSettings',
            ],
        },
    },
]

#WSGI_APPLICATION = 'core.wsgi.application'
ASGI_APPLICATION = 'core.asgi.application'

FILE_UPLOAD_HANDLERS = [
    'django.core.files.uploadhandler.MemoryFileUploadHandler',
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'django_instagram_bayi',
        'USER':'rootadminbayi',
        'PASSWORD':'prjvpc930ghuj',
        'HOST':'127.0.0.1',
        'PORT':'5432',
    },

}

CHANNEL_LAYERS = {
    'default': {
     'BACKEND': 'channels_redis.core.RedisChannelLayer', 
     'CONFIG': {
        "hosts": [("localhost", 6379)],
      }, 
     #"BACKEND": "channels.layers.InMemoryChannelLayer"
    },
}



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

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': (
        ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser'),
}

CRISPY_TEMPLATE_PACK = 'bootstrap4'


LANGUAGE_CODE = 'tr'


TIME_ZONE = 'Europe/Istanbul'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = 'static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

MEDIA_URL = '/media/'
MEDIA_ROOT = 'media'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#import django
#django.setup()

try:
    smtp_info = None   
    from custom_admin.models import MailSMTPInfo

    smtp_info = MailSMTPInfo.objects.last()
    if smtp_info:
        
        EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
        EMAIL_HOST = smtp_info.EMAIL_HOST
        EMAIL_PORT = smtp_info.EMAIL_PORT
        EMAIL_USE_TLS = True
        EMAIL_HOST_USER = smtp_info.EMAIL_HOST_USER
        EMAIL_HOST_PASSWORD = smtp_info.EMAIL_HOST_PASSWORD
        ACCOUNT_EMAIL_VERIFICATION = 'none'

    else:
        EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
        EMAIL_HOST = ''
        EMAIL_PORT = ''
        EMAIL_USE_TLS = True
        EMAIL_HOST_USER = ''
        EMAIL_HOST_PASSWORD = ''
        ACCOUNT_EMAIL_VERIFICATION = 'none'

except Exception as e:
    print('settings mail smtp except e düstü', e)
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = ''
    EMAIL_PORT = ''
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = ''
    EMAIL_HOST_PASSWORD = ''
    ACCOUNT_EMAIL_VERIFICATION = 'none'