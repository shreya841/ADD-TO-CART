from django.urls import path
from .views import *

urlpatterns = [
     path('',dashboard,name='dashboard'),
     path('cartss',cartss,name='cartss'),
     path('addtocart/<int:pk>',addtocart ,name='addtocart'),
     path('delete/<int:pk>',delete,name='delete'),
     path("payment/",payment,name='payment'),
     path('payment-status', payment_status, name='payment-status')


     
]