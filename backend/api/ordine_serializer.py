from rest_framework import serializers

from home.models import Ordine


class Ordineserializer(serializers.ModelSerializer):

    class Meta:
        model = Ordine

        fields ='__all__'
