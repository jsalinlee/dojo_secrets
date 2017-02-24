from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^success$', views.success),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^post_secret$', views.post_secret),
    url(r'^like/(?P<secret_id>\d+)$', views.like),
    url(r'^del_like/(?P<secret_id>\d+)$', views.del_like),
    url(r'^most_liked$', views.most_liked),
    url(r'^.*$', views.nonsense)
]
