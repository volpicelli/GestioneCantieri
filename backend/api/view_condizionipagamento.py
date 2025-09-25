from django.shortcuts import render
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import exceptions

from .condizioni_pagamento_serializer import CondizioniPagamentoserializer

# Create your views here.
from home.models import CondizioniPagamento

import json
from django.conf import settings

class CondizioniPagamentoList(generics.ListCreateAPIView):
    queryset = CondizioniPagamento.objects.all()
    serializer_class = CondizioniPagamentoserializer



