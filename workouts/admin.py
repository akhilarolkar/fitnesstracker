from django.contrib import admin
from workouts.models import Workout, Exercise
# Register your models here.

class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('user','name','created_at','updated_at')
    search_fields = ('user',)
admin.site.register(Workout, WorkoutAdmin)

class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('user','workout','name','created_at','updated_at')
    search_fields = ('user',)
admin.site.register(Exercise, ExerciseAdmin)

 