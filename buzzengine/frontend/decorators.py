#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__    = "Alexandru Nedelcu"
__email__     = "contact@alexn.org"


from django.conf import settings
from google.appengine.api import users
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response


def requires_admin(view):
    def f(request, *args, **kwargs):
        user = users.get_current_user()
        uri = "http://" + request.API_DOMAIN + request.get_full_path()

        if not user:
            return HttpResponseRedirect(users.create_login_url(uri))

        if not users.is_current_user_admin():
            resp = render_to_response("admin/login_required.html", {'login_url': users.create_login_url(uri), 'user': user})
            resp.status_code = 403
            return resp

        request.user = user
        return view(request, *args, **kwargs)

    return f

