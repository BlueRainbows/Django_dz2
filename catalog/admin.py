from django.contrib import admin

from catalog.models import Category, Product, Blog


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_category',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_products', 'price', 'category',)
    list_filter = ('category',)
    search_fields = ('name_products', 'description_products',)


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'head', 'created_at',)
    search_fields = ('head', 'content',)

