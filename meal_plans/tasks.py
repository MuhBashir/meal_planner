from datetime import datetime
from django.utils import timezone
from meal_plans.models import MealPlan



def remove_expired_meal_plans():
    current_time = timezone.now()
    expired_plans = MealPlan.objects.filter(end_date__lt=current_time)
    expired_plans.delete()
