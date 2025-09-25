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

from .assegnato_cantiere_serializer import Assegnato_CantiereSerializer

from home.models import Personale,Assegnato_Cantiere,Cantiere,Azienda

import json
from django.conf import settings
class PersonaleAziendaAssegnatiCantieri(APIView):
    queryset = Assegnato_Cantiere.objects.all()
    serializer_class = Assegnato_CantiereSerializer
    def get(self,request,azienda_id):
        a=Azienda.objects.get(pk=azienda_id)
        p=a.azienda_personale.all()
        resp=[]
        for one in p:
            ac = one.personale_assegnato.all()
            for pac in ac:
                #resp.append(pac)
                serializer =self.serializer_class(pac)
                serializer2 = serializer.data
                serializer2['cognome']=pac.personale.cognome
                serializer2['nomecantiere']=pac.cantiere.nome
                resp.append(serializer2)
                

            #ac = self.queryset.filter(personale=one)
            #serializer =self.serializer_class(resp, many=True)
            #resp.append(serializer.data)
        #serializer = self.serializer_class(resp, many=True)
        #serializer =self.serializer_class(resp, many=True)
        return Response(resp)




class Assegnato_CantiereList(generics.ListCreateAPIView):
    queryset = Assegnato_Cantiere.objects.all()
    serializer_class = Assegnato_CantiereSerializer
    cognome = ""
    cantiere = ""

    def post(self, request, *args, **kwargs):
        #data = json.loads(request.body)

        personale = request.POST.get('personale')
        cantiere = request.POST.get('cantiere')
        ore_lavorate = request.POST.get('ore_lavorate')
        responsabile = request.POST.get('responsabile')
        p = Personale.objects.get(pk=int(personale))
        #c = Cantiere.objects.get(pk=cantiere)
        self.cognome  = p.cognome
        self.cantiere = cantiere
        return self.create(request, *args, **kwargs)
    
    def list(self,request):

        #def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        for one in serializer.data:
            c=Cantiere.objects.get(pk=one['cantiere'])
            p=Personale.objects.get(pk=one['personale'])
            one['cognome'] = p.cognome
            one['nomecantiere']=c.nome
        return Response(serializer.data)


    def handle_exception(self, exc):
        """
        Handle any exception that occurs, by returning an appropriate response,
        or re-raising the error.
        """
        if isinstance(exc, (exceptions.NotAuthenticated,
                            exceptions.AuthenticationFailed)):
            # WWW-Authenticate header for 401 responses, else coerce to 403
            auth_header = self.get_authenticate_header(self.request)

            if auth_header:
                exc.auth_header = auth_header
            else:
                exc.status_code = status.HTTP_403_FORBIDDEN

        exception_handler = self.get_exception_handler()

        context = self.get_exception_handler_context()
        #context="POLLO"
        response = exception_handler(exc, context)

        if response is None:
            self.raise_uncaught_exception(exc)

        response.exception = True
        response.data.pop('non_field_errors')
        response.data["warning"]="Personale {} gia assegnato al cantiere {}".format(self.cognome.upper(),self.cantiere)
        return response


class Assegnato_CantiereDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Assegnato_Cantiere.objects.all()
    serializer_class = Assegnato_CantiereSerializer
    
    def destroy(self, request, pk,*args, **kwargs):
        #pk = self.kwargs.get('pk')
        object = Assegnato_Cantiere.objects.get(pk=pk).delete() #kwargs['pk'])
        serializer = self.serializer_class(object)
        return Response({'Msg':'OK '+str(pk) +' deleted'})

    def retrieve(self, request, pk,*args, **kwargs):
        #pk = self.kwargs.get('pk')
        object = Assegnato_Cantiere.objects.get(pk=pk) #kwargs['pk'])
        serializer = self.serializer_class(object)
        return Response(serializer.data)
