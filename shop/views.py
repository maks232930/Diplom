from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View

from shop.models import Product


class HomeView(View):
    @staticmethod
    def get(request):
        products = Product.objects.order_by('id')
        page_number = request.GET.get('page')

        paginator = Paginator(products, 20)
        page_obj = paginator.get_page(page_number)

        context = {
            'products': page_obj
        }

        return render(request, 'shop/index.html', context)
