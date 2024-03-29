from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView

from catalog.forms import VersionForm, ProductFormForModerCatalog, ProductFormForAllUser
from catalog.models import Product, Version


class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'


class ProductListView(LoginRequiredMixin, ListView):
    model = Product

    def get_context_data(self, *args, **kwargs):
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
    model = Product


class ProductCreateView(PermissionRequiredMixin, CreateView):
    model = Product
    form_class = ProductFormForAllUser
    success_url = reverse_lazy('catalog:product_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        us = form.save(commit=False)
        us.user = self.request.user
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductFormForAllUser
    success_url = reverse_lazy('catalog:product_list')
    permission_required = ('catalog.change_product', 'catalog.set_published',
                           'catalog.set_description', 'catalog.set_category')

    def get_form_class(self):
        if self.request.user.is_staff and self.request.user.has_perms(perm_list=self.permission_required) and not self.request.user.is_superuser:
            return ProductFormForModerCatalog
        elif self.request.user.is_superuser and self.request.user.has_perm('catalog.change_product'):
            return ProductFormForAllUser
        else:
            if self.request.user != self.get_object().user:
                raise PermissionDenied
            return ProductFormForAllUser

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:product_list')
    permission_required = 'catalog.delete_product'
