import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from orders.models import Order
from django.shortcuts import get_object_or_404
from shop.models import Product
from shop.recommender import Recommender
from orders.tasks import order_created

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)
    if event.type == 'checkout.session.completed':
        session = event.data.object
        if (session.mode == 'payment' and session.payment_status == 'paid'
        ):
            order = get_object_or_404(Order , id=session.client_reference_id)
            # mark order as paid
            order.stripe_id = session.payment_intent
            order.paid = True
            order_created.delay(order.id) #You call the delay() method of the task to execute it asynchronously. The task will be added to the message queue and executed by the Celery worker as soon as possible.
            # save items bought for product recommendations
            product_ids = order.items.values_list('product_id')
            products = Product.objects.filter(id__in=product_ids)
            r = Recommender()
            r.products_bought(products) 
            
            order.save()
    return HttpResponse(status=200)
