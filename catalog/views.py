from django.shortcuts import render


def index_1(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'Имя - {name}, телефон - {phone}, сообщение - {message}')
    return render(request, 'catalog/contacts.html')


def index_2(request):
    return render(request, 'catalog/home.html')
