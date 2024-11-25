from django.shortcuts import get_object_or_404, render
from .models import Category, Product
from cart.forms import CartAddProductForm
from cart.cart import Cart
from .recommender import Recommender
from django.utils.translation import gettext as _


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.exclude()
    if category_slug:
        language = request.LANGUAGE_CODE
        category = get_object_or_404(Category,
        translations__language_code=language,
        translations__slug=category_slug
        )
        products = products.filter(category=category)
    
    return render(
        request,
        'shop/product/list.html',
        {
            'category': category,
            'categories': categories,
            'products': products
        }
    )

def product_detail(request, id, slug):
    language = request.LANGUAGE_CODE
    product = get_object_or_404(Product, id=id,translations__language_code=language,translations__slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    r = Recommender()
    recommended_products = r.suggest_products_for([product], 4)
    cartUser = Cart(request)
    cartUser.cart = {int(k):v for k,v in cartUser.cart.items()}
    return render(
        request,
        'shop/product/detail.html',
        {'product': product,'cart_product_form': cart_product_form , 'cart':cartUser ,'recommended_products': recommended_products}
    )


