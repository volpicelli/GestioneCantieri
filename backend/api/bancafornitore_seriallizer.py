from rest_framework import serializers

from home.models import BancaFornitori


class BancaFornitoriserializer(serializers.ModelSerializer):

    class Meta:
        model = BancaFornitori

        fields = '__all__'
