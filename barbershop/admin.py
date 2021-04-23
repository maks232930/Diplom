from django.contrib import admin

from .models import (
    SocialLink,
    Master,
    Gallery,
    Message,
    Statistics,
    GeneralInformation,
    Service,
    Recording,
    WorkingHours
)

admin.site.register(SocialLink)
admin.site.register(Service)
admin.site.register(Recording)
admin.site.register(WorkingHours)
admin.site.register(Master)
admin.site.register(Gallery)
admin.site.register(Message)
admin.site.register(Statistics)
admin.site.register(GeneralInformation)
