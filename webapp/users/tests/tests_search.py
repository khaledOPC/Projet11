from django.test import TestCase, Client
from django.urls import reverse
from users.models import Product, Category
from django.db.models import Q

class SearchViewTestCase(TestCase):

    def setUp(self):
        # Initialisation du client de test
        self.client = Client()
        
        # Initialisation des catégories et des produits
        self.category = Category.objects.create(name='Test Category')
        
        self.products = [
            Product.objects.create(name=f'Test Product {i}', category=self.category, nutriscore='A', novascore='1') 
            for i in range(55)  # Création de 55 produits pour tester la limite de 50
        ]
        
        # URL de la vue à tester
        self.search_url = reverse('search')
        
    def test_search_view_uses_correct_template(self):
        # Teste si la vue utilise le bon template
        response = self.client.get(self.search_url, {'query': 'Test'})
        self.assertTemplateUsed(response, 'search.html')
        
    def test_search_view_with_query(self):
        # Teste la recherche avec une requête
        response = self.client.get(self.search_url, {'query': 'Test'})
        self.assertEqual(response.context['product'].name, 'Test Product 0')  # Vérifie le premier produit retourné
        
    def test_search_view_without_query(self):
        # Teste la recherche sans requête
        response = self.client.get(self.search_url)
        self.assertIsNone(response.context['product'])  # Aucune requête ne devrait retourner None pour le produit
        
    def test_search_view_substitutes_displayed(self):
        # Teste l'affichage des substituts
        category = Category.objects.create(name='TestCategory')
        
        original_product = Product.objects.create(
            name='Original Product', category=category, nutriscore='D', novascore='4')
        
        substitute_product = Product.objects.create(
            name='Substitute Product', category=category, nutriscore='B', novascore='4')
        
        response = self.client.get(reverse('search'), {'query': 'Original'})
        
        # Vérifie si les substituts sont retournés correctement
        self.assertEqual(len(response.context['substitutes']), 1)
        self.assertIn(substitute_product, response.context['substitutes'])
        
    def test_search_view_no_substitutes_for_better_nutriscore(self):
        # Teste qu'aucun substitut n'est retourné pour un produit avec un meilleur Nutri-Score
        category = Category.objects.create(name='TestCategory')
        
        non_substitute_product = Product.objects.create(
            name='Non Substitute Product', category=category, nutriscore='A', novascore='1')
        
        response = self.client.get(self.search_url, {'query': 'Non Substitute'})
        
        self.assertEqual(len(response.context['substitutes']), 0)
