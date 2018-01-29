from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^dashboard$', views.dashboard),
    url(r'^add$', views.add),
    url(r'^create$', views.create),
    url(r'^remove/(?P<id>\d+)/$', views.remove),
    url(r'^delete/(?P<id>\d+)/$', views.delete),
    url(r'^wish$', views.wish),
    url(r'^item/(?P<id>\d+)/$', views.item),
    url(r'^logout$', views.logout)
]