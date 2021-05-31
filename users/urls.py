from django.urls import path

from users.views import login_view, user_logout, profile_view

app_name = 'users'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/', profile_view, name='profile')
]
