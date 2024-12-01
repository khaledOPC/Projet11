import requests
from django.core.management.base import BaseCommand
from users.models import Product, Category, Store, Brand

def clean_category(category):
    # Supprimer 'en:' et 'fr:' et prendre la dernière catégorie
    categories = category.split(',')
    cleaned_categories = [cat.replace('en:', '').replace('fr:', '') for cat in categories]
    return cleaned_categories[-1].strip() if cleaned_categories else None

def get_products_data(categories):
    products = []
    url = "https://world.openfoodfacts.org/cgi/search.pl"
    for category in categories:
        params = {
            "action": "process",
            "json": 1,
            "tagtype_0": "categories",
            "tag_contains_0": "contains",
            "tag_0": category,
            "page_size": 200,
        }
        response = requests.get(url, params=params)
        if response.ok:
            products.extend(response.json()["products"])
    return products

class Command(BaseCommand):
    help = "Importe les produits à partir d'Open Food Facts"

    def handle(self, *args, **kwargs):
        categories_to_fetch = [
            "pizzas",
            "pasta",
            "sodas",
            "cakes",
            "breakfast-biscuits",
            "cheeses",
            "breads",
            "pastries",
            "juices",
            "cereals",
        ]

        products_data = get_products_data(categories_to_fetch)

        for product_data in products_data:
            try:
                raw_category = product_data.get("categories", "").strip()
                cleaned_category = clean_category(raw_category)
                category = (
                    Category.objects.get_or_create(name=cleaned_category)[0]
                    if cleaned_category
                    else None
                )

                # Vérification des doublons avant d'ajouter un produit
                existing_product = Product.objects.filter(
                    name=product_data.get("product_name", ""),
                    nutriscore=product_data.get("nutrition_grades", ""),
                    novascore=product_data.get("nova_groups", None),
                    brand__name=product_data.get("brands", "").strip(),
                    # ... ajoutez d'autres critères si nécessaire
                )
        
                if existing_product.exists():
                    self.stdout.write(
                        self.style.WARNING(f"Le produit '{product_data.get('product_name', '')}' existe déjà, il n'a donc pas été ajouté.") # noqa
                    )
                    continue

                nom_marque = product_data.get("brands", "").strip()
                brand = (
                    Brand.objects.get_or_create(name=nom_marque)[0]
                    if nom_marque
                    else None
                )

                product, created = Product.objects.update_or_create(
                    url=product_data.get("url", ""),
                    defaults={
                        "name": product_data.get("product_name", ""),
                        "nutriscore": product_data.get("nutrition_grades", ""),
                        "novascore": product_data.get("nova_groups", None),
                        "image_url": product_data.get("image_url", ""),
                        "category": category,
                        "brand": brand,
                        "nutrition_data": product_data.get("nutriments", {}),
                    },
                )

                store_names = product_data.get("stores", "").split(",")
                stores = [
                    Store.objects.get_or_create(name=store_name.strip())[0]
                    for store_name in store_names
                    if store_name.strip()
                ]
                product.stores.set(stores)

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Produit '{product.name}' importé avec l'ID : {product.id}" # noqa
                    )
                )

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"Erreur lors de l'importation du produit : {e}") # noqa
                )
