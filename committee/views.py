from django.shortcuts import render

def show_match_page(request):
    return render(request, 'match_page.html')

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
    return render(request, 'meeting_list_page.html')

def show_create_meeting_page(request):
    return render(request, 'create_meeting.html')