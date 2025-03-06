from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from products.models import Basket, Product
from products.serializers import BasketSerializer, ProductsSerializer


class ProductsModelViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductsSerializer

    # permission_classes = [IsAuthenticatedOrReadOnly,]

    def get_permissions(self):
        if self.action in ['create', 'partial_update', 'update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        return super(ProductsModelViewSet, self).get_permissions()


class BasketModelViewSet(ModelViewSet):
    queryset = Basket.objects.all()
    serializer_class = BasketSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        queryset = super(BasketModelViewSet, self).get_queryset()
        return queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            product_id = request.data['product_id']  # data from user(post/patch)
            product = Product.objects.filter(id=product_id)
            print(f'product - {product}, product_id - {product_id}')
            print(f'product.first().id - {product.first().id}')

            if not product.exists():
                return Response({"product_id": "this object doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

            object, is_created = Basket.update_or_create(product.first().id, self.request.user)
            status_code = status.HTTP_201_CREATED if is_created else status.HTTP_200_OK
            serializer = self.get_serializer(object)
            return Response(serializer.data, status=status_code)

        except KeyError:
            return Response({"product_id": "this field is required"}, status=status.HTTP_400_BAD_REQUEST)
