from django.shortcuts import render

def show_login_page(request):
    return render(request, 'login.html')

def show_registration_page(request):
    return render(request, 'registration.html')