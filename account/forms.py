from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Customer


# class CustomerCreationForm(forms.ModelForm):
#     phone = forms.CharField(max_length=20, required=True)
#     address = forms.CharField(max_length=100, required=True)
#     class Meta:
#         model = Customer
#         fields = ['phone', 'address']
#         widgets = {
#             'phone': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
#             'address': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
#         }


class SignUpForm(UserCreationForm):
    # customer = CustomerCreationForm()
    # first_name = forms.CharField(max_length=30, required=True)
    # last_name = forms.CharField(max_length=30, required=True)
    phone = forms.CharField(max_length=20, required=True)
    address = forms.CharField(max_length=100, required=True)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2', 'phone', 'address']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
        }


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class CustomerUpdateForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput)
    class Meta:
        model = Customer
        fields = ['phone', 'address', 'image']
