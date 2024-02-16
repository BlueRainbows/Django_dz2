from django.urls import path

from catalog.views import index_1, index_2

urlpatterns = [
    path('contacts/', index_1),
    path('', index_2),
]