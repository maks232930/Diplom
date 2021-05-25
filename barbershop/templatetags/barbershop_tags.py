from django import template

from barbershop.models import Specialization, Review

register = template.Library()


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


@register.inclusion_tag('barbershop/list_specializations.html')
def get_specialisation():
    return {'specializations': Specialization.objects.values('name')}


@register.inclusion_tag('barbershop/list_review.html')
def get_recent_review():
    return {'reviews': Review.objects.order_by('date_time')[:2]}

