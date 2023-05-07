from django.urls import path
from authentication.views import show_login_page, show_registration_page

app_name = 'authentication'

urlpatterns = [
    path('login', show_login_page, name='show_login_page'),
    path('registration', show_registration_page, name='show_registration_page'),
]