from rest_framework import serializers

from home.models import Assegnato_Cantiere


class Assegnato_CantiereSerializer(serializers.ModelSerializer):

    class Meta:
        model = Assegnato_Cantiere

        fields = '__all__'
