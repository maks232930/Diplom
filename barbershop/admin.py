from django.contrib import admin

from .models import (
    Specialization,
    SocialLink,
    Master,
    Gallery,
    Message,
    Statistics,
    ServicePrice,
    GeneralInformation
)

admin.site.register(Specialization)
admin.site.register(SocialLink)
admin.site.register(Master)
admin.site.register(Gallery)
admin.site.register(Message)
admin.site.register(Statistics)
admin.site.register(ServicePrice)
admin.site.register(GeneralInformation)
