from rest_framework import serializers

from home.models import AnagraficaPersonale


class AnagraficaPersonaleserializer(serializers.ModelSerializer):

    class Meta:
        model = AnagraficaPersonale

        fields = '__all__'