from django.urls import path
from viewer.views import show_buy_ticket_page,show_buy_ticket_choose_stadium,show_buy_ticket_matches
app_name = 'viewer'

urlpatterns = [
    path('buyticket/buy', show_buy_ticket_page, name='show_buy_ticket_page'),
    path('buyticket',show_buy_ticket_choose_stadium, name='show_buy_ticket_choose_stadium'),
    path('buyticket/show-matches',show_buy_ticket_matches, name='show_buy_ticket_matches')
]