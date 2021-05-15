from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View

from barbershop.views import Base
from shop.models import Product


class HomeView(Base, View):
    def get(self, request):
        products = Product.objects.order_by('id')
        page_number = request.GET.get('page')

        paginator = Paginator(products, 20)
        page_obj = paginator.get_page(page_number)

        context = {
            'info': self.general_information,
            'products': page_obj
        }

        return render(request, 'shop/index.html', context)
