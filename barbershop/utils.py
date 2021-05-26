from datetime import timedelta

from twilio.rest import Client

from .templatetags.barbershop_tags import plural_rus_variant


def get_execution_time_in_normal_format(time, return_format='str'):
    if return_format == 'str':
        if time > 60:
            hours = time // 60
            suffix = ["час", "часа", "часов"][plural_rus_variant(hours)]
            return f'{time // 60} {suffix} {time % 60} минут'
        return f'{time} минут'
    else:
        if time > 60:
            return timedelta(hours=time // 60, minutes=time * 60)
        return timedelta(minutes=60)


def send_sms(account_sid, auth_token, phone_number_from, phone_number_to, message):
    client = Client(account_sid, auth_token)

    client.messages.create(
        body=message,
        to=phone_number_to,
        from_=phone_number_from)
