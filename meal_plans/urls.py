from django.urls import path
from . import views
from .views import search_view

app_name = "meal_plans"

urlpatterns = [
    path("", views.index, name="index"),
    path('meal_plans/', views.meal_plan_list, name='meal_plan_list'),
    path('meal_plans/<int:pk>/', views.meal_plan_detail, name='meal_plan_detail'),
    path('meal_plans/create/', views.meal_plan_create, name='meal_plan_create'),
    path('meal_plans/<int:pk>/update/', views.meal_plan_update, name='meal_plan_update'),
    path('meal_plans/<int:pk>/delete/', views.meal_plan_delete, name='meal_plan_delete'),
    path('meal_plans/<int:meal_plan_id>/add_meal/', views.add_meal, name='add_meal'),
    path('meal_plans/meal_list/', views.meal_list_view, name="meal_list"),
    path('meal_plans/meal/update/<int:meal_id>/', views.meal_update, name='meal_update'),
    path('meal_plans/meal/delete/<int:meal_id>/', views.meal_delete, name='meal_delete'),
    path('meal_plans/<int:meal_id>/recipe/create/', views.recipe_create, name='recipe_create'),
    path('meal_plans/<int:recipe_id>/recipe/update/', views.recipe_update, name='recipe_update'),
    path('meal_plans/<int:recipe_id>/recipe/delete/', views.recipe_delete, name='recipe_delete'),
    path('recipes/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('search/', search_view, name='search'),

]


















# urlpatterns = [
    #   path("", views.index, name="index"),
    # path('meal_plans/', views.meal_plan_list, name='meal_plan_list'),
    # path('meal_plans/create/', views.meal_plan_create, name='meal_plan_create'),
    # path('meal_plans/<int:pk>/', views.meal_plan_detail, name='meal_plan_detail'),
    # path('meal_plans/<int:pk>/update/', views.meal_plan_update, name='meal_plan_update'),
    # path('meal_plans/<int:pk>/delete/', views.meal_plan_delete, name='meal_plan_delete'),
    # path('meal_plans/<int:pk>/add_meal/', views.add_meal, name='add_meal'),
    # path('meal_plans/meal_list', views.meal_list_view, name="meal_list"),
    # path('meal_plans/<int:meal_plan_id>/recipe/create/', views.recipe_create, name='recipe_create'),
    # path('recipes/<int:meal_plan_id>/', views.recipe_detail, name='recipe_detail'),
    # path('search/', search_view, name='search'),
#     path('meal_plans/meal/update/<int:meal_id>/', views.meal_update, name='meal_update'),
#     path('meal_plans/meal/delete/<int:meal_id>/', views.meal_delete, name='meal_delete'),
#     path('meal_plans/<int:meal_plan_id>/recipe/update/', views.recipe_update, name='recipe_update'),
#     path('meal_plans/<int:meal_plan_id>/recipe/delete/', views.recipe_delete, name='recipe_delete'),
# ]
