from django.urls import path
from manager.views import show_team_registration_page, show_team_page, show_add_player_page, show_add_coach_page, show_stadium_page, show_rent_stadium_page

app_name = 'manager'

urlpatterns = [
    path('team', show_team_page, name='show_team_page'),
    path('team/add-player', show_add_player_page, name='show_add_player_page'),
    path('team/add-coach', show_add_coach_page, name='show_add_coach_page'),
    path('team/registration', show_team_registration_page, name='show_team_registration_page'),
    path('stadium', show_stadium_page, name='show_stadium_page'),
    path('stadium/rent', show_rent_stadium_page, name='show_rent_stadium_page'),
]