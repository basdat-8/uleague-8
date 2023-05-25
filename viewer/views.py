from django.shortcuts import redirect, render

from viewer.models import *

# Create your views here.

def show_buy_ticket_page(request):
    matches = get_matches()
    
    context = {
        'matches': matches
    }
    
    return render(request, 'matches.html', context)

def show_buy_ticket_choose_stadium(request, pertandingan_id):
    if request.method == 'POST':
        buy_ticket(request.POST, pertandingan_id, request.session['user'].get('id'))
        return redirect('/ticket')
    
    context = {
        'pertandingan_id': pertandingan_id
    }
    
    return render(request, 'buy_ticket.html', context)