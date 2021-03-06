from datetime import datetime, timedelta

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import ListView
from easy_pdf.views import PDFTemplateResponseMixin

import GraduateWork.settings
from barbershop.models import Master, Recording, FreeTime, Service
from users.forms import LoginForm, GenerateFreeTimesForm, RecordingByDateForm, GenerateReportPdfForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('barbershop:home')

    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect('users:profile_admin')
                else:
                    return redirect('users:profile_master')

    context = {
        'form': form,
    }

    return render(request, 'users/login.html', context)


@login_required
def profile_for_admin_view(request):
    if not request.user.is_superuser:
        return redirect('users:profile_master')

    master = Master.objects.filter(user=request.user).first()
    recordings = Recording.objects.all()

    date_time_start = datetime.strptime(f'{datetime.now().day}.{datetime.now().month}.{datetime.now().year} 00:00:00',
                                        '%d.%m.%Y %H:%M:%S')
    date_time_end = datetime.strptime(f'{datetime.now().day}.{datetime.now().month}.{datetime.now().year} 23:59:59',
                                      '%d.%m.%Y %H:%M:%S')

    if master is not None:
        recordings_master = recordings.filter(date_and_time_of_recording__master=master,
                                              date_and_time_of_recording__date_time__range=(
                                                  date_time_start, date_time_end))

        context = {
            'recordings': set(recordings_master),
        }

    else:
        context = {
            'recordings': recordings,
        }

    return render(request, 'users/profile_for_admin.html', context)


@login_required
def profile_for_master_view(request):
    if request.user.is_superuser:
        return redirect('users:profile_admin')

    master = Master.objects.get(user=request.user)

    if request.GET.get('date'):
        date_ = datetime.strptime(str(request.GET.get('date')), '%Y-%m-%d')

        date_time_start = datetime.strptime(f'{date_.day}.{date_.month}.{date_.year} 00:00:00',
                                            '%d.%m.%Y %H:%M:%S')
        date_time_end = datetime.strptime(f'{date_.day}.{date_.month}.{date_.year} 23:59:59',
                                          '%d.%m.%Y %H:%M:%S')

        recordings = Recording.objects.filter(date_and_time_of_recording__master=master,
                                              date_and_time_of_recording__date_time__range=(
                                                  date_time_start, date_time_end))

        form = RecordingByDateForm(initial={'date': date_})

        context = {
            'date': f'{date_.day}.{date_.month}.{date_.year}',
            'form': form,
            'recordings': set(recordings)
        }

        return render(request, 'users/profile_for_master.html', context)

    date_time_start = datetime.strptime(f'{datetime.now().day}.{datetime.now().month}.{datetime.now().year} 00:00:00',
                                        '%d.%m.%Y %H:%M:%S')
    date_time_end = datetime.strptime(f'{datetime.now().day}.{datetime.now().month}.{datetime.now().year} 23:59:59',
                                      '%d.%m.%Y %H:%M:%S')

    recordings = Recording.objects.filter(date_and_time_of_recording__master=master,
                                          date_and_time_of_recording__date_time__range=(date_time_start, date_time_end))

    date_now = datetime.strptime(f'{datetime.now().day}.{datetime.now().month}.{datetime.now().year}', '%d.%m.%Y')
    form = RecordingByDateForm(initial={'date': date_now})

    context = {
        'date': f'{datetime.now().day}.{datetime.now().month}.{datetime.now().year}',
        'form': form,
        'recordings': set(recordings)
    }

    return render(request, 'users/profile_for_master.html', context)


def user_logout(request):
    logout(request)
    return redirect('barbershop:home')


@login_required
def generate_free_times_step_one(request):
    if not request.user.is_superuser:
        return redirect('users:profile_master')

    return_path = request.META.get('HTTP_REFERER', '/')

    form = GenerateFreeTimesForm()

    context = {
        'form': form,
        'return_path': return_path
    }

    return render(request, 'users/generate_free_times_step_1.html', context)


