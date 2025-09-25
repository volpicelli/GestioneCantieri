from rest_framework import serializers
#from rest_framework_money_field import MoneyField
from home.models import Personale


class Personaleserializer(serializers.ModelSerializer):

    class Meta:
        model = Personale

        fields = '__all__'