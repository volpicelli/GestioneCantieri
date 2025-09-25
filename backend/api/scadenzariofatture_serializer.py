from rest_framework import serializers

from home.models import ScadenzarioFatture


class ScadenzarioFattureSerializer(serializers.ModelSerializer):

    class Meta:
        model = ScadenzarioFatture

        fields = '__all__'