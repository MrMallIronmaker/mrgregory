from django.conf.urls import url

from . import views

app_name = 'paperwork'
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^client_info_types/$', views.client_info_types),
    url(r'^clients/$', views.clients),
    url(r'^deliverables/$', views.deliverables),
    url(r'^new_deliverable/$', views.new_deliverable),
    url(r'^deliverable/(?P<deliverable_id>[0-9]+)/$', views.view_deliverable, name="deliverable"),
    url(r'^tasks/$', views.tasks),
    url(r'^dpc/$', views.dpc),
]