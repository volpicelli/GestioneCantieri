from django.shortcuts import render
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from django.http import FileResponse
from rest_framework.views import APIView
from rest_framework import generics
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import exceptions

from .articoli_serializer import Articoliserializer
from .azienda_serializer import Aziendaserializer
from .cantiere_serializer import Cantiereserializer
from .cliente_serializer import Clienteserializer
from home.models import Azienda,Cliente

import json
from django.conf import settings


class ClienteList(APIView):
    #azienda=Azienda.objects.get(current=True)
    #queryset = Cliente.objects.filter(azienda=azienda)
    serializer_class = Clienteserializer
    def get(self,request,azienda_id):
        if azienda_id is None:
            azienda=Azienda.objects.get(current=True)
            c = Cliente.objects.filter(azienda=azienda)
            serializer = self.serializer_class(c,many=True)
            return Response(serializer.data)

class ClienteListAll(generics.ListCreateAPIView):
    #azienda=Azienda.objects.get(current=True)
    queryset = Cliente.objects.all() #filter(azienda_id=azienda)
    serializer_class = Clienteserializer
    #def get(self,request):
    #    queryset = Cliente.objects.filter(azienda_id={{azienda}})
    #    serializer = self.serializer_class(queryset,many=True)
    #    return Response(serializer.data)
    

class ClienteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cliente.objects.all()
    serializer_class = Clienteserializer
    
    def destroy(self, request, pk,*args, **kwargs):
        #pk = self.kwargs.get('pk')
        object = Cliente.objects.get(pk=pk).delete() #kwargs['pk'])
        serializer = self.serializer_class(object)
        return Response({'Msg':'OK '+str(pk) +' deleted'})

    def retrieve(self, request, pk,*args, **kwargs):
        #pk = self.kwargs.get('pk')
        object = Cliente.objects.get(pk=pk) #kwargs['pk'])
        serializer = self.serializer_class(object)
        return Response(serializer.data)
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

class ClientePersoc(APIView):
    def get(self,request):
        c = Cliente.persoc.field.choices
    
        return Response(c)
