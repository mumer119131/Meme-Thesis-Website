from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, ProfileForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.


def login_user(request):
    if request.user.is_authenticated:
        return redirect('home_page')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist")

        user = authenticate(
            request=request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home_page')
        else:
            messages.error(request, "Invalid Username or Password")

    form = CustomUserCreationForm
    context = {'form': form}
    return render(request, 'landing/login.html', context=context)


def register_user(request):
    form = CustomUserCreationForm()
    context = {'form': form}
    if request.method == 'POST':
        print("GOT REQUEST")
        form = CustomUserCreationForm(request.POST)
        print(form)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            print("Saved")
            return redirect('home_page')
        else:
            print("Invalid Form")

    form = CustomUserCreationForm
    context = {'form': form}
    return render(request, 'landing/login.html', context=context)


def home_page(request):
    if request.user.is_authenticated:
        user = request.user
        context = {'user': user}
        return render(request, 'landing/home.html', context=context)
    else:
        return redirect('login')
