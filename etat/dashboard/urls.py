from django.conf.urls import patterns, url

from .views import *

urlpatterns = patterns('',
    url(r'^$',
        home,
        name='dashboard_home'
    ),
)
