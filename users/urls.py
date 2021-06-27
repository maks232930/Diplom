from django.urls import path

from users.views import (
    login_view,
    user_logout,
    profile_for_admin_view,
    profile_for_master_view,
    generate_free_times_step_one,
    generate_free_times_step_two,
    generate_report_pdf_step_one,
    PDFUserDetailView
)

app_name = 'users'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile-admin/', profile_for_admin_view, name='profile_admin'),
    path('profile-master/', profile_for_master_view, name='profile_master'),
    path('generate-free-times-step-one/', generate_free_times_step_one, name='generate_free_times_step_one'),
    path('generate-free-times-step-two/', generate_free_times_step_two, name='generate_free_times_step_two'),
    path('generate-report-master-step-one/', generate_report_pdf_step_one, name='generate_report_steep_one'),
    path('report-master/', PDFUserDetailView.as_view(), name='report_master'),


]
