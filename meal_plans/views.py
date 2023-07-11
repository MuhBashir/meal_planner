from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import MealPlanForm, MealForm, RecipeForm
from .models import MealPlan, Meal, Recipe
import requests
from itertools import groupby
from operator import attrgetter
import datetime
import environ
import dj_database_url

env = environ.Env()
environ.Env.read_env()



def index(request):
    return render(request, "meal_plans/index.html")

@login_required
def meal_plan_list(request):
    meal_plans = MealPlan.objects.filter(user=request.user)
    context = {'meal_plans': meal_plans}
    return render(request, 'meal_plans/meal_plan_list.html', context)


@login_required
def meal_plan_detail(request, pk):
    meal_plan = get_object_or_404(MealPlan, pk=pk, user=request.user)
    meals = meal_plan.meal_set.all()
    now = datetime.date.today()
    context = {'meal_plan': meal_plan, 'meals': meals, "now": now,}
    return render(request, 'meal_plans/meal_plan_detail.html', context)


@login_required
def meal_plan_create(request):
    if request.method == 'POST':
        form = MealPlanForm(request.POST)
        if form.is_valid():
            meal_plan = form.save(commit=False)
            meal_plan.user = request.user
            meal_plan.save()
            return redirect('meal_plans:meal_plan_detail', pk=meal_plan.pk)
    else:
        form = MealPlanForm()
    context = {'form': form}
    return render(request, 'meal_plans/meal_plan_create.html', context)


@login_required
def meal_plan_update(request, pk):
    meal_plan = get_object_or_404(MealPlan, pk=pk, user=request.user)
    if request.method == 'POST':
        form = MealPlanForm(request.POST, instance=meal_plan)
        if form.is_valid():
            form.save()
            return redirect('meal_plans:meal_plan_detail', pk=meal_plan.pk)
    else:
        form = MealPlanForm(instance=meal_plan)
    context = {'form': form, 'meal_plan': meal_plan}
    return render(request, 'meal_plans/meal_plan_update.html', context)


@login_required
def meal_plan_delete(request, pk):
    meal_plan = get_object_or_404(MealPlan, pk=pk, user=request.user)
    if request.method == 'POST':
        meal_plan.delete()
        return redirect('meal_plans:meal_plan_list')
    context = {'meal_plan': meal_plan}
    return render(request, 'meal_plans/meal_plan_delete.html', context)


@login_required
def add_meal(request, meal_plan_id):
    meal_plan = get_object_or_404(MealPlan, pk=meal_plan_id, user=request.user)
    if request.method == 'POST':
        form = MealForm(request.POST)
        if form.is_valid():
            meal = form.save(commit=False)
            meal.meal_plan = meal_plan
            meal.save()
            return redirect('meal_plans:meal_plan_detail', pk=meal_plan.pk)
    else:
        form = MealForm()
    context = {'form': form, 'meal_plan': meal_plan}
    return render(request, 'meal_plans/add_meal.html', context)



@login_required
def meal_list_view(request):
    meals = Meal.objects.filter(meal_plan__user=request.user)

    meal_groups =[]

    for date, meals_in_date in groupby(meals, key=attrgetter('date_added')):
        meal_group = {
            'date': date,
            'meals': list(meals_in_date)
        }
        meal_groups.append(meal_group)
    
    context = {
        'meal_groups': meal_groups,
        'all_meals': meals
    }
    return render(request, 'meal_plans/meal_list.html', context)



@login_required
def meal_update(request, meal_id):
    meal = get_object_or_404(Meal, pk=meal_id, meal_plan__user=request.user)
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
def meal_delete(request, meal_id):
    meal = get_object_or_404(Meal, pk=meal_id, meal_plan__user=request.user)
    if request.method == 'POST':
        meal.delete()
        return redirect('meal_plans:meal_list')
    context = {'meal': meal}
    return render(request, 'meal_plans/meal_delete.html', context)


@login_required
def recipe_create(request, meal_id):
    meal = get_object_or_404(Meal, pk=meal_id, meal_plan__user=request.user)
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.meal = meal
            recipe.save()
            return redirect('meal_plans:recipe_detail', recipe_id=recipe.id)
    else:
        form = RecipeForm()
    context = {'form': form, 'meal': meal}
    return render(request, 'meal_plans/recipe_create.html', context)



@login_required
def recipe_update(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id )

    if request.method == 'POST':
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('meal_plans:recipe_detail', recipe_id=recipe.id)
    else:
        form = RecipeForm(instance=recipe)

    context = {
        'form': form,
        'recipe': recipe
    }
    return render(request, 'meal_plans/recipe_update.html', context)



@login_required
def recipe_delete(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)

    if request.method == 'POST':
        recipe.delete()
        return redirect('meal_plans:meal_list')

    context = {
        'recipe': recipe
    }
    return render(request, 'meal_plans/recipe_delete.html', context)


