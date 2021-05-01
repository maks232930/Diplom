from django.urls import path

from .views import (
    HomeView,
    ServicePriceView,
    GalleryView,
    contact_form_view
)

app_name = 'barbershop'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('service-price/', ServicePriceView.as_view(), name='service_price'),
    path('gallery/', GalleryView.as_view(), name='gallery'),
    path('contact/', contact_form_view, name='contact')
]
