from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm
from .models import Customer

def user_login(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'User or password is invalid!!!')
            return redirect('user_login')
    return render(request, 'account/login.html', {})


def user_logout(request):
    logout(request)
    return redirect('user_login')


def user_register(request):
    if request.user.is_authenticated:
        return redirect('store:home')

    if request.method == 'POST':
        forms = SignUpForm(request.POST)

        if forms.is_valid():
            user = forms.save()
            first_name = forms.cleaned_data.get('first_name')
            last_name = forms.cleaned_data.get('last_name')
            email = forms.cleaned_data.get('email')
            customer = Customer.objects.create(first_name=first_name, last_name=last_name, email=email, user=user)
            customer.save()
            return redirect('user_login')
        else:
            messages.error(request, 'User already exist!!!')
            return redirect('user_register')
    else:
        forms = SignUpForm()
    return render(request, 'account/register.html', {'forms': forms})