@login_required
def generate_free_times_step_two(request):
    if not request.user.is_superuser:
        return redirect('users:profile_master')

    master = Master.objects.get(id=request.GET.get('master'))
    start_day = datetime.strptime(request.GET.get('start_day').replace('T', ' '), '%Y-%m-%d %H:%M')
    end_day = datetime.strptime(request.GET.get('end_day').replace('T', ' '), '%Y-%m-%d %H:%M')
    interval = timedelta(minutes=int(request.GET.get('interval')))

    start_day_timedelta = timedelta(days=start_day.day, hours=start_day.hour, minutes=start_day.minute,
                                    seconds=start_day.second)
    end_day_timedelta = timedelta(days=end_day.day, hours=end_day.hour, minutes=end_day.minute, seconds=end_day.second)

    times = [start_day]

    while True:
        if start_day_timedelta >= end_day_timedelta:
            break

        start_day_timedelta += interval

        total_seconds = start_day_timedelta.total_seconds()

        new_date_time = start_day.replace(day=start_day_timedelta.days,
                                          hour=int((total_seconds // 3600) % 24),
                                          minute=int((total_seconds % 3600) // 60),
                                          second=int((total_seconds % 3600) % 60)
                                          )

        times.append(new_date_time)

    if request.method == 'POST':
        free_times = [time.date_time for time in FreeTime.objects.filter(master=master)]

        times_list = [datetime.strptime(time, '%Y-%m-%d %H:%M') for time in request.POST.getlist('time')]

        start_day = times_list[0]
        end_day = times_list[-1]

        free_times_list = []

        for time in times:
            if time not in free_times:
                if time == start_day:
                    free_times_list.append(FreeTime(master=master, date_time=time, status='start_day'))
                    continue
                if time == end_day:
                    free_times_list.append(FreeTime(master=master, date_time=time, status='end_day'))
                    continue
                if time not in times_list:
                    free_times_list.append(FreeTime(master=master, date_time=time, status='does_not_work'))
                    continue
                free_times_list.append(FreeTime(master=master, date_time=time))

        FreeTime.objects.bulk_create(free_times_list)

        return redirect('users:profile_admin')

    context = {
        'times': times
    }

    return render(request, 'users/generate_free_times_step_2.html', context)


@login_required
def generate_report_pdf_step_one(request):
    if not request.user.is_superuser:
        return redirect('users:profile_master')

    context = {
        'form': GenerateReportPdfForm(),
        'return_path': request.META.get('HTTP_REFERER', '/')
    }

    return render(request, 'users/generate_report_pdf_step_one.html', context)


class PDFUserDetailView(PDFTemplateResponseMixin, ListView):
    model = Master
    template_name = 'users/report_pdf.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        services = []
        result_list = []

        result_price = 0
        result_count = 0
        result_time = 0

        master = Master.objects.filter(id=int(self.request.GET.get('master'))).first()

        start_date = datetime.strptime(self.request.GET.get('start_date'), '%Y-%m-%d')
        end_date = datetime.strptime(self.request.GET.get('end_date'), '%Y-%m-%d')

        recordings = Recording.objects.filter(date_and_time_of_recording__master=master,
                                              date_and_time_of_recording__date_time__range=(start_date, end_date))

        for recording in recordings:
            for service in recording.services.all().values('name'):
                services.append(f"{service['name']}")

        set_services = set(services)
        services_ = Service.objects.filter(name__in=set_services)

        for service in set_services:
            service_ = services_.filter(name=service).first()
            result_list.append(
                [service, int(services.count(service)), int(services.count(service) * service_.execution_time),
                 int(services.count(service)) * service_.price])

        for _, count, time, price in result_list:
            result_price += price
            result_count += count
            result_time += time

        context['services'] = result_list
        context['start_date'] = start_date
        context['end_date'] = end_date
        context['master'] = master
        context['result_price'] = result_price
        context['result_count'] = result_count
        context['result_time'] = result_time
        context['base'] = GraduateWork.settings.BASE_DIR

        return context
