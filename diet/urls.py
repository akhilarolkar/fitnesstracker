from django.contrib import admin
from django.urls import path
from diet import views
urlpatterns = [
   path('diet/', views.index, name="diet"),
   path("goal_change", views.goal_change, name="goal_change"),
   path("create_meal", views.create_meal, name="create_meal"),
   path('generate-diet-pdf', views.generate_pdf, name='generate-diet-pdf'),
   path('generate-thirty-days-pdf', views.generate_thirty_days_pdf, name='generate-thirty-days-pdf'),
   # path("cal_calc", views.cal_calc, name="cal_calc")
   # path('addfood/', views.FoodInventory, name="addfood"),
   # path('diet/<int:id>/delete', views.DeleteFood, name="deletefooditem"),
]