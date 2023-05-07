from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    STATUS_CHOICES = [
        ('manager', 'Manager'),
        ('viewer', 'Viewer'),
        ('committee', 'Committee')
    ]
    POSITION_CHOICES = [
        ('', '---'),
        ('head', 'Head'),
        ('coordinator', 'Coordinator'),
        ('staff', 'Staff')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(max_length=254)
    address = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    position = models.CharField(max_length=20, choices=POSITION_CHOICES, blank=True)

class Team(models.Model):
    name = models.CharField(max_length=100)
    manager = models.ForeignKey(User, on_delete=models.CASCADE)

class Match(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    date = models.DateField()
    opponent = models.CharField(max_length=100)

class Meeting(models.Model):
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    description = models.TextField()