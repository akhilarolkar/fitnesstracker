from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from . models import Meal, Profile
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.models import User
from django.db.models import Sum
import datetime
from datetime import timedelta
from django.contrib import messages
from diet.utils import render_to_pdf

def base(request):
	context = {
		"user": request.user,
	}
	return render(request, "diet/base.html", context)

def index(request):
	daily =None
	# weekly =None
	profile = Profile.objects.get(user=request.user)
	date_now = datetime.date.today()
	meals = Meal.objects.filter(userfk=request.user, date=date_now).order_by('-date')
	seven_days_meals = Meal.objects.filter(userfk=request.user, date__gte=datetime.date.today()-timedelta(days=7)).order_by('-date')
	seven_days_kcal = Meal.objects.filter(userfk=request.user, date__gte=datetime.date.today()-timedelta(days=7)).aggregate(
		Sum('kcal'))['kcal__sum'] or 0.00
	seven_days_carbs = Meal.objects.filter(userfk=request.user, date__gte=datetime.date.today()-timedelta(days=7)).aggregate(
		Sum('carbs'))['carbs__sum'] or 0.00
	seven_days_protein = Meal.objects.filter(userfk=request.user, date__gte=datetime.date.today()-timedelta(days=7)).aggregate(
		Sum('protein'))['protein__sum'] or 0.00
	seven_days_fats = Meal.objects.filter(userfk=request.user, date__gte=datetime.date.today()-timedelta(days=7)).aggregate(
		Sum('fats'))['fats__sum'] or 0.00

	kcal = Meal.objects.filter(date=date_now, userfk=request.user).aggregate(
		Sum('kcal'))['kcal__sum'] or 0.00
	carbs_total = Meal.objects.filter(date=date_now, userfk=request.user).aggregate(
		Sum('carbs'))['carbs__sum'] or 0.00 
	protein_total = Meal.objects.filter(date=date_now, userfk=request.user).aggregate(
		Sum('protein'))['protein__sum'] or 0.00
	fats_total = Meal.objects.filter(date=date_now, userfk=request.user).aggregate(
		Sum('fats'))['fats__sum'] or 0.00
	
	
	labels =[]
	data =[]
	labels1 =[]
	data1 =[]
	labels2 =[]
	data2 =[]

	data3 =[]
	data4 =[]
	data5 =[]

	labels.append('Protein (gm)')
	labels1.append('Carbohydrates (gm)')
	labels2.append('Fats (gm)')
	data.append(str(protein_total))
	data1.append(str(carbs_total))
	data2.append(str(fats_total))

	data3.append(str(seven_days_protein))
	data4.append(str(seven_days_carbs))
	data5.append(str(seven_days_fats))

	goal_cals = profile.goal_cals
	if kcal is not None:
		kcal_total = int(kcal)
		kcal_left = goal_cals - kcal_total
	else:
		kcal_total = 0
		kcal_left = goal_cals
	
	progress = (int(kcal) / int(goal_cals)) * 100
	if request.method == 'POST':
		gender = request.POST.get("gender")
		age = request.POST.get("age")
		kgs = request.POST.get("kgs")
		cms = request.POST.get("cms")
		activity = request.POST.get("activity")
		if gender == '0':
			bmr = 88.362 + (13.397 * int(kgs)) + (4.799 * int(cms)) - (5.677 * int(age))
		elif gender == '1':
			bmr = 447.539 + (9.247 * int(kgs)) + (3.098 * int(cms)) - (4.330 * int(age))
		daily = bmr * float(activity)
		print(bmr)
		print(daily)
		messages.success(request,f'You need {daily} calories daily to maintain your body weight')
		# weekly = daily * 7
	context = {
		"user": request.user,
		"date": datetime.date.today(),
		"kcal_total": int(kcal_total),
		"kcal_left": int(kcal_left),
		"kcal_goal": int(goal_cals),
		"progress": int(progress),
		'daily': daily,
		'meals': meals,
		'seven_days_meals' : seven_days_meals,
		"labels" : labels,
		"data" : data,
		"labels1" : labels1,
		"data1" : data1,
		"labels2" : labels2,
		"data2" : data2,
		'data3' : data3,
		'data4' : data4,
		'data5' : data5,
		# 'weekly': weekly,
	}
	return render(request, "diet/diet.html", context)


