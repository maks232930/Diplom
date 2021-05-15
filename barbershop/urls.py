from django.urls import path

from .views import (
    HomeView,
    ServicePriceView,
    GalleryView,
    contact_form_view,
    RecordingStepOneView,
    RecordingStepTwoView,
    RecordingStepThreeView,
    RecordingSteepFourView,
    ReviewView
)

app_name = 'barbershop'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('service-price/', ServicePriceView.as_view(), name='service_price'),
    path('gallery/', GalleryView.as_view(), name='gallery'),
    path('contact/', contact_form_view, name='contact'),
    path('review/', ReviewView.as_view(), name='review'),
    path('recording-step-one/', RecordingStepOneView.as_view(), name='recording_step_one'),
    path('recording-step-two/', RecordingStepTwoView.as_view(), name='recording_step_two'),
    path('recording-step-three/', RecordingStepThreeView.as_view(), name='recording_step_three'),
    path('recording-step-four/', RecordingSteepFourView.as_view(), name='recording_step_four'),
]
