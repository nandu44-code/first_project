from django.shortcuts import redirect, render
from django.contrib import messages

from accounts.models import CustomUser
from .models import Address

# Create your views here.
def user_profile(request):
    email=request.session['useremail']
    user=CustomUser.objects.get(email=email)
    user_id=user.id
    address=Address.objects.filter(user_id=user_id)
    context={
        'users':user,
        'address':address
    }

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

        address=Address(    user_id        =user_id,
                            house_no       = house_no,
                            recipient_name = recipient_name,
                            street_name    = street_name,
                            village_name   =  village_name,
                            postal_code    = postal_code,
                            district       =  district,
                            state          =  state,
                            country        =  country
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