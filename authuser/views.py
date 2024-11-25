from django.shortcuts import render,redirect
from authuser.models import User
from orders.models import Order,OrderItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login,authenticate
from django.contrib import messages
from .forms import UserProfileForm,EditAccount
from django.contrib.auth.hashers import make_password
from .decorators import unauthenticated_user


def profileView(request):
    user = request.user
    allOrders = Order.objects.filter(account = user).order_by('-created').all()
    productsOrders = []
    for order in allOrders:
        toAdd = []
        extraProduct=False
        for i,orderItem in enumerate(order.items.all()):
            if i >= 3:
                extraProduct=True
                break
            toAdd.append(orderItem.product)
        productsOrders.append((order ,toAdd,extraProduct))

    if 'editAccount' in request.POST:
        form = EditAccount(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('authuser:profile')
        
    elif 'deleteOrder' in request.POST:
        idOrder = request.POST['deleteOrder']
        Order.objects.get(id = idOrder).delete()
        return redirect('authuser:profile')
        
    else:
        form = EditAccount(instance=user)

    context = {'orders':productsOrders , 'editForm':form}
    return render(request ,'profile.html' , context = context)

@unauthenticated_user
def loginPAge(request):
    print(request.session.get('order_id'))
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        try:
            account = User.objects.get(email = email)
            if account.check_password(password):
                login(request,account)
                return redirect("shop:product_list")
                
            else:
                messages.error(request, f"The password is incorrect.")
                return redirect("authuser:login")

        except ObjectDoesNotExist:
            messages.error(request, f"A user with email {email} doesn't exist.")
            return redirect("authuser:login")
    
    return render(request,'login.html')

@unauthenticated_user
def registerPage(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            login(request,user)

            newUser = authenticate(email = user.email, password = form.cleaned_data['password'])
            if newUser:
                login(request,newUser)
                return redirect("shop:product_list")


    else:
        form = UserProfileForm()

    context = {
        'form':form
    }
    return render(request,"register.html",context=context)
