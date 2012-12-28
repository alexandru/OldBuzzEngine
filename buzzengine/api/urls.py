from django.conf.urls.defaults import patterns
from buzzengine.api import views

urlpatterns = patterns('',
    (r'^test-email/$', views.send_test_email),
    (r'^test-session/$', views.test_session),
)
