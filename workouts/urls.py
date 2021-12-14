from django.contrib import admin
from django.urls import path
from workouts import views
urlpatterns = [
    path('workouts',views.workouts, name="workouts"),
  
    path('delete/<int:id>',views.deleteworkout, name="deleteworkout"),
    path('end/<int:id>',views.endworkout, name="endworkout"),
    path('workout/<int:id>',views.view_workout, name="workout"),
    path('workout/<int:id>/exercise', views.exercise, name="exercise"),

 
]