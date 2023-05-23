from django.urls import path
from . import views

urlpatterns = [
    path('history', views.list_rapat, name='list_rapat'),
    path('laporan/<int:rapat_id>/', views.lihat_laporan, name='lihat_laporan'),
]