from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

from users.models import Product, Category, Brand


class ResultatViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Création d'un utilisateur pour le test
        User.objects.create_user(username='testuser', password='12345')

    def test_resultat_view_get_request(self):
        # Teste la réponse à une requête GET
        response = self.client.get(reverse('resultat'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'resultat.html')

    def test_resultat_view_post_request_valid_credentials(self):
        # Teste la connexion avec des informations d'identification valides
        valid_credentials = {'username': 'testuser', 'password': '12345'}
        response = self.client.post(reverse('resultat'), valid_credentials)
        self.assertEqual(response.status_code, 302)  # Doit rediriger après une connexion réussie

    def test_resultat_view_post_request_invalid_credentials(self):
        # Teste la connexion avec des informations d'identification invalides
        invalid_credentials = {'username': 'wronguser', 'password': 'wrongpass'}
        response = self.client.post(reverse('resultat'), invalid_credentials)
        self.assertEqual(response.status_code, 200)
        # Vérifie que le formulaire avec des erreurs est retourné
        self.assertIsInstance(response.context['form'], AuthenticationForm)
        self.assertFalse(response.context['form'].is_valid())

    def test_resultat_view_uses_correct_template(self):
        # Vérifie que le bon template est utilisé
        response = self.client.get(reverse('resultat'))
        self.assertTemplateUsed(response, 'resultat.html')

    def test_resultat_view_context_data(self):
        # Vérifie les données du contexte lors de l'utilisation d'un GET
        response = self.client.get(reverse('resultat'))
        self.assertIn('form', response.context)  # Vérifie que 'form' est dans le contexte
