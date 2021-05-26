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
    FreeTime,
    Specialization,
    Review,
    TwilioSettings
)


class GeneralInformationAdmin(admin.ModelAdmin):
    list_display = ('name', 'heading', 'contact_number', 'contact_number_description',
                    'contact_email', 'location', 'location_description', 'working_days', 'working_hours',
                    )
    list_display_links = ('name', 'heading', 'contact_number', 'contact_number_description',
                          'contact_email', 'location', 'location_description', 'working_days', 'working_hours',
                          )


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('specialisation', 'name', 'price', 'execution_time')
    list_display_links = ('specialisation', 'name', 'price', 'execution_time')

    list_filter = ('specialisation',)


class FreeTimeAdmin(admin.ModelAdmin):
    list_display = ('id', 'master', 'date_time', 'status')
    list_display_links = ('master', 'date_time')

    list_filter = ('status', 'master')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'is_show', 'date_time')
    list_display_links = ('name', 'email', 'date_time')

    list_editable = ('is_show', )
    list_filter = ('email', 'is_show')


admin.site.register(SocialLink)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Recording)
admin.site.register(Master)
admin.site.register(Gallery)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Message)
admin.site.register(FreeTime, FreeTimeAdmin)
admin.site.register(Statistics)
admin.site.register(Specialization)
admin.site.register(GeneralInformation, GeneralInformationAdmin)
admin.site.register(TwilioSettings)
