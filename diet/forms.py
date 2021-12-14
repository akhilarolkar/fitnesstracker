from django import forms
from django.forms import ModelForm 
from django.contrib.auth.models import User
from diet.models import *

class AddFoodForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = ('foodname','amount','carbohydrates','protiens','fats')

class SelectFoodForm(forms.ModelForm):
    class Meta:
        model = DietDetail
        fields = ('fooditem_selected','quantity')

    def __init__(self,user,*args,**kwargs):
        super(SelectFoodForm,self).__init__(*args,**kwargs)
        self.fields['fooditem_selected'].queryset = FoodItem.objects.filter(user=user)