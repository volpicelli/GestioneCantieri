from django.shortcuts import render
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import exceptions

from .scadenzariofatture_serializer import ScadenzarioFattureSerializer
from .fatture_serializer import Fattureserializer
from .fornitori_serializer import Fornitoriserializer,CondizioniPagamentoserializer


# Create your views here.
from home.models import ScadenzarioFatture,Fatture,Azienda,Fornitori,CondizioniPagamento

import json
from django.conf import settings


class FatturaCreate(APIView):
    fatture_serialize = Fattureserializer
    scadenza_serializer = ScadenzarioFattureSerializer
    fornitore_serializer = Fornitoriserializer
    def post(self,request):
        data = json.loads(request.body)

        if 'azienda' not in data.keys() :
            msg = 'Azienda non specificata'
            return Response(msg)
        if 'fornitore' not in data.keys() :
            msg = 'Fornitore non specificato'
            return Response(msg)
        


        
        azienda_id = data['azienda']
        azienda = Azienda.objects.get(pk=azienda_id)
        fornitore_id = data['fornitore']
        fornitore = Fornitori.objects.get(pk=fornitore_id)
        #numerorate = fornitore.codpag.numrate
        #codpag = data['codpag']
        


        pagato = None
        if 'pagato'  in data.keys():
            pagato = data['pagato']
                
        if 'importo' in data.keys():
            importo = data['importo']
        else:
            importo = 0.0
        if 'data_fattura' in data.keys():
            data_fattura = data['data_fattura']
        else:
            data_fattura = None

        if 'n_fattura' in data.keys():
            n_fattura = data['n_fattura']
        else:
            n_fattura = None

        if 'data_scadenza' in data.keys():
            data_scadenza = data['data_scadenza']
        else:
            data_scadenza = None

        if 'codpag' in data.keys():
            codpag = data['codpag']
            condizionipag = CondizioniPagamento.objects.get(pk=codpag)
            numerorate = condizionipag.numrate
            tipologiapagamento = condizionipag.tipopag
        else:
            condizionipag = fornitore.codpag
            tipologiapagamento = fornitore.codpag.tipopag
            numerorate = fornitore.codpag.numrate

        


        fattura = Fatture.objects.create(
            pagato=pagato,
            fornitore=fornitore,
            importo=importo,
            data_scadenza= data_scadenza,
            data_fattura=data_fattura,
            n_fattura=n_fattura,
            #tipologiapagamento = fornitore.codpag.tipopag,
            tipologiapagamento = tipologiapagamento,
            azienda=azienda,
            codpag= condizionipag)

        fattura.save()

        if 'scadenze' in data.keys():
            scadenze = data['scadenze']
            if len(scadenze) != numerorate:
                fattura.tipologiapagamento = 3000
                fattura.save()
            

            

            for scadenza in scadenze:
                if 'scadenza_rata' in scadenza.keys():
                    scadenza_rata = scadenza['scadenza_rata']
                else:
                    scadenza_rata = None
                if scadenza_rata == '':
                    scadenza_rata = None

                if 'importo_pagato' in scadenza.keys():
                    importo_pagato = scadenza['importo_pagato']
                else:
                    importo_pagato = 0.0

                if 'importo_rata' in scadenza.keys():
                    importo_rata = scadenza['importo_rata']
                else:
                    importo_rata = 0.0

                if 'data_pagamento' in scadenza.keys():
                    data_pagamento = scadenza['data_pagamento']
                else:
                    data_pagamento = ''
                if data_pagamento == '':
                    data_pagamento = None

                if 'status' in scadenza.keys():
                    status = scadenza['status']
                else:
                    status = False
                

                sf = ScadenzarioFatture.objects.create(
                    fattura=fattura,
                    scadenza_rata=scadenza_rata,
                    importo_pagato=importo_pagato,
                    data_pagamento=data_pagamento,
                    status=status,
                    importo_rata=importo_rata
                )
                sf.save()

        
        resp={}

        os = self.fatture_serialize(fattura)
        resp['fattura']=os.data
        f = self.fornitore_serializer(fornitore)
        resp['fornitore'] = f.data
        scadenze =[]
        for one in fattura.fatture_scadenzario.all():
            scadenze.append(self.scadenza_serializer(one).data)
        resp['scadenze'] = scadenze
        return Response(resp)


