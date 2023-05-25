from django.shortcuts import render

# Create your views here.

def show_buy_ticket_page(request):
    return render(request, 'buy_ticket.html')

def show_buy_ticket_choose_stadium(request):
    return render(request, 'choose_stadium.html')

def show_buy_ticket_matches(request):
    return render(request, 'matches.html')