# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from files.models import File

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to dashboard page after successful login
    return render(request, 'accounts/login.html')


def user_files(request):
    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        # Handle unauthenticated user (e.g., redirect to login page)
        pass

    # Fetch the files associated with the user
    user_files = File.objects.filter(owner=request.user)

    return render(request, 'accounts/user_files.html', {'files': user_files})


def dashboard(request):
    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        return redirect('login')
    user_files = File.objects.filter(owner=request.user)
    return render(request, 'accounts/dashboard.html')
