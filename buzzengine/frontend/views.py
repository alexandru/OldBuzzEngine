#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__    = "Alexandru Nedelcu"
__email__     = "contact@alexn.org"


import hashlib
import re

from datetime import datetime, timedelta
from django.utils import simplejson as json

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404
from buzzengine.api import models
from buzzengine.frontend.decorators import requires_admin
from buzzengine.frontend.forms import CommentForm


def homepage(request):
    return render_to_response("homepage.html", {'API_DOMAIN': request.API_DOMAIN})


@requires_admin
def edit_comment(request):
    comment = _get_item(request)
    form = CommentForm(instance=comment)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return render_to_response("admin/edit_done.html", {"link": request.get_full_path(), 'comment': comment})

    return render_to_response("admin/edit.html", {"form": form, "comment": comment})


@requires_admin
def delete_comment(request):
    comment = _get_item(request)
    article_url = comment.article.url

    if request.method == "POST" and request.POST.get('yes'):
        comment.delete()
        return render_to_response("admin/delete_done.html", {"link": request.get_full_path(), 'article_url': article_url})

    return render_to_response("admin/delete.html", {"link": request.get_full_path(), 'article_url': article_url, 'comment': comment})


def _get_item(request):
    comment_id = request.REQUEST.get('comment_id')
    article_url = request.REQUEST.get('article_url')

    article = models.Article.get_by_key_name(article_url)
    if not article: raise Http404

    comment_id = int(comment_id)
    comment = models.Comment.get_by_id(comment_id, parent=article)
    if not comment: raise Http404        

    return comment
    
