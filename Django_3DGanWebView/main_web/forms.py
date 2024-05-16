from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import GanGeneratedModel

class LoginForm(forms.Form):
    username = forms.CharField(max_length=65, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(max_length=65, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class RegisterForm(UserCreationForm):
    class Meta:
        model=User
        fields = ['username', 'first_name', 'last_name','email','password1','password2']

class GenerateForm(forms.ModelForm):
    class Meta:
        model = GanGeneratedModel
        fields = ['name', 'generated_Img']