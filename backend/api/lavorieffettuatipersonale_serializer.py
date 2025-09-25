from rest_framework import serializers

from home.models import LavoriEffettuatiPersonale


class LavoriEffettuatiPersonaleserializer(serializers.ModelSerializer):

    class Meta:
        model = LavoriEffettuatiPersonale

        fields = '__all__'
