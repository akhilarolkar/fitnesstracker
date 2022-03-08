from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_text  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from accounts.tokens import account_activation_token   
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
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
		user.is_active = False
		user.save() # create and save user into database
		current_site = get_current_site(request)  
		mail_subject = 'Activation link has been sent to your email id'  
		message = render_to_string('accounts/acc_active_email.html', {  
			'user': user,  
			'domain': current_site.domain,  
			'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
			'token':account_activation_token.make_token(user),  
		})
		to_email = email  
		email = EmailMessage(
			mail_subject, message, to=[to_email]  
		)  
		email.send()
		messages.info(request,f'Please confirm your email address to complete the registration') 
		return redirect('login') # after creating new user redirects to login page
	
	return render(request, template_name)

#view for activating user account
def activate(request, uidb64, token):  
	User = get_user_model() 
	try:  
		uid = force_text(urlsafe_base64_decode(uidb64))  
		user = User.objects.get(pk=uid)  
	except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
		user = None  
	if user is not None and account_activation_token.check_token(user, token):  
		user.is_active = True  
		user.save()
		messages.info(request,f'Thankyou for confirming your email, You can login to your account now!')
		return redirect('login')  
	else:  
		return HttpResponse('Activation link is invalid!')  


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