from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.views.decorators.cache import never_cache
from django.db.models import Q,Max
from categories.models import Category
from categories.models import Sub_Category
from accounts.models import CustomUser
from store.models import Product, Variation
# Create your views here.
# @never_cache  
def homepage(request):

   
    
    if 'adminemail' in request.session:
        return redirect('admin_home')



    
    return render(request,'home/index.html')

def view_shop(request):
    categories=Category.objects.filter(is_activate=True)
    products=Product.objects.filter(is_activate=True)
    variants = Variation.objects.order_by('product').distinct('product')

   
    context={
        'category':categories,
        'product':products,
        'variants':variants
    }



    return render(request,'home/shop.html',context)

def view_subcategory(request,category_id):
   
    subcategory=Sub_Category.objects.filter(Q(is_activate=True) & Q(category=category_id))
    # Assuming you already have 'subcategory' containing the filtered subcategories
    products = Product.objects.filter(sub_category__in=subcategory, is_activate=True)

    
    base_variants = Variation.objects.filter(product__in=products).values('product').distinct()

    context={
        'subcategory':subcategory,
        'base_variant':base_variants
    }

    return render(request,'home/subcategory.html',context)

def display_products(request,sub_category_id):
    
    product = Product.objects.filter(Q(is_activate=True) & Q(sub_category = sub_category_id))
    
    # Fetch one variant for each product using distinct
    variants = Variation.objects.order_by('product').distinct('product')

    context={
        'variants':variants
            
            }                            

    return render(request,'home/products_display.html',context)

def product_details(request,variant_id):


    variants = Variation.objects.get(pk=variant_id)
    product_id = variants.product

    available_variants =Variation.objects.filter(product=product_id)

    for i in available_variants:

        print(i.color)
    context={
        # 'product':product,
        'variant': variants,
        'available_variants':available_variants
    }

    return render(request,'home/product_details.html',context)

def variant_select(request,variant_id):


    variants = Variation.objects.get(pk=variant_id)
    product_id = variants.product

    available_variants =Variation.objects.filter(product=product_id)
    
   
    
    variant_price = variants.selling_price
    variant_stock = variants.stock
    variant_image1 = variants.image1.url
    variant_image2 = variants.image2.url
    variant_image3 = variants.image3.url
    variant_image4 = variants.image4.url

        # 'available_vatiants':available_variants
    

    return JsonResponse({'variant':variant_price,
                         'variant_stock':variant_stock,
                         'variant_image1':variant_image1,
                         'variant_image2':variant_image2,
                         'variant_image3':variant_image3,
                         'variant_image4':variant_image4
                         })


def product_search(request):

    query=request.GET.get('q')
    modified_string = query.replace(" ", "")
    variants=None
    product_id=[]
    if modified_string == "":
        
        return redirect('shop_page')
    else:

        product=Product.objects.filter(product_name__icontains=query)
        for product in product:
            # product_id.append(product.id)

            variants=Variation.objects.filter(product=product)

        context={
            "product":product,
            "variants":variants,
        }
        return render(request,'home/product_search.html',context)