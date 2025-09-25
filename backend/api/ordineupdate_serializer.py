from rest_framework import serializers

from home.models import Ordine,Articoli

class ArticoliUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articoli
        fields = '__all__'

class OrdineUpdateserializer(serializers.ModelSerializer):
    articoli = ArticoliUpdateSerializer()
    
    class Meta:
        model = Ordine
        fields ='__all__'
