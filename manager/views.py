from django.shortcuts import redirect, render
from django.db import connection

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

def show_listmatch_page(request):
    if request.session['role'] == 'PENONTON' or request.session['role'] == 'MANAJER':
        with connection.cursor() as cursor:
            cursor.execute("set search_path to public")
            cursor.execute('''
                SELECT array_to_string(array_agg("Tim_Pertandingan"."Nama_Tim"),' VS ') as tim_bertanding, "Pertandingan"."Start_Datetime" as tanggal_dan_waktu, "Stadium"."Nama" as nama_stadium
                from "Pertandingan", "Tim_Pertandingan", "Stadium"
                WHERE "Tim_Pertandingan"."ID_Pertandingan" = "Pertandingan"."ID_Pertandingan" 
                    AND "Pertandingan"."Stadium" = "Stadium"."ID_Stadium"
                GROUP BY "Pertandingan"."Start_Datetime", "Stadium"."Nama"
                ORDER BY "Pertandingan"."Start_Datetime";
            ''')
            row = dictfetchall(cursor)
        context = {'row': row}

        return render(request, 'list_match.html', context)

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

def show_history_page(request):
    with connection.cursor() as cursor:
        cursor.execute("set search_path to public")
        cursor.execute('''
            SELECT array_to_string(array_agg("Tim_Pertandingan"."Nama_Tim"), ' VS ') AS rapat_tim, "Panitia"."Username" AS nama_panitia, "Stadium"."Nama" AS nama_stadium, "Pertandingan"."Start_Datetime" AS tanggal_dan_waktu
            FROM "Rapat", "Panitia", "Tim_Pertandingan", "Stadium", "Pertandingan"
            WHERE "Tim_Pertandingan"."ID_Pertandingan" = "Rapat"."ID_Pertandingan" 
                AND "Pertandingan"."ID_Pertandingan" = "Rapat"."ID_Pertandingan" 
                AND "Pertandingan"."Stadium" = "Stadium"."ID_Stadium"
                AND "Rapat"."Perwakilan_Panitia" = "Panitia"."ID_Panitia"
            GROUP BY "Pertandingan"."Start_Datetime", "Stadium"."Nama", "Panitia"."Username"
            ORDER BY "Pertandingan"."Start_Datetime";
        ''')
        row = dictfetchall(cursor)
    context = {'row': row}
    return render(request, 'history_rapat.html', context)

def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]