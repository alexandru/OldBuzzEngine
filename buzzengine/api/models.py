#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__    = "Alexandru Nedelcu"
__email__     = "contact@alexn.org"


import hashlib

from google.appengine.ext import webapp
from google.appengine.ext import db


class Article(db.Model):
    url = db.LinkProperty(required=True)
    title = db.StringProperty(required=False)

    created_at = db.DateTimeProperty(auto_now_add=True)


class Author(db.Model):
    email      = db.EmailProperty(required=True)
    name       = db.StringProperty(required=True)
    url        = db.StringProperty(required=False)    
    email_hash = db.StringProperty(required=False)
    created_at = db.DateTimeProperty(auto_now_add=True)

    def put(self):
        email = self.email.strip()
        md5 = hashlib.md5()    
        md5.update(email)
        email = md5.hexdigest()
        self.email_hash = email
        return super(Author, self).put()

    def get_email_hash(self):
        if not self.email_hash:
            self.put()
        return self.email_hash

    @property
    def gravatar_url(self):
        return "http://www.gravatar.com/avatar/" + self.get_email_hash() + ".jpg?s=80&d=mm"


class Comment(db.Model):
    article = db.ReferenceProperty(Article, required=True)
    author  = db.ReferenceProperty(Author,  required=True)
    comment = db.TextProperty(required=True)

    created_at = db.DateTimeProperty(auto_now_add=True)
    updated_at = db.DateTimeProperty(auto_now=True)
    
