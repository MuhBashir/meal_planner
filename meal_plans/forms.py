from django import forms
from .models import MealPlan, Meal, Recipe

class MealPlanForm(forms.ModelForm):
    
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))



    class Meta:
        model = MealPlan
        fields = ['name', 'start_date', 'end_date']

class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ['meal_name', 'meal_time']




class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['meal', 'ingredients', 'instructions']

