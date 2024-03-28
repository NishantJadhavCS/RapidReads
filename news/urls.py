from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("home.html", views.home, name="home"),
    path("feed.html", views.feed, name="feed"),
    path("topheadline.html", views.topheadline, name="topheadline"),
    path("inshorts.html", views.inshorts, name="inshorts"),
    path("summarize.html", views.summarizeurl, name="summarizeurl"),
]
