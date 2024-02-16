from django.db import models


class Category(models.Model):
    name_category = models.CharField(max_length=150, verbose_name='Наименование категории')
    description_category = models.CharField(max_length=300, verbose_name='Описание категории')

    def __str__(self):
        return f'{self.name_category} - {self.description_category}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


NULLABLE = {'blank': True, 'null': True}


class Product(models.Model):
    name_products = models.CharField(max_length=100, verbose_name='Наименование продукта')
    description_products = models.CharField(max_length=300, verbose_name='Описание продукта')
    image = models.ImageField(upload_to='products/', verbose_name='Изображение', **NULLABLE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField(verbose_name='Цена продукта')
    created_at = models.DateTimeField(verbose_name='Дата создания', **NULLABLE)
    updated_at = models.DateTimeField(verbose_name='Дата изменения', **NULLABLE)

    def __str__(self):
        return f'{self.name_products}: {self.description_products}. Цена - {self.price}'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
