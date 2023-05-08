from django.urls import path
from committee.views import show_match_list_page, show_create_match_page, show_event_list_page, show_event_page, show_match_page, show_meeting_list_page, show_create_meeting_page

app_name = 'committee'

urlpatterns = [
    path('match', show_match_page, name='show_match_page'),
    path('match/list', show_match_list_page, name='show_match_list_page'),
    path('match/create', show_create_match_page, name='show_create_match_page'),
    path('match/event', show_event_page, name='show_event_page'),
    path('match/event/list', show_event_list_page, name='show_event_list_page'),
    path('meeting', show_meeting_list_page, name='show_meeting_list_page'),
    path('meeting/create', show_create_meeting_page, name='show_create_meeting_page'),
]