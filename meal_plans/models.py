from django.db import models
from django.contrib.auth.models import User

class MealPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()


    def __str__(self):
        return self.name
    

class Meal(models.Model):
    MEAL_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
    ]
    
    meal_plan = models.ForeignKey(MealPlan, on_delete=models.CASCADE)
    meal_name = models.CharField(max_length=200)
    meal_time = models.CharField(max_length=20, choices=MEAL_CHOICES)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'meals'

    
    def __str__(self):
        return self.meal_name




class Recipe(models.Model):
    meal = models.OneToOneField(Meal, on_delete=models.CASCADE, related_name='recipe')
    ingredients = models.TextField()
    instructions = models.TextField()
    # Add other fields as per your requirements

    def __str__(self):
        return f"Recipe for {self.meal.meal_name}"