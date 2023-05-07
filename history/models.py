from django.db import models

class Rapat(models.Model):
    nama_tim = models.CharField(max_length=100)
    panitia = models.CharField(max_length=100)
    stadion = models.CharField(max_length=100)
    tanggal_waktu = models.DateTimeField()
    laporan = models.TextField(blank=True)

    def __str__(self):
        return self.nama_tim