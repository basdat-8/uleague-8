from django.urls import path
from authentication.views import show_login_page

app_name = 'authentication'

urlpatterns = [
    path('', show_login_page, name='show_login_page'),
]