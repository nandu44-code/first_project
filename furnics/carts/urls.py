from django.urls import path
from . import views



urlpatterns = [
    
      
       path('',views.cart_page,name='cart_page'),
       path('add-cart/<int:product_id>/',views.add_cart,name='add_cart'),
       path('remove-cart/<int:product_id>/',views.decrement_cartitem,name="decrement_cartitem"),
]