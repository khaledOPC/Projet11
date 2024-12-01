from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from users.models import Product, Category, Brand, Favorite

class FavoritesViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client = Client()
        self.client.login(username='testuser', password='12345')
        self.product = Product.objects.create(name='Test Product')
        Favorite.objects.create(user=self.user, product=self.product)

    def test_favorites_view_lists_user_favorites(self):
        response = self.client.get(reverse('favorites'))
        favorite_products = [favorite.product for favorite in response.context['favorites']]
        self.assertIn(self.product, favorite_products)

    def test_favorites_view_with_authenticated_user(self):
        response = self.client.get(reverse('favorites'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'favorites.html')


    def test_favorites_view_with_unauthenticated_user(self):
        self.client.logout()
        response = self.client.get(reverse('favorites'))
        self.assertNotEqual(response.status_code, 200)

    def test_favorites_view_context(self):
        response = self.client.get(reverse('favorites'))
        self.assertTrue('favorites' in response.context)

    def test_favorites_view_empty_list(self):
        Favorite.objects.filter(user=self.user).delete()
        response = self.client.get(reverse('favorites'))
        self.assertEqual(len(response.context['favorites']), 0)
