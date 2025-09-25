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

from .documentifornitori_serializer import DocumentiFornitoriserializer
from home.models import DocumentiFornitori,Cantiere,Azienda,Fornitori,TipologiaDocumenti
import json,os
from django.db.models import Sum
from django.conf import settings

class DocumentiFornitoriList(generics.ListCreateAPIView):
    queryset = DocumentiFornitori.objects.all()
    serializer_class = DocumentiFornitoriserializer
    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        #for one in serializer.data:
        #    c=Cantiere.objects.get(pk=one['cantiere'])
        #    a=c.cliente.azienda
        #    one['aziendaSS']=a.id
        return Response(serializer.data)

class DocumentiFornitoriCantiere(APIView):
    serializer_class = DocumentiFornitoriserializer
    

    def get(self,request,cantiere_id):
        c = Cantiere.objects.get(pk=cantiere_id)
        d=c.cantiere_documentifornitori.all()
        
        serializer = self.serializer_class(d,many=True)
        return Response(serializer.data)


class DocumentiFornitoriDelete(APIView):
    queryset = DocumentiFornitori.objects.all()
    serializer_class = DocumentiFornitoriserializer
    
    def delete(self, request, pk,*args, **kwargs):
        #pk = self.kwargs.get('pk')
        object = DocumentiFornitori.objects.get(pk=pk)#.delete() #kwargs['pk'])
        #serializer = self.serializer_class(object)
        if object.media:
            if os.path.exists(object.get_media_path):            
                os.remove(object.get_media_path)
                #print(f"File '{file_path}' deleted successfully.")
                objid = object.id
                object.delete()
                msg = "Documento %s rimosso e file   %s  cancellato" % (objid,object.get_media_path)
                return Response({'Msg':msg})
        msg = "File  non trovato. Documento %s rimosso dal database" % (object.id)
        object.delete()

        return Response({'Msg':msg})
        

class DocumentiFornitoriDetail(APIView):
    #queryset = DocumentiFornitori.objects.all()
    serializer_class = DocumentiFornitoriserializer
    def get(self, request, pk,*args, **kwargs):
            #pk = self.kwargs.get('pk')
            object = DocumentiFornitori.objects.get(pk=pk) #kwargs['pk'])
            serializer = self.serializer_class(object)
            return Response(serializer.data)
"""
class DocumentiFornitoriDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DocumentiFornitori.objects.all()
    serializer_class = DocumentiFornitoriserializer
    
    def destroy(self, request, pk,*args, **kwargs):
        #pk = self.kwargs.get('pk')
        object = DocumentiFornitori.objects.get(pk=pk).delete() #kwargs['pk'])
        #serializer = self.serializer_class(object)
        return Response({'Msg':'OK '+str(pk) +' deleted'})

    def retrieve(self, request, pk,*args, **kwargs):
        #pk = self.kwargs.get('pk')
        object = DocumentiFornitori.objects.get(pk=pk) #kwargs['pk'])
        serializer = self.serializer_class(object)
        return Response(serializer.data)

"""

class DocumentiFornitoriCreate(APIView):
    serializer_class = DocumentiFornitoriserializer

    def post(self,request,cantiere_id):
        data = json.loads(request.body)
        #data['pollo']='POLLO'
        #fornitore_id = request.POST.get('fornitore',None)
        #tipologia = request.POST.get('tpologia',None)

        #f = Fornitori.objects.get(pk=fornitore_id)
        df_id=[]
        c = Cantiere.objects.get(pk=cantiere_id)
        for one in data['documenti']:
            fornitore_id = one['fornitore']
            try:
                td = TipologiaDocumenti.objects.get(descrizione=one['tipologia'])
                
                td_duplicato = DocumentiFornitori.objects.get(cantiere=c,fornitore=Fornitori.objects.get(pk=fornitore_id),tipologia=td)
                if td_duplicato:
                        raise exceptions.ValidationError({"errore":f"Documento già esistente per fornitore {td_duplicato.fornitore} con tipologia {td_duplicato.tipologia}"})
            except ObjectDoesNotExist :
                td = TipologiaDocumenti(descrizione=one['tipologia'])
                td.save()
            
            caricato_da = one.get('caricato_da',None)
            note = one.get('note',None)

            df = DocumentiFornitori()
            df.cantiere = c 
            df.fornitore = Fornitori.objects.get(pk=fornitore_id)
            df.tipologia = td #one['tipologia]']
            df.caricato_da = caricato_da
            df.note = note
            df.save()
            df_id.append(df.id)

        alldf = DocumentiFornitori.objects.filter(pk__in=df_id)
            
        serializer = self.serializer_class(alldf,many=True)
        
        return Response(serializer.data)
       
