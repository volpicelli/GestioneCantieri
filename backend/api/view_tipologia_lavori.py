from django.shortcuts import render
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import exceptions

from .tipologialavori_serializer import TipologiaLavoriSerializer

# Create your views here.
from home.models import TipologiaLavori

import json
from django.conf import settings

class TipologiaLavoriList(generics.ListCreateAPIView):
    queryset = TipologiaLavori.objects.all()
    serializer_class = TipologiaLavoriSerializer


class TipologiaLavoriDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TipologiaLavori.objects.all()
    serializer_class = TipologiaLavoriSerializer
    
    def destroy(self, request, pk,*args, **kwargs):
        #pk = self.kwargs.get('pk')
        object = TipologiaLavori.objects.get(pk=pk).delete() #kwargs['pk'])
        serializer = self.serializer_class(object)
        return Response({'Msg':'OK '+str(pk) +' deleted'})

    def retrieve(self, request, pk,*args, **kwargs):
        #pk = self.kwargs.get('pk')
        object = TipologiaLavori.objects.get(pk=pk) #kwargs['pk'])
        serializer = self.serializer_class(object)
        return Response(serializer.data)
