from datetime import timedelta, datetime

from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from blog.models import Post
from .forms import MessageForm, ReviewForm, RecordingForm
from .models import (
    GeneralInformation,
    SocialLink,
    Gallery,
    Service,
    FreeTime,
    Master,
    Specialization,
    Review,
    Recording
)
from .utils import get_execution_time_in_normal_format


class Base:
    general_information = GeneralInformation.objects.first()


class HomeView(Base, View):

    def get(self, request):
        context = {
            'info': self.general_information,
            'social_links': SocialLink.objects.all(),
            'masters': Master.objects.all()
        }

        return render(request, 'barbershop/index.html', context)


class GalleryView(Base, View):

    def get(self, request):
        context = {
            'info': self.general_information,
            'images': Gallery.objects.all()
        }

        return render(request, 'barbershop/gallery.html', context)


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
        context = {
            'info': self.general_information,
            'specialisations': Specialization.objects.all()
        }

        return render(request, 'barbershop/service_price.html', context)


class RecordingStepOneView(Base, View):
    def get(self, request):
        context = {
            'info': self.general_information,
            'categories': Specialization.objects.all()
        }

        return render(request, 'barbershop/step-1.html', context)


class RecordingStepTwoView(Base, View):
    def get(self, request):
        category = request.GET.get('category')
        services = Service.objects.filter(specialisation__id=category)

        if not services:
            return redirect('barbershop:recording_step_one')

        context = {
            'info': self.general_information,
            'services': Service.objects.filter(specialisation__id=category),
        }

        return render(request, 'barbershop/step-2.html', context)


class RecordingStepThreeView(Base, View):
    def get(self, request):
        services_id = request.GET.getlist('service_id')
        services = Service.objects.filter(id__in=services_id)

        len_services = len(services)
        return_path = request.META.get('HTTP_REFERER', '/')

        if not services or len_services != len(services_id):
            return redirect(return_path)

        masters = Master.objects.all()
        times = FreeTime.objects.filter(date_time__gte=datetime.today()).order_by('date_time')

        result_list_times = []

        execution_time_and_price = Service.objects.filter(id__in=services_id).values('execution_time', 'price')
        spent_minutes = execution_time_and_price.values('execution_time').aggregate(Sum('execution_time'))
        execution_time = get_execution_time_in_normal_format(spent_minutes.get('execution_time__sum'))
        price_services = execution_time_and_price.values('price').aggregate(Sum('price')).get('price__sum')

        execution_time_in_datetime_format = get_execution_time_in_normal_format(
            spent_minutes.get('execution_time__sum'), 'datetime')

        for master in masters:
            counter = 0
            for service in services:
                counter += 1
                if service in master.get_services():
                    if counter == len_services:
                        counter_times = 0
                        for time in times.filter(master=master):
                            counter_times += 1
                            if time.status == 'works_free' or 'start_day':
                                last_time = timedelta(hours=time.date_time.hour,
                                                      minutes=time.date_time.minute) + execution_time_in_datetime_format
                                for t in times.all()[counter_times:]:
                                    if t.status == 'works_free' or 'start_day':
                                        if timedelta(hours=t.date_time.hour, minutes=t.date_time.minute) >= last_time:
                                            result_list_times.append(time)
                                            break
                                        continue
                                    else:
                                        if timedelta(hours=t.date_time.hour, minutes=t.date_time.minute) >= last_time:
                                            result_list_times.append(time)
                                            break
                                        break
                    continue
                break

        context = {
            'info': self.general_information,
            'execution_time': execution_time,
            'times': result_list_times,
            'masters': set([time.master.user.get_full_name() for time in result_list_times]),
            'price_services': price_services,
            'services': Service.objects.filter(id__in=services_id).values('name', 'id'),
            'category_id': Specialization.objects.filter(service__in=services_id).values('id').first(),
        }

        return render(request, 'barbershop/step-3.html', context)


# class RecordingSteepFourView(Base, View):
#     def get(self, request):
#         price = request.GET.get('price')
#         time_start = datetime.strptime(request.GET.get('times'), '%Y-%m-%d %H:%M')
#         execution_time = request.GET.get('execution_time')
#         services_id = request.GET.getlist('services_id')
#
#         services = Service.objects.filter(id__in=services_id)
#         free_times = FreeTime.objects.filter(date_time__gte=time_start).order_by('date_time')
#
#         if len(services_id) != len(services) or float(price.replace(',', '.')) != services.values('price').aggregate(
#                 Sum('price')).get('price__sum'):
#             return redirect('barbershop:recording_step_one')
#
#         spent_minutes = services.values('execution_time').aggregate(Sum('execution_time'))
#         execution_time_in_datetime_format = get_execution_time_in_normal_format(
#             spent_minutes.get('execution_time__sum'), 'datetime')
#
#         times = []
#         counter_free_times = 0
#         for time in free_times:
#             if len(times):
#                 break
#             counter_free_times += 1
#             if time.status == 'works_free' or 'start_day':
#                 last_time = timedelta(hours=time.date_time.hour,
#                                       minutes=time.date_time.minute) + execution_time_in_datetime_format
#                 for t in free_times.all()[counter_free_times:]:
#                     if t.status == 'works_free' or 'start_day':
#                         if timedelta(hours=t.date_time.hour, minutes=t.date_time.minute) >= last_time:
#                             times.append(t)
#                             break
#                         continue
#                     else:
#                         if timedelta(hours=t.date_time.hour, minutes=t.date_time.minute) >= last_time:
#                             times.append(t)
#                             break
#                         break
#             break
#
#         right_time = []
#         for time in free_times:
#             if time != times[0]:
#                 right_time.append(time)
#             else:
#                 right_time.append(time)
#                 break
#
#         form = RecordingForm(initial={'date_and_time_of_recording': right_time, 'services': services})
#
#         context = {
#             'info': self.general_information,
#             'recent_posts': self.recent_reviews,
#             'form': form,
#             'services': services,
#             'recording_time': right_time[0],
#             'price': price,
#             'execution_time': execution_time
#         }
#
#         return render(request, 'barbershop/step-4.html', context)

def recording_steep_four(request):
    price = request.GET.get('price')
    time_start = datetime.strptime(request.GET.get('times'), '%Y-%m-%d %H:%M')
    execution_time = request.GET.get('execution_time')
    services_id = request.GET.getlist('services_id')

    services = Service.objects.filter(id__in=services_id)
    free_times = FreeTime.objects.filter(date_time__gte=time_start).order_by('date_time')

    return_path = request.META.get('HTTP_REFERER', '/')

    if len(services_id) != len(services) or float(price.replace(',', '.')) != services.values('price').aggregate(
            Sum('price')).get('price__sum'):
        return redirect(return_path)

    spent_minutes = services.values('execution_time').aggregate(Sum('execution_time'))
    execution_time_in_datetime_format = get_execution_time_in_normal_format(
        spent_minutes.get('execution_time__sum'), 'datetime')

    times = []
    counter_free_times = 0
    for time in free_times:
        if len(times):
            break
        counter_free_times += 1
        if time.status == 'works_free' or 'start_day':
            last_time = timedelta(hours=time.date_time.hour,
                                  minutes=time.date_time.minute) + execution_time_in_datetime_format
            for t in free_times.all()[counter_free_times:]:
                if t.status == 'works_free' or 'start_day':
                    if timedelta(hours=t.date_time.hour, minutes=t.date_time.minute) >= last_time:
                        times.append(t)
                        break
                    continue
                else:
                    if timedelta(hours=t.date_time.hour, minutes=t.date_time.minute) >= last_time:
                        times.append(t)
                        break
                    break
        break

    right_time = []
    for time in free_times:
        if time != times[0]:
            right_time.append(time)
        else:
            right_time.append(time)
            break

    form = RecordingForm(initial={'date_and_time_of_recording': right_time, 'services': services})

    if request.method == 'POST':
        form = RecordingForm(request.POST)

        del form.errors['date_and_time_of_recording']
        del form.errors['services']
        del form.errors['price']

        if form.is_valid():
            try:
                recordings = Recording.objects.all()

                for time in right_time:
                    if datetime.now() > time.date_time:
                        return redirect(return_path)

                for recording in recordings:
                    for time in recording.date_and_time_of_recording.all():
                        if time in right_time:
                            return redirect(return_path)

                instance = form.save(commit=False)
                instance.price = float(price.replace(',', '.'))
                instance.save()
                instance.date_and_time_of_recording.set(right_time)
                instance.services.set(services)

                return redirect('barbershop:home')
            except Exception:
                return redirect(return_path)

    context = {
        'info': GeneralInformation.objects.first(),
        'recent_posts': Review.objects.order_by('date_time')[:2],
        'form': form,
        'services': services,
        'recording_time': right_time[0],
        'price': price,
        'execution_time': execution_time,
        'return_path': return_path
    }

    return render(request, 'barbershop/step-4.html', context)


class ReviewView(Base, View):
    def get(self, request):
        reviews = Review.objects.filter(is_show=True).order_by('date_time')
        paginator = Paginator(reviews, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        form = ReviewForm()

        context = {
            'info': self.general_information,
            'form': form,
            'page_obj': page_obj
        }

        return render(request, 'barbershop/review.html', context)

    def post(self, request):
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('barbershop:review')
        return redirect('barbershop:review')
