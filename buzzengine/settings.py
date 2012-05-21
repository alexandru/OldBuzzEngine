import os

# when a new comment happens, 
# this email address receives an alert
ADMIN_EMAIL  = "contact@alexn.org"

# FROM header of new message notifications.  Unfortunately it must be
# an approved sender ... like the emails of admins you approve for the
# GAE Application Instance.
#
# Some details here:
#   http://code.google.com/appengine/docs/python/mail/sendingmail.html
#
EMAIL_SENDER = "TheBuzzEngine <messages@thebuzzengine.com>"


## Web framework specific stuff ...

DEBUG = False
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


