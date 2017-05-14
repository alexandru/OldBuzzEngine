#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__    = "Alexandru Nedelcu"
__email__     = "noreply@alexn.org"


from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^api/', include('buzzengine.api.urls')),
    (r'', include('buzzengine.frontend.urls')),
)


