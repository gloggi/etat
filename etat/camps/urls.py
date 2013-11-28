from django.conf.urls import patterns, url

urlpatterns = patterns('etat.camps.views',
    url(r'^$',
        'camp_list',
        name='camp_list'
    ),
    url(r'^(?P<c_id>\d+)/$',
        'camp_edit',
        name='camp_edit',
    ),
)