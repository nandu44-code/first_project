from django.urls import path
from . import views


urlpatterns = [
    path('',views.wishlist,name="wishlist_view"),
    path('add-to-wishlist<int:product_id>',views.add_to_wishlist,name="add_to_wishlist"),
    
]