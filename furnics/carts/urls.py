from django.urls import path
from . import views



urlpatterns = [
    
      
       path('',views.cart_page,name='cart_page'),
       path('add-cart/<int:product_id>/',views.add_cart,name='add_cart'),
       path('decrement-cart/<int:product_id>/',views.decrement_cartitem,name="decrement_cartitem"),
       path('remove-cart-item/<int:product_id>/',views.remove_cart_item,name="remove_cartitem"),
       path('checkout/<int:quantity>/',views.checkout_page,name="checkout_page"),

]
