from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


class UserRegistrationForm(forms.Form):
    username = forms.CharField(label='Nom d\'utilisateur', max_length=30)
    email = forms.EmailField(label='Adresse e-mail')
    password1 = forms.CharField(label='Mot de passe', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmation du mot de passe', widget=forms.PasswordInput)



class Search(forms.Form):
    recherche = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rechercher...'}))
