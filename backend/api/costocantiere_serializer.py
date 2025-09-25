from rest_framework import serializers
from .personale_serializer import Personaleserializer
from home.models import Assegnato_Cantiere,CondizioniPagamento

class Costo_Cantiereserializer(serializers.ModelSerializer):
    personale = Personaleserializer()
    class Meta:
      model = Assegnato_Cantiere
      fields = '__all__'
      
#class Fornitoriserializer(serializers.ModelSerializer):

#    class Meta:
#        model = Fornitori

#        fields = '__all__'