from django.shortcuts import render
#from rest_framework.parsers import JSONParser
from rest_framework.response import Response
#from rest_framework import status
#from django.http import FileResponse
from rest_framework.views import APIView
from rest_framework import generics
#from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import exceptions

from .articoli_serializer import Articoliserializer
#from .azienda_serializer import Aziendaserializer
#from .cantiere_serializer import Cantiereserializer
##from .cliente_seriallizer import Clienteserializer
#from .fatture_serializer  import Fattureserializer
#from .fornitori_serializer import Fornitoriserializer
from .ordine_serializer import Ordineserializer
#from .magazzino_serializer import Magazzinoserializer
from .ordineupdate_serializer import OrdineUpdateserializer
#from .assegnato_cantiere_serializer import Assegnato_CantiereSerializer


from home.models import Cantiere,Articoli,Fatture,Fornitori,Ordine,Personale,TipologiaLavori,Assegnato_Cantiere,Magazzino,\
                        Documenti

import json
from django.db.models import Sum
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated



class OrdineGetTipologia(APIView):
    def get(self,request):
        o = Ordine.tipologia.field.choices
        return Response(o)


class CloseOrdineCreate(APIView):
    serializer_class = Ordineserializer

    def get(self,request,ordine_id):
        #data = json.loads(request.body)

        o = Ordine.objects.get(pk=ordine_id)
        if o.completato:
            return Response({'Messaggio':'Ordine completato e chiuso'})
        az = o.azienda

        ar = o.ordine_articoli.all()

        if o.permagazzino:
            for one in ar:
                m = Magazzino.objects.get(azienda=az,descrizione=one.descrizione)
                m.quantita += one.quantita

                m.quantita_inarrivo -= one.quantita
                if m.quantita_inarrivo < 0:
                    m.quantita_inarrivo=0
                if m.prezzo_unitario > 0:
                    m.prezzo_unitario = (m.prezzo_unitario + one.prezzo_unitario) / 2
                else:
                    m.prezzo_unitario = one.prezzo_unitario
                m.importo_totale = m.quantita *  m.prezzo_unitario
                m.save()
            o.completato = True
            o.save()
        if o.damagazzino:
            for one in ar:
                m = Magazzino.objects.get(azienda=az,descrizione=one.descrizione)
                m.quantita -= one.quantita
                m.quantita_impegnata -= one.quantita
                #m.prezzo_unitario = (m.prezzo_unitario + one.prezzo_unitario) / 2
                m.importo_totale = m.quantita *  m.prezzo_unitario
                m.save()
            o.completato =True
            o.save()
        if o.permagazzino is False and o.damagazzino is False:
            o.completato = True
            o.save()
        return Response({'success':True})


        



