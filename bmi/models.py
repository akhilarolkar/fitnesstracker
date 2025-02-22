from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Bmi(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    weight = models.FloatField()
    height = models.FloatField()
    bmi = models.FloatField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.username