from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from blog.models import Post

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
            user = forms.save(commit=False)
            user.is_staff = True
            user.save()
            first_name = forms.cleaned_data.get('first_name')
            last_name = forms.cleaned_data.get('last_name')
            email = forms.cleaned_data.get('email')
            customer = Customer.objects.create(first_name=first_name, last_name=last_name, email=email, user=user)
            customer.save()
            # Gán quyền CRUD cho model Post
            content_type = ContentType.objects.get_for_model(Post)  # Lấy ContentType cho model Post
            permissions = Permission.objects.filter(
                content_type=content_type)  # Lấy tất cả các quyền liên quan đến model Post

            # Gán các quyền CRUD cho user
            user.user_permissions.add(*permissions)
            return redirect('user_login')
        else:
            messages.error(request, 'User already exist!!!')
            return redirect('user_register')
    else:
        forms = SignUpForm()
    return render(request, 'account/register.html', {'forms': forms})