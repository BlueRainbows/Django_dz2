from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):
    name_category = models.CharField(max_length=150, verbose_name='Наименование категории')
    description_category = models.CharField(max_length=300, verbose_name='Описание категории')

    def __str__(self):
        return f'{self.name_category} - {self.description_category}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    name_products = models.CharField(max_length=100, verbose_name='Наименование продукта')
    description_products = models.CharField(max_length=300, verbose_name='Описание продукта')
    image = models.ImageField(upload_to='products/', verbose_name='Изображение', **NULLABLE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория продукта')
    price = models.IntegerField(verbose_name='Цена продукта')
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата изменения', auto_now=True)

    def __str__(self):
        return f'{self.name_products}: {self.description_products}. Цена - {self.price}'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    version_number = models.PositiveSmallIntegerField(verbose_name='Номер версии продукта')
    version_name = models.CharField(max_length=150, verbose_name='Название версии продукта')
    current_version = models.BooleanField(default=True, verbose_name='Признак текущей версии')

    def __str__(self):
        return f'{self.product}. Название версии: {self.version_name}, номер {self.version_number}.'

    class Meta:
        verbose_name = 'Версия'
        verbose_name_plural = 'Версии'
