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


    

    
class BancaClientiSync(APIView):
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
            
            ss.tabella = 'bancheclienti'
            

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
                    c = Cliente.objects.get(codcf=one['codcli'],azienda_id=azienda)
                except:
                    return Response(one['codcli'])
                boolobject = BancaClienti.objects.filter(codcli=one['codcli'],cliente=c).update(**one)
                obj = BancaClienti.objects.get(codcli=one['codcli'],cliente=c)
                log = SyncLog()
                log.tabella='bancaclienti'
                log.operazione='update'
                log.uniquefield='codcli'
                log.fieldvalue=one['codcli']
                log.azienda= azienda
                log.save()
                

            for one in todelete:
                try:
                    c = Cliente.objects.get(codcf=one['codcli'],azienda_id=azienda)
                except:
                    return Response(one['codcli'])
                obj = BancaClienti.objects.get(codcli=one['codcli'],cliente=c)#.delete()
                log = SyncLog()
                log.tabella='bancaclienti'
                log.operazione='delete'
                log.uniquefield='codcli'
                log.fieldvalue=one['codcli']
                log.azienda= None
                log.save()
            for one in add:
                
                #one['azienda']=azienda
                try:
                    c = Cliente.objects.get(codcf=one['codcli'],azienda_id=azienda)
                except:
                    return Response(one['codfor'])
                one['codfor']=one['codfor']+"_DEL"
                c = BancaCliente.objects.create(**one)
                c.cliente=c
                c.save()
                log = SyncLog()
                log.tabella='bancaclienti'
                log.operazione='add'
                log.uniquefield='codcli'
                log.fieldvalue=one['codcli']
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