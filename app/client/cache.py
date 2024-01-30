from django.core.cache import cache
from django.db.models import QuerySet

from client.models import Client


def cache_client_key(qs: QuerySet):
    cache.set('client', qs, 86400)
    return qs


def get_client_key(api_key: str):
    cache_queryset: QuerySet[Client] = cache.get('client', {})
    if not cache_queryset:
        qs = Client.objects.all()
        instance = qs.filter(key=api_key).first()
        cache.set('client', qs, 86400)
    else:
        instance = cache_queryset.filter(key=api_key).first()
    return instance