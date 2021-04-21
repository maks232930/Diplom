from django.urls import path

from .views import index, service_price, gallery, contact

app_name = 'barbershop'

urlpatterns = [
    path('', index),
    path('service-price/', service_price),
    path('gallery/', gallery),
    path('contact/', contact)
]
