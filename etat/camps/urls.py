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
    url(r'^(?P<c_id>\d+)/participants/$',
        'participant_list',
        name='participant_list'
    ),
    url(r'^participant/(?P<p_id>\d+)/$',
        'participant_edit',
        name='participant_edit'
    ),
    url(r'^participant/(?P<p_id>\d+)/delete/$',
        'participant_delete',
        name='participant_delete'
    ),
)