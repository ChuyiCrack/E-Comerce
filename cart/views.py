from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from coupons.forms import CouponApplyForm
from shop.recommender import Recommender



@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            product=product,
            quantity=cd['quantity'],
            override_quantity=cd['override']
        )
    return redirect('cart:cart_detail')

@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    for c in cart:
        print(c)
    coupon_apply_form = CouponApplyForm()
    r = Recommender()
    cart_products = [item['product'] for item in cart]
    if(cart_products):
        recommended_products = r.suggest_products_for(
            cart_products, max_results=4
        )
    else:
        recommended_products = []
    context = {
        'cart': cart ,
        'coupon_apply_form':coupon_apply_form ,
        'recommended_products': recommended_products,
        'authenticated':request.user.is_authenticated
        }
    return render(request, 'cart/detail.html',context)

@require_POST
def incrementDecrementCart(request,product_id):
    cart = Cart(request)
    product = get_object_or_404(Product , id = product_id)
    action = request.POST.get('action')
    toAdd = 1 if action == "plus" else -1
    if toAdd > 0 or ((cart.cart[str(product_id)]['quantity'] - 1) > 0 and toAdd < 0): 
        cart.add(
            product=product,
            quantity=toAdd,
        )

    else:
        cart.remove(product)
    
    return redirect('cart:cart_detail')

