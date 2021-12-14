from django.contrib import admin
from django.urls import path
from bmi import views
urlpatterns = [
    path('bmi',views.bmi, name='bmi'),
    path('generate-pdf', views.generate_pdf, name='generate-pdf'), 
]