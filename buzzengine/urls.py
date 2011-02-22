#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__    = "Alexandru Nedelcu"
__email__     = "contact@alexn.org"


from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^api/', include('buzzengine.api.urls'))
)


