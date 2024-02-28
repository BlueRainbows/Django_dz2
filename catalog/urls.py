from django.urls import path

from catalog.apps import MainConfig
from catalog.views import ContactsView, ProductListView, ProductDetailView, BlogCreateView, BlogListView, \
    BlogDetailView, BlogUpdateView, BlogDeleteView, activates

app_name = MainConfig.name

urlpatterns = [
    path('contacts/', ContactsView.as_view()),
    path('', ProductListView.as_view()),
    path('products/<int:pk>', ProductDetailView.as_view(), name='product'),

    path('settings/', BlogCreateView.as_view(), name='create'),
    path('blogs/', BlogListView.as_view(), name='list'),
    path('info/<int:pk>', BlogDetailView.as_view(), name='detail'),
    path('setting/<int:pk>', BlogUpdateView.as_view(), name='update'),
    path('blogs/<int:pk>', BlogDeleteView.as_view(), name='delete'),
    path('activate/<int:pk>', activates, name='activate'),
]
