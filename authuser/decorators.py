from django.shortcuts import redirect
from functools import wraps

def unauthenticated_user(view_func):
    @wraps(view_func) #This ensures that the original view function's name and docstring are preserved.
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("shop:product_list")
        return view_func(request, *args, **kwargs)
    return wrapper