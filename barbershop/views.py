from django.shortcuts import render
from django.views import View

from .models import GeneralInformation


class HomeView(View):

    def get(self, request):
        information = GeneralInformation.objects.first()
        return render(request, 'barbershop/index.html', {'info': information})


def service_price(request):
    return render(request, 'barbershop/service_price.html')


def gallery(request):
    return render(request, 'barbershop/gallery.html')


def contact(request):
    return render(request, 'barbershop/contact.html')
