import datetime
from django.shortcuts import render
#from django.contrib.auth.decorators import login_required
from .models import Profile, Team, Match, Meeting


def dashboard(request):
    # user = request.user
    # try:
    #     profile = Profile.objects.get(user=user)
    # except Profile.DoesNotExist:
    #     profile = None
    # if profile:
    #     if profile.status == 'manager':
    #         try:
    #             team = Team.objects.get(manager=user)
    #             matches = Match.objects.filter(team=team, date__gte=datetime.date.today())
    #         except Team.DoesNotExist:
    #             team = None
    #             matches = None
    #         context = {
    #             'first_name': profile.first_name,
    #             'last_name': profile.last_name,
    #             'phone_number': profile.phone_number,
    #             'email': profile.email,
    #             'address': profile.address,
    #             'status': profile.status,
    #             'position': profile.position,
    #             'team': team,
    #             'matches': matches,
    #         }
    #         return render(request, 'manager_dashboard.html', context)
    #     elif profile.status == 'viewer':
    #         matches = Match.objects.filter(date__gte=datetime.date.today())
    #         context = {
    #             'first_name': profile.first_name,
    #             'last_name': profile.last_name,
    #             'phone_number': profile.phone_number,
    #             'email': profile.email,
    #             'address': profile.address,
    #             'status': profile.status,
    #             'matches': matches,
    #         }
    #         return render(request, 'viewer_dashboard.html', context)
    #     elif profile.status == 'committee':
    #         meetings = Meeting.objects.filter(date__gte=datetime.date.today())
    #         context = {
    #             'first_name': profile.first_name,
    #             'last_name': profile.last_name,
    #             'phone_number': profile.phone_number,
    #             'email': profile.email,
    #             'address': profile.address,
    #             'status': profile.status,
    #             'meetings': meetings,
    #         }
    #         return render(request, 'committee_dashboard.html', context)
    # else:
        return render(request, 'manager_dashboard.html')