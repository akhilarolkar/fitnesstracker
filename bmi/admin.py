from django.contrib import admin
from bmi.models import Bmi
# Register your models here.
class BmiAdmin(admin.ModelAdmin):
    list_display=('user','height','weight','bmi','date')
admin.site.register(Bmi,BmiAdmin)