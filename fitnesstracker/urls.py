"""fitnesstracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from accounts import urls as a_urls
from workouts import urls as w_urls
from diet import urls as d_urls
from bmi import urls as b_urls
urlpatterns = [
    path('adminpanel/', admin.site.urls),
    path('', include(a_urls), name='a_urls'),
    path('', include(w_urls), name='w_urls'),
    path('', include(b_urls), name='b_urls'),
    path('', include(d_urls), name='d_urls'),
]
