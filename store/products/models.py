import stripe
from django.conf import settings
from django.db import models

from users.models import User

stripe.api_key = settings.STRIPE_SECRET_KEY


# Create your models here.
class Category(models.Model):
    name_category = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name_category


class Product(models.Model):
    name = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=0)
    stripe_price_id = models.CharField(max_length=30, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=0)
    description = models.TextField()
    img = models.ImageField(upload_to='product_images')
    category = models.ForeignKey(to=Category, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'Product name: {self.name} ~ Category:  {self.category}'

    def save(self, *args, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.stripe_price_id:
            stripe_product_price = self.create_stripe_product()
            self.stripe_price_id = stripe_product_price['id']
        super(Product, self).save(force_insert=False, force_update=False, using=None, update_fields=None)

    def create_stripe_product(self):
        stripe_product = stripe.Product.create(name=self.name)
        print(stripe_product)
        stripe_price = stripe.Price.create(product=stripe_product['id'], unit_amount=self.price * 100, currency="usd")
        print(stripe_price)
        return stripe_price


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

    def de_json(self):
        print('call this func')
        basket_items = {
            'product_name': self.product.name,
            'price': int(self.product.price),
            'quantity': self.quantity,
            'current_sum': int(self.sum())
        }
        print('BASKET items: ', basket_items)
        return basket_items
