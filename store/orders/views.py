from http import HTTPStatus

import stripe
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView

from mixins.views import TitleMixin
from orders.forms import OrderForm
from store.settings import MAIN_PATH, STRIPE_SECRET_KEY, STRIPE_SECRET_WEBHOOK

stripe.api_key = STRIPE_SECRET_KEY


class OrdersView(TitleMixin, TemplateView):
    template_name = 'orders/orders.html'
    title = 'Orders'


class SuccessView(TitleMixin, TemplateView):
    template_name = 'orders/success.html'
    title = 'Successful payment'


class CancelView(TitleMixin, TemplateView):
    template_name = 'orders/cancel.html'
    title = 'Canceled payment'


class CreateOrderView(TitleMixin, CreateView):
    template_name = 'orders/order_create.html'
    title = 'Create order'
    form_class = OrderForm
    success_url = reverse_lazy('index')

    def post(self, request, *args, **kwargs):
        super(CreateOrderView, self).post(request, *args, **kwargs)
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': 'price_1QvxO14f7pACW7PgiNHQpdPE',
                    'quantity': 1,
                },
            ],

            mode='payment',
            success_url=MAIN_PATH + reverse('orders:order_success'),
            cancel_url=MAIN_PATH + reverse('orders:order_canceled'),
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
            payload, sig_header, STRIPE_SECRET_WEBHOOK
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    if (
            event['type'] == 'checkout.session.completed'
            or event['type'] == 'checkout.session.async_payment_succeeded'
    ):
        fulfill_checkout(event['data']['object']['id'])


def fulfill_checkout(session_id):
    print("Fulfilling Checkout Session", session_id)
