from rest_framework import serializers

from home.models import Fornitori,CondizioniPagamento

class CondizioniPagamentoserializer(serializers.ModelSerializer):
    class Meta:
      model = CondizioniPagamento
      fields = '__all__'
      
class Fornitoriserializer(serializers.ModelSerializer):
    codpag = CondizioniPagamentoserializer()

    class Meta:
        model = Fornitori

        fields = '__all__'