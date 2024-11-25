from django.urls import path
from . import views
app_name = 'authuser'
urlpatterns = [
    path('login/',views.loginPAge , name="login"),
    path('register/',views.registerPage , name="register"),
    path('profile',views.profileView , name='profile'),
    
]
