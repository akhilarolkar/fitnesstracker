from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from bmi.models import Bmi
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
import datetime
from datetime import timedelta
from bmi.utils import render_to_pdf

# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def bmi(request, template_name='bmi/bmi.html'):
	bmi = None
	state = None
	context = {}
	if request.method == 'POST':
		height = float(request.POST.get("height"))
		weight = float(request.POST.get("weight"))
		bmi = (weight/(height**2))
		save = request.POST.get("save")
		if save == "on":
			Bmi.objects.create(user=request.user, weight=weight, height=height, bmi=round(bmi))
		if bmi < 16:
			state = "severe thinness"
		elif bmi > 16 and bmi < 17:
			state = "moderate thinness"
		elif bmi > 17 and bmi < 18:
			state = "mild thinness"
		elif bmi > 18 and bmi < 25:
			state = "normal"
		elif bmi > 25 and bmi < 30:
			state = "overweight"
		elif bmi > 30 and bmi < 35:
			state = "obese class I"
		elif bmi > 35 and bmi < 40:
			state = "obese class II"
		elif bmi > 40:
			state = "obese class III"
		context["bmi"] = round(bmi)
		context["state"] = state
	if request.user.is_authenticated:
		labels =[]
		data =[]
		queryset = Bmi.objects.all().filter(user = request.user)[:10]
		for qr in queryset:
			labels.append(str(qr.date))
			data.append(str(qr.bmi))
		context["labels"] = labels
		context["data"] = data

		labels1 =[]
		data1 =[]
		queryset1 = Bmi.objects.all().filter(user = request.user)
		for qr in queryset1:
			labels1.append(str(qr.date))
			data1.append(str(qr.weight))
		context["labels1"] = labels1
		context["data1"] = data1
	return render(request, template_name,context)


def generate_pdf(request):
	template_name = "bmi/report-pdf.html"
	date = datetime.date.today()
	if request.method=='POST':
		datefrom=request.POST['datefrom']
		dateto=request.POST['dateto']
		reports = Bmi.objects.filter(user=request.user, date__lte=dateto, date__gte=datefrom).order_by('-date')
	return render_to_pdf(
		template_name,
		{
			"report":reports,
			"date":date,
			"datefrom":datefrom,
			"dateto":dateto,
		}
	)
	# buff = io.BytesIO()
	# p = canvas.Canvas(buff, pagesize=A4, bottomup=0)
	# p.drawString(260,30,"BMI REPORT")
	# p.line(0,48,1000,48)
	# p.line(0,46,1000,46)

	# textob = p.beginText()
	# textob.setTextOrigin(inch, inch)
	# textob.setFont("Helvetica",14)
	# # lines = [
	# # 	"line number 1",
	# # 	"line number 2",
	# # 	"line number 3",
	# # 	"line number 4",
	# # ]
	# queryset = Bmi.objects.all().filter(user = request.user)
	# lines = []
	# for qr in queryset:
	# 	lines.append(f'Your BMI Recorded on Date:{qr.date} is {qr.bmi}')
	# for line in lines:
	# 	textob.textLine(line)
	# p.drawText(textob)
	# p.setTitle(f'bmi report')
	# p.showPage()
	# p.save()
	# buff.seek(0)
	# return FileResponse(buff, filename='Report.pdf')