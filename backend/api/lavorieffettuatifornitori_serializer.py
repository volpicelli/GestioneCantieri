from rest_framework import serializers

from home.models import LavoriEffettuatiFornitori


class LavoriEffettuatiFornitoriserializer(serializers.ModelSerializer):

    class Meta:
        model = LavoriEffettuatiFornitori

        fields = '__all__'
