from django.shortcuts import render,redirect
from django.views.decorators.cache import never_cache
from django.db.models import Q
from categories.models import Category
from categories.models import Sub_Category
from accounts.models import CustomUser
from store.models import Product
# Create your views here.
# @never_cache  
def homepage(request):

   
    
    if 'adminemail' in request.session:
        return redirect('admin_home')




    return render(request,'home/index.html')

def view_shop(request):
    categories=Category.objects.filter(is_activate=True)
    products=Product.objects.filter(is_activate=True)
    context={
        'category':categories,
        'product':products,
    }



    return render(request,'home/shop.html',context)

def view_subcategory(request,category_id):
   
    subcategory=Sub_Category.objects.filter(Q(is_activate=True) & Q(category=category_id))
    context={
        'subcategory':subcategory
    }

    return render(request,'home/subcategory.html',context)

def display_products(request,sub_category_id):
    
    product=Product.objects.filter(Q(is_activate=True) & Q(sub_category = sub_category_id))
    context={
        'product':product
            
            }                            

    return render(request,'home/products_display.html',context)       

def product_details(request,product_id):

    product=Product.objects.filter(Q(is_activate=True) & Q(id=product_id))

    context={
        'product':product
    }

    return render(request,'home/product_details.html',context)

def user_profile(request):
    email=request.session['useremail']
    user=CustomUser.objects.filter(email=email)

    context={
        'users':user
    }

    return render(request,'home/user_profile.html',context)

def edit_user_profile(request,user_id):
  
   
    if request.method=='POST':
        user  =CustomUser.objects.get(id=user_id)

        if user:
            print(user.username)
            user.username=request.POST.get('username')
            user.email   =request.POST.get('email')
            user.phone   =request.POST.get('phone')
            user.save()

    return redirect('user_profile')