class UploadDocumentoFornitore(APIView):
    serializer_class = DocumentiFornitoriserializer


    def post(self,request,doc_id):
        file = request.FILES.get('file')
        #tipologia_doc = request.POST.get('tipologia_documento',None)
        caricato_da = request.POST.get('caricato_da',None)
        note = request.POST.get('note',None)

        d = DocumentiFornitori.objects.get(id=doc_id)
        #d = ModelWithFileField(file_field=request.FILES["file"])
        #instance.save()
        
        d.media=file
        d.caricato_da = caricato_da
        d.note = note

        d.save()

        serializer = self.serializer_class(d)

        return Response(serializer.data)
    
   
"""
class DocumentiCreate(APIView):
    serializer_class = Documentiserializer

    def post(self,request,cantiere_id):
        data = json.loads(request.body)
        #data['pollo']='POLLO'
        id = Cantiere.objects.get(pk=cantiere_id)
        for one in data['documenti']:
            d = Documenti(tipologia_id=one['tipologia'],cantiere=id)

            d.save()
            one['data']=d.data_inserimento
            one['id'] = d.id
        serializer = self.serializer_class(Documenti.objects.filter(cantiere=id),many=True)
        
        return Response(serializer.data)


class DocumentiList(generics.ListCreateAPIView):
    queryset = Documenti.objects.all()
    serializer_class = Documentiserializer
    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        for one in serializer.data:
            c=Cantiere.objects.get(pk=one['cantiere'])
            a=c.cliente.azienda
            one['aziendaSS']=a.id
        return Response(serializer.data)

class DocumentiDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Documenti.objects.all()
    serializer_class = Documentiserializer
    
    def destroy(self, request, pk,*args, **kwargs):
        #pk = self.kwargs.get('pk')
        object = Documenti.objects.get(pk=pk).delete() #kwargs['pk'])
        serializer = self.serializer_class(object)
        return Response({'Msg':'OK '+str(pk) +' deleted'})

    def retrieve(self, request, pk,*args, **kwargs):
        #pk = self.kwargs.get('pk')
        object = Documenti.objects.get(pk=pk) #kwargs['pk'])
        serializer = self.serializer_class(object)
        return Response(serializer.data)
    
class DocumentiCantiere(APIView):
    serializer_class = Documentiserializer

    def get(self,request,cantiere_id):
        c = Cantiere.objects.get(pk=cantiere_id)
        d=c.cantiere_documenti.all()
        
        serializer = self.serializer_class(d,many=True)
        return Response(serializer.data)


class DocumentiAzienda(APIView):
    serializer_class = Documentiserializer

    def get(self,request,azienda_id):
        a = Azienda.objects.get(pk=azienda_id)
        clienti = a.azienda_cliente.all()
        #serialzer = self.serializer_class(clienti,many=True)
        resp = []
        
        for one in clienti:
            cantieri = one.cliente_cantiere.all()
            for c in cantieri:
                d=c.cantiere_documenti.all()
                serializer = self.serializer_class(d,many=True)
                resp.append(serializer.data)

            
        return Response(resp)
        

"""
