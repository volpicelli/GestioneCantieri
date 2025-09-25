from rest_framework import serializers

from home.models import AnagraficaFornitori


class AnagraficaFornitoriserializer(serializers.ModelSerializer):

    class Meta:
        model = AnagraficaFornitori

        fields = '__all__'