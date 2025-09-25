from rest_framework import serializers

from home.models import Magazzino


class Magazzinoserializer(serializers.ModelSerializer):

    class Meta:
        model = Magazzino

        fields = '__all__'
