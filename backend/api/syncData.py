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
import json


class FornitoriSync(APIView):
    """
    json={'fornitore':2,
        'cantiere':16,
        'tipologia':'NO',
        'data_ordine':'2026-5-23',
        'damagazzino': false,
        'permagazzino': false,
        'articoli':[{'id':1,'descrizione': 'mattoni 40x40','quantita': 230,'prezzo_unitario':0.34,'preleva':12},
                    {'id': 2,'descrizione': ' seconda ','quantita': 12,'prezzo_unitario': 12.4,'preleva':4}
                    ]}

    """
    def post(self,request):
        data = json.loads(request.body)
        a=[]
        for one in data:
            b={}
            b['id']=one['id']
            b['codcf']=one['codcf']
            a.append(b)
        


        #os = Ordineserializer(o)
        return Response(json.dumps(a))