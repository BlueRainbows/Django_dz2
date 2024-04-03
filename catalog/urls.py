from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.apps import MainConfig
from catalog.views import ContactsView, ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, \
    ProductDeleteView, CategoryListView, get_category_and_products

app_name = MainConfig.name

urlpatterns = [
    # Переход на страницу контактов
    path('contacts/', ContactsView.as_view()),


    # Переход на страницу категорий
    path('categories/', CategoryListView.as_view(), name='categories_list'),
    # Переход на страницу продуктов категории
    path('category/<int:pk>', get_category_and_products, name='category'),


    # Переход на главную страницу
    path('', ProductListView.as_view(), name='product_list'),
    # Переход на страницу просмотра отдельного продукта
    path('products/<int:pk>', cache_page(60)(ProductDetailView.as_view()), name='product'),
    # Переход на страницу создания продукта
    path('create_product/', ProductCreateView.as_view(), name='create_product'),
    # Переход на страницу редактирования продукта
    path('update_product/<int:pk>', ProductUpdateView.as_view(), name='update_product'),
    # Переход на страницу удаления продукта
    path('delete_product/<int:pk>', ProductDeleteView.as_view(), name='delete_product'),
]
