from django.urls import path

from users.views import (
    login_view,
    user_logout,
    profile_for_admin_view,
    profile_for_master_view,
    generate_free_times_step_one,
    generate_free_times_step_two
)

app_name = 'users'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile-admin/', profile_for_admin_view, name='profile_admin'),
    path('profile-master/', profile_for_master_view, name='profile_master'),
    path('generate-free-times-step-one/', generate_free_times_step_one, name='generate_free_times_step_one'),
    path('generate-free-times-step-two/', generate_free_times_step_two, name='generate_free_times_step_two')

]
