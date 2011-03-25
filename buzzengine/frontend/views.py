#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__    = "Alexandru Nedelcu"
__email__     = "contact@alexn.org"


import hashlib
import re

from urllib import quote
from datetime import datetime, timedelta
from django.utils import simplejson as json

from google.appengine.api import users
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from buzzengine.api import models
from buzzengine.frontend.decorators import requires_admin
from buzzengine.frontend.forms import CommentForm


def homepage(request):
    return render_to_response("frontend/homepage.html", {'API_DOMAIN': request.API_DOMAIN})


@requires_admin
def edit_comment(request):
    comment = _get_item(request)
    form = CommentForm(instance=comment)

    if request.method == "POST":
        if request.POST.get('delete'):
            comment.delete()

            article_url = request.REQUEST.get('article_url')
            if article_url.find('#') == -1:
                article_url += '#comments'

            return HttpResponseRedirect(article_url) 
        else:
            form = CommentForm(request.POST, instance=comment)
            if form.is_valid():
                form.save()
                return _render(request, "frontend/admin/edit.html", {"form": form, "comment": comment, 'message': 'Message saved!'})

    return _render(request, "frontend/admin/edit.html", {"form": form, "comment": comment})


def _get_item(request):
    comment_id = request.REQUEST.get('comment_id')
    article_url = request.REQUEST.get('article_url')

    article = models.Article.get_by_key_name(article_url)
    if not article: raise Http404

    comment_id = int(comment_id)
    comment = models.Comment.get_by_id(comment_id, parent=article)
    if not comment: raise Http404        

    return comment
    

def _render(request, tpl_name, kwargs):
    kwargs['user'] = request.user
    kwargs['logout_url'] = users.create_logout_url("/")
    return render_to_response(tpl_name, kwargs)