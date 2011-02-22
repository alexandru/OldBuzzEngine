#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__    = "Alexandru Nedelcu"
__email__     = "contact@alexn.org"


from django.conf.urls.defaults import *
from buzzengine.api import views 

urlpatterns = patterns('',
    (r'^comments/$', views.comments),
    (r'^test/page.html$', views.test_page),
)
