from django.shortcuts import redirect, render

from committee.models import *

def show_match_page(request):
    matches = get_matches()
    
    context = {
        "matches": matches
    }
    
    return render(request, 'match_page.html', context)

def show_match_list_page(request):
    matches = [
      
    ]
 
    context = {
        "matches": matches
    }
    
    return render(request, 'match_list.html', context)

def show_create_match_page(request):
    return render(request, 'create_match.html')

def show_event_page(request):
    return render(request, 'event_page.html')

def show_event_list_page(request):
    return render(request, 'create_event_page.html')

def show_meeting_list_page(request):
    matches = get_unstarted_matches()
    
    context = {
        "matches": matches
    }
    
    return render(request, 'meeting_list_page.html', context)

def show_create_meeting_page(request, pertandingan_id):
    if request.method == 'POST':
        create_meeting(request.POST['isi_rapat'], pertandingan_id, request.session['user'].get('id'))
        return redirect('/meeting')
    
    context = {
        "pertandingan_id": pertandingan_id
    }
    
    return render(request, 'create_meeting.html', context)