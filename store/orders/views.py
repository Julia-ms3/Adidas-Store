from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView

from mixins.views import TitleMixin
from orders.forms import OrderForm


class OrdersView(TitleMixin, TemplateView):
    template_name = 'orders/orders.html'
    title = 'Orders'


class CreateOrderView(TitleMixin, CreateView):
    template_name = 'orders/order_create.html'
    title = 'Create order'
    form_class = OrderForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.order_creator = self.request.user
        return super(CreateOrderView, self).form_valid(form)
