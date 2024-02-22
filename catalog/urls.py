from django.urls import path

from catalog.apps import MainConfig
from catalog.views import index_1, index_2, index_3

app_name = MainConfig.name

urlpatterns = [
    path('contacts/', index_1),
    path('', index_2),
    path('products/<int:pk>', index_3, name='product')
]
