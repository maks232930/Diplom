from django.shortcuts import render
from django.views import View

from barbershop.views import Base


class HomeView(Base, View):
    def get(self, request):

        context = {
            'info': self.general_information
        }

        return render(request, 'shop/index.html', context)
