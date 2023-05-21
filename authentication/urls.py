from django.urls import path
from authentication.views import logout, show_login_page, show_registration_page, show_dashboard_page

app_name = 'authentication'

urlpatterns = [
    path('', show_dashboard_page, name='dashboard'),
    path('login', show_login_page, name='show_login_page'),
    path('logout', logout, name='logout'),
    path('registration', show_registration_page, name='show_registration_page'),
]