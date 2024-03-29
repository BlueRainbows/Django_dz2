from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from blog.models import Blog
from catalog.models import Product, Version, Category

ct_pr = ContentType.objects.get_for_model(Product)
# ct_bl = ContentType.objects.get_for_model(Blog)
# ct_vers = ContentType.objects.get_for_model(Version)
# ct_cat = ContentType.objects.get_for_model(Category)

# Поиск по коднейму в бд
# perm = [
#     {'codename': 'view_category', 'content_type': ct_cat},
#     {'codename': 'change_category', 'content_type': ct_pr},
#     {'codename': 'view_blog', 'content_type': ct_bl},
#     {'codename': 'change_discription', 'content_type': ct_pr},
#     {'codename': 'set_is_published', 'content_type': ct_pr},
#     {'codename': 'view_product', 'content_type': ct_pr},
#     {'codename': 'view_version', 'content_type': ct_vers},
#     {'codename': 'change_product', 'content_type': ct_pr},
# ]


# Поиск по айди в бд
perm = [
    {'id': 26, 'content_type': ct_pr},
    {'id': 41, 'content_type': ct_pr},
    {'id': 42, 'content_type': ct_pr},
    {'id': 43, 'content_type': ct_pr},
]


class Command(BaseCommand):

    def handle(self, *args, **options):
        new_group = Group.objects.create(name='moderator_catalog')
        for p in perm:
            permission = Permission.objects.get(**p)
            new_group.permissions.add(permission)
