from django.core.management import BaseCommand
from catalog.models import Category, Product, Version


class Command(BaseCommand):

    def handle(self, *args, **options):

        Category.objects.all().delete()
        Product.objects.all().delete()
        Version.objects.all().delete()

        cat_1 = Category.objects.create(name_category='Мебель', description_category='Мебель для дома, офиса и сада')
        cat_2 = Category.objects.create(name_category='Одежда', description_category='Одежда для детей и взрослых')
        cat_3 = Category.objects.create(name_category='Обувь', description_category='Обувь для детей и взрослых')

        product_1 = Product.objects.create(name_products='Диван', description_products='Диван для дома и офиса',
                                           image='/products/диван_10YBE5j.jpeg', category=cat_1, price=30000)
        product_2 = Product.objects.create(name_products='Брюки', description_products='Брюки мужские',
                                           image='/products/брюки_67dV3Eq.jpg', category=cat_2, price=2000)
        product_3 = Product.objects.create(name_products='Кеды', description_products='Кеды женские',
                                           image='/products/кеды_i5bt06M.jpg', category=cat_3, price=3500)

        version_1 = Version.objects.create(product=product_1, version_number=200, version_name='Габариты')

        version_2 = Version.objects.create(product=product_2, version_number=42, version_name='Размер')

        version_3 = Version.objects.create(product=product_3, version_number=37, version_name='Размер')