def create_meal(request):
	if request.method == 'POST' and 'add' in request.POST:
		try:
			meal = Meal.objects.create(
				userfk=request.user,
				name=request.POST["name"],
				kcal=request.POST["kcal"],
				carbs=request.POST["carbs"],
				protein=request.POST["protein"],
				fats=request.POST["fats"],
				date=datetime.date.today())
			meal.save()
			return redirect('diet')
		except:
			return redirect('diet')
	return render(request, "diet/diet.html")


def goal_change(request):
	if request.method == 'POST':
		goal = int(request.POST.get("goal", 2000))
		Profile.objects.filter(user=request.user).update(goal_cals=goal)
		return redirect('diet')
	return render(request, "diet/diet.html", context)

def generate_pdf(request):
	template_name = "diet/report-pdf.html"
	profile = Profile.objects.get(user=request.user)
	goal_cals = profile.goal_cals
	date = datetime.date.today()
	#Report for the day
	reports = Meal.objects.filter(userfk=request.user, date=datetime.date.today()).order_by('-date')
	kcal = Meal.objects.filter(date=datetime.date.today(), userfk=request.user).aggregate(
		Sum('kcal'))['kcal__sum'] or 0.00
	carbs = Meal.objects.filter(userfk=request.user, date=datetime.date.today()).aggregate(
		Sum('carbs'))['carbs__sum'] or 0.00
	protein = Meal.objects.filter(userfk=request.user, date=datetime.date.today()).aggregate(
		Sum('protein'))['protein__sum'] or 0.00
	fats = Meal.objects.filter(userfk=request.user, date=datetime.date.today()).aggregate(
		Sum('fats'))['fats__sum'] or 0.00
	#Report for Last 7 days
	sevendaysreport = Meal.objects.filter(userfk=request.user, date__gte=datetime.date.today()-timedelta(days=7)).order_by('-date')
	sevendayskcal = Meal.objects.filter(userfk=request.user, date__gte=datetime.date.today()-timedelta(days=7)).aggregate(
		Sum('kcal'))['kcal__sum'] or 0.00
	sevendayscarbs = Meal.objects.filter(userfk=request.user, date__gte=datetime.date.today()-timedelta(days=7)).aggregate(
		Sum('carbs'))['carbs__sum'] or 0.00
	sevendaysprotein = Meal.objects.filter(userfk=request.user, date__gte=datetime.date.today()-timedelta(days=7)).aggregate(
		Sum('protein'))['protein__sum'] or 0.00
	sevendaysfats = Meal.objects.filter(userfk=request.user, date__gte=datetime.date.today()-timedelta(days=7)).aggregate(
		Sum('fats'))['fats__sum'] or 0.00

	return render_to_pdf(
		template_name,
		{
			"profile":profile,
			"date":date,
			"goal_cals":goal_cals,

			"report":reports,
			"kcal":kcal,
			"carbs":carbs,
			"protein":protein,
			"fats":fats,
			
			"sevendaysreport":sevendaysreport,
			"sevendayskcal":sevendayskcal,
			"sevendayscarbs":sevendayscarbs,
			"sevendaysprotein":sevendaysprotein,
			"sevendaysfats":sevendaysfats,
		}
	)
def generate_thirty_days_pdf(request):
	template_name = "diet/thirtydaysreport.html"
	profile = Profile.objects.get(user=request.user)
	date = datetime.date.today()

	thirtydaysreport = Meal.objects.filter(userfk=request.user, date__gte=datetime.date.today()-timedelta(days=30)).order_by('-date')
	thirtydayskcal = Meal.objects.filter(userfk=request.user, date__gte=datetime.date.today()-timedelta(days=30)).aggregate(
		Sum('kcal'))['kcal__sum'] or 0.00
	thirtydayscarbs = Meal.objects.filter(userfk=request.user, date__gte=datetime.date.today()-timedelta(days=30)).aggregate(
		Sum('carbs'))['carbs__sum'] or 0.00
	thirtydaysprotein = Meal.objects.filter(userfk=request.user, date__gte=datetime.date.today()-timedelta(days=30)).aggregate(
		Sum('protein'))['protein__sum'] or 0.00
	thirtydaysfats = Meal.objects.filter(userfk=request.user, date__gte=datetime.date.today()-timedelta(days=30)).aggregate(
		Sum('fats'))['fats__sum'] or 0.00

	return render_to_pdf(
		template_name,
		{
			"profile":profile,
			"date":date,
			"thirtydaysreport":thirtydaysreport,
			"thirtydayskcal":thirtydayskcal,
			"thirtydayscarbs":thirtydayscarbs,
			"thirtydaysprotein":thirtydaysprotein,
			"thirtydaysfats":thirtydaysfats,
		}
	)
