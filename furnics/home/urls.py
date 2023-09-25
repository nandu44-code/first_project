
from django.urls import path
from . import views



urlpatterns = [
    
      path('',views.homepage,name="homepage"),
      path('view-shop',views.view_shop,name="shop_page"),
      path('view-subcategory/<int:category_id>/',views.view_subcategory,name="sub_category_page"),
      path('display-products/<int:sub_category_id>/',views.display_products,name="display_product"),
      path('product-details/<int:product_id>/',views.product_details,name="product_details"),
    
      
      

]