from django.contrib import admin
from django.urls import path,include
from django.urls import re_path
from rest_framework import permissions
from django.views.decorators.csrf import csrf_exempt
from .views import CreateAzienda

urlpatterns = [
    #path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True))),
    path('createAzienda',CreateAzienda.as_view())
    #path('email', SendEmail.as_view()),
    #re_path(r'^playground/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    #re_path(r'^docs/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc')
]
