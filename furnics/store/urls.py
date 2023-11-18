from django.urls import path
from . import views


urlpatterns = [
    path('',views.product_view,name="product_view"),
    path('add-products',views.add_product,name="add_product"),
    path('edit-products/<int:product_id>/',views.edit_product,name="edit_product"),
    path('delete-products/<int:product_id>/',views.delete_product,name="delete_product"),

    path('view-varirants/<int:product_id>/',views.variant_view,name="variant_view"),
    path('add-varirants/<int:product_id>/',views.add_variant,name="add_variant"),
    path('edit-varirants/<int:variant_id>/',views.edit_variants,name="edit_variants"),
    path('delete-variant/<int:variant_id>/',views.delete_variant,name="delete_variant"),

    path('edit_variant_image',views.variant_image_edit,name="variant_image_edit")
       
       
]