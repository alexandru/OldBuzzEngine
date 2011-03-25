#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__    = "Alexandru Nedelcu"
__email__     = "contact@alexn.org"


from django.conf.urls.defaults import *
from buzzengine.api import views 
from buzzengine.api import tasks

urlpatterns = patterns('',
    (r'^hello/$', views.say_hello),
    (r'^comments/$', views.comments),
    (r'^notify/$', tasks.notify),
    (r'^test/page.html$', views.test_page),
)
