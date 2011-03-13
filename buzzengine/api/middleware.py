#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__    = "Alexandru Nedelcu"
__email__     = "alex@magnolialabs.com"


from buzzengine.api.models import Author

class TrackingMiddleware:
    def process_request(self, request):        
        authorhash = request.COOKIES.get('author')
        if authorhash:
            author = Author.gql("WHERE email_hash = :1", authorhash)[:1]            
            request.author = author[0] if author else None
        else:
            request.author = None

class HttpControlMiddleware(object):
    def process_response(self, request, response):
        response['Access-Control-Allow-Origin'] = "*"
        response['Access-Control-Allow-Credentials'] = 'true'
        return response