class OrdineCreate(APIView):
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
        
        #return Response(data)
        # If data['permagazzino'] == True
        # Ordine da fornitore esterno per riempire il magazzino

        # if data['damagazzino'] == True
        # ordine per un cantiere con materiale preso dal Magazzino

        # data['permagazzino'] == False e data['damagazzino'] == False
        # Ordine normale da fornitore per un cantiere

        # Tipologia qualsiasi

        damagazzino = False
        #if 'damagazzino' not in data or data['damagazzino'] == False:
        
        if 'damagazzino' in data.keys() :
            if data['damagazzino'] == True:
        
                damagazzino = True
                try:
                    c  = Cantiere.objects.get(pk=data['cantiere'])
                    # Il Fornitore e' l'azienda stessa
                    f = Fornitori.objects.get(pk=data['fornitore'])
                    azienda  = c.cliente.azienda

                except ObjectDoesNotExist:
                    error_msg=" Fornitore non esiste"
                    return Response(error_msg)

        permagazzino = False
        if 'permagazzino' in data.keys():
            if data['permagazzino']== True:
                permagazzino = True

                try:
                    c  = None # Cantiere.objects.get(pk=data['cantiere'])
                    f = Fornitori.objects.get(pk=data['fornitore'])
                    azienda = f.azienda
                except ObjectDoesNotExist:
                    error_msg=" Fornitore non esiste"
                    return Response(error_msg)#,safe=False)
        
    # Ordine.TipologiaFornitore.choices
    # [('SE', 'Servizio'), ('MA', 'Materiale'), ('NO', 'Noleggio')]

        if permagazzino == False and damagazzino == False:
            c  = Cantiere.objects.get(pk=data['cantiere'])
            f  = Fornitori.objects.get(pk=data['fornitore'])
            azienda  = c.cliente.azienda
        
        if len(data['tipologia']) > 2:
            data['tipologia']=data['tipologia'][:2]
        o = Ordine( cantiere=c,
                    fornitore=f,
                    data_ordine=data['data_ordine'],
                    data_consegna = data['data_consegna'],
                    permagazzino=permagazzino,
                    damagazzino= damagazzino, 
                    tipologia= data['tipologia'], 
                    azienda=azienda,
                    completato=False
                    )
        o.save()
        importo = 0.0
        # Preleva materiale dal Magazzino
        if damagazzino: 
            for one in data['articoli']:
                a = Articoli()
                a.ordine=o
                a.descrizione=one['descrizione']
                a.quantita = one['preleva']
                a.prezzo_unitario = one['prezzo_unitario']
                a.importo_totale = round(int(one['preleva']) * float(one['prezzo_unitario']),2)
                importo += a.importo_totale
                a.save()
                m = Magazzino.objects.get(pk=one['id']) 
                #m.quantita = m.quantita - a.quantita
                m.quantita_impegnata += a.quantita
                #m.ordine=o
                m.save()
            o.importo = importo
            o.save()
            
            # Ordina  materiale per il  Magazzino
        elif permagazzino: 
            for one in data['articoli']:
                a = Articoli()
                a.ordine=o
                a.descrizione=one['descrizione']
                a.quantita = one['quantita']
                a.prezzo_unitario = one['prezzo_unitario']
                a.importo_totale = round(int(one['quantita']) * float(one['prezzo_unitario']),2)
                importo += a.importo_totale
                a.save()
                try:
                    m = Magazzino.objects.get(azienda=azienda,descrizione=one['descrizione'])
                    #if m.exists():
                    #m.quantita = m.quantita+a.quantita
                    #m.prezzo_unitario = (m.prezzo_unitario + a.prezzo_unitario)/2
                    m.quantita_inarrivo += a.quantita 
                    m.save()
                except:
                    m = Magazzino()
                    m.descrizione = a.descrizione
                    m.quantita = 0 #a.quantita
                    #m.prezzo_unitario = a.prezzo_unitario
                    #m.importo_totale = a.importo_totale
                    #m.ordine=o
                    m.quantita_impegnata=0
                    m.azienda=f.azienda
                    m.quantita_inarrivo = 0 
                    m.save()
                    m.quantita_inarrivo += a.quantita 
                    m.save()
            o.importo = importo
            o.save()
        
        else: 
            for one in data['articoli']:
                a = Articoli()
                a.ordine=o
                a.descrizione=one['descrizione']
                a.quantita = one['quantita']
                a.prezzo_unitario = one['prezzo_unitario']
                a.importo_totale = round(int(one['quantita']) * float(one['prezzo_unitario']),2)
                importo += a.importo_totale
                a.save()
            o.importo = importo
            o.save()
        
        
        os = Ordineserializer(o)
        return Response(os.data)#,safe=False)

        #    os = Ordineserializer(o)

