from .settings_dev import *  # noqa
from .settings_dev import BASE_DIR
import os

DEBUG = False
SECRET_KEY = os.environ['SECRET_KEY']
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',')
CSRF_TRUSTED_ORIGINS = [os.environ.get('CSRF_ORIGIN', 'http://localhost')]


# DB (Postgres on PaaS, fallback SQLite if not set)
DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL:
    # dj-database-url is handy; but keep it stdlib to avoid new dep:
    import urllib.parse as up
    url = up.urlparse(DATABASE_URL)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': url.path.lstrip("/"),
            'USER': url.username,
            'PASSWORD': url.password,
            'HOST': url.hostname,
            'PORT': url.port or 5432,
        }
    }

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

CORS_ALLOW_ALL_ORIGINS = os.getenv('CORS_ALLOW_ALL_ORIGINS', 'False') == 'True'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')