import os

DEBUG = True
ROOT_PATH = os.path.dirname(__file__)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'buzzengine.api.middleware.TrackingMiddleware',
    'buzzengine.api.middleware.HttpControlMiddleware',
)
INSTALLED_APPS = (
    'buzzengine.api',
    'buzzengine.frontend',
)
TEMPLATE_DIRS = (
    os.path.join(ROOT_PATH, 'templates'),
)
ROOT_URLCONF = 'buzzengine.urls'

ADMIN_EMAIL  = "contact@alexn.org"
EMAIL_SENDER = "TheBuzzEngine <noreply@thebuzzengine.appspot.com>"
