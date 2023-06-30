from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import UserProfileForm
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm,  UserProfileForm, UserLoginForm


# Create your views here.

# regitration view
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('meal_plans:index')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})



# login view
def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('meal_plans:meal_plan_list')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = UserLoginForm()
    return render(request, 'registration/login.html', {'form': form})



# user profile view
@login_required
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('users:profile')
    else:
        form = UserProfileForm(instance=user)

    context = {
        'user': user,
        'form': form
    }
    return render(request, 'registration/profile.html', context)


def logout_view(request):
    logout(request)
    return render(request, "registration/loggedout.html")


# search functionality