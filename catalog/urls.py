from django.urls import path

from catalog.apps import MainConfig
from catalog.views import ContactsView, ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView

app_name = MainConfig.name

urlpatterns = [
    path('contacts/', ContactsView.as_view()),
    path('', ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>', ProductDetailView.as_view(), name='product'),
    path('create_product/', ProductCreateView.as_view(), name='create_product'),
    path('update_product/<int:pk>', ProductUpdateView.as_view(), name='update_product'),
]
