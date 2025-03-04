from rest_framework import serializers

from products.models import Product


# Create your views here.
class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price',  'quantity', 'description', 'img', 'category']
