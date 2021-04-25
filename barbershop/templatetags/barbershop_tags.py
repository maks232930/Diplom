from django import template

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
