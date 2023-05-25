from django.shortcuts import redirect, render

from manager.models import *

def show_stadium_page(request):
    stadiums = get_rented_stadium(request.session['user'].get('id'))
 
    context = {
        "stadiums": stadiums
    }
    
    return render(request, 'stadium.html', context)

def show_rent_stadium_page(request):
    if request.method == "POST":
        rent_stadium(request.POST, request.session['user'].get('id'))
        return redirect('/stadium')
    
    stadiums = get_stadiums()
 
    context = {
        "stadiums": stadiums
    }
    
    return render(request, 'rent_stadium.html', context)

def show_team_registration_page(request):
    if not "username" in request.session:
        return redirect('/login')
    if request.session["role"] != "MANAJER":
        return redirect('/') 

    if request.method == 'POST':
        create_manager_team(request.POST, request.session['user'].get('id'))
        return redirect('/team')
    
    return render(request, 'team_registration.html')

def show_add_coach_page(request):
    if not "username" in request.session:
        return redirect('/login')
    if request.session["role"] != "MANAJER":
        return redirect('/')    
    
    if request.method == 'POST':
        team = get_manager_team(request.session['user'].get('id'))
        add_coach(request.POST['pelatih_id'], team['nama'])
        return redirect('/team')
    
    coaches = get_coaches()
    
    context = {
        "coaches": coaches
    }
    
    return render(request, 'add_coach.html',context)

def show_add_player_page(request):
    if not "username" in request.session:
        return redirect('/login')
    if request.session["role"] != "MANAJER":
        return redirect('/')
    
    if request.method == 'POST':
        team = get_manager_team(request.session['user'].get('id'))
        add_player(request.POST['pemain_id'], team['nama'])
        return redirect('/team')
    
    players = get_players()
    
    context = {
        "players": players
    }
    
    return render(request, 'add_player.html', context)

def show_team_page(request):
    if not "username" in request.session:
        return redirect('/login')
    if request.session["role"] != "MANAJER":
        return redirect('/')
    
    if request.method == "POST":
        if request.POST['_method'] == 'DELETE':
            if request.POST['type'] == "COACH":
                remove_coach(request.POST['id'])
            else: 
                remove_player(request.POST['id'])
        if request.POST['_method'] == 'PATCH':
            if request.POST['type'] == "PLAYER":
                promote_player(request.POST['id'])
                
    team = get_manager_team(request.session['user'].get('id'))
    
    if len(team) == 0:
       return redirect('/team/registration')
    
    coaches = get_coaches_by_team(team['nama'])
    
    players = get_players_by_team(team['nama'])
    
    context = {
        "players": players,
        "coaches": coaches,
    }
    
    return render(request, 'team.html', context)