from datetime import timedelta, datetime

from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt

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
    Recording,
    Statistics,
    TwilioSettings
)
from .utils import get_execution_time_in_normal_format, send_sms


class HomeView(View):
    @staticmethod
    def get(request):
        context = {
            'info': GeneralInformation.objects.first(),
            'masters': Master.objects.all(),
            'statistics': Statistics.objects.all()
        }

        return render(request, 'barbershop/index.html', context)


class GalleryView(View):
    @staticmethod
    def get(request):
        context = {
            'images': Gallery.objects.all()
        }

        return render(request, 'barbershop/gallery.html', context)


@csrf_exempt
def contact_form_view(request):
    form = MessageForm()

    context = {
        'form': form,
    }

    if request.POST and request.is_ajax():
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Ваше сообщение отправлено.'}, status=200)
        else:
            return JsonResponse({'errors': 'Проверьте поля!'}, status=400)

    return render(request, 'barbershop/contact.html', context)


class ServicePriceView(View):
    @staticmethod
    def get(request):
        context = {
            'specialisations': Specialization.objects.all()
        }

        return render(request, 'barbershop/service_price.html', context)


class RecordingStepOneView(View):
    @staticmethod
    def get(request):
        context = {
            'categories': Specialization.objects.all()
        }

        return render(request, 'barbershop/step-1.html', context)


class RecordingStepTwoView(View):
    @staticmethod
    def get(request):
        category = request.GET.get('category')
        services = Service.objects.filter(specialisation__id=category)

        if not services:
            return redirect('barbershop:recording_step_one')

        context = {
            'services': Service.objects.filter(specialisation__id=category),
        }

        return render(request, 'barbershop/step-2.html', context)


class RecordingStepThreeView(View):
    @staticmethod
    def get(request):
        services_id = request.GET.getlist('service_id')
        services = Service.objects.filter(id__in=services_id)

        len_services = len(services)
        return_path = request.META.get('HTTP_REFERER', '/')

        if not services or len_services != len(services_id):
            return redirect(return_path)

        result_list_times = []

        masters = Master.objects.all().select_related('user').prefetch_related('services')
        times = FreeTime.objects.filter(date_time__gte=datetime.today()).select_related('master__user').order_by('date_time')

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
                master_services = master.get_services()
                if service in master_services:
                    if counter == len_services:
                        counter_times = 0
                        filter_times = times.filter(master=master)
                        for time in filter_times:
                            counter_times += 1
                            if time.status in ['works_free', 'start_day']:
                                last_time = timedelta(hours=time.date_time.hour,
                                                      minutes=time.date_time.minute,
                                                      days=time.date_time.day) + execution_time_in_datetime_format
                                start_times = times.all()[counter_times:]
                                for t in start_times:
                                    if t.status in ['works_free', 'start_day']:
                                        if timedelta(hours=t.date_time.hour, minutes=t.date_time.minute,
                                                     days=t.date_time.day) >= last_time:
                                            result_list_times.append(time)
                                            break
                                        continue
                                    elif t.status == 'end_day':
                                        if timedelta(hours=t.date_time.hour, minutes=t.date_time.minute,
                                                     days=t.date_time.day) >= last_time:
                                            result_list_times.append(time)
                                            break
                                        break

                    continue
                break

        context = {
            'execution_time': execution_time,
            'times': result_list_times,
            'masters': set([time.master.user.get_full_name() for time in result_list_times]),
            'price_services': price_services,
            'services': Service.objects.filter(id__in=services_id).values('name', 'id'),
            'category': Specialization.objects.filter(service__in=services_id).values('id').first(),
        }

        return render(request, 'barbershop/step-3.html', context)


def recording_steep_four(request):
    price = request.GET.get('price')
    time_start = datetime.strptime(request.GET.get('times'), '%Y-%m-%d %H:%M')
    execution_time = request.GET.get('execution_time')
    services_id = request.GET.getlist('services_id')

    services = Service.objects.filter(id__in=services_id)
    free_times = FreeTime.objects.filter(date_time__gte=time_start).order_by('date_time')
    info = GeneralInformation.objects.first()

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
        if time.status in ['works_free', 'start_day']:
            last_time = timedelta(hours=time.date_time.hour,
                                  minutes=time.date_time.minute,
                                  days=time.date_time.day) + execution_time_in_datetime_format
            for t in free_times.all()[counter_free_times:]:
                if t.status in ['works_free', 'start_day']:
                    if timedelta(hours=t.date_time.hour, minutes=t.date_time.minute, days=t.date_time.day) >= last_time:
                        times.append(t)
                        break
                    continue
                else:
                    if timedelta(hours=t.date_time.hour, minutes=t.date_time.minute, days=t.date_time.day) >= last_time:
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

        del form.errors['date_and_time_of_recording'], form.errors['services'], form.errors['price']

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

                updated_times = []

                for time in right_time:
                    if time.status in ['start_day', 'end_day']:
                        updated_times.append(time)
                    else:
                        time.status = 'works_busy'
                        time.save()
                        updated_times.append(time)

                instance.date_and_time_of_recording.set(updated_times)
                instance.services.set(services)

                twilio_settings = TwilioSettings.objects.first()
                if twilio_settings:
                    message = f"Сообщение из парикмахерской {info.name}. Ваш номер заказа {instance.id}. У вас запись на {right_time[0].date_time}. Длительность {execution_time}."
                    send_sms(account_sid=twilio_settings.account_sid, auth_token=twilio_settings.auth_token,
                             phone_number_from=twilio_settings.phone_number, phone_number_to=str(instance.phone),
                             message=message)

                return redirect('barbershop:recording_done')
            except Exception:
                return redirect(return_path)

    context = {
        'recent_posts': Review.objects.order_by('date_time')[:2],
        'form': form,
        'services': services,
        'recording_time': right_time[0],
        'price': price,
        'execution_time': execution_time,
        'return_path': return_path
    }

    return render(request, 'barbershop/step-4.html', context)


class RecordingDoneView(View):
    @staticmethod
    def get(request):
        context = {

        }

        return render(request, 'barbershop/recording_done.html', context)


class ReviewView(View):
    @staticmethod
    def get(request):
        reviews = Review.objects.filter(is_show=True).order_by('date_time')
        paginator = Paginator(reviews, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        form = ReviewForm()

        context = {
            'form': form,
            'page_obj': page_obj
        }

        return render(request, 'barbershop/review.html', context)

    @staticmethod
    def post(request):
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('barbershop:review')
        return redirect('barbershop:review')
