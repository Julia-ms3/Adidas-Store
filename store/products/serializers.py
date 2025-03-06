from rest_framework import fields, serializers

from products.models import Basket, Category, Product


# Create your views here.
class ProductsSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='name_category',
        queryset=Category.objects.all(),

    )

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'quantity', 'description', 'img', 'category']


class BasketSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True

    )
    product = ProductsSerializer()
    sum = fields.IntegerField(required=False)
    total_sum = fields.SerializerMethodField()
    total_quantity = fields.SerializerMethodField()

    class Meta:
        model = Basket
        fields = ['id', 'user', 'product', 'sum', 'total_sum', 'quantity', 'total_quantity', 'timestamp']
        read_only_fields = ['timestamp']

    def get_total_sum(self, obj):
        return Basket.objects.filter(user_id=obj.user.id).total_sum()

    def get_total_quantity(self, obj):
        return Basket.objects.filter(user_id=obj.user.id).total_quantity()
