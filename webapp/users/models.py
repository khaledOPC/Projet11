from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q

class Category(models.Model):
    name = models.CharField(max_length=200)

class Store(models.Model):
    name = models.CharField(max_length=200)

class Brand(models.Model):
    name = models.CharField(max_length=200)

class Product(models.Model):
    name = models.CharField(max_length=200)
    nutriscore = models.CharField(max_length=1, null=True, blank=True)
    novascore = models.IntegerField(null=True, blank=True)
    image_url = models.URLField(max_length=300, null=True, blank=True)
    url = models.URLField(max_length=300, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    stores = models.ManyToManyField(Store, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, blank=True)
    nutrition_reference = models.CharField(max_length=50, null=True, blank=True)
    nutrition_data = models.JSONField(null=True, blank=True)

    def substitutes_exists(self):
        return Product.objects.filter(category=self.category).exclude(id=self.id).filter(
            Q(nutriscore__lt=self.nutriscore) | Q(novascore__lt=self.novascore)).exists()



class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
