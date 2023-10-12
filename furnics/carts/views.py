from django.shortcuts import render,redirect,get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import CustomUser
from userprofile.models import Address
from store.models import Product, Variation
from carts.models import Cart,CartItem
# Create your views here.
def cart_page(request,total=0,quantity=0,cart_items=None):
    if 'useremail' not in request.session:
        return redirect('user_login')
    tax=0
    grand_total=0
    
    if 'useremail' in request.session:
        email = request.session['useremail']
        user=CustomUser.objects.get(email=email)

    
    cart_id = _cart_id(request) #get or generate the cart_id
    try:
       

        cart = Cart.objects.get(user=user)
        cart_items = CartItem.objects.filter(cart=cart,is_active=True).order_by('id')
        for cart_item in cart_items:
            total += (cart_item.product.selling_price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2*total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        
        pass

    context = {
        
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax': tax,
        'grand_total':grand_total
    }
    # print(cart_items.product.product_name)
    return render(request,'cart/cart.html',context)

def _cart_id(request):
    
    cart=request.session.session_key
    
    if not cart:
        cart=request.session.create()
    return cart

def add_cart(request,product_id):

    if 'useremail' in request.session:
        email = request.session['useremail']
        user=CustomUser.objects.get(email=email)

    
    variant = Variation.objects.get(id=product_id) #get the product variation
    # if product.stock is None:
    #     return redirect('view_shop')
    cart_id = _cart_id(request)
    
    try:
        cart = Cart.objects.get(user = user) #get the cart using cart_id present in the session
        
    except Cart.DoesNotExist:
        if 'useremail' in request.session:
            email = request.session['useremail']
        user=CustomUser.objects.get(email=email)
        if user is not None:

            cart = Cart.objects.create(
                cart_id = _cart_id(request),
                user = user
            )
            cart.save()
    
    try:
        cart_item = CartItem.objects.get(product=variant,cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:

        cart_item =CartItem.objects.create(

            product = variant,
            quantity = 1,
            cart = cart,
        )
        cart_item.save()
    return redirect('cart_page')


def decrement_cartitem(request,product_id):

    
    if 'useremail' in request.session:
        email = request.session['useremail']
        user=CustomUser.objects.get(email=email)

    cart    = Cart.objects.get(user = user)
    product =   get_object_or_404(Variation,id = product_id)
    cart_item = CartItem.objects.get(product=product,cart=cart)

    if cart_item.quantity > 1:
        cart_item.quantity -=1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart_page')

def remove_cart_item(request,product_id):

    if 'useremail' in request.session:
        email = request.session['useremail']
        user=CustomUser.objects.get(email=email)


    cart    = Cart.objects.get(user=user)
    product =   get_object_or_404(Variation,id = product_id)
    cart_item = CartItem.objects.get(product=product,cart=cart)
    
    cart_item.delete()

    return redirect('cart_page')



def checkout_page(request,quantity):
    if 'useremail' in  request.session:
        
        if quantity :
        
            email = request.session['useremail'] #getting the email of the user from the session
            user = CustomUser.objects.get(email=email) 
            user_id = user.id
            address = Address.objects.filter(user_id=user_id)#using the user id getting all addresses associated with that user

            tax=0
            quantity=0
            cart_items=None
            grand_total=0
            total=0
            cart_id = _cart_id(request) #get or generate the cart_id
            try:
                cart = Cart.objects.get(cart_id=cart_id)
                cart_items = CartItem.objects.filter(cart=cart,is_active=True)
                for cart_item in cart_items:
                    total += (cart_item.product.price * cart_item.quantity)
                    quantity += cart_item.quantity
                tax = (2*total)/100
                grand_total = total + tax
            except ObjectDoesNotExist:
                
                pass
            context = {

                'address': address,
                'tax': tax,
                'grand_total': grand_total,
                'quantity': quantity,
                'cart_items': cart_items,
                'total' : total
            
            }
        
            return render(request,'cart/checkout.html',context)
        else:
            return redirect('cart_page')
    else:
        return redirect('user_login')