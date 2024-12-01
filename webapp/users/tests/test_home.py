from django.test import TestCase, Client
from django.urls import reverse

class HomeViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_view_status_code(self):
        # Teste si la vue 'home' est accessible
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_view_uses_correct_template(self):
        # Vérifie que la vue 'home' utilise le bon template
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'home.html')
