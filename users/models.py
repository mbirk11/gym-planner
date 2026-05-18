from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    height = models.FloatField(null=True, blank=True, help_text="სიმაღლე სმ-ში")
    weight = models.FloatField(null=True, blank=True, help_text="წონა კგ-ში")
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.username


class Exercise(models.Model):
    """სავარჯიშოს ბაზა (მაგ: აზიდვა, ჩაჯდომა)"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Workout(models.Model):
    """მომხმარებლის კონკრეტული დღის ვარჯიში"""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='workouts')
    date = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.date}"

class Set(models.Model):
    """მისვლა (წონა და გამეორება)"""
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name='sets')
    exercise = models.ForeignKey(Exercise, on_delete=models.PROTECT)
    weight = models.FloatField()
    reps = models.IntegerField()

    def __str__(self):
        return f"{self.exercise.name}: {self.weight}kg x {self.reps}"