@login_required
def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    
    context = {
        'recipe': recipe
    }
    
    return render(request, 'meal_plans/recipe_detail.html', context)



def search_recipe(request):
    
    url =f"https://api.edamam.com/api/recipes/v2?type=public&q={request}&app_id={env('app_id')}&app_key={env('app_key')}"

    response = requests.get(url)
    print(response)
    data = response.json()
    # Parse the response and extract the search results
    results = data.get('hits', [])
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

















































































































































































































# from django.shortcuts import render, redirect, get_object_or_404
# from .models import MealPlan, Meal,Recipe
# from .forms import MealPlanForm, MealForm, RecipeForm
# from django.contrib.auth.decorators import login_required
# from py_edamam import Recipe
# import requests
# from itertools import groupby
# from operator import attrgetter



# def index(request):
#     return render(request, "meal_plans/index.html")

# @login_required
# def meal_plan_list(request):
#     meal_plans = MealPlan.objects.filter(user=request.user)
#     context = {'meal_plans': meal_plans}
#     return render(request, 'meal_plans/meal_plan_list.html', context)


# @login_required
# def meal_plan_detail(request, pk):
#     meal_plan = MealPlan.objects.get(pk=pk, user=request.user)
#     context = {'meal_plan': meal_plan}
#     return render(request, 'meal_plans/meal_plan_detail.html', context)



# @login_required
# def meal_plan_create(request):
#     if request.method == 'POST':
#         form = MealPlanForm(request.POST)
#         if form.is_valid():
#             meal_plan = form.save(commit=False)
#             meal_plan.user = request.user
#             meal_plan.save()
#             return redirect('meal_plans:meal_plan_list')
#     else:
#         form = MealPlanForm()
#     context = {'form': form}
#     return render(request, 'meal_plans/meal_plan_create.html', context)


# @login_required
# def meal_plan_update(request, pk):
#     meal_plan = MealPlan.objects.get(pk=pk, user=request.user)
#     if request.method == 'POST':
#         form = MealPlanForm(request.POST, instance=meal_plan)
#         if form.is_valid():
#             form.save()
#             return redirect('meal_plans:meal_plan_list')
#     else:
#         form = MealPlanForm(instance=meal_plan)
#     context = {'form': form, 'meal_plan': meal_plan}
#     return render(request, 'meal_plans/meal_plan_update.html', context)



# @login_required
# def meal_plan_delete(request, pk):
#     meal_plan = MealPlan.objects.get(pk=pk, user=request.user)
#     if request.method == 'POST':
#         meal_plan.delete()
#         return redirect('meal_plans:meal_plan_list')
#     context = {'meal_plan': meal_plan}
#     return render(request, 'meal_plans/meal_plan_delete.html', context)



# # add meals
# @login_required
# def add_meal(request, pk):
#     meal_plan = MealPlan.objects.get(pk=pk)

#     if request.method == 'POST':
#         form = MealForm(data=request.POST)
#         if form.is_valid():
#             meal = form.save(commit=False)
#             meal.meal_plan = meal_plan
#             meal.save()
#             return redirect('meal_plans:meal_list')
#     else:
#         form = MealForm()
    
#     context = {
#         'meal_plan': meal_plan,
#         'form': form,
#     }
    
#     return render(request, 'meal_plans/add_meal.html', context)



# @login_required
# def meal_list_view(request):
    
#     meals = Meal.objects.all().order_by('date_added')
#     meal_groups = []
    
    # for date, meals_in_date in groupby(meals, key=attrgetter('date_added')):
    #     meal_group = {
    #         'date': date,
    #         'meals': list(meals_in_date)
    #     }
    #     meal_groups.append(meal_group)
    
    # context = {
    #     'meal_groups': meal_groups
    # }


#     return render(request, 'meal_plans/meal_list.html', context)


# # @login_required
# # def meal_delete(request, meal_id):
# #     meal = Meal.objects.get(pk=meal_id)

# #     if request.method == 'POST':
# #         meal.delete()
# #         return redirect('meal_plans:meal_list')

# #     context = {'meal': meal}
# #     return render(request, 'meal_plans/meal_delete.html', context)



# # @login_required
# # def meal_update(request, meal_id):
# #     meal = get_object_or_404(Meal, id=meal_id)

# #     if request.method == 'POST':
# #         form = MealForm(request.POST, instance=meal)
# #         if form.is_valid():
# #             form.save()
# #             return redirect('meal_plans:meal_list')
# #     else:
# #         form = MealForm(instance=meal)

# #     context = {'form': form, 'meal': meal}
# #     return render(request, 'meal_plans/meal_update.html', context)



# @login_required
# def recipe_create(request, ):
#     # Retrieve the associated meal object
#     meal = Meal.objects.get()

