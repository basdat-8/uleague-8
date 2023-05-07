from django.shortcuts import render

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
    return render(request, 'team_registration.html')

def show_add_trainer_page(request):
    return render(request, 'add_trainer.html')

def show_add_player_page(request):
    return render(request, 'add_player.html')

def show_team_page(request):
    players = [
      
    ]
    trainers = [
        
    ]
    
    context = {
        "players": players,
        "trainers": trainers,
    }
    
    return render(request, 'team.html', context)