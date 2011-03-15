#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__    = "Alexandru Nedelcu"
__email__     = "contact@alexn.org"


import hashlib
import re

from datetime import datetime, timedelta
from django.utils import simplejson as json

from google.appengine.api import mail
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.conf import settings
from buzzengine.api.forms import NewCommentForm
from buzzengine.api import models


def comments(request):
    url = request.REQUEST.get('article_url') or request.META.get('HTTP_REFERER')
    if not url:
        raise Http404

    if url.rfind('#') > 0:
        url = url[:url.rfind('#')]

    if not url:        
        resp = HttpResponse(json.dumps({'article_url': ['This field is required.']}, indent=4), mimetype='text/plain')
        resp.status_code = 400
        return resp

    if request.method == 'POST':
        return _comment_create(request, url)
    else:
        return _comment_list(request, url)


def _comment_create(request, article_url):
    data = request.POST
    data = dict([ (k,data[k]) for k in data.keys() ])
    data['article_url'] = article_url

    is_json = not request.META['HTTP_ACCEPT'].find("html")

    form = NewCommentForm(data)
    if not form.is_valid():
        if is_json:
            resp = HttpResponse(json.dumps(form.errors, indent=4), mimetype='text/plain')
            resp.status_code = 400
            return resp
        else:
            return _comment_list(request, article_url, form=form)

    new_comment = form.save()
    if is_json:
        response = HttpResponse("OK", mimetype='text/plain')

    return _comment_list(request, article_url=article_url, author=new_comment.author)


def _comment_list(request, article_url, form=None, author=None):

    comments = models.Comment.get_comments(article_url)

    is_json = not request.META['HTTP_ACCEPT'].find("html")
    if is_json:
        comments = [ {'comment': c['comment'], "author": { "name": c['author']['name'], 'url': c['author']['url'], 'gravatar_url': c['author']['gravatar_url'] }} for c in comments ]
        return HttpResponse(json.dumps(comments, indent=4), mimetype="text/plain")

    data = request.POST
    data = dict([ (k,data[k]) for k in data.keys() ])
    data['article_url'] = article_url
    data['comment']     = None

    author = author or request.author
    if author and not (data.get('author_name') or data.get('author_email') or data.get('author_url')):
        data['author_name']  = author.name
        data['author_email'] = author.email
        data['author_url']   = author.url

    comments.sort(lambda a,b: cmp(a['created_at'], b['created_at']))

    form = form or NewCommentForm(initial=data)
    return render_to_response("api/comments.html", {'comments': comments, 'form': form, 'API_DOMAIN': request.API_DOMAIN, 'current_author': author})


def notify(request):
    comment_id = request.REQUEST.get('comment_id')
    article_url = request.REQUEST.get('article_url')

    article = models.Article.get_by_key_name(article_url)
    if not article: raise Http404

    comment_id = int(comment_id)
    comment = models.Comment.get_by_id(comment_id, parent=article)
    if not comment: raise Http404        

    padded = comment.comment
    padded = re.split(r'\r?\n', padded)
    padded = "\n".join([ "  " + line for line in padded ])

    author = comment.author

    tpl = get_template("api/email_notification.txt")
    ctx = Context({'author': author, 'comment': comment, 'padded': padded, 'API_DOMAIN': request.API_DOMAIN})
    txt = tpl.render(ctx)

    mail.send_mail(
        sender=settings.EMAIL_SENDER,
        to=settings.ADMIN_EMAIL,
        subject=author.name + " commented on your blog",
        body=txt)

    return HttpResponse("Mail sent!")


def test_page(request):
    return render_to_response("api/test_page.html", { 'API_DOMAIN': request.API_DOMAIN })


def crossdomain_xml(request):
    return HttpResponseRedirect("/static/local-policy.xml")
