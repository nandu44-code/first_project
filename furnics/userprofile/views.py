from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import Http404
from accounts.models import CustomUser
from carts.models import Order, OrderItem
from .models import Address

# Create your views here.
def user_profile(request):
    if 'useremail' in request.session:
        email=request.session['useremail']
        user=CustomUser.objects.get(email=email)
        user_id=user.id
        address=Address.objects.filter(user_id=user_id)
        context={
                'users':user,
                'address':address
            }
    else:
        return redirect('user_login')
    return render(request,'userprofile/user_profile.html',context)

def edit_user_profile(request,user_id):
  
   
    if request.method=='POST':

        user  =CustomUser.objects.get(id=user_id)

        if user:
            
            user.username=request.POST.get('username')
            user.email   =request.POST.get('email')
            user.phone   =request.POST.get('phone')
            user.save()
 
            return redirect('user_profile')

def address_view(request):

    if 'useremail' in request.session:
        email=request.session['useremail']
        user=CustomUser.objects.get(email=email)
        user_id=user.id
        address=Address.objects.filter(user_id=user_id)
        context={
                'users':user,
                'address':address
            }
    else:
        return redirect('user_login')
    return render(request,'userprofile/address.html',context)

def add_address(request,user_id):
    
    if request.method=='POST':
        user=CustomUser.objects.get(pk=user_id)
        user_id=user
        house_no = request.POST.get('house_no')
        recipient_name = request.POST.get('RecipientName')
        street_name = request.POST.get('street_name')
        village_name =  request.POST.get('Village')
        postal_code =  request.POST.get('postal_code')
        district =  request.POST.get('district')
        state =  request.POST.get('state')
        country =  request.POST.get('country')
        exists = Address.objects.filter(user_id=user_id).exists()
        print(exists)
        if exists == False:
        
            address=Address(    
                            user_id = user_id,
                            house_no = house_no,
                            recipient_name = recipient_name,
                            street_name = street_name,
                            village_name =  village_name,
                            postal_code = postal_code,
                            district =  district,
                            state =  state,
                            country =  country,
                            is_default = True
                        )

        else:
             address=Address(
                            user_id = user_id,
                            house_no = house_no,
                            recipient_name = recipient_name,
                            street_name = street_name,
                            village_name =  village_name,
                            postal_code = postal_code,
                            district =  district,
                            state =  state,
                            country =  country,
                            
                        )


        address.save()

        return redirect('user_profile')

def edit_address(request,address_id):
 
    if request.method=='POST':   
        address=Address.objects.get(id=address_id)
        
        address.house_no = request.POST.get('house_no')
        address.recipient_name = request.POST.get('RecipientName')
        address.street_name = request.POST.get('street_name')
        address.village_name =  request.POST.get('Village')
        address.postal_code =  request.POST.get('postal_code')
        address.district =  request.POST.get('district')
        address.state =  request.POST.get('state')
        address.country =  request.POST.get('country')

        address.save()

        return redirect('user_profile')

def delete_address(request,address_id):

    address=Address.objects.get(id=address_id)
    address.delete()
    return redirect('user_profile')



def default_address(request):

    if request.method =='POST':
        try:
            # Attempt to retrieve the default address
            default_address_check = Address.objects.get(is_default=True)
            
            # If a default address exists, remove the old default address
            default_address_check.is_default = False
            default_address_check.save()
            
        except Address.DoesNotExist:
            # Handle the case where no default address exists
            pass

        address_id = request.POST.get("default_address")  # getting the address selected by the user
        
        try:
            # Attempt to retrieve the selected address
            address = Address.objects.get(id=address_id)
            address.is_default = True
            address.save()
        except Address.DoesNotExist:
            # Handle the case where the selected address doesn't exist
            raise Http404("The selected address does not exist")  # Raise Http404 to indicate a not found error

    return redirect('user_profile')

def my_orders(request):
    if request.user:
        order_items=None
        order=Order.objects.filter(user=request.user)
        order_items = OrderItem.objects.order_by('order').distinct('order')
        # order_item =order_item.objects.filter(order=order)
        context={
            "order":order,
            "order_items":order_items
        }

        return render(request,"userprofile/my_orders.html",context)
def order_details(request,order_id):
    
    order=Order.objects.get(id=order_id)
    order_items=OrderItem.objects.filter(order=order)
    context={
        "order_items":order_items,
        "order":order
    }
    return render(request,"userprofile/order_details.html",context)