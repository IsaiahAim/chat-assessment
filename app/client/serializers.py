from django.core.cache import cache
from django.core.signing import Signer
from rest_framework import serializers

from client.models import Client


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
        read_only_fields = ['key', ]

    def create(self, validated_data):
        client = Client(name=validated_data['name'])
        client.key = Signer().sign(client.id)
        client.save()
        cache.set('client', Client.objects.all(), 86400)
        return client
