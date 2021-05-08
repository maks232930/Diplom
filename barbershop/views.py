from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from blog.models import Post
from .forms import MessageForm
from .models import GeneralInformation, SocialLink, Gallery, Service, FreeTime, Master, Specialization
from .utils import get_execution_time_in_normal_format


class Base:
    general_information = GeneralInformation.objects.first()
    recent_posts = Post.objects.all()[:2]


class HomeView(Base, View):

    def get(self, request):
        social_links = SocialLink.objects.all()

        context = {
            'info': self.general_information,
            'recent_posts': self.recent_posts,
            'social_links': social_links
        }

        return render(request, 'barbershop/index.html', context)


class GalleryView(Base, View):

    def get(self, request):
        images = Gallery.objects.all()

        context = {
            'info': self.general_information,
            'recent_posts': self.recent_posts,
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
        'recent_posts': Post.objects.all()[:2],
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
            'recent_posts': self.recent_posts,
            'services': services
        }

        return render(request, 'barbershop/service_price.html', context)


class RecordingStepOneView(Base, View):
    def get(self, request):
        context = {
            'recent_posts': self.recent_posts,
            'info': self.general_information,
            'categories': Specialization.objects.all()
        }

        return render(request, 'barbershop/step-1.html', context)


class RecordingStepTwoView(Base, View):
    def get(self, request):
        context = {
            'info': self.general_information,
            'recent_posts': self.recent_posts,
            'services': Service.objects.filter(specialisation__id=request.GET.get('category'))
        }

        return render(request, 'barbershop/step-2.html', context)


class RecordingStepThreeView(Base, View):
    def get(self, request):
        services_id = request.GET.getlist('service_id')
        services = Service.objects.filter(id__in=services_id)
        if services is None:
            return redirect('barbershop:recording_step_two')
        len_services = len(services)

        masters = Master.objects.all()
        suitable_masters = []

        for master in masters:

            counter = 0
            for service in services:
                counter += 1
                if service in master.get_services():
                    if counter == len_services:
                        suitable_masters.append(master)
                    continue
                break

        execution_time_and_price = Service.objects.filter(id__in=services_id).values('execution_time', 'price')
        spent_minutes = execution_time_and_price.values('execution_time').aggregate(Sum('execution_time'))
        execution_time = get_execution_time_in_normal_format(spent_minutes.get('execution_time__sum'))
        price_services = execution_time_and_price.values('price').aggregate(Sum('price')).get('price__sum')

        times = FreeTime.objects.filter(is_free=True, master__in=suitable_masters)

        context = {
            'info': self.general_information,
            'recent_posts': self.recent_posts,
            'execution_time': execution_time,
            'times': times,
            'price_services': price_services,
            'services': Service.objects.filter(id__in=services_id).values('name')
        }

        return render(request, 'barbershop/step-3.html', context)
