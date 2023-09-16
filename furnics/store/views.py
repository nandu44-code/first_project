from django.shortcuts import render,redirect
from store.models import Product
from categories.models import Category,Sub_Category
from django.contrib import messages
# Create your views here.
def product_view(request):
    if 'adminemail' in request.session:
        products = Product.objects.all()
        categories = Category.objects.filter(is_activate=True)
        sub_categories = Sub_Category.objects.filter(is_activate=True)

        context={
            'products' : products,
            'category' : categories,
            'sub_category' : sub_categories,
        }
    return render(request,'dashboard/products.html',context)
def add_product(request):
    if request.method=='POST':
        product_name          =  request.POST['product_name']
        stock                 =  request.POST['stock']
        price                 =  request.POST['price']
        description           =  request.POST['product_description']
        image                 =  request.FILES.get('product_img', None)
        image1                =  request.FILES.get('product_img1', None)
        image2                =  request.FILES.get('product_img2', None)
        image3                =  request.FILES.get('product_img3',None)
        sub_category_id       =  request.POST.get('subcategory_name')
        sub_category_instance =  Sub_Category.objects.get(pk=sub_category_id)
        category              =  sub_category_instance.category

        if Product.objects.filter(product_name=product_name).exists():

            messages.error(request, 'Product name already exist')
            return redirect('product_view')
        else:
            product = Product.objects.create(
                product_name=product_name,
                stock=stock,
                price=price,
                images=image,
                image1=image1,
                image2=image2,
                image3=image3,
                category=category,
                sub_category=sub_category_instance,
                description=description,
                
               )
              
            product.save()
            return redirect('product_view')


def edit_product(request,product_id):
    product=Product.objects.get(pk=product_id)
    if request.method=='POST':
        product_name=request.POST['product_name']
        product.product_name = request.POST['product_name']
        product.stock = request.POST['stock']
        product.price = request.POST['price']
        product.description = request.POST['product_description']
        product.image = request.FILES.get('product_img', None)
        product.image1 = request.FILES.get('product_img1', None)
        product.image2 = request.FILES.get('product_img2', None)
        product.image3 = request.FILES.get('product_img3',None)
        sub_category_id = request.POST.get('subcategory_name')
        sub_category_instance=Sub_Category.objects.get(pk=sub_category_id)
        product.category=sub_category_instance.category

        if Product.objects.filter(product_name=product_name).exclude(pk=product_id).exists():

            messages.error(request,"Entered Sub Category is already taken!!")
            return redirect('sub_categories')
        else:
            product.save()
            return redirect('product_view')
        
def delete_product(request,product_id):
     product=Product.objects.get(pk=product_id)

     if product.is_activate:
        product.is_activate=False
        product.save()

       
        
        products = Product.objects.all()
        categories = Category.objects.filter(is_activate=True)
        sub_categories = Sub_Category.objects.filter(is_activate=True)

        context={
            'products' : products,
            'category' : categories,
            'sub_category' : sub_categories,
        }
        return render(request,'dashboard/products.html',context)
     
     else:
        product.is_activate=True
        product.save()
        
        products = Product.objects.all()
        categories = Category.objects.filter(is_activate=True)
        sub_categories = Sub_Category.objects.filter(is_activate=True)

        context={
            'products' : products,
            'category' : categories,
            'sub_category' : sub_categories,
        }
        return render(request,'dashboard/products.html',context)
        