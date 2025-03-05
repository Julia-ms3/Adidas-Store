from django.urls import path, include
from api.views import ProductsListAPIView
from rest_framework import routers

app_name = 'api'
router = routers.DefaultRouter()
router.register(r'products', ProductsListAPIView)
urlpatterns = [
    path('', include(router.urls))
]
