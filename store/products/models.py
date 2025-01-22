from django.db import models
from users.models import User


# Create your models here.
class Category(models.Model):
    name_category = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name_category


class Product(models.Model):
    name = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=0)
    quantity = models.PositiveIntegerField(default=0)
    description = models.TextField()
    img = models.ImageField(upload_to='product_images')
    category = models.ForeignKey(to=Category, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'Product name: {self.name} ~ Category:  {self.category}'


class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        return sum(basket.sum() for basket in self)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)


class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f'BASKET FOR {self.user.username}  PRODUCT {self.product.name}'

    def sum(self):
        return self.product.price * self.quantity


