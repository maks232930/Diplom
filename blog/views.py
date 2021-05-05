from django.shortcuts import render
from django.views import View

from barbershop.views import Base
from blog.models import Post


class HomeView(Base, View):
    def get(self, request):

        context = {
            'info': self.general_information,
            'posts': Post.objects.filter(is_published=True)
        }

        return render(request, 'blog/index.html', context)
