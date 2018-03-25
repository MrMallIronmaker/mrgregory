"""
Urls take the URLS from the http request and convert them to function calls
in the Views module.
"""

from django.conf.urls import url

from . import views

app_name = 'paperwork'
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^client_info_types/$', views.client_info_types),
    url(r'^clients/$', views.view_clients),
    url(r'^deliverables/$', views.view_deliverables),
    url(r'^new_deliverable/$', views.new_deliverable),
    url(r'^deliverable/(?P<deliverable_id>[0-9]+)/$',
        views.view_deliverable, name="deliverable"),
    url(r'^deliverable/(?P<deliverable_id>[0-9]+)/new_deadline/$',
        views.new_deadline),
    url(r'^tasks/$', views.view_tasks),
    url(r'^dpc/$', views.dpc),
    url(r'^login/$', views.login_page),
    url(r'^make_tasks/$', views.make_tasks),
    url(r'^client/(?P<client_id>[0-9]+)/$',
        views.view_client, name="client"),
    url(r'^deliverable/(?P<deliverable_id>[0-9]+)'
        r'/edit_deadline/(?P<deadline_id>[0-9]+)/$',
        views.edit_deadline),
    url(r'^edit_deliverable/(?P<deliverable_id>[0-9]+)/$',
        views.edit_deliverable)
]
