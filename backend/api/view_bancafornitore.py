from django.shortcuts import render
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import exceptions

from .bancafornitore_seriallizer import BancaFornitoriserializer

# Create your views here.
from home.models import BancaFornitori

import json
from django.conf import settings

class BancaFornitoriList(generics.ListCreateAPIView):
    queryset = BancaFornitori.objects.all()
    serializer_class = BancaFornitoriserializer


class BancaFornitoriDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BancaFornitori.objects.all()
    serializer_class = BancaFornitoriserializer
    
    def destroy(self, request, pk,*args, **kwargs):
        #pk = self.kwargs.get('pk')
        object = BancaFornitori.objects.get(pk=pk).delete() #kwargs['pk'])
        serializer = self.serializer_class(object)
        return Response({'Msg':'OK '+str(pk) +' deleted'})

    def retrieve(self, request, pk,*args, **kwargs):
        #pk = self.kwargs.get('pk')
        object = BancaFornitori.objects.get(pk=pk) #kwargs['pk'])
        serializer = self.serializer_class(object)
        return Response(serializer.data)
