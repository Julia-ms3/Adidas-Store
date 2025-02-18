from django.urls import path

from orders.views import CreateOrderView, OrdersView

app_name = 'orders'

urlpatterns = [
    path('', OrdersView.as_view(), name='orders'),
    path('order_creation/', CreateOrderView.as_view(), name='order_creation')
]
