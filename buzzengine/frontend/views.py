#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__    = "Alexandru Nedelcu"
__email__     = "contact@alexn.org"


import hashlib
import re

from datetime import datetime, timedelta
from django.utils import simplejson as json

from django.shortcuts import render_to_response
from buzzengine.api import models

def homepage(request):
    return render_to_response("homepage.html")
