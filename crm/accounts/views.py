from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login, authenticate


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('index')  # Changed from 'myapp:index'
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})  # Fixed path

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return render(request, 'accounts/logout.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # 🔐 Role-based redirect
            if user.is_staff:
                return redirect('dashboard:index')
            else:
                return redirect('index')  # myapp homepage

        else:
            return render(request, 'accounts/login.html', {
                'error': 'Invalid credentials'
            })

    return render(request, 'accounts/login.html')