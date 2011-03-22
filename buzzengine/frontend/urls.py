#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__    = "Alexandru Nedelcu"
__email__     = "contact@alexn.org"


from django.conf.urls.defaults import *
from buzzengine.frontend import views


urlpatterns = patterns('',
    (r'^$', views.homepage),
    (r'^admin/edit/$', views.edit_comment),
    (r'^admin/delete/$', views.delete_comment),
)
