from django.shortcuts import redirect, render

from manager.models import add_coach, create_manager_team, get_manager_team, get_coaches, get_coaches_by_team, remove_coach

def show_stadium_page(request):
    stadiums = [
      
    ]
 
    context = {
        "stadiums": stadiums
    }
    
    return render(request, 'stadium.html', context)

def show_rent_stadium_page(request):
    stadium_schedules = [
      
    ]
 
    context = {
        "stadium_schedules": stadium_schedules
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
    return render(request, 'add_player.html')

def show_team_page(request):
    if not "username" in request.session:
        return redirect('/login')
    if request.session["role"] != "MANAJER":
        return redirect('/')
    
    if request.method == "POST":
        if request.POST['_method'] == 'DELETE':
            type = request.POST['type']
            if type == "COACH":
                remove_coach(request.POST['id'])
     
    team = get_manager_team(request.session['user'].get('id'))
    
    if len(team) == 0:
       return redirect('/team/registration')
    
    coaches = get_coaches_by_team(team['nama'])
    
    players = [
        
    ]
    
    context = {
        "players": players,
        "coaches": coaches,
    }
    
    return render(request, 'team.html', context)