#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__    = "Alexandru Nedelcu"
__email__     = "contact@alexn.org"


from google.appengine.api import mail
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse, Http404
from django.conf import settings
from buzzengine.api import models


def notify(request):
    comment_id = request.REQUEST.get('comment_id')
    article_url = request.REQUEST.get('article_url')

    article = models.Article.get_by_key_name(article_url)
    if not article: raise Http404

    comment_id = int(comment_id)
    comment = models.Comment.get_by_id(comment_id, parent=article)
    if not comment: raise Http404        

    author = comment.author

    tpl = get_template("api/email_notification.txt")
    ctx = Context({'author': author, 'article_url': article_url, 'comment': comment, 'API_DOMAIN': request.API_DOMAIN})
    txt = tpl.render(ctx)

    mail.send_mail(
        sender=settings.EMAIL_SENDER,
        to=settings.ADMIN_EMAIL,
        subject=author.name + " commented on your blog",
        body=txt)

    return HttpResponse("Mail sent!")
