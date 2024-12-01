from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from users.models import Product, Category

class ProductSubstitutesViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Création de données pour le test
        cls.category = Category.objects.create(name="Snacks")
        cls.product_with_scores = Product.objects.create(name="Chips", category=cls.category, nutriscore='b', novascore=2)
        Product.objects.create(name="Pretzels", category=cls.category, nutriscore='a', novascore=1)  # Substitut potentiel

    def test_no_substitutes_when_product_not_found(self):
        # Teste la réponse lorsque le produit n'est pas trouvé
        response = self.client.get(reverse('product_substitutes', args=[999]))
        self.assertEqual(response.status_code, 404)  # Doit retourner un 404

    def test_no_substitutes_when_product_has_no_scores(self):
        # Teste quand le produit n'a pas de scores nutritionnels
        product_without_scores = Product.objects.create(name="Soda", category=self.category)
        response = self.client.get(reverse('product_substitutes', args=[product_without_scores.id]))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Pretzels")  # Aucun substitut ne doit être trouvé

    def test_substitutes_found(self):
        # Teste la présence de substituts
        response = self.client.get(reverse('product_substitutes', args=[self.product_with_scores.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pretzels")  # Le substitut "Pretzels" doit être trouvé

    def test_substitutes_view_uses_correct_template(self):
        # Vérifie que le bon template est utilisé
        response = self.client.get(reverse('product_substitutes', args=[self.product_with_scores.id]))
        self.assertTemplateUsed(response, 'substitutes.html')

    def test_substitutes_context_data(self):
        # Vérifie les données du contexte
        response = self.client.get(reverse('product_substitutes', args=[self.product_with_scores.id]))
        self.assertIn('substitutes', response.context)  # Vérifie que 'substitutes' est dans le contexte
