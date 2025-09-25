from rest_framework import serializers

from home.models import ScadenzarioFattureCliente


class ScadenzarioFattureClienteSerializer(serializers.ModelSerializer):

    class Meta:
        model = ScadenzarioFattureCliente

        fields = '__all__'