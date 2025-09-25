from rest_framework import serializers

from home.models import Cantiere


class Cantiereserializer(serializers.ModelSerializer):

    class Meta:
        model = Cantiere

        fields = '__all__'
