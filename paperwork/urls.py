"""
Urls take the URLS from the http request and convert them to function calls
in the Views module.
"""

from django.conf.urls import url

from . import views

app_name = 'paperwork'
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^client_info_types/$', views.client_info_types, name='cit'),
    url(r'^clients/$', views.view_clients, name='clients'),
    url(r'^deliverables/$', views.view_deliverables, name='deliverables'),
    url(r'^new_deliverable/$', views.new_deliverable, name='new_deliverable'),
    url(r'^deliverable/(?P<deliverable_id>[0-9]+)/$',
        views.view_deliverable, name="deliverable"),
    url(r'^deliverable/(?P<deliverable_id>[0-9]+)/new_deadline/$',
        views.new_deadline, name="new_deadline"),
    url(r'^tasks/$', views.view_tasks, name="tasks"),
    url(r'^dpc/$', views.dpc, name="dpc"),
    url(r'^login/$', views.login_page, name='login'),
    url(r'^make_tasks/$', views.make_tasks),
    url(r'^client/(?P<client_id>[0-9]+)/$',
        views.view_client, name="client"),
    url(r'^deliverable/(?P<deliverable_id>[0-9]+)'
        r'/edit_deadline/(?P<deadline_id>[0-9]+)/$',
        views.edit_deadline, name="edit_deadline"),
    url(r'^edit_deliverable/(?P<deliverable_id>[0-9]+)/$',
        views.edit_deliverable, name="edit_deliverable"),
    url(r'^tasks/complete/(?P<task_id>[0-9]+)/$', views.complete_task,
        name="complete_task"),
    url(r'^completed_tasks/$', views.completed_tasks, name="completed_tasks"),
    url(r'^tasks/uncomplete/(?P<task_id>[0-9]+)/$', views.uncomplete_task,
        name="uncomplete_task"),
]
