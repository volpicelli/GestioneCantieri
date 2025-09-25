from rest_framework import serializers

from home.models import Responsabile


class Responsabileserializer(serializers.ModelSerializer):

    class Meta:
        model = Responsabile

        fields = '__all__'
