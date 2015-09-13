from django.shortcuts import render
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.homePage, name="homePage"),
    url(r'^userAdmin/$', views.addUserProfile, name="addUserProfile"),
    url(r'^appAdmin/$', views.addUser, name="addUser"),
]