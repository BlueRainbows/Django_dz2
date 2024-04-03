from django.conf import settings
from django.core.cache import cache

from catalog.models import Category


def get_cache_categories_catalogs():
    queryset = Category.objects.all()
    if settings.CACHE_ENABLE:
        key = 'categories'
        cache_data = cache.get(key)
        if cache_data is None:
            cache_data = queryset
            cache.set(key, cache_data)
    else:
        cache_data = queryset

    return cache_data

