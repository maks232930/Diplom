from django.urls import path

from .views import HomeView, service_price, gallery, contact

app_name = 'barbershop'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('service-price/', service_price),
    path('gallery/', gallery),
    path('contact/', contact)
]
