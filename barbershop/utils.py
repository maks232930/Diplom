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
            return timedelta(hours=time // 60, minutes=time % 60)
        return timedelta(minutes=time)


def send_sms(account_sid, auth_token, phone_number_from, phone_number_to, message):
    try:
        client = Client(account_sid, auth_token)

        client.messages.create(
            body=message,
            to=phone_number_to,
            from_=phone_number_from)
    except:
        return


def get_datetime_and_master_id(times):
    date_time = ''
    master_id = ''
    counter = 0

    for i in times:
        counter += 1

        if i == ',':
            for j in times[counter:]:
                counter += 1

                master_id += j

        if len(times) == counter:
            break

        date_time += i

    return date_time, int(master_id)
