from django.shortcuts import render
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from django.http import FileResponse
from django.db.models import Sum,Count

from rest_framework.views import APIView
from rest_framework import generics
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import exceptions
from .cantiere_serializer import Cantiereserializer
from .ordine_serializer import Ordineserializer
from .fatture_serializer import Fattureserializer
from .documenti_serializer import Documentiserializer
from .documentifornitori_serializer import DocumentiFornitoriserializer
from .fornitori_serializer import Fornitoriserializer
from .costocantiere_serializer import Costo_Cantiereserializer
from home.models import Cantiere,Azienda,Cliente,Fatture,Ordine,DocumentiFornitori
import json
from django.conf import settings

   
class CantieriAzienda(APIView):
    serializer_class = Cantiereserializer

    #def get(self,request,id_cliente,id_azienda):
    def get(self,request,azienda_id):
        #azienda=Azienda.objects.get(current=True)

        clienti=Cliente.objects.filter(azienda_id=azienda_id)
        tutticantieri = []
        for one in clienti:
            try:
                cantiere = Cantiere.objects.filter(cliente=one)
                for o in cantiere:
                    tutticantieri.append(o)
            except ObjectDoesNotExist:
                pass


        serializer = self.serializer_class(tutticantieri,many=True)
        return Response(serializer.data)

class CantiereList(generics.ListCreateAPIView):
    #azienda=Azienda.objects.get(current=True)
    queryset = Cantiere.objects.all()
    serializer_class = Cantiereserializer



class CantiereDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cantiere.objects.all()
    serializer_class = Cantiereserializer
    
    def destroy(self, request, pk,*args, **kwargs):
        #pk = self.kwargs.get('pk')
        object = Cantiere.objects.get(pk=pk).delete() #kwargs['pk'])
        serializer = self.serializer_class(object)
        return Response({'Msg':'OK '+str(pk) +' deleted'})

    def retrieve(self, request, pk,*args, **kwargs):
        #pk = self.kwargs.get('pk')
        object = Cantiere.objects.get(pk=pk) #kwargs['pk'])
        serializer = self.serializer_class(object)
        return Response(serializer.data)
    
class OrdiniCantiere(APIView):
    serializer_class = Ordineserializer

    def get(self,request,id_cantiere):
        c = Cantiere.objects.get(pk=id_cantiere)
        o = c.cantiere_ordine.all()
        serializer = self.serializer_class(o,many=True)

        return Response(serializer.data)
    
class CantiereDocumenti(APIView):
    serializer_class = Documentiserializer

    def get(self,request,id_cantiere):
        c = Cantiere.objects.get(pk=id_cantiere)
        d = c.cantiere_documenti.all()
        serializer = self.serializer_class(d,many=True)

        return Response(serializer.data)

class CantiereDocumentiFornitori(APIView):
    serializer_class = DocumentiFornitoriserializer

    def get(self,request,id_cantiere,id_fornitore):
        df = DocumentiFornitori.objects.filter(cantiere_id=id_cantiere,fornitore_id=id_fornitore)
        serializer = self.serializer_class(df,many=True)

        return Response(serializer.data)

class CantiereFornitori(APIView):
    serializer_class = Fornitoriserializer

    def get(self,request,id_cantiere):
        c = Cantiere.objects.get(pk=id_cantiere)
        o = c.cantiere_ordine.all()
        f=set()
        for one in o:
            f.add(one.fornitore)
        fornitori=[]
        for one in f:
            fornitori.append(one)

        serializer = self.serializer_class(fornitori,many=True)

        return Response(serializer.data)

class CantiereCosto(APIView):
       
       def get(self,request,id_cantiere):
        cantiere = Cantiere.objects.get(pk=id_cantiere)
        ordini = cantiere.GetOrdini()
        #fatture = cantiere.GetFatture()
        personaleassegnato = cantiere.cantiere_assegnato.all()
        pa = Costo_Cantiereserializer(personaleassegnato,many=True)
        totale=0
        for one in personaleassegnato:
            tot = float(one.ore_lavorate * one.personale.wage_lordo)
            totale+=tot

        resptot = {}
        resptot['CostoPersonale'] = pa.data
        

        context ={}
        #context['fatture']= fatture
        context['cantiere']= cantiere
        context['ordini']= ordini
        
        resptot['CostoOrdini']= [] #Ordine.tipologia.field.choices

        tipologia_ordini =  Ordine.tipologia.field.choices
        for one in tipologia_ordini:
            ct = {}
            im = ordini.filter(tipologia=one[0]).aggregate(Sum('importo'),count=Count('id'))
            ct['tipologia'] = one[0] #,one[1]]
            ct['importo']=im['importo__sum']
            ct['n_ordini'] = str(im['count'])
            resptot['CostoOrdini'].append(ct)

       
        return Response(resptot)