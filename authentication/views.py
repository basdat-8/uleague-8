from http.client import HTTPResponse
from django.shortcuts import render, redirect
from authentication.models import get_additional_data, get_user_by_username,get_user_role, get_user_by_role, insert_user

def show_login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = get_user_by_username(username=username)
        if user and user['password'] == password:
            [is_penonton, is_manajer, is_panitia] = get_user_role(username)
            request.session['username'] = user['username']
            request.session['role'] = 'PENONTON' if is_penonton else 'MANAJER' if is_manajer else 'PANITIA' if is_panitia else ''
            if request.session['role'] == '':
                return HTTPResponse('Invalid role')
            return redirect('/')
        else:
            return HTTPResponse('Invalid username or password.')
    
    return render(request, 'login.html')

def show_dashboard_page(request):
    if not "username" in request.session:
        return redirect('/login')
    
    username = request.session['username']
    role = request.session['role']
    
    user  = get_user_by_role(username=username, role=role)
    additional_data = get_additional_data(id=user["id"], role=role)
    
    context = {
        "user": user,
        "additional_data": additional_data
    }
    
    return render(request, 'dashboard.html', context)

def show_registration_page(request):
    if request.method == 'POST':
        username =  insert_user(request.POST)
        request.session['username'] = username
        request.session['role'] = request.POST['role']
        return redirect('/')
    
    return render(request, 'registration.html')

def logout(request):
    request.session.flush()
    return redirect('/login')
