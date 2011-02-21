#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__    = "Alexandru Nedelcu"
__email__     = "contact@alexn.org"


from google.appengine.ext import webapp
from google.appengine.ext import db


class Article(db.Model):
    url = db.LinkProperty(required=True)
    title = db.StringProperty(required=False)

    created_at = db.DateTimeProperty(auto_now_add=True)


class Author(db.Model):
    email = db.EmailProperty(required=True)
    name  = db.StringProperty(required=True)
    url   = db.StringProperty(required=False)

    created_at = db.DateTimeProperty(auto_now_add=True)


class Comment(db.Model):
    article = db.ReferenceProperty(Article, required=True)
    author  = db.ReferenceProperty(Author,  required=True)
    comment = db.StringProperty(required=True, multiline=True)

    created_at = db.DateTimeProperty(auto_now_add=True)
    updated_at = db.DateTimeProperty(auto_now=True)
    
