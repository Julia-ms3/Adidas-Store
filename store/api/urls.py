from django.urls import path, include
from api.views import ProductsModelViewSet
from rest_framework import routers

app_name = 'api'
router = routers.DefaultRouter()
router.register(r'products', ProductsModelViewSet)
urlpatterns = [
    path('', include(router.urls))
]
