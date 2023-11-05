from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Horse(models.Model):
    name = models.CharField (max_length=64)
    age = models.IntegerField()
    pedigree = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='horses')
    competitions = models.ManyToManyField('Competition', related_name='horses')

class TrainingSchedule(models.Model):
    place = models.CharField(max_length=64)
    date = models.DateField(auto_now_add=True)
    horse = models.ForeignKey(Horse, on_delete=models.CASCADE, related_name='schedule')

class Feeding(models.Model):
    ingredients = models.TextField(max_length=250)
    time_of_day = models.CharField(max_length=64)
    horse = models.ForeignKey(Horse, on_delete=models.CASCADE, related_name='horse_feeding')

class Health(models.Model):
    care = models.TextField(max_length=300)
    date = models.DateField(auto_now_add=True)
    horse = models.ForeignKey(Horse, on_delete=models.CASCADE, related_name='horse_healthy')

class Competition(models.Model):
    place = models.CharField(max_length=64)
    date = models.DateField()

class HorseCompetition(models.Model):
    horse = models.ForeignKey(Horse, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    score = models.IntegerField()






