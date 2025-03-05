from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from products.models import Product
from products.serializers import ProductsSerializer


class ProductsModelViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductsSerializer

    # permission_classes = [IsAuthenticatedOrReadOnly,]

    def get_permissions(self):
        if self.action in ['create', 'partial_update', 'update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        return super(ProductsModelViewSet, self).get_permissions()
