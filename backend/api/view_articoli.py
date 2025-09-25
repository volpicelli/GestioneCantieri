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
from home.models import Articoli,Ordine,Magazzino
import json
from django.db.models import Sum
from django.conf import settings
class ArticoliList(generics.ListCreateAPIView):
    queryset = Articoli.objects.all()
    serializer_class = Articoliserializer

class ArticoliDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Articoli.objects.all()
    serializer_class = Articoliserializer
    
    def destroy(self, request, pk,*args, **kwargs):
        #pk = self.kwargs.get('pk')
        object = Articoli.objects.get(pk=pk)#.delete() #kwargs['pk'])
        #ordine =  object.ordine
        if object.ordine.completato:
            raise exceptions.ValidationError('Impossibile eliminare un articolo di un ordine completato')
        if object.ordine.damagazzino:
            # Bisogna sottrare la quantita' impegnata al magazzino
            if object.quantita > 0:
                m = Magazzino.objects.get(descrizione=object.descrizione,azienda=object.ordine.azienda)
                m.quantita_impegnata -= object.quantita
                m.save()
                
        if object.ordine.permagazzino:
            # Bisogna sottrarre la quantita' in arrivo al magazzino
            if object.quantita > 0:
                m = Magazzino.objects.get(descrizione=object.descrizione,azienda=object.ordine.azienda)
                m.quantita_inarrivo -= object.quantita
                m.save()
                
        object.delete() #kwargs['pk'])

        #serializer = self.serializer_class(object)
        return Response({'Msg':'OK '+str(pk) +' deleted'})

    def retrieve(self, request, pk,*args, **kwargs):
        #pk = self.kwargs.get('pk')
        object = Articoli.objects.get(pk=pk) #kwargs['pk'])
        serializer = self.serializer_class(object)
        return Response(serializer.data)
    
    def put(self, request, pk,*args, **kwargs):
        #pk = self.kwargs.get('pk')
        object = Articoli.objects.get(pk=pk)
        serializer = self.serializer_class(object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
class ArticoliOrdine(APIView):
    serializer_class = Articoliserializer

    def get(self,request,id_ordine):
        o = Ordine.objects.get(pk=id_ordine)
        a = o.ordine_articoli.all()
        serializer = self.serializer_class(a,many=True)
        return Response(serializer.data)


class GroupArticoli(APIView):
    def get(self,request):
        articoli = Articoli.objects.values('descrizione').annotate(totale=Sum('importo_totale'),quantita=Sum('quantita'))
        res=[]
        for one in articoli:
            a={}
            a['descrizione']=one['descrizione']
            a['totale'] = one['totale']
            a['quantita'] = one['quantita']
            res.append(a)

        return Response(res  )