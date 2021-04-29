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


class GeneralInformationAdmin(admin.ModelAdmin):
    list_display = ('name', 'heading', 'contact_number', 'contact_number_description',
                    'contact_email', 'location', 'location_description', 'working_days', 'working_hours',
                    )
    list_display_links = ('name', 'heading', 'contact_number', 'contact_number_description',
                          'contact_email', 'location', 'location_description', 'working_days', 'working_hours',
                          )


admin.site.register(SocialLink)
admin.site.register(Service)
admin.site.register(Recording)
admin.site.register(WorkingHours)
admin.site.register(Master)
admin.site.register(Gallery)
admin.site.register(Message)
admin.site.register(Statistics)
admin.site.register(GeneralInformation, GeneralInformationAdmin)
