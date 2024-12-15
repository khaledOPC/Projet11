from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Adresse e-mail")

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)  # Enregistre partiellement l'utilisateur
        user.email = self.cleaned_data["email"]  # Ajoute l'email à l'utilisateur
        if commit:
            user.save()  # Sauvegarde complète l'utilisateur dans la base de données
        return user


class Search(forms.Form):
    recherche = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rechercher...'}))

