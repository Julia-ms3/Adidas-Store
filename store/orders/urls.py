from django.urls import path

from orders.views import CancelView, CreateOrderView, OrdersView, SuccessView

app_name = 'orders'

urlpatterns = [
    path('', OrdersView.as_view(), name='orders'),
    path('order_creation/', CreateOrderView.as_view(), name='order_creation'),
    path('order_success/', SuccessView.as_view(), name='order_success'),
    path('order_canceled/', CancelView.as_view(), name='order_canceled'),
]

