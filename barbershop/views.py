from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt

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


# class ContactView(Base, View):
#
#     def get(self, request):
#         context = {
#             'info': self.general_information,
#             'form': MessageForm()
#         }
#
#         return render(request, 'barbershop/contact.html', context)
#
#     def post(self, request):
#         form = MessageForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('barbershop:home')
#
#         context = {
#             'info': self.general_information,
#             'form': form
#         }
#
#         return render(request, 'barbershop/contact.html', context)

@csrf_exempt
def contact_form_view(request):
    form = MessageForm()

    context = {
        'form': form,
        'info': GeneralInformation.objects.first()
    }

    if request.POST and request.is_ajax():
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Ваше сообщение отправлено.'}, status=200)
        else:
            return JsonResponse({'errors': 'Проверьте поля!'}, status=400)

    return render(request, 'barbershop/contact.html', context)


class ServicePriceView(Base, View):

    def get(self, request):
        services = Service.objects.all()

        context = {
            'info': self.general_information,
            'services': services
        }

        return render(request, 'barbershop/service_price.html', context)


class RecordingStepOneView(Base, View):
    def get(self, request):
        context = {
            'info': self.general_information
        }

        return render(request, 'barbershop/step-1.html', context)


class RecordingStepTwoView(Base, View):
    def get(self, request):
        context = {
            'info': self.general_information,
            'services': Service.objects.filter(sex=request.GET.get('sex'))
        }

        return render(request, 'barbershop/step-2.html', context)


class RecordingStepThreeView(Base, View):
    def get(self, request):
        context = {
            'info': self.general_information,
            'services': Service.objects.filter(sex=request.GET.get('sex'))
        }

        return render(request, 'barbershop/step-3.html', context)
