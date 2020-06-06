from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
# class SignupForm(UserCreationForm):
#     email = forms.EmailField(max_length=200, help_text='Required')
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password1', 'password2')

class register(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'input'}),max_length=50,required=True)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'input'}),max_length=50,required=True)
    firstname = forms.CharField(widget=forms.TextInput(attrs={'class':'input'}),max_length=50,required=True)
    lastname = forms.CharField(widget=forms.TextInput(attrs={'class':'input'}),max_length=50,required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'input'}),max_length=50,required=True)

    class Meta():
        model = User
        fields = ['username','email','firstname','lastname','password']