from django.urls import path

from blog.apps import BlogConfig
from blog.views import BlogCreateView, BlogListView, BlogDetailView, BlogUpdateView, BlogDeleteView, activates

app_name = BlogConfig.name

urlpatterns = [
    path('blog_create/', BlogCreateView.as_view(), name='create'),
    path('blog/', BlogListView.as_view(), name='list'),
    path('blog_detail/<int:pk>', BlogDetailView.as_view(), name='detail'),
    path('blog_update/<int:pk>', BlogUpdateView.as_view(), name='update'),
    path('blog/<int:pk>', BlogDeleteView.as_view(), name='delete'),
    path('blog_activate/<int:pk>', activates, name='activate'),
]