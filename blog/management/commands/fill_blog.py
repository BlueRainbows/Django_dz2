from django.core.management import BaseCommand
from blog.models import Blog


class Command(BaseCommand):

    def handle(self, *args, **options):
        Blog.objects.all().delete()

        blog_1 = Blog.objects.create(head='О чем на самом деле «Маленький принц»?', published=True,
                                     image='/blogs/the-little-prince-10k-wallpaper-3840x2400_9.jpg',
                                     content='Ищем скрытые за простыми диалогами метафоры, чтобы лучше считывать подтексты. Вместо скепсиса в сторону сказок и тоски по ушедшему детству.',
                                     slug='malenkii_price')
        blog_2 = Blog.objects.create(head='О чем повесть «Собачье сердце»', published=True,
                                     image='/blogs/d7ae6ee5ece2819004abeb010cb47b6a.jpeg',
                                     content='Полный разбор произведения, чтобы уловить все авторские отсылки. Вместо неловкого молчания при обсуждении и нескольких прочтений.',
                                     slug='sobachie_serdce')
