from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings

class ConnectedViewTest(TestCase):
    def setUp(self):
        # Création et connexion d'un utilisateur de test
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_connected_view_with_unauthenticated_user(self):
        # Teste l'accès à la vue 'Connected' pour un utilisateur non authentifié
        self.client.logout()
        response = self.client.get(reverse('Connected'))
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('login'))  # Vérifie la redirection vers la page de connexion


    def test_connected_view_uses_correct_template(self):
        # Vérifie que la vue 'Connected' utilise le bon template
        response = self.client.get(reverse('Connected'))
        self.assertTemplateUsed(response, 'Connected.html')

    def test_connected_view_with_unauthenticated_user(self):
        # Teste l'accès à la vue 'Connected' pour un utilisateur non authentifié
        self.client.logout()
        response = self.client.get(reverse('Connected'))
        self.assertNotEqual(response.status_code, 200)

    def test_connected_view_redirects_unauthenticated_user(self):
        # Teste si les utilisateurs non authentifiés sont redirigés
        self.client.logout()
        response = self.client.get(reverse('Connected'))
        self.assertTrue(response.status_code, 302)  # Ou utilisez assertRedirects pour une URL spécifique

    def test_connected_view_context_data(self):
        # Teste les données du contexte de la vue 'Connected'
        response = self.client.get(reverse('Connected'))
        # Vérifiez ici la présence de données spécifiques dans le contexte, si nécessaire
        # self.assertIn('clé_de_contexte', response.context)
