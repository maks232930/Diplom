from django.shortcuts import render
from django.views import View

from barbershop.views import Base
from shop.models import Product


class HomeView(Base, View):
    def get(self, request):

        context = {
            'info': self.general_information,
            'products': Product.objects.filter(is_published=True)
        }

        return render(request, 'shop/index.html', context)
