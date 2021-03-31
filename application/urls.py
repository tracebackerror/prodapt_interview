from django.contrib import admin
from django.urls import path
from django.urls import include 

from . import views

urlpatterns = [
    path('ping', views.ping, name='ping'),
    path('etl', views.ETLView.as_view(), name='etl'),
    path('wipe', views.WipeView.as_view(), name='wipe'),
    path('', views.PostListView.as_view(), name='display'),
]