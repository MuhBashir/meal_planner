from django.contrib import admin
from .models import MealPlan, Meal, Recipe

admin.site.register(MealPlan)
admin.site.register(Meal)
admin.site.register(Recipe)
