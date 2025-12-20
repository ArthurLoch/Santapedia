from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path('<slug:slug>/', views.article_detail, name='article_detail'),
]
