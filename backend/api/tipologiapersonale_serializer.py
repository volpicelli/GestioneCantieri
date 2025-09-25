from rest_framework import serializers

from home.models import TipologiaPersonale


class TipologiaPersonaleserializer(serializers.ModelSerializer):

    class Meta:
        model = TipologiaPersonale

        fields = '__all__'