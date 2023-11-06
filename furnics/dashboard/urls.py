from django.urls import path
from . import views


urlpatterns = [
    
       path('',views.admin_login,name='admin_login'),
       path('admin-home/',views.adminhome,name='admin_home'),
       path('admin-logout',views.adminlogout,name='admin_logout'),
       path('users/',views.users,name='users'),
       path('block/<int:user_id>/',views.block_user,name='block_user'),

       path('categories/',views.categories,name='categories'),
       path('add-categories/',views.add_categories,name='add_categories'),
       path('edit-categories/<int:category_id>/',views.edit_categories,name='edit_categories'),
       path('delete-categories/<int:category_id>/',views.delete_categories,name='delete_categories'),

       path('sub-categories/',views.sub_categories,name='sub_categories'),
       path('add-subcategories/',views.add_subcategories,name='add_subcategories'),
       path('edit-subcategories/<int:subcategory_id>/',views.edit_subcategories,name='edit_subcategories'),
       path('delete-subcategories/<int:subcategory_id>/',views.delete_subcategories,name='delete_subcategories'),

       path('orders',views.orders,name="orders"),
       path("orders-details/<int:order_id>/",views.orders_details,name="orders_details"),
       path('order-status',views.order_status,name="order_status")
       
]

