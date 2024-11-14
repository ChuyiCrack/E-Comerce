from django.shortcuts import redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from .forms import CouponApplyForm
from .models import Coupon

@require_POST #Exclusive for POST request and you put it on the forr method post action to use this view whenever you pish the submit button
def coupon_apply(request):
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(
                code__iexact=code, #This case will match eventhought if its upper or lowercase, if the code matches all ok
                valid_from__lte=now,# Here validates that valid_from is less than the curr time
                valid_to__gte=now,# Here validates that valid_to is greather than the curr time 
                active=True
            )
            request.session['coupon_id'] = coupon.id
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None
    return redirect('cart:cart_detail')

