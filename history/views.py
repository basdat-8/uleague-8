from django.shortcuts import render, HttpResponse
from .models import Rapat

def list_rapat(request):
    # list_rapat = Rapat.objects.all()
    # context = {
    #     'list_rapat': list_rapat
    # }
    return render(request, 'list_rapat.html')

def lihat_laporan(request, rapat_id):
    rapat = Rapat.objects.get(id=rapat_id)
    return HttpResponse(rapat.laporan)