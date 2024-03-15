from django.contrib import admin

from catalog.models import Category, Product, Version


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_category',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_products', 'price', 'category',)
    list_filter = ('category',)
    search_fields = ('name_products', 'description_products',)


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ('product', 'version_number', 'version_name', 'current_version',)
    list_filter = ('product',)
