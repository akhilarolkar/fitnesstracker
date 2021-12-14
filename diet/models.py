from django.db import models
from datetime import datetime  
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Meal(models.Model):
    userfk = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=15)
    kcal = models.FloatField()
    carbs = models.FloatField()
    protein = models.FloatField()
    fats = models.FloatField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
       return f"User {self.userfk}: meal {self.name} with {self.kcal} kcal, on {self.date}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    goal_cals = models.FloatField(blank=True, null=True,  default='2000')
    date = models.DateField(auto_now_add=True)

    @receiver(post_save, sender=User)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
    @receiver(post_save, sender=User)
    def save_profile(sender,instance,**kwargs):
        instance.profile.save()

    def __str__(self):
        return f"{self.user}'s profile"
        
