from django.shortcuts import render

from catalog.models import Product


def index_1(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'Имя - {name}, телефон - {phone}, сообщение - {message}')
    return render(request, 'catalog/contacts.html')


def index_2(request):
    product_list = Product.objects.all()
    content = {
        'object_list': product_list
    }
    return render(request, 'catalog/home.html', content)


def index_3(request, pk):
    content = {
        'object': Product.objects.get(pk=pk)
    }
    return render(request, 'catalog/products.html', content)
