from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from accounts import views
urlpatterns = [
    path('', views.home,name='home'),
    path('signup/', views.signup,name='signup'),
    path('login/', views.userlogin,name='login'),
    path('logout/', views.userlogout,name='logout'),
    path('change_password', views.change_password, name='change_password'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'),name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_sent.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_form.html'),name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_done.html'),name='password_reset_complete'),

]