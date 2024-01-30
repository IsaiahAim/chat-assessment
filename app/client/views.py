from rest_framework import viewsets

from client.models import Client
from client.serializers import ClientSerializer
from users.permissions import IsSuperAdmin


class ClientViewset(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    http_method_names = ["get",  'post']
    permission_classes = [IsSuperAdmin]

