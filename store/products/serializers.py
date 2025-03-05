from rest_framework import serializers

from products.models import Product,Category


# Create your views here.
class ProductsSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='name_category',
        queryset=Category.objects.all(),

    )

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'quantity', 'description', 'img', 'category']
