from django.urls import path

from .views import (
    HomeView,
    ServicePriceView,
    GalleryView,
    contact_form_view,
    RecordingStepOneView
)

app_name = 'barbershop'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('service-price/', ServicePriceView.as_view(), name='service_price'),
    path('gallery/', GalleryView.as_view(), name='gallery'),
    path('contact/', contact_form_view, name='contact'),
    path('recording-step-one/', RecordingStepOneView.as_view(), name='recording_step_one'),
    path('recording-step-two/', RecordingStepOneView.as_view(), name='recording_step_two'),
]
