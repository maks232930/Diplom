from django.shortcuts import render, redirect
from django.views import View

from .forms import MessageForm
from .models import GeneralInformation, SocialLink, Gallery, Service


class Base:
    general_information = GeneralInformation.objects.first()


class HomeView(Base, View):

    def get(self, request):
        social_links = SocialLink.objects.all()

        context = {
            'info': self.general_information,
            'social_links': social_links
        }

        return render(request, 'barbershop/index.html', context)


class GalleryView(Base, View):

    def get(self, request):
        images = Gallery.objects.all()

        context = {
            'info': self.general_information,
            'images': images
        }

        return render(request, 'barbershop/gallery.html', context)


class ContactView(Base, View):

    def get(self, request):
        context = {
            'info': self.general_information,
            'form': MessageForm()
        }

        return render(request, 'barbershop/contact.html', context)

    def post(self, request):
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('barbershop:home')

        context = {
            'info': self.general_information,
            'form': form
        }

        return render(request, 'barbershop/contact.html', context)


class ServicePriceView(Base, View):

    def get(self, request):
        services = Service.objects.all()

        context = {
            'info': self.general_information,
            'services': services
        }

        return render(request, 'barbershop/service_price.html', context)
