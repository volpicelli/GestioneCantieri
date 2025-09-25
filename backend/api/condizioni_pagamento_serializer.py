from rest_framework import serializers

from home.models import CondizioniPagamento


class CondizioniPagamentoserializer(serializers.ModelSerializer):
    #media_url = serializers.ReadOnlyField(source='get_media_url')
    #media_url = serializers.SerializerMethodField()

    class Meta:
        model = CondizioniPagamento

        fields = '__all__'

    #def get_media_url(self, object):
    #    url = object.get_media_url()
    #    return url