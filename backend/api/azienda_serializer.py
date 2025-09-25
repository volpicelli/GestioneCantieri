from rest_framework import serializers

from home.models import Azienda


class Aziendaserializer(serializers.ModelSerializer):

    class Meta:
        model = Azienda

        fields = '__all__'
