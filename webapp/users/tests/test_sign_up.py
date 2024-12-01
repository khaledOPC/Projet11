# Django testing utilities
from django.test import TestCase
# URL resolving
from django.urls import reverse
# User model (si vous testez des fonctionnalités liées aux utilisateurs)
from django.contrib.auth.models import User
# Vos modèles personnalisés (remplacez 'YourApp' et 'YourModel' par les noms appropriés)
from users.models import Product, Category, Brand


class SignupViewTest(TestCase):
    def test_signup_view_get(self):
        # Teste si la vue 'signup' répond correctement à une requête GET
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)  # Vérifie que le statut de la réponse est 200 (OK)
        self.assertTemplateUsed(response, 'signup.html')  # Vérifie que le bon template est utilisé pour la réponse

    def test_successful_signup(self):
        # Teste un cas d'inscription réussi avec des données de formulaire valides
        form_data = {'username': 'newuser', 'password1': 'testpassword123', 'password2': 'testpassword123'}
        response = self.client.post(reverse('signup'), form_data)
        self.assertEqual(response.status_code, 302)  # Vérifie que la réponse est une redirection (302)
        # Vérifie que l'utilisateur est bien créé dans la base de données
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_signup_with_mismatched_passwords(self):
        # Teste l'inscription avec des mots de passe qui ne correspondent pas
        form_data = {'username': 'testuser', 'password1': 'testpassword123', 'password2': 'differentpassword'}
        response = self.client.post(reverse('signup'), form_data)
        self.assertEqual(response.status_code, 200)  # Vérifie qu'il n'y a pas de redirection
        # Vérifie qu'aucun utilisateur n'est créé lorsque les mots de passe ne correspondent pas
        self.assertFalse(User.objects.filter(username='testuser').exists())

    def test_signup_with_existing_username(self):
        # Teste l'inscription avec un nom d'utilisateur déjà existant
        User.objects.create_user(username='existinguser', password='password123')  # Crée un utilisateur
        form_data = {'username': 'existinguser', 'password1': 'password123', 'password2': 'password123'}
        response = self.client.post(reverse('signup'), form_data)
        self.assertEqual(response.status_code, 200)  # Vérifie qu'il n'y a pas de redirection
        # Vérifie qu'il n'y a qu'un seul utilisateur avec ce nom d'utilisateur dans la base de données
        self.assertEqual(User.objects.filter(username='existinguser').count(), 1)
