#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__    = "Alexandru Nedelcu"
__email__     = "contact@alexn.org"


import re

from django import newforms as forms
from buzzengine.api import models


class NewCommentForm(forms.Form):
    article_url = forms.URLField(required=True)
    article_title = forms.CharField(required=False)

    author_email = forms.EmailField(required=True)
    author_name  = forms.CharField(required=True)
    author_url   = forms.URLField(required=False)
    
    comment = forms.CharField(required=True)

    def save(self):
        data = self.clean_data
        
        article_url = data.get('article_url')
        article_title = data.get('article_title') or data.get('article_url')

        article = models.Article.get_or_insert(article_url, url=article_url, title=article_title)

        author_email = data.get('author_email')
        author_name  = data.get('author_name')
        author_url   = data.get('author_url')
        author_key   = author_email + author_name

        author = models.Author.get_or_insert(author_key, email=author_email, name=author_name)
        if author.url != author_url:
            author.url = author_url
            author.put()

        comment = models.Comment(parent=article, comment=data.get('comment'), author=author, article=article)
        comment.put()

        self._author  = author
        self._article = article
        self._comment = comment

        
    @property
    def output(self):
        return {
            'article': {
                'url': self._article.url,
                'title': self._article.title,
            },
            'author': {
                'email': self._author.email,
                'name':  self._author.name,
                'url':  self._author.url,
            },
            'comment': self._comment.comment,
        }
