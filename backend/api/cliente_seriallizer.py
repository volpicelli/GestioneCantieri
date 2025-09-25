from rest_framework import serializers

from home.models import Cliente


class Clienteserializer(serializers.ModelSerializer):

    class Meta:
        model = Cliente

        fields = '__all__'
