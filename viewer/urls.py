from django.urls import path
from viewer.views import show_buy_ticket_page,show_buy_ticket_choose_stadium,show_buy_ticket_matches
app_name = 'viewer'

urlpatterns = [
    path('ticket', show_buy_ticket_page, name='show_buy_ticket_page'),
    path('ticket/<str:pertandingan_id>/buy',show_buy_ticket_choose_stadium, name='show_buy_ticket_choose_stadium'),
    path('buyticket/show-matches',show_buy_ticket_matches, name='show_buy_ticket_matches')
]