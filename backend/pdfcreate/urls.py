from django.contrib import admin
from django.urls import path,include
from django.urls import re_path
from rest_framework import permissions
from .views import GeneratePDF
urlpatterns = [
    path('create',GeneratePDF.as_view())
]
