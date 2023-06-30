from django.shortcuts import render, redirect, get_object_or_404
from .models import MealPlan, Meal,Recipe
from .forms import MealPlanForm, MealForm, RecipeForm
from django.contrib.auth.decorators import login_required
from py_edamam import PyEdamam
from py_edamam import exceptions
from py_edamam import Recipe
import requests



def index(request):
    return render(request, "meal_plans/index.html")

@login_required
def meal_plan_list(request):
    meal_plans = MealPlan.objects.filter(user=request.user)
    context = {'meal_plans': meal_plans}
    return render(request, 'meal_plans/meal_plan_list.html', context)


@login_required
def meal_plan_detail(request, pk):
    meal_plan = MealPlan.objects.get(pk=pk, user=request.user)
    context = {'meal_plan': meal_plan}
    return render(request, 'meal_plans/meal_plan_detail.html', context)



@login_required
def meal_plan_create(request):
    if request.method == 'POST':
        form = MealPlanForm(request.POST)
        if form.is_valid():
            meal_plan = form.save(commit=False)
            meal_plan.user = request.user
            meal_plan.save()
            return redirect('meal_plans:meal_plan_list')
    else:
        form = MealPlanForm()
    context = {'form': form}
    return render(request, 'meal_plans/meal_plan_create.html', context)


@login_required
def meal_plan_update(request, pk):
    meal_plan = MealPlan.objects.get(pk=pk, user=request.user)
    if request.method == 'POST':
        form = MealPlanForm(request.POST, instance=meal_plan)
        if form.is_valid():
            form.save()
            return redirect('meal_plans:meal_plan_list')
    else:
        form = MealPlanForm(instance=meal_plan)
    context = {'form': form, 'meal_plan': meal_plan}
    return render(request, 'meal_plans/meal_plan_update.html', context)



@login_required
def meal_plan_delete(request, pk):
    meal_plan = MealPlan.objects.get(pk=pk, user=request.user)
    if request.method == 'POST':
        meal_plan.delete()
        return redirect('meal_plans:meal_plan_list')
    context = {'meal_plan': meal_plan}
    return render(request, 'meal_plans/meal_plan_delete.html', context)



# add meals
@login_required
def add_meal(request, meal_plan_id):
    meal_plan = MealPlan.objects.get(id=meal_plan_id)
    
    if request.method == 'POST':
        form = MealForm(data=request.POST)
        if form.is_valid():
            meal = form.save(commit=False)
            meal.meal_plan = meal_plan
            meal.save()
            return redirect('meal_plans:meal_plan_detail', pk=meal_plan.pk)
    else:
        form = MealForm()
    
    context = {
        'meal_plan': meal_plan,
        'form': form,
    }
    
    return render(request, 'meal_plans/add_meal.html', context)



@login_required
def meal_list_view(request):
    meals = Meal.objects.all()
    context = {'meals': meals}
    return render(request, 'meal_plans/meal_list.html', context)


@login_required
def meal_delete(request, meal_id):
    meal = get_object_or_404(Meal, id=meal_id)

    if request.method == 'POST':
        meal.delete()
        return redirect('meal_plans:meal_list')

    context = {'meal': meal}
    return render(request, 'meal_plans/meal_delete.html', context)



@login_required
def meal_update(request, meal_id):
    meal = get_object_or_404(Meal, id=meal_id)

    if request.method == 'POST':
        form = MealForm(request.POST, instance=meal)
        if form.is_valid():
            form.save()
            return redirect('meal_plans:meal_list')
    else:
        form = MealForm(instance=meal)

    context = {'form': form, 'meal': meal}
    return render(request, 'meal_plans/meal_update.html', context)



@login_required
def recipe_create(request, meal_id):
    meal = get_object_or_404(Meal, id=meal_id)
    
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.meal = meal
            recipe.save()
            return redirect('meal_plans:meal_list')
    else:
        form = RecipeForm()
    
    context = {
        'form': form,
        'meal': meal
    }
    return render(request, 'meal_plans/recipe_create.html', context)




@login_required
def recipe_update(request, meal_id):
    meal = get_object_or_404(Meal, id=meal_id)
    recipe = meal.recipe
    
    if request.method == 'POST':
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('meal_plans:meal_list', meal_id=meal.id)
    else:
        form = RecipeForm(instance=recipe)
    
    context = {
        'form': form,
        'meal': meal
    }
    return render(request, 'meal_plans/recipe_update.html', context)



@login_required
def recipe_delete(request, meal_id):
    meal = get_object_or_404(Meal, id=meal_id)
    recipe = meal.recipe
    
    if request.method == 'POST':
        recipe.delete()
        return redirect('meal_plans:meal_list', meal_id=meal.id)
    
    context = {
        'meal': meal,
        'recipe': recipe
    }
    return render(request, 'meal_plans/recipe_delete.html', context)


@login_required
def recipe_detail(request, meal_id):
    recipe = get_object_or_404(Recipe, id=meal_id)
    
    context = {
        'recipe': recipe
    }
    
    return render(request, 'meal_plans/recipe_detail.html', context)



# search functionality for the recipe

# def search_recipe(query):
#     """search for some recipe"""

#     try:
#         # Make the search query using the `search_food method
#         api = PyEdamam(food_appid="60424334", food_appkey="f3ee584ad09758ccd002a15d5f6cb391")

#         # Make the search query using the `search_food` method
#         results = api.search_food(query)

#         return results
#     except exceptions as e:
#          # Handle any exceptions that may occur during the API call

#         print(f"An error occurred: {str(e)}")
#         return []



def search_recipe(request):
    app_id = 'd9011687'
    app_key = "bd6fc5344fac17ee891c216612444a4c"
    url = f"https://api.edamam.com/api/recipes/v2?type=public&q={request}&app_id={app_id}&app_key={app_key}"
    

    response = requests.get(url)
    data = response.json()
    # Parse the response and extract the search results
    results = data.get('hits', [])
        
    # result = [result for result in results if result == "recipe"]
    # print(result)
    # Pass the results to the template
    # return render(request, 'meal_plans/search.html', {'results': results})
    return results






def search_view(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        if query:
            # Call the search_recipe function with the query parameter
            results = search_recipe(query)
            for result in results:
                if result["recipe"].get("label") == query:
                    return render(request, 'meal_plans/search.html', {'result': result})
                else:
                    return render(request, 'meal_plans/search.html', {'results': results})
                    
    return render(request, 'meal_plans/search.html')


