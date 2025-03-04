from rest_framework.generics import ListAPIView

from products.models import Product
from products.serializers import ProductsSerializer


class ProductsListAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductsSerializer
