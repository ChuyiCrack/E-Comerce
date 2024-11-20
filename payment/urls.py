from django.urls import path
from . import views,webhooks
from django.utils.translation import gettext_lazy as _

app_name = 'payment'
urlpatterns = [
    path(_('process/'), views.payment_process, name='process'),
    path(_('completed/'), views.payment_completed, name='completed'),
    path(_('canceled/'), views.payment_canceled, name='canceled'),
    #path('webhook/', webhooks.stripe_webhook, name='stripe-webhook'),However, we need a single URL for Stripe to notify events, and we need to avoid language prefixes in the webhook URL
    #We remove it and we will ad it directly to the main urrls.py on my shop
]

