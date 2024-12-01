from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class BaseViewTest(TestCase):
    def setUp(self):
        # Création d'un utilisateur pour le test
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client = Client()
        self.client.login(username='testuser', password='12345')

    def test_base_view_authenticated_user(self):
        # Teste l'accès à la vue 'base' pour un utilisateur authentifié
        response = self.client.get(reverse('base'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
    
    def test_base_view_unauthenticated_user(self):
        # Teste l'accès à la vue 'base' pour un utilisateur non authentifié
        self.client.logout()
        response = self.client.get(reverse('base'))
        self.assertEqual(response.status_code, 302)
        # Vérifiez également que la redirection mène à la page de connexion
        self.assertTrue(response.url.startswith(reverse('login')))
