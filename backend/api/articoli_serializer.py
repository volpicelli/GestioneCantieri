from rest_framework import serializers

from home.models import Articoli


class Articoliserializer(serializers.ModelSerializer):

    class Meta:
        model = Articoli

        fields = '__all__'
