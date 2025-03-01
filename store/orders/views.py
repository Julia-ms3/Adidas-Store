from http import HTTPStatus

import stripe
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from mixins.views import TitleMixin
from orders.forms import OrderForm
from orders.models import Order
from products.models import Basket

# from store.settings import DOMAIN_NAME, STRIPE_SECRET_KEY, STRIPE_SECRET_WEBHOOK

stripe.api_key = settings.STRIPE_SECRET_KEY


class OrdersListView(TitleMixin, ListView):
    title = 'Orders'
    template_name = 'orders/orders.html'
    model = Order
    ordering = ('-created_time')

    def get_queryset(self):
        queryset = super(OrdersListView, self).get_queryset()
        return queryset.filter(order_creator=self.request.user)


class OrderDetailView(TitleMixin, DetailView):
    title = 'Order detail'
    template_name = 'orders/order.html'
    model = Order


class SuccessView(TitleMixin, TemplateView):
    template_name = 'orders/success.html'
    title = 'Successful payment'


class CancelView(TitleMixin, TemplateView):
    template_name = 'orders/cancel.html'
    title = 'Canceled payment'


class CreateOrderView(TitleMixin, CreateView):
    template_name = 'orders/order_create.html'
    form_class = OrderForm
    success_url = reverse_lazy('index')
    title = 'Create order'

    def post(self, request, *args, **kwargs):
        super(CreateOrderView, self).post(request, *args, **kwargs)
        print(f"DEBUG: self.object = {self.object}")
        baskets = Basket.objects.filter(user=self.request.user)
        line_items = []
        for basket in baskets:
            item = {
                'price': basket.product.stripe_price_id,
                'quantity': basket.quantity
            }
            line_items.append(item)

        checkout_session = stripe.checkout.Session.create(
            line_items=line_items,

            mode='payment',
            success_url=settings.DOMAIN_NAME + reverse('orders:order_success'),
            cancel_url=settings.DOMAIN_NAME + reverse('orders:order_canceled'),
            metadata={'order_id': self.object.id}

        )
        return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)

    def form_valid(self, form):
        form.instance.order_creator = self.request.user
        return super(CreateOrderView, self).form_valid(form)


@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_SECRET_WEBHOOK
        )
    except ValueError as e:
        print(f"Invalid payload: {e}")
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        print(f"Invalid signature: {e}")
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        fulfill_checkout(session)

    return HttpResponse(status=200)


def fulfill_checkout(session):
    print(session)
    order_id = int(session.metadata.order_id)
    order = Order.objects.get(id=order_id)
    order.update_after_payment()

    print("Fulfilling Checkout Session", session)
