from django.conf.urls import patterns, url

urlpatterns = patterns('etat.members.views',
    url(r'^$',
        'member_list',
        name='member_list'
    ),
    url(r'^data/$',
        'member_data',
        name='member_data'
    ),
    url(r'^add/$',
        'member_add',
        name='member_add'
    ),
    url(r'^(?P<m_id>\d+)/$',
        'member_view',
        name='member_view',
    ),
    url(r'^(?P<m_id>\d+)/edit/$',
        'member_edit',
        name='member_edit'
    ),
    url(r'^(?P<m_id>\d+)/delete/$',
        'member_delete',
        name='member_delete'
    ),
)
