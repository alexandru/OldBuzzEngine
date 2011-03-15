#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__    = "Alexandru Nedelcu"
__email__     = "contact@alexn.org"


import random
import hashlib

from django.conf import settings
from google.appengine.api import memcache
from google.appengine.ext import webapp
from google.appengine.ext import db


CACHE_EXP_SECS = 60 * 60 * 24 * 7 * 4 # 4 weeks


class Article(db.Model):
    url = db.LinkProperty(required=True)
    title = db.StringProperty(required=False)

    created_at = db.DateTimeProperty(auto_now_add=True)


class Author(db.Model):
    name       = db.StringProperty(required=True)
    email      = db.EmailProperty(required=False)
    url        = db.StringProperty(required=False)    
    email_hash = db.StringProperty(required=False)
    created_at = db.DateTimeProperty(auto_now_add=True)

    def put(self):
        email = self.email and self.email.strip()
        name  = self.name.strip()

        md5 = hashlib.md5()    
        md5.update(email or name)

        email_hash = md5.hexdigest()
        self.email_hash = email_hash

        obj = super(Author, self).put()
        memcache.delete(self.email_hash, namespace="authors")
        return obj

    def get_email_hash(self):
        if not self.email_hash:
            self.put()
        return self.email_hash

    @property
    def gravatar_url(self):        
        return "http://www.gravatar.com/avatar/" + self.get_email_hash() + ".jpg?s=80&d=mm"

    @classmethod
    def get_by_hash(self, email_hash):
        author = memcache.get(email_hash, namespace="authors")
        if not author:
            author = Author.gql("WHERE email_hash = :1", email_hash)[:1]            
            author = author[0] if author else None
            memcache.set(email_hash, author, time=CACHE_EXP_SECS, namespace='authors')
        return author


class Comment(db.Model):
    article   = db.ReferenceProperty(Article, required=True)
    author    = db.ReferenceProperty(Author,  required=True)
    comment   = db.TextProperty(required=True)
    author_ip = db.StringProperty(required=False)

    created_at = db.DateTimeProperty(auto_now_add=True)
    updated_at = db.DateTimeProperty(auto_now=True)    

    def put(self, *args, **kwargs):
        obj = super(Comment, self).put(*args, **kwargs)
        # invalidates cache
        memcache.delete(self.article.url, namespace='comments')
        return obj

    @classmethod
    def get_comments(self, article_url):
        comments = memcache.get(article_url, namespace="comments")

        if not comments:
            article = Article.get_by_key_name(article_url)
            if article:
                comments = Comment.gql("WHERE article = :1", article)
                comments = [ {'comment': c.comment, 'created_at': c.created_at, "author": { "name": c.author.name, 'url': c.author.url, 'email': c.author.email, 'gravatar_url': c.author.gravatar_url }} for c in comments ]
            else:
                comments = []

            memcache.set(article_url, comments, time=CACHE_EXP_SECS, namespace='comments')

        return comments
