from django.urls import path, include
from . import views

app_name = "users"
urlpatterns = [
    # include the defaults urls
    # path('', include('django.contrib.auth.urls')),
    path("login/", views.user_login, name="login"),
    path("register/", views.register, name="register"),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', views.logout_view, name='logout'),

]