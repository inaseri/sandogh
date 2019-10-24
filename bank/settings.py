"""
Django settings for bank project.

Generated by 'django-admin startproject' using Django 1.10.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
import client

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'n0bkxd%6y!w30ng#sl_x5^m(-m%ui3-3(c=fmcafom992m0k7%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['sandogh-zainab.vps-vds.com',"127.0.0.1"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'client',
    'django.contrib.humanize',
    'pwa',
]
AUTH_USER_MODEL = "client.User"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bank.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'bank.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mydatabase',
    }
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         # 'NAME': 'sandogh_zainab',
#         # 'USER': 'sandogh_zainab',
#         # 'PASSWORD': '22bahman2010',
#         'HOST': '127.0.0.1',
#         # 'PORT': '5432',
#         'NAME': 'sandoghzainabvps_qwds',
#         'USER': 'sandoghzainabvps_lksjdn',
#         'PASSWORD': 'twwS,D#)%$H?',
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'

NORECAPTCHA_SITE_KEY = "6LekdikTAAAAAO2XWzairddfZz88GjFaiqJFEPWo"
NORECAPTCHA_SECRET_KEY = "6LekdikTAAAAAP1eXYh_kgz492Q-UNg4KJtWRfBe"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = ""

STATICFILES_DIRS=("./static/",)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

THUMBNAIL_UPLOAD_PATH='images/th/'

THUMBNAIL_STORAGE='images/'

telegapiKey="312010028:AAHyIG-OlQz1Eks7TDST-1J44o1dHgbfYBg"

PWA_APP_NAME = 'صندوق حضرت زینب (س)'
PWA_APP_DESCRIPTION = "مدیریت هزینه ها بدون هزینه"
PWA_APP_THEME_COLOR = '#0A0302'
PWA_APP_BACKGROUND_COLOR = '#ffffff'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_SCOPE = '/',
PWA_APP_ORIENTATION = 'any'
PWA_APP_START_URL = '/'
PWA_APP_ICONS = [
{
'src': '/static/img/ic-icone.jpg',
'sizes': '160x160',
}
]
PWA_APP_SPLASH_SCREEN = [
{
# 'src': '/static/my-app-icone.png',
# 'media': '(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)'
}
]
PWA_APP_DIR = 'rtl'
PWA_APP_LANG = 'en-US'

PWA_SERVICE_WORKER_PATH = os.path.join(BASE_DIR, 'static/js', 'serviceworker.js')