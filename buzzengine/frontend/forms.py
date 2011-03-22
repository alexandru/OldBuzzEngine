#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__    = "Alexandru Nedelcu"
__email__     = "alex@magnolialabs.com"


from google.appengine.ext.db import djangoforms as forms
#from django import newforms as forms
from buzzengine.api.models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['author_ip', 'article', 'author']