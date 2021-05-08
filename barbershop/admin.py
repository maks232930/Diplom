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
    WorkingHours,
    FreeTime,
    Specialization
)


class GeneralInformationAdmin(admin.ModelAdmin):
    list_display = ('name', 'heading', 'contact_number', 'contact_number_description',
                    'contact_email', 'location', 'location_description', 'working_days', 'working_hours',
                    )
    list_display_links = ('name', 'heading', 'contact_number', 'contact_number_description',
                          'contact_email', 'location', 'location_description', 'working_days', 'working_hours',
                          )


class WorkingHoursAdmin(admin.StackedInline):
    model = WorkingHours
    extra = 1
    show_change_link = True


class MasterAdmin(admin.ModelAdmin):
    inlines = [WorkingHoursAdmin]


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('specialisation', 'name', 'price', 'execution_time')
    list_display_links = ('specialisation', 'name', 'price', 'execution_time')

    list_filter = ('specialisation', )


class FreeTimeAdmin(admin.ModelAdmin):
    list_display = ('master', 'date_time', 'is_free')
    list_display_links = ('master', 'date_time')

    list_editable = ('is_free',)


admin.site.register(SocialLink)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Recording)
admin.site.register(WorkingHours)
admin.site.register(Master, MasterAdmin)
admin.site.register(Gallery)
admin.site.register(Message)
admin.site.register(FreeTime, FreeTimeAdmin)
admin.site.register(Statistics)
admin.site.register(Specialization)
admin.site.register(GeneralInformation, GeneralInformationAdmin)
