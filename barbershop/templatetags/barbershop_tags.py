from django import template

from barbershop.models import Specialization, Review, SocialLink, GeneralInformation

register = template.Library()
general_information = GeneralInformation.objects.values('main_photo', 'mini_text', 'contact_number', 'contact_email', 'location',
                                                        'name').first()


def plural_rus_variant(hours):
    last_two_digits = hours % 100
    tens = last_two_digits // 10
    if tens == 1:
        return 2
    ones = last_two_digits % 10
    if ones == 1:
        return 0
    if 2 <= ones <= 4:
        return 1
    return 2


@register.simple_tag
def get_execution_time_in_normal_format(time):
    if time > 60:
        hours = time // 60
        suffix = ["час", "часа", "часов"][plural_rus_variant(hours)]
        return f'{time // 60} {suffix} {time % 60} минут'
    return f'{time} минут'


@register.simple_tag
def get_time_start(time):
    return time.date_time


@register.simple_tag
def get_execution_time_in_normal_format(time, input_format='int'):
    if input_format == 'list':
        count_minutes = 0
        for t in time:
            count_minutes += t.execution_time
        time = count_minutes

    if time > 60:
        hours = time // 60
        suffix = ["час", "часа", "часов"][plural_rus_variant(hours)]
        return f'{time // 60} {suffix} {time % 60} минут'
    return f'{time} минут'


@register.inclusion_tag('barbershop/list_specializations.html')
def get_specialisations():
    return {'specializations': Specialization.objects.values('name')}


@register.inclusion_tag('barbershop/list_recent_reviews.html')
def get_recent_reviews():
    return {'reviews': Review.objects.order_by('date_time')[:2]}


@register.inclusion_tag('barbershop/list_social_links.html')
def get_social_links():
    return {'social_links': SocialLink.objects.all()}


@register.inclusion_tag('barbershop/list_contacts.html')
def get_contacts():
    return {'info': general_information}


@register.inclusion_tag('barbershop/mini_text_tpl.html')
def get_mini_text():
    return {'info': general_information}


@register.inclusion_tag('barbershop/logo_tpl.html')
def get_logo_name():
    return {'info': general_information}


@register.inclusion_tag('barbershop/main_photo_tpl.html')
def get_main_photo():
    return {'info': GeneralInformation.objects.first()}
