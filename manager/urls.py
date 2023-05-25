from django.urls import path
from manager.views import show_history_page, show_listmatch_page, show_team_registration_page, show_team_page, show_add_player_page, show_add_coach_page, show_stadium_page, show_rent_stadium_page, show_laporan_page 

app_name = 'manager'

urlpatterns = [
    path('team', show_team_page, name='show_team_page'),
    path('team/add-player', show_add_player_page, name='show_add_player_page'),
    path('team/add-coach', show_add_coach_page, name='show_add_coach_page'),
    path('team/registration', show_team_registration_page, name='show_team_registration_page'),
    path('stadium', show_stadium_page, name='show_stadium_page'),
    path('stadium/rent', show_rent_stadium_page, name='show_rent_stadium_page'),
    path('listmatch', show_listmatch_page, name='show_listmatch_page'),
    path('history', show_history_page, name='show_history_page'),
    path('history/laporan/<str:id>', show_laporan_page, name='show_laporan_page')
]