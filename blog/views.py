from django.shortcuts import render
from django.views import View

from blog.models import Post


class HomeView(View):
    def get(self, request):

        context = {
            'posts': Post.objects.filter(is_published=True)
        }

        return render(request, 'blog/index.html', context)
