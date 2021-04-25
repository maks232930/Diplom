from django.urls import path

from .views import (
    HomeView,
    ServicePriceView,
    GalleryView,
    ContactView
)

app_name = 'barbershop'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('service-price/', ServicePriceView.as_view(), name='service_price'),
    path('gallery/', GalleryView.as_view(), name='gallery'),
    path('contact/', ContactView.as_view(), name='contact')
]
