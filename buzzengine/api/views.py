# Create your views here.

from datetime import datetime
from django.http import HttpResponse
from django.core.mail import mail_admins
from django.shortcuts import render_to_response
from django.template import RequestContext

def send_test_email(request):
    mail_admins("Hello from TheBuzzEngine2", "Salut, ce mail faci?")
    return HttpResponse("OK!")

def test_session(request):
    if not request.session.has_key("hello"):
        request.session["hello"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return render_to_response(
        "api_test_session.html",
        dict(timestamp=request.session["hello"]),
        context_instance=RequestContext(request))
