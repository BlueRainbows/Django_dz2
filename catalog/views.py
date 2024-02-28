from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from pytils.translit import slugify
from catalog.models import Product, Blog


class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'


class ProductListView(ListView):
    model = Product


class ProductDetailView(DetailView):
    model = Product


######################################################################################################################


class BlogCreateView(CreateView):
    model = Blog
    fields = ('head', 'content', 'slug', 'image',)
    success_url = reverse_lazy('catalog:list')

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.head)
            new_blog.save()

        return super().form_valid(form)


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views += 1
        self.object.save()
        return self.object


class BlogListView(ListView):
    model = Blog

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(published=True)
        return queryset


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ('head', 'content', 'slug', 'image',)

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.head)
            new_blog.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('catalog:detail', args=[self.kwargs.get('pk')])


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('catalog:list')


def activates(request, pk):
    blogs_item = get_object_or_404(Blog, pk=pk)
    if blogs_item.published:
        blogs_item.published = False
    else:
        blogs_item.published = True
    blogs_item.save()
    return redirect(reverse('catalog:list'))
