from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Blog(models.Model):
    head = models.CharField(max_length=300, verbose_name='Заголовок')
    slug = models.CharField(max_length=300, verbose_name='Slug', **NULLABLE)
    content = models.TextField(verbose_name='Содержимое')
    image = models.ImageField(upload_to='blogs/', verbose_name='Изображение', **NULLABLE)
    created_at = models.DateField(verbose_name='Дата создания', auto_now=True)
    published = models.BooleanField(verbose_name='Публикация', default=False)
    views = models.IntegerField(verbose_name='Просмотры', default=0)

    def __str__(self):
        return f'{self.head}. Дата создания - {self.created_at}'

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'
