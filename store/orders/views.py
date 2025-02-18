from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView

from mixins.views import TitleMixin
from orders.forms import OrderForm

class OrdersView(TemplateView, TitleMixin):
    template_name = 'orders/orders.html'
    title = 'Orders'

class CreateOrderView(CreateView, TitleMixin):

    template_name = 'orders/order_create.html'
    title = 'Create order'
    form_class = OrderForm

