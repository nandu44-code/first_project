   
from django.urls import path
from . import views



urlpatterns = [
    
     
    
      path('',views.user_profile,name="user_profile"),
      path('edit-profile/<int:user_id>/',views.edit_user_profile,name="edit_user_profile"),
      path('user-address<int:user_id>',views.add_address,name="add_address"),
      path('user-address<int:address_id>',views.edit_address,name="edit_address"),

      
      
      

]   