#     if request.method == 'POST':
#         form = RecipeForm(request.POST)
#         if form.is_valid():
#             # Create a new recipe object
#             recipe = form.save(commit=False)
#             recipe.meal = meal
#             recipe.save()
#             return redirect('meal_plans:recipe_detail', meal_plan_id=recipe.id)
#     else:
#         form = RecipeForm()

#     context = {
#         'form': form,
#         'meal_plan_id': meal_plan_id,
#     }

#     return render(request, 'meal_plans/recipe_create.html', context)




# # @login_required

# # def recipe_update(request, meal_plan_id):
# #     # recipe = get_object_or_404(Recipe, pk=recipe_id)
# #     recipe= Meal.objects.get(id=meal_plan_id)


# #     if request.method == 'POST':
# #         form = RecipeForm(request.POST, instance=recipe)
# #         if form.is_valid():
# #             form.save()
# #             return redirect('meal_plans:recipe_detail', meal_plan_id=meal_plan_id)
# #     else:
# #         form = RecipeForm(instance=recipe)

# #     context = {
# #         'form': form,
# #         'recipe': recipe,
# #     }
# #     return render(request, 'meal_plans/recipe_update.html', context)

# # # def recipe_update(request, recipe_id):
# # #     # recipe = Meal.objects.get(id=recipe_id)
# # #     recipe = get_object_or_404(Recipe, pk=recipe_id)
    
# # #     if request.method == 'POST':
# # #         form = RecipeForm(request.POST, instance=recipe)
# # #         if form.is_valid():
# # #             form.save()
# # #             return redirect('meal_plans:meal_list', meal_id=meal.id)
# # #     else:
# # #         form = RecipeForm(instance=recipe)
    
# # #     context = {
# # #         'form': form,
# # #         'meal': meal,
# # #         'recipe': recipe
# # #     }
# # #     return render(request, 'meal_plans/recipe_update.html', context)

# # # def recipe_update(request, meal_id):
# # #     meal = get_object_or_404(Meal, id=meal_id)
# # #     print(meal.id)
# # #     recipe = meal.recipe
    
# # #     if request.method == 'POST':
# # #         form = RecipeForm(request.POST, instance=recipe)
# # #         if form.is_valid():
# # #             form.save()
# # #             return redirect('meal_plans:meal_list', meal_id=meal.id)
# # #     else:
# # #         form = RecipeForm(instance=recipe)
    
# # #     context = {
# # #         'form': form,
# # #         'meal': meal
# # #     }
# # #     return render(request, 'meal_plans/recipe_update.html', context)



# # @login_required
# # def recipe_delete(request, meal_plan_id):
# #     recipe = Meal.objects.get(id=meal_plan_id)
# #     # recipe = meal.recipe
    
# #     if request.method == 'POST':
# #         recipe.delete()
# #         return redirect('meal_plans:recipe_detail', meal_plan_id=recipe.id)
    
# #     context = {
# #         'recipe': recipe
# #     }
# #     return render(request, 'meal_plans/recipe_delete.html', context)


# # # def recipe_delete(request, recipe_id):
# # #     # recipe = get_object_or_404(Recipe, pk=recipe_id)
# # #     recipe = Meal.objects.get(pk=recipe_id)
    
# # #     # Check if the meal associated with the recipe exists
# # #     if recipe.meal:
# # #         meal = recipe.meal
# # #         recipe.delete()
# # #         return redirect('meal_detail', meal_id=meal.id)
# # #     else:
# # #         # Handle the case when the meal doesn't exist
# # #         # Redirect or display an error message
# # #         # ...
# # #         pass


# @login_required
# def recipe_detail(request, meal_plan_id):
#     recipe = Meal.objects.get(pk=meal_plan_id)
#     context = {
#         'recipe': recipe,

#     }
    
#     return render(request, 'meal_plans/recipe_detail.html', context)



# def search_recipe(request):
#     app_id = 'd9011687'
#     app_key = "bd6fc5344fac17ee891c216612444a4c"
#     url = f"https://api.edamam.com/api/recipes/v2?type=public&q={request}&app_id={app_id}&app_key={app_key}"
    

#     response = requests.get(url)
#     data = response.json()
#     # Parse the response and extract the search results
#     results = data.get('hits', [])
#     return results






# def search_view(request):
#     if request.method == 'GET':
#         query = request.GET.get('query')
#         if query:
#             # Call the search_recipe function with the query parameter
#             results = search_recipe(query)
#             for result in results:
#                 if result["recipe"].get("label") == query:
#                     return render(request, 'meal_plans/search.html', {'result': result})
#                 else:
#                     return render(request, 'meal_plans/search.html', {'results': results})
                    
#     return render(request, 'meal_plans/search.html')