class FatturaUpdate(APIView):
    fatture_serialize = Fattureserializer
    scadenza_serializer = ScadenzarioFattureSerializer
    codpag_serializer = CondizioniPagamentoserializer
    fornitore_serializer = Fornitoriserializer

    def get(self,request,pk):
        try:
            f = Fatture.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response( f" Fattura {pk} non esiste ")        
        
        fornitore = Fornitori.objects.get(pk=f.fornitore.id)
        codpag = self.codpag_serializer(f.codpag)


        sf = f.fatture_scadenzario.all()
        fatture_serializer = self.fatture_serialize(f)
        #serializer.data['articoli'] =[]
        scadenze=[]
        #ars = Articoliserializer(ar,many=True)
        for one in sf:
            sfs = ScadenzarioFattureSerializer(one)
            scadenze.append(sfs.data)
        #serializer.data['articoli']=a
        resp = {}
        resp['fattura']=fatture_serializer.data
        resp['scadenze'] = scadenze
        resp['codpag'] = codpag.data
        return Response(resp)

    def post(self,request,pk):
        data = json.loads(request.body)

        
        try:
            fattura = Fatture.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response( " Fattura non esiste ")

        
        azienda_id =fattura.azienda.id
        fornitore_id = fattura.fornitore.id

        sf = fattura.fatture_scadenzario.all()
        lensf_indb = len(sf)

       
        
        if 'scadenze' in data.keys():
            scadenze = data['scadenze']
            lenscadenze = len(scadenze)
            if lensf_indb != lenscadenze:
                tipopag = 3000
                fattura.tipologiapagamento = tipopag
                
            #else:
            #    fattura.tipologiapagamento = fattura.fornitore.codpag.tipopag
            fattura.save()

            for one in sf:
                one.delete()



            for scadenza in scadenze:
                if 'scadenza_rata' in scadenza.keys():
                    scadenza_rata = scadenza['scadenza_rata']
                else:
                    scadenza_rata = None
                if scadenza_rata == '':
                    scadenza_rata = None

                if 'importo_pagato' in scadenza.keys():
                    importo_pagato = scadenza['importo_pagato']
                else:
                    importo_pagato = 0.0

                if 'importo_rata' in scadenza.keys():
                    importo_rata = scadenza['importo_rata']
                else:
                    importo_rata = 0.0

                if 'data_pagamento' in scadenza.keys():
                    data_pagamento = scadenza['data_pagamento']
                else:
                    data_pagamento = ''
                if data_pagamento == '':
                    data_pagamento = None

                if 'status' in scadenza.keys():
                    status = scadenza['status']
                else:
                    status = False
                

                sf = ScadenzarioFatture.objects.create(
                    fattura=fattura,
                    scadenza_rata=scadenza_rata,
                    importo_pagato=importo_pagato,
                    data_pagamento=data_pagamento,
                    status=status,
                    importo_rata=importo_rata
                )
                sf.save()

        
        
        resp={}

        os = self.fatture_serialize(fattura)
        resp['fattura']=os.data
        f = self.fornitore_serializer(fattura.fornitore)
        resp['fornitore'] = f.data
        scadenze =[]
        for one in fattura.fatture_scadenzario.all():
            scadenze.append(self.scadenza_serializer(one).data)
        resp['scadenze'] = scadenze
        return Response(resp)



class FattureList(generics.ListCreateAPIView):
    queryset = Fatture.objects.all()
    serializer_class = Fattureserializer
    #permission_classes = [IsAuthenticated]

    

class FattureDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Fatture.objects.all()
    serializer_class = Fattureserializer
    scadenza_serializer = ScadenzarioFattureSerializer

    
    def destroy(self, request, pk,*args, **kwargs):
        #pk = self.kwargs.get('pk')
        object = Fatture.objects.get(pk=pk).delete() #kwargs['pk'])
        serializer = self.serializer_class(object)
        return Response({'Msg':'OK '+str(pk) +' deleted'})

    def retrieve(self, request, pk,*args, **kwargs):
        #pk = self.kwargs.get('pk')
        fattura = Fatture.objects.get(pk=pk) #kwargs['pk'])
        serializer = self.serializer_class(fattura)
        scadenze =[]
        #for one in fattura.fatture_scadenzario.all():
        #    scadenze.append(self.scadenza_serializer(one).data)
        #serializer.data['scadenze'] = scadenze
        return Response(serializer.data)
 


  
class ScadenzarioFattureList(generics.ListCreateAPIView):
    queryset = ScadenzarioFatture.objects.all()
    serializer_class = ScadenzarioFattureSerializer
    serializer_sp = CondizioniPagamentoserializer
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        resp=[]
        for one in queryset:
            ss ={}
            #codpag = one.fattura.fornitore.codpag
            codpag = CondizioniPagamento.objects.get(pk=one.fattura.codpag.id)
            serializer_sf = self.serializer_class(one)
            serializer_codpag = self.serializer_sp(codpag)
            serializer_sf.data['codpag'] = serializer_codpag.data
            ss = serializer_sf.data   
            ss['codpag'] = serializer_codpag.data        
            resp.append(ss)



        #page = self.paginate_queryset(queryset)
        #if page is not None:
        #    serializer = self.get_serializer(page, many=True)
        #
        #return self.get_paginated_response(serializer.data)

        #serializer = self.serializer_class(queryset, many=True)
        return Response(resp)


class ScadenzarioFattureDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ScadenzarioFatture.objects.all()
    serializer_class = ScadenzarioFattureSerializer
    
    def destroy(self, request, pk,*args, **kwargs):
        #pk = self.kwargs.get('pk')
        object = ScadenzarioFatture.objects.get(pk=pk).delete() #kwargs['pk'])
        #serializer = self.serializer_class(object)
        return Response({'Msg':'OK '+str(pk) +' deleted'})

    def retrieve(self, request, pk,*args, **kwargs):
        #pk = self.kwargs.get('pk')
        object = ScadenzarioFatture.objects.get(pk=pk) #kwargs['pk'])
        
        serializer = self.serializer_class(object)
        return Response(serializer.data)
