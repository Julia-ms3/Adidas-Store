from django.db import models

# Create your models here.
class Category(models.Model):
    name_category = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name_category

class Product(models.Model):
    name = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=3)
    quantity = models.PositiveIntegerField(default=0)
    description = models.TextField()
    img = models.ImageField(upload_to='product_images')
    category = models.ForeignKey(to=Category, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'product name - {self.name} category - {self.category}'

