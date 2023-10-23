from django.urls import path
from . import views



urlpatterns = [
    
      
       path('',views.cart_page,name='cart_page'),
       path('add-cart/<int:product_id>/',views.add_cart,name='add_cart'),
       path('decrement-cart/<int:product_id>/',views.decrement_cartitem,name="decrement_cartitem"),
       path('remove-cart-item/<int:product_id>/',views.remove_cart_item,name="remove_cartitem"),
       path('address-checkout',views.address_checkout,name="address_checkout"),
       path('add-address-checkout/<int:user_id>/',views.add_address_checkout,name="add_address_checkout"),
       path('checkout',views.checkout_page,name="checkout_page"),
       path('order',views.place_order,name='place_order'),
       path('order-success',views.order_success,name="order_success")
]
