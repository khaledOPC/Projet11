from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from users.models import Product, Category, Brand, Favorite


class AddToFavoritesViewTest(TestCase):
    def setUp(self):
        # Crée un utilisateur et connecte-le pour les tests
        self.user = User.objects.create_user(username='testuser', password='12345') 
        self.client = Client()
        self.client.login(username='testuser', password='12345')
        
        # Crée un produit de test à ajouter aux favoris
        self.product = Product.objects.create(name='Test Product')

    def test_add_to_favorites_with_authenticated_user(self):
        # Teste l'ajout d'un produit aux favoris avec un utilisateur authentifié
        response = self.client.post(reverse('add_to_favorites', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)  # Vérifie que l'utilisateur est redirigé (statut 302)
        # Vérifie que le produit a bien été ajouté aux favoris de l'utilisateur
        self.assertTrue(Favorite.objects.filter(user=self.user, product=self.product).exists())

    def test_add_to_favorites_redirects_to_favorites_page(self):
        # Vérifie que l'utilisateur est redirigé vers la page des favoris après l'ajout
        response = self.client.post(reverse('add_to_favorites', args=[self.product.id]))
        self.assertRedirects(response, reverse('favorites'))  # Vérifie la redirection vers la page 'favorites'

    def test_add_to_favorites_with_unauthenticated_user(self):
        # Teste l'ajout aux favoris sans être connecté (utilisateur non authentifié)
        self.client.logout()  # Déconnecte l'utilisateur
        response = self.client.post(reverse('add_to_favorites', args=[self.product.id]))
        self.assertNotEqual(response.status_code, 200)  # Le statut ne doit pas être 200 car l'utilisateur n'est pas connecté

    def test_add_to_favorites_with_nonexistent_product(self):
        # Teste l'ajout d'un produit inexistant aux favoris
        response = self.client.post(reverse('add_to_favorites', args=[999]))  # Utilise un ID de produit inexistant
        self.assertEqual(response.status_code, 404)  # Vérifie que le statut est 404 (produit non trouvé)

    def test_add_to_favorites_prevents_duplicate(self):
        # Vérifie qu'un produit ne peut pas être ajouté plusieurs fois aux favoris du même utilisateur
        Favorite.objects.create(user=self.user, product=self.product)  # Ajoute le produit une première fois aux favoris
        response = self.client.post(reverse('add_to_favorites', args=[self.product.id]))
        # Vérifie qu'il n'y a qu'une seule instance du produit dans les favoris de l'utilisateur
        self.assertEqual(Favorite.objects.filter(user=self.user, product=self.product).count(), 1)
