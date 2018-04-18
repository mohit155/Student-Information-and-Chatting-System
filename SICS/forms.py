from django import forms
from .models import User

class Login(forms.Form):
    user_name = forms.CharField(label='Username', max_length=30,widget=forms.TextInput(attrs={'class': 'username'}))
    password = forms.CharField(label='Password', max_length=50, widget=forms.PasswordInput(attrs={'class': 'password'}))