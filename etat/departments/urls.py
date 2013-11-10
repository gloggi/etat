from django.conf.urls import patterns, url

urlpatterns = patterns('etat.departments.views',
    url(r'^data/$',
        'department_data',
        name='department_data'
    )
)