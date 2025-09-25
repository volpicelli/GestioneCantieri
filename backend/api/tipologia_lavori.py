from rest_framework import serializers

from home.models import TipologiaLavori


class TipologiaLavoriSerializer(serializers.ModelSerializer):

    class Meta:
        model = TipologiaLavori

        fields = '__all__'