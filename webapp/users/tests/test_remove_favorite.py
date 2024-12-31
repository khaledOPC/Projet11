from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from users.models import Product, Favorite


class RemoveFavorite(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', 
            password='12345')
        self.product = Product.objects.create(name='test_product')
        self.client.login(username='testuser', password='12345')
        Favorite.objects.create(user=self.user, product=self.product)

    def test_remove_favorite(self):
        response = self.client.post(reverse('remove_favorite', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('favorites'))
        self.assertFalse(Favorite.objects.filter(user=self.user, product=self.product).exists())

    def test_user_authenticate(self):
        self.client.logout()
        login = self.client.login(username='testuser', password='12345')
        self.assertTrue(login)
 