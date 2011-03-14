#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__    = "Alexandru Nedelcu"
__email__     = "alex@magnolialabs.com"

import re
from django.conf import settings
from buzzengine.api.models import Author

class TrackingMiddleware:
    def process_request(self, request):
        authorhash = request.GET.get('author') or request.COOKIES.get('author') 
        if authorhash:
            request.author = Author.get_by_hash(authorhash)
        else:
            request.author = None

class HttpControlMiddleware(object):
    def process_request(self, request):
        url    = request.REQUEST.get('article_url') or request.META.get('HTTP_REFERER')
        host   = None
        origin = None

        if url:
            origin = re.findall('^(https?://[^/]+)', url)
            origin = origin[0] if origin else None

        host = request.META['SERVER_NAME']
        if str(request.META.get('SERVER_PORT')) != str(80):
            host += ":" + request.META['SERVER_PORT']

        request.API_DOMAIN  = host
        request.ROOT_DOMAIN = origin

    def process_response(self, request, response):
        origin = request.ROOT_DOMAIN
        if origin:
            response['Access-Control-Allow-Origin'] = origin
            response['Access-Control-Allow-Credentials'] = 'true'
            response['Access-Control-Allow-Headers'] = 'Content-Type, *'
            response['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
            response['Access-Control-Max-Age'] = '111111'
        return response
