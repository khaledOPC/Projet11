import django
import os
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from users.models import Product, Category, Brand

# Configure les paramètres de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webapp.settings')
django.setup()

class ProductPageTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Configurer les options de Chrome
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Exécute Chrome en mode sans tête.
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # Utilisation de webdriver_manager pour installer la version correcte de ChromeDriver
        chrome_service = ChromeService(ChromeDriverManager().install())
        
        # Initialise le driver Chrome avec le service et les options
        cls.selenium = webdriver.Chrome(service=chrome_service, options=chrome_options)
        cls.selenium.implicitly_wait(10)  # Attente implicite pour trouver les éléments

    @classmethod
    def tearDownClass(cls):
        # Quitter le navigateur après les tests
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        # Configure les éléments nécessaires pour le test
        self.category = Category.objects.create(name="Some Category")
        self.brand = Brand.objects.create(name="Some Brand")
        self.product = Product.objects.create(
            name="Test Product",
            nutriscore='A',
            novascore=1,
            category=self.category,
            brand=self.brand,
            url="https://fr.openfoodfacts.org/produit/1234567890/test-product"  # URL fictive pour le test
        )

    def test_product_detail(self):
        # Construit l'URL pour la page de détail du produit
        product_detail_url = self.live_server_url + reverse('product_detail', kwargs={'product_id': self.product.id})
        
        # Demande à Selenium d'aller sur cette page
        self.selenium.get(product_detail_url)

        # Vérification de l'affichage du nom du produit dans la bannière
        product_name_element = self.selenium.find_element(By.CSS_SELECTOR, "h1")
        self.assertEqual(product_name_element.text, "Test Product")

        # Vérification de l'affichage du Nutri-Score
        nutriscore_element = self.selenium.find_element(By.CSS_SELECTOR, ".row .col-lg-6.text-center div")
        self.assertEqual(nutriscore_element.text, "A")

        # Vérification de la présence du lien vers Open Food Facts
        openfood_link = self.selenium.find_element(By.LINK_TEXT, "Voir le produit sur Open Food Facts")
        self.assertEqual(openfood_link.get_attribute("href"), "https://fr.openfoodfacts.org/produit/1234567890/test-product")

