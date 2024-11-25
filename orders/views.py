from django.shortcuts import render,redirect, get_object_or_404
from cart.cart import Cart
from .tasks import order_created
from django.contrib.admin.views.decorators import staff_member_required
from .models import Order
from django.contrib.staticfiles import finders
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .forms import OrderCreateForm
from .models import OrderItem

@login_required
def order_create(request):
    cart = Cart(request)
    user = request.user
    if request.method == 'POST':
        form = OrderCreateForm(request.POST) #Retrieve all the data to create a new Instance
        if form.is_valid(): #Check if nothing is missing
            order = form.save(commit=False)#Then with .save() create a new instance 
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.account = user
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            # clear the cart
            cart.clear()
            # launch asynchronous task
            order_created.delay(order.id) #You call the delay() method of the task to execute it asynchronously. The task will be added to the message queue and executed by the Celery worker as soon as possible.
            # set the order in the session
            request.session['order_id'] = order.id
            # redirect for payment
            return redirect('payment:process')
    else:
        form = OrderCreateForm()
    return render(
        request,
        'orders/order/create.html',
        {'cart': cart, 'form': form}
    )


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(
        request, 'admin/orders/order/detail.html', {'order': order}
    )



@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request , 'orders/order/pdf.html' , {'order':order})

@login_required
def orderDetail(request , orderId):
    order = get_object_or_404(Order, id=orderId)
    context = {
        'order':order
    }
    return render(request,'orders/order/orderDetail.html',context)


# @staff_member_required
# def admin_order_pdf(request, order_id):
# # Render the HTML content using Django's template system
#     order = get_object_or_404(Order, id=order_id)
#     html_content = render_to_string('orders/order/pdf.html', {'order': order})

#     # Generate the PDF from the HTML content
#     pdf_file = weasyprint.HTML(string=html_content).write_pdf()

#     # Create an HTTP response with the PDF file and set the appropriate content type
#     response = HttpResponse(pdf_file, content_type='application/pdf')
#     response['Content-Disposition'] = f'attachment; filename=order_{order_id}.pdf"'
#     return response

