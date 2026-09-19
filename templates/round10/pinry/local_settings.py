"""Copied only on first startup. Existing persistent settings are preserved."""
import os
from urllib.parse import urlparse

STATIC_ROOT = '/data/static'
MEDIA_ROOT = '/data/static/media'
SECRET_KEY = os.environ['PINRY_SECRET_KEY']
DEBUG = False
TEMPLATE_DEBUG = False
ALLOWED_HOSTS = [urlparse(os.environ['PUBLIC_URL']).hostname, 'localhost', '127.0.0.1']
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': '/data/production.db'}}
ALLOW_NEW_REGISTRATIONS = False
PUBLIC = False
IMAGE_AUTO_DELETE = True
IMAGE_SIZES = {
    'thumbnail': {'size': [240, 0]},
    'standard': {'size': [600, 0]},
    'square': {'crop': True, 'size': [125, 125]},
}
ENABLED_PLUGINS = []
CSRF_TRUSTED_ORIGINS = [os.environ['PUBLIC_URL']]
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
