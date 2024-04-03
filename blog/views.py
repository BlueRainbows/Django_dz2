from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from pytils.translit import slugify

from blog.models import Blog

# LoginRequiredMixin - класс-миксин для проверки анонимности пользователя (стоит ли is_active у пользователя)
# PermissionRequiredMixin - класс-миксин для проверки прав у пользоватя (работает совместно с permission_required)


class BlogCreateView(CreateView):
    """
    Контроллер для создания.
    Примимает модель Blog.
    Поля для отображения в fields.
    Переход при удачной отправке blog:list.
    """
    model = Blog
    fields = ('head', 'content', 'slug', 'image',)
    success_url = reverse_lazy('blog:list')

    def form_valid(self, form):
        """
        Метод при успешном создании.
        Формирует поле slug с помощью библиотеки slugify из заголовка.
        """
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.head)
            new_blog.save()

        return super().form_valid(form)


class BlogDetailView(DetailView):
    """
    Контроллер для детального просмотра.
    Примимает модель Blog.
    """
    model = Blog

    def get_object(self, queryset=None):
        """
        Метод для накрутки просмотров.
        Добавляет к полю +1 при каждом обновлении страницы.
        """
        self.object = super().get_object(queryset)
        self.object.views += 1
        self.object.save()
        return self.object


class BlogListView(ListView):
    """
    Контроллер для главной страницы.
    Примимает модель Blog.
    """
    model = Blog

    def get_queryset(self, *args, **kwargs):
        """
        Метод выполняющий фильтрацию по наличию публикации.
        Выводит на главную страницу только те блоги, которые имеют положительный признак публикации(True)
        """
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(published=True)
        return queryset


class BlogUpdateView(PermissionRequiredMixin, UpdateView):
    """
    Контроллер для редактирования.
    Примимает модель Blog.
    Поля для отображения в fields.
    Переход при удачной отправке редирект на (blog:detail).
    Ограничение прав у пользователей прописаны в permission_required.
    """
    model = Blog
    fields = ('head', 'content', 'slug', 'image',)
    permission_required = 'blog.change_blog'

    def form_valid(self, form):
        """
        Метод при успешном создании.
        Формирует поле slug с помощью библиотеки slugify из заголовка.
        """
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.head)
            new_blog.save()

        return super().form_valid(form)

    def get_success_url(self):
        """
        Метод для перехода при удачной отправке.
        Редирект на на страницу детального просмотра, принимает pk(айди блога)
        """
        return reverse('blog:detail', args=[self.kwargs.get('pk')])


class BlogDeleteView(PermissionRequiredMixin, DeleteView):
    """
    Контроллер для удаления.
    Примимает модель Blog.
    Переход при удачной отправке редирект на ('blog:list').
    Ограничение прав у пользователей прописаны в permission_required.
    """
    model = Blog
    success_url = reverse_lazy('blog:list')
    permission_required = 'blog.delete_blog'


def activates(request, pk):
    """
    Метод переключения флага публикации блога с False на True и наоборот,
    Переход на 'blog:list'
    """
    blogs_item = get_object_or_404(Blog, pk=pk)
    if blogs_item.published:
        blogs_item.published = False
    else:
        blogs_item.published = True
    blogs_item.save()
    return redirect(reverse('blog:list'))

