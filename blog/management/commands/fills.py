from django.core.management import BaseCommand
from blog.models import Blog


class Command(BaseCommand):

    def handle(self, *args, **options):
        Blog.objects.all().delete()

        blog_1 = Blog.objects.create(head='О чем на самом деле «Маленький принц»?', published=True, \
                                     content='Ищем скрытые за простыми диалогами метафоры, чтобы лучше считывать подтексты. Вместо скепсиса в сторону сказок и тоски по ушедшему детству.')
        blog_2 = Blog.objects.create(head='О чем повесть «Собачье сердце»', published=True, \
                                     content='Полный разбор произведения, чтобы уловить все авторские отсылки. Вместо неловкого молчания при обсуждении и нескольких прочтений.')