class OrdineUpdate(APIView):
    serializer_class = Ordineserializer

    def get(self,request,ordine_id):
        o = Ordine.objects.get(pk=ordine_id)
        ar = o.ordine_articoli.all()
        serializer = self.serializer_class(o)
        #serializer.data['articoli'] =[]
        a=[]
        #ars = Articoliserializer(ar,many=True)
        for one in ar:
            ars = Articoliserializer(one)
            a.append(ars.data)
        #serializer.data['articoli']=a
        resp = {}
        resp['ordine']=serializer.data
        resp['articoli'] = a
        return Response(resp)
    
    #def post(self,request):
    def put(self, request, ordine_id,*args, **kwargs):
        #pk = self.kwargs.get('pk')
        
        data = json.loads(request.body)
        ordine = Ordine.objects.get(pk=ordine_id)
        f = Fornitori.objects.get(pk=data['fornitore'])

        # o = Ordine( cantiere=c,
        ordine.fornitore=f
        ordine.data_ordine=data['data_ordine']
        ordine.data_consegna = data['data_consegna']
        #            permagazzino=permagazzino,
        #           damagazzino= damagazzino, 
        ordine.tipologia= data['tipologia']
        #            azienda=azienda,
        #            completato=False
        #            )
        ordine.save()
        old_object = ordine
        articoli = ordine.ordine_articoli.all()
        if 'articoli' in data.keys(): 
            if not ordine.permagazzino and not ordine.damagazzino:
                # Ordine da fornitore a cantiere
                #               Devo solo modificare l'
                # Eliminare gli articoli esistenti nel DB
                # Inserire quelli nuovi

                for articolo in articoli:
                    articolo.delete()
                importo = 0.0
                for one in data['articoli']:
                        a = Articoli()
                        a.ordine=ordine
                        a.descrizione=one['descrizione']
                        a.quantita = one['quantita']
                        a.prezzo_unitario = one['prezzo_unitario']
                        a.importo_totale = round(int(one['quantita']) * float(one['prezzo_unitario']),2)
                        importo += a.importo_totale
                        a.save()
                ordine.importo = importo
                c  = Cantiere.objects.get(pk=data['cantiere'])
                ordine.cantiere = c
                ordine.save()
            
            # ORDINE DA MAGAZZINO A CANTIERE
            # loopare sugli articoli
            #              cercare l'articolo nel magazzino con la descrizione
            #           togliere la quantita articolo da quantita_impegnata 
            #            eliminare l' articolo esistente nel DB

            #              Inserire quelli nuovi

            if  ordine.damagazzino:

                for articolo in articoli:
                    m = Magazzino.objects.get(azienda=ordine.azienda,descrizione=articolo.descrizione)
                    m.quantita_impegnata -= articolo.quantita
                    m.save()
                    articolo.delete()

                importo = 0.0
                for one in data['articoli']:
                        a = Articoli()
                        a.ordine=ordine
                        a.descrizione=one['descrizione']
                        a.quantita = one['quantita']
                        a.prezzo_unitario = one['prezzo_unitario']
                        a.importo_totale = round(int(one['quantita']) * float(one['prezzo_unitario']),2)
                        importo += a.importo_totale
                        a.save()
                        m = Magazzino.objects.get(azienda=ordine.azienda,descrizione=a.descrizione)
                        m.quantita_impegnata += a.quantita
                        m.save()
                ordine.importo = importo
                c  = Cantiere.objects.get(pk=data['cantiere'])
                ordine.cantiere = c
                ordine.save()

            # ORDINE DA FORNITORE A MAGAZZINO
            #loopare sugli articoli
            #              cercare l'articolo nel magazzino con la descrizione
            #           togliere la quantita articolo da quantita_inarrivo 
            #            eliminare l' articolo esistente nel DB
            #              Inserire quelli nuovi



            if  ordine.permagazzino:

                for articolo in articoli:
                    m = Magazzino.objects.get(azienda=ordine.azienda,descrizione=articolo.descrizione)
                    m.quantita_inarrivo -= articolo.quantita
                    m.save()
                    articolo.delete()

                importo = 0.0
                for one in data['articoli']:
                        a = Articoli()
                        a.ordine=ordine
                        a.descrizione=one['descrizione']
                        a.quantita = one['quantita']
                        a.prezzo_unitario = one['prezzo_unitario']
                        a.importo_totale = round(int(one['quantita']) * float(one['prezzo_unitario']),2)
                        importo += a.importo_totale
                        a.save()
                        m = Magazzino.objects.get(azienda=ordine.azienda,descrizione=a.descrizione)
                        m.quantita_inarrivo +=  int(one['quantita'])
                        m.save()
                ordine.importo = importo
                ordine.save()

        articoli = ordine.ordine_articoli.all()
        resp={}

        serializer_ordine = self.serializer_class(ordine)#, data=request.data)
        serializer_articoli  = Articoliserializer(articoli,many=True)
        #if serializer_ordine.is_valid():
        resp['ordine'] = serializer_ordine.data
        #else:
        #    return Response(serializer_ordine.errors, status=400)
        #if serializer_articoli.is_valid():
        resp['articoli'] = serializer_articoli.data
        resp['PROVA'] = 'PROVA'

        #else:
        #   return Response(serializer_articoli.errors, status=400)
        
       
       
        #resp['data'] = data


        return Response(resp)

        
        #o = Ordine.objects.get(pk=serializer.data['ordine'])
        # Ordine da fornitore a cantiere
        #               Devo solo modificare l'articolo

        # ORDINE DA MAGAZZINO A CANTIERE
        #               Devo modificare l'articolo il magazzino e l'ordine


        # ORDINE DA FORNITORE A MAGAZZINO
        #               Devo modificare l'articolo il magazzino e l'ordine
        
        
        #m = Magazzino.objects.get(azienda=o.azienda)
        #if o.stato == 'C':
        #    raise exceptions.ValidationError('Impossibile modificare l\'articolo, ordine già chiuso')
        
        #if o.damagazzino:


             
class OrdineList(generics.ListCreateAPIView):
    queryset = Ordine.objects.all()
    serializer_class = Ordineserializer

    

class OrdineDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ordine.objects.all()
    serializer_class = Ordineserializer
    
    def destroy(self, request, pk,*args, **kwargs):
        #pk = self.kwargs.get('pk')
        object = Ordine.objects.get(pk=pk)# .delete() #kwargs['pk'])
        if object.completato:
            raise exceptions.ValidationError('Impossibile eliminare l\'ordine, ordine già chiuso')
        if object.damagazzino:
            articoli = object.ordine_articoli.all()
            for one in articoli:
                m = Magazzino.objects.get(azienda=object.azienda,descrizione=one.descrizione)
                m.quantita_impegnata -= one.quantita
                m.save()
                one.delete()
        elif object.permagazzino:
            articoli = object.ordine_articoli.all()
            for one in articoli:
                m = Magazzino.objects.get(azienda=object.azienda,descrizione=one.descrizione)
                m.quantita_inarrivo -= one.quantita
                m.save()
                one.delete()
        
        if object.damagazzino is False and object.permagazzino is False:
            articoli = object.ordine_articoli.all()
            for one in articoli:
                one.delete()

        object.delete()

        #serializer = self.serializer_class(object)
        return Response({'Msg':'OK '+str(pk) +' deleted'})

    def retrieve(self, request, pk,*args, **kwargs):
        #pk = self.kwargs.get('pk')
        object = Ordine.objects.get(pk=pk) #kwargs['pk'])
        serializer = self.serializer_class(object)
        return Response(serializer.data)


