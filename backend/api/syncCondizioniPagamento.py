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
from rest_framework.authentication import TokenAuthentication
from home.models import *
import json
import logging


    

    
class CondizioniPagamentoSync(APIView):
    authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]
    #logger = logging.getLogger(__name__)
    #authentication_classes = [TokenAuthentication]
    #serialzer = CondizioniPagamentoserializer

    
    def post(self,request):
        if  request.user.is_authenticated:
            #return Response(" AUTENTICATO")
            

            data = json.loads(request.body)
            #with open("/srv/dev/gestione-cantieri-app/miro_backend/codpag.json", "w") as out:
            #    dataw = self.serializer(data, many=True)
            #    out.write(dataw)
            ss = SyncDataFiles()
            
            ss.tabella = 'CondizioniPagamento'
            

            update = data['to_update']
            lenupd = len(update)
            add = data['to_add']
            lenadd=len(add)
            todelete = data['to_delete']
            lendel = len(todelete)
            aa=[]
            ss.json_update = update
            ss.json_delete = todelete
            ss.json_add = add
            ss.save()
            
            for one in update:
                
                boolobject = CondizioniPagamento.objects.filter(codpag=one['codpag']).update(**one)
                obj = CondizioniPagamento.objects.get(codpag=one['codpag'])
                log = SyncLog()
                log.tabella='CondizioniPagamento'
                log.operazione='update'
                log.uniquefield='codpag'
                log.fieldvalue=one['codpag']
                log.azienda= None
                log.save()
                

            for one in todelete:
                obj = CondizioniPagamento.objects.get(codpag=one['codpag'])#.delete()
                log = SyncLog()
                log.tabella='CondizioniPagamennto'
                log.operazione='delete'
                log.uniquefield='codpag'
                log.fieldvalue=one['codpag']
                log.azienda= None
                log.save()
            for one in add:
                one['codpag']=one['codpag']+"_DEL"
                #one['azienda']=azienda

                c = CondizioniPagamento.objects.create(**one)
                c.save()
                log = SyncLog()
                log.tabella='CondizioniPagamento'
                log.operazione='add'
                log.uniquefield='codpag'
                log.fieldvalue=one['codpag']
                log.azienda= None
                log.save()
                
            
            g={}
            g['to_add'] = "Added %d entries " %lenadd
            #aa.append(g)
            g['to_update'] = "Updated %d entries " %lenupd
            #aa.append(g)
            g['to_delete'] = "Deleted %d entries " %lendel
            aa.append(g)

            #os = Ordineserializer(o)
            return Response(aa)
        else:
            return Response(" NO AUTENTICATO")