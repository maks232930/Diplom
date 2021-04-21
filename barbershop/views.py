from django.shortcuts import render


def index(request):
    return render(request, 'barbershop/index.html')


def service_price(request):
    return render(request, 'barbershop/service_price.html')


def gallery(request):
    return render(request, 'barbershop/gallery.html')


def contact(request):
    return render(request, 'barbershop/contact.html')
