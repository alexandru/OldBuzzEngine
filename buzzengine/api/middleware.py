#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__    = "Alexandru Nedelcu"
__email__     = "alex@magnolialabs.com"

from django.conf import settings
from buzzengine.api.models import Author

class TrackingMiddleware:
    def process_request(self, request):        
        authorhash = request.COOKIES.get('author')
        if authorhash:
            request.author = Author.get_by_hash(authorhash)
        else:
            request.author = None

class HttpControlMiddleware(object):
    def process_response(self, request, response):
        response['Access-Control-Allow-Origin'] = "http://" + settings.ROOT_DOMAIN
        response['Access-Control-Allow-Credentials'] = 'true'
        response['Access-Control-Allow-Headers'] = 'Content-Type, *'
        response['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        response['Access-Control-Max-Age'] = '111111'
        return response