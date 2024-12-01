from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
# Vos modèles personnalisés (remplacez 'YourApp' et 'YourModel' par les noms appropriés)
from users.models import Product, Category, Brand

class HomePageTest(TestCase):
    def test_search_form_submission(self):
        # Teste la soumission du formulaire de recherche
        response = self.client.get(reverse('search'), {'query': 'produit test'})
        self.assertEqual(response.status_code, 200)

    def test_home_page_status_code(self):
        # Vérifie que la page d'accueil est accessible
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')


    def test_search_form_empty_query(self):
        # Teste la soumission du formulaire de recherche sans données
        response = self.client.get(reverse('search'), {'query': ''})
        self.assertEqual(response.status_code, 200)
        # Vérifiez ici si le comportement est celui attendu (par exemple, tous les produits sont retournés)
    
    def test_search_form_invalid_query(self):
        # Teste la soumission du formulaire avec une requête invalide
        response = self.client.get(reverse('search'), {'query': 'invalidquery123'})
        self.assertEqual(response.status_code, 200)
        # Vérifiez si le comportement est correct (par exemple, aucun produit n'est retourné)
    
    def test_search_form_valid_query(self):
        # Teste la soumission du formulaire avec une requête valide
        response = self.client.get(reverse('search'), {'query': 'produit existant'})
        self.assertEqual(response.status_code, 200)
        # Vérifiez si le comportement est correct (par exemple, des produits correspondants sont retournés)
