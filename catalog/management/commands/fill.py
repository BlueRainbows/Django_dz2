from django.core.management import BaseCommand
from catalog.models import Category, Product


class Command(BaseCommand):

    def handle(self, *args, **options):

        Category.objects.all().delete()
        Product.objects.all().delete()

        cat_1 = Category.objects.create(name_category='Мебель', description_category='Мебель для дома, офиса и сада')
        cat_2 = Category.objects.create(name_category='Одежда', description_category='Одежда для детей и взрослых')
        cat_3 = Category.objects.create(name_category='Обувь', description_category='Обувь для детей и взрослых')

        product_1 = Product.objects.create(name_products='Диван', description_products='Диван для дома и офиса',
                                           category=cat_1, price=30000)
        product_2 = Product.objects.create(name_products='Брюки', description_products='Брюки мужские',
                                           category=cat_2, price=2000)
        product_2 = Product.objects.create(name_products='Кеды', description_products='Кеды женские',
                                           category=cat_3, price=3500)
