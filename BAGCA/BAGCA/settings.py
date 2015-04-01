"""
Django settings for BAGCA project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')^rq(122selkpl#m1n&*a5@6td$zm@edd83$!+0lc@gqwjlvk('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

TEMPLATE_CONTEXT_PROCESSORS = ( 'django.core.context_processors.request',
                                'django.contrib.auth.context_processors.auth',
                            )


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_s3_storage',
    'embed_video',
    'quizzes',
    'quiz_admin',
    'user_data',
    'jquery',
    'bootstrap_toolkit',
    'bootstrap3',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'BAGCA.urls'

WSGI_APPLICATION = 'BAGCA.wsgi.application'

DEFAULT_FILE_STORAGE = 'django_s3_storage.storage.S3Storage'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "bagca",
        "USER": "errang",
        "HOST": "localhost",
        "PORT": "5432",
        }
}
'''
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "d693c240mhuopn",
        "USER": "fwiswwhprrntqe",
        "PASSWORD": "KZnLDk6ZQmHvO5gxK3OcM9GqXx",
        "HOST": "ec2-107-22-253-198.compute-1.amazonaws.com",
        "PORT": "5432",
        }
}

AWS_REGION = "us-east-1"

AWS_ACCESS_KEY_ID = "AKIAIIG7RD53TWKTDUNQ"

AWS_SECRET_ACCESS_KEY = "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"

AWS_S3_BUCKET_NAME = "bagca"

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(os.path.dirname(__file__), 'static')

# Send email
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'bagca.training@gmail.com'
EMAIL_HOST_PASSWORD = 'adminpassw'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# typically, os.path.join(os.path.dirname(__file__), 'media')
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media')
MEDIA_ROOT_FILES = MEDIA_ROOT + '/USER_UPLOADED_FILES'
MEDIA_URL = '/media/'