from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
# Create your views here.

#view for homepage
def home(request, template_name='accounts/home.html'):
	if request.user.is_authenticated: #check if user is already loggedin from browser
		return redirect("workouts")
	return render(request, template_name)

# view for registering new users
def signup(request, template_name='accounts/signup.html'):
	if request.user.is_authenticated: #check if user is already loggedin from browser
		return redirect("workouts")
	if request.method == 'POST':
		username = request.POST['username']
		email = request.POST['email']
		password1 = request.POST['password1']
		password2 = request.POST['password2']

		if User.objects.filter(username=username).exists(): #check if username is taken or not
			messages.info(request,f'Username {username} already exists')
			return redirect('signup')

		if password1 != password2: # check if 2 passwords matches or not
			messages.error(request,'Passwords do not match. Please try again.')
			return redirect('signup')
			
		user = User.objects.create_user(username,email,password1)
		user.save() # create and save user into database
		messages.info(request,f'Successfully SignedUp as {username}.Login into your account now!')
		return redirect('login') # after creating new user redirects to login page
	
	return render(request, template_name)

# view for logging in registered users
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def userlogin(request, template_name='accounts/login.html'):#check if user is already loggedin from browser
	if request.user.is_authenticated:
		return redirect("workouts")
	loginusername = request.POST.get('loginusername')
	if request.method == 'POST':
		loginusername = request.POST['loginusername']
		loginpassword = request.POST['loginpassword']
		user = authenticate(username = loginusername, password  = loginpassword)
		if user is not None:
			login(request, user) # authenticate user and login
			messages.info(request,f'Successfully logged in as {loginusername}.')
			return redirect('workouts')# if user is logged in redirect to user dashboard
		else:
			messages.info(request,'Invalid credentials') # check if credentials entered are correct
			return redirect("login")

	return render(request, template_name)

# view for logging out users
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def userlogout(request):
	logout(request) # logs out the user
	messages.info(request,'Successfully logged out')
	return redirect('login')

 # view for password change
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def change_password(request, template_name='accounts/change_password.html'):
	if request.method == 'POST':
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)
			messages.info(request,'password updated successfully')
			return redirect('workouts')
		else:
			messages.error(request,'correct error')
	else:
		form = PasswordChangeForm(request.user)
	return render(request,template_name,{'form':form})