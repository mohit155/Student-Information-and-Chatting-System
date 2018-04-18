from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^index.html$', views.index, name="index"),
    url(r'^login/$', views.index_login, name="index_login"),
    url(r'^logout/$', views.index_logout, name="index_logout"),
    url(r'^post/$', views.index_post, name="index_post"),
    url(r'^message/index.html$', views.index_message, name="index_message"),
    url(r'^friend/$', views.index_friend, name="index_friend"),
    url(r'^chat_sub_div/$', views.index_chat_sub_div, name="index_chat_sub_div"),
]
