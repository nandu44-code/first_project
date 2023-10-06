from django.urls import path
from . import views


urlpatterns = [
    path('',views.product_view,name="product_view"),
    path('add-products',views.add_product,name="add_product"),
    path('edit-products/<int:product_id>/',views.edit_product,name="edit_product"),
    path('delete-products/<int:product_id>/',views.delete_product,name="delete_product"),
    path('view-varirants/<int:product_id>/',views.variant_view,name="variant_view"),
    path('add-varirants/<int:product_id>/',views.add_variant,name="add_variant"),
       
       
]