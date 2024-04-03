from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView

from catalog.forms import VersionForm, ProductFormForModerCatalog, ProductFormForAllUser
from catalog.models import Product, Version, Category
from catalog.services import get_cache_categories_catalogs


# LoginRequiredMixin - класс-миксин для проверки анонимности пользователя (стоит ли is_active у пользователя)
# PermissionRequiredMixin - класс-миксин для проверки прав у пользоватя (работает совместно с permission_required)


class ContactsView(TemplateView):
    """
    Контроллер для отображения страницы с контактами.
    В template_name указывается путь к шаблону страницы.
    """
    template_name = 'catalog/contacts.html'


class CategoryListView(LoginRequiredMixin, ListView):
    """
    Контроллер для отображения страницы категорий.
    Принимает модель Category.
    """
    model = Category
    template_name = 'catalog/category_list.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = get_cache_categories_catalogs()
        return queryset


@login_required
def get_category_and_products(request, pk):
    """
    Метод принимает pk категории, фильтрует в модели продуктов данное значение.
    Образует список со строковым значением найденных продуктов,
    Возвращается список с категорией и продуктами в виде контекста используемого в шаблоне.
    """
    if request.method == 'GET':
        list_product = []
        category = Category.objects.get(pk=pk)
        prod_cat = Product.objects.filter(category=category)
        for value in range(len(prod_cat)):
            list_product.append(prod_cat[value])

    return render(request, 'catalog/category_detail.html', {'category': category, 'products': list_product})


class ProductListView(LoginRequiredMixin, ListView):
    """
    Контроллер для отображения главной страницы.
    Принимает модель Product.
    """
    model = Product

    def get_context_data(self, *args, **kwargs):
        """
        Метод для получения контекста.
        В переменную сохраняются все объкты класса Product, в цикле сравниваются по взаимосвязи с Version,
        Происходит фильтрация по активной версии, в переменную выводиться название/номер/признак активной версии
        Если данные не найдены, то выводиться 'Нет активной версии'/''/False
        Возвращает обновленный контекст под названием 'products', который можно вызвать в шаблоне
        """
        context_data = super().get_context_data(*args, **kwargs)
        products = Product.objects.all()

        for product in products:
            version = Version.objects.filter(product=product)
            active_version = version.filter(current_version=True).first()
            product.active_version = active_version.version_name if active_version else 'Нет активной версии'
            product.number_version = active_version.version_number if active_version else ''
            product.current_versions = active_version.current_version if active_version else False

        context_data['products'] = products

        return context_data


class ProductDetailView(LoginRequiredMixin, DetailView):
    """
    Контроллер для просмотра детальной информации.
    Принимает модель Product.
    """
    model = Product


class ProductCreateView(LoginRequiredMixin, CreateView):
    """
    Контроллер для создания.
    Принимает модель Product, стандартная форма ProductFormForAllUser.
    При успешном ответе выполняется переход на product_list.
    """
    model = Product
    form_class = ProductFormForAllUser
    success_url = reverse_lazy('catalog:product_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        Метод получения контекста.
        Формирует формсет для модели Product, Version, указывается форма VersionForm.
        """
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        """
        Метод при успешной отправке формы.
        Получает значение формы, добавляет текущего пользователя к продукту.
        Так же переносит значения в формсет.
        """
        us = form.save(commit=False)
        us.user = self.request.user
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """
    Контроллер для редактирования.
    Принимает модель Product, стандартная форма ProductFormForAllUser, прописан метод для переключения формы.
    При успешном ответе выполняется переход на product_list.
    В переменной permission_required переданы права которые считываются и проверяются у конкретного пользователя.
    """
    model = Product
    form_class = ProductFormForAllUser
    success_url = reverse_lazy('catalog:product_list')
    permission_required = ('catalog.change_product', 'catalog.set_published',
                           'catalog.set_description', 'catalog.set_category')

    def get_form_class(self):
        """
        Метод переключения формы, где выполняется проверка прав для пользователя через has_perm.
        В случае подтверждения прав у пользователя, форма переключается.
        Так же указывается проверка на авторство пользователя(взаимосвязь у Product и User).
        """
        if self.request.user.is_staff and self.request.user.has_perms(
                perm_list=self.permission_required) and not self.request.user.is_superuser:
            return ProductFormForModerCatalog
        elif self.request.user.is_superuser and self.request.user.has_perm('catalog.change_product'):
            return ProductFormForAllUser
        else:
            if self.request.user != self.get_object().user:
                raise PermissionDenied
            return ProductFormForAllUser

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        Метод получения контекста.
        Формирует формсет для модели Product, Version, указывается форма VersionForm.
        """
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        """
        Метод при успешной отправке формы.
        Получает значение формы, переносит в формсет.
        """
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
    Контроллер для удаления.
    Принимает модель Product, переход при успешном ответе в product_list.
    Открывается только при наличии прав на удаление продукта.
    """
    model = Product
    success_url = reverse_lazy('catalog:product_list')
    permission_required = 'catalog.delete_product'
