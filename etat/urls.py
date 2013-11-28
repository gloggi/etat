import sys

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from .api import api

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include(api.urls)),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^departments/', include('etat.departments.urls')),
    url(r'^members/', include('etat.members.urls')),
    url(r'^camps/', include('etat.camps.urls')),
    url(r'^select2/', include('django_select2.urls')),
    url(r'', include('etat.dashboard.urls')),
)

if 'runserver' in sys.argv:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += patterns('',
        url(r'^uploads/(.*)', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    )
else:
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT
        }),
    )