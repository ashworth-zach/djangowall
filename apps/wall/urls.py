from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^process$', views.add), 
    url(r'^login$', views.login),
    url(r'^thewall$', views.show),
]  