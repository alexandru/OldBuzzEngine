import os,sys
os.environ['DJANGO_SETTINGS_MODULE'] = 'buzzengine.settings'

# Force Django to reload its settings.
from django.conf import settings
settings._target = None

import django.core.signals
import django.db
import django.dispatch

# Log errors.
#import logging
#def log_exception(*args, **kwds):
#    logging.exception('Exception in request:')
#
#django.dispatch.Signal.connect(
#    django.core.signals.got_request_exception, log_exception)

# Unregister the rollback event handler.
django.dispatch.Signal.disconnect(
    django.core.signals.got_request_exception,
    django.db._rollback_on_exception)

from buzzengine import wsgi
app = wsgi.application
