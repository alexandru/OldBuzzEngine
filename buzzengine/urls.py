#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__    = "Alexandru Nedelcu"
__email__     = "contact@alexn.org"


from django.conf.urls.defaults import *
from buzzengine import api

urlpatterns = patterns('',
    (r'^api/hello/?$', api.hello),
    (r'^api/comment/create/?$', api.comment_create),
    (r'^api/comment/?$', api.comment_list),
)


