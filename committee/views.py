from django.shortcuts import render, redirect

from committee.models import *

def show_match_page(request):
    return render(request, 'match_page.html')

def show_match_list_page(request):
    matches = show_all_tim_bertanding()
 
    context = {
        "matches": matches
    }
    
    return render(request, 'match_list.html', context)

def show_create_match_page(request):
    if not "username" in request.session:
        return redirect('/login')
    if request.session["role"] != "PANITIA":
        return redirect('/')
    
    stadiums = get_all_stadium()
    referees = get_all_wasit()
    teams = get_all_team()

    if request.method == 'POST':
        create_pertandingan(request.POST)
        return redirect('/match/list')

    context = {
        "referees": referees,
        "stadiums": stadiums,
        "teams" : teams
    }
    
    return render(request, 'create_match.html', context)

def show_event_page(request):
    return render(request, 'event_page.html')

def show_event_list_page(request):
    return render(request, 'create_event_page.html')

def show_meeting_list_page(request):
    return render(request, 'meeting_list_page.html')

def show_create_meeting_page(request):
    return render(request, 'create_meeting.html')

def delete_match(request, id):
    if not "username" in request.session:
        return redirect('/login')
    if request.session["role"] != "PANITIA":
        return redirect('/')
    delete_page_by_id(id)
    return redirect('/match/list')