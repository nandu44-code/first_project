from decimal import Decimal
from django.shortcuts import render,redirect
from store.models import Product, VariantImage, Variation
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
     product = Product()
     if request.method == 'POST':
        # product_name = request.POST.get('product_name')
        product.product_name = request.POST.get('product_name')
        product.description = request.POST.get('product_description')
        sub_category = request.POST.get('subcategory_name')
        sub_cat = Sub_Category.objects.get(id=sub_category)
        product.sub_category = sub_cat
        product.category = sub_cat.category
      
        product.save()
            

        return redirect('product_view')
       

def edit_product(request,product_id):
    product=Product.objects.get(pk = product_id)

    if request.method == 'POST':
        product_name = request.POST['product_name']
        product.product_name = request.POST['product_name']
        # product.price = request.POST['price']
        product.description = request.POST['product_description']
        sub_category_id = request.POST.get('subcategory_name')
        sub_category_instance=Sub_Category.objects.get(pk=sub_category_id)
        product.category=sub_category_instance.category
       
        
        if Product.objects.filter(product_name=product_name).exclude(pk=product_id).exists():

            messages.error(request,"Entered product is already taken!!")
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
        
def variant_view(request,product_id):

    variants = Variation.objects.filter(product=product_id)
    product = Product.objects.get(pk=product_id)
    # for variant in variants:

    # variant_image = VariantImage.objects.filter(variant=variant)
    # first_variant_image = variant_image.first()
    context = {
       
       'variant': variants,
       'product': product,
    #    'variant_image': first_variant_image
    }

    return render(request, 'dashboard/variants.html',context)

def add_variant(request,product_id):
    product_id = product_id
    if request.method =='POST':
        product = Product.objects.get(pk=product_id)
        color = request.POST.get('color')
        stock = request.POST.get('stock')
        actual_price = request.POST.get('ActualPrice')
        selling_price = request.POST.get('SellingPrice')
        images = request.FILES.getlist('VariantImage')
        image1 = images[0]
        image2 = images[1]
        image3 = images[2]
        image4 = images[3]
        
        variant = Variation(
            product = product,
            color = color,
            stock = stock,
            actual_price = actual_price,
            selling_price = selling_price,
            image1 = image1,
            image2 = image2,
            image3 = image3,
            image4 = image4

        )
        variant.save()
        
        # if images:
        #     for image in images:
        #         VariantImage.objects.create(
        #             variant =  variant,
        #             image = image
        #         )
                
                


        return redirect('variant_view',product_id)
