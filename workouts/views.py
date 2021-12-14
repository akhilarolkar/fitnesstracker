from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from workouts.models import Workout, Exercise
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def exercise(request, id):
	try:
		if request.method == "GET":
			Exercise.objects.get(id=request.GET["exercise_id"]).delete()
			data = {
			'workout': Workout.objects.get(id=id),
			'exercises': Exercise.objects.filter(workout__id=id).order_by('-updated_at'),
			}
			return render(request, 'workout/viewworkout.html', data)

		if request.method == "POST":
			exercise = {
				"user_id": request.user.id,
				"name": request.POST["name"],
				"weight": request.POST["weight"],
				"sets": request.POST["sets"],
				"repetitions": request.POST["repetitions"],
				"workout": Workout.objects.get(id=id),
			}
			Exercise.objects.create(**exercise)
			messages.info(request,'Exercise Added.')
			data = {
				'workout': Workout.objects.get(id=id),
				'exercises': Exercise.objects.filter(workout__id=id).order_by('-updated_at'),
			}
			return render(request, 'workout/viewworkout.html', data)
	except:
		return HttpResponse('ERROR! Please navigate through web app')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def workouts(request, template_name='workout/workouts.html'):#view all workouts of a user
	if request.method == 'POST':
		workout ={
			"user_id": request.user.id,
			"name": request.POST["name"],
			"description": request.POST["description"]
		}
		Workout.objects.create(**workout)
	all_workouts = Workout.objects.filter(user=request.user).order_by('-id')
	paginator = Paginator(all_workouts, 6)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	return render(request, template_name,{'page_obj':page_obj})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def view_workout(request,id,template_name='workout/viewworkout.html'):#view a specific workout
	try:
		data = {
			'workout': Workout.objects.get(id=id),
			'exercises': Exercise.objects.filter(workout__id=id).order_by('-updated_at'),
		}
		return render(request, template_name, data)
	except:
		return redirect('dashboard')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def deleteworkout(request, id):#delete a workout
	try:
		delete = Workout.objects.get(id=id)
		delete.delete()
		messages.info(request,'Workout Deleted')
		return redirect('workouts')
	except:
		return redirect('dashboard')
		
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def endworkout(request, id):
	try:
		workout = Workout.objects.get(id=id)
		workout.completed = True
		workout.save()
		return redirect('workouts')
	except:
		return redirect('/')
