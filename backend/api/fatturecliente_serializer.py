from rest_framework import serializers

from home.models import FattureCliente



class FattureClienteserializer(serializers.ModelSerializer):
    class Meta:
        model = FattureCliente

        fields = '__all__'
