from rest_framework import serializers

from home.models import Fatture



class Fattureserializer(serializers.ModelSerializer):
    class Meta:
        model = Fatture

        fields = '__all__'
