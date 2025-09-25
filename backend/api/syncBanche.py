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


    

    
class BancaFornitoriSync(APIView):
    authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]
    #logger = logging.getLogger(__name__)
    #authentication_classes = [TokenAuthentication]
    #serialzer = CondizioniPagamentoserializer

    
    def post(self,request,azienda):
        if  request.user.is_authenticated:
            #return Response(" AUTENTICATO")
            

            data = json.loads(request.body)
            #with open("/srv/dev/gestione-cantieri-app/miro_backend/codpag.json", "w") as out:
            #    dataw = self.serializer(data, many=True)
            #    out.write(dataw)
            ss = SyncDataFiles()
            
            ss.tabella = 'banchefornitori'
            

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
            az = Azienda.objects.get(pk=azienda)

            for one in update:
                try:
                    f = Fornitori.objects.get(codcf=one['codfor'],azienda_id=azienda)
                except:
                    return Response(one['codfor'])
                boolobject = BancaFornitori.objects.filter(codfor=one['codfor'],fornitore=f).update(**one)
                obj = BancaFornitori.objects.get(codfor=one['codfor'],fornitore=f)
                log = SyncLog()
                log.tabella='bancafornitori'
                log.operazione='update'
                log.uniquefield='codfor'
                log.fieldvalue=one['codfor']
                log.azienda= azienda
                log.save()
                

            for one in todelete:
                try:
                    f = Fornitori.objects.get(codcf=one['codfor'],azienda_id=azienda)
                except:
                    return Response(one['codfor'])
                obj = BancaFornitori.objects.get(codfor=one['codfor'],fornitore=f)#.delete()
                log = SyncLog()
                log.tabella='bancafornitori'
                log.operazione='delete'
                log.uniquefield='codfor'
                log.fieldvalue=one['codfor']
                log.azienda= None
                log.save()
            for one in add:
                
                #one['azienda']=azienda
                #try:
                #    f = Fornitori.objects.get(codcf=one['codfor'],azienda_id=azienda)
                #except:
                #    return Response(one['codfor'])
                one['codfor']=one['codfor']+"_DEL"
                c = BancaFornitori.objects.create(**one)
                c.fornitore=f
                c.save()
                log = SyncLog()
                log.tabella='bancafornitori'
                log.operazione='add'
                log.uniquefield='codfor'
                log.fieldvalue=one['codfor']
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