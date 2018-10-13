"""
    This file will determine what view any particular URL
    will map to.
"""
from django.conf.urls import url

from . import views

app_name = 'IndrasNet'


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^ab_models/*$', views.ab_models, name='ab_models'),
    url(r'^parameters/*$', views.parameters, name='parameters'),
    url(r'^run/*$', views.run, name='run'),
    url(r'^help/*$', views.help_page, name='help'),
    url(r'^feedback/*$', views.feedback, name='feedback'),
    url(r'^about/*$', views.about, name='about')
]
