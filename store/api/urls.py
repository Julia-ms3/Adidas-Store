from django.urls import include, path
from rest_framework import routers

from api.views import BasketModelViewSet, ProductsModelViewSet

app_name = 'api'
router = routers.DefaultRouter()
router.register(r'products', ProductsModelViewSet)
router.register(r'basket', BasketModelViewSet)
urlpatterns = [
    path('', include(router.urls)),


]
