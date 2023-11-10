import random
from django.db.models import Q
from django.contrib import messages
from django.http import JsonResponse,HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import CustomUser
from wishlist.models import WishlistItem
from userprofile.models import Address
from store.models import Product, Variation
from carts.models import Cart,CartItem, Order, OrderItem
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
    is_exist = WishlistItem.objects.filter(user = user, product_name=variant).exists()

    if is_exist:
        wishlist_item = WishlistItem.objects.get(user = user, product_name=variant)
        wishlist_item.delete()
        return redirect('shop_page')
    else:
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



def checkout_page(request):
    if request.method=='POST':

        if 'useremail' in  request.session:
        
            email = request.session['useremail'] #getting the email of the user from the session
            user = CustomUser.objects.get(email=email) 
            user_id = user.id

            selected_address_id=request.POST.get('selectedAddress')
            if selected_address_id is None:
                default_address=Address.objects.get(user_id=user_id,is_default=True)
                selected_address_id=default_address.id

            print(selected_address_id)
            address = Address.objects.get(id=selected_address_id) #using the user id getting all addresses associated with that user

            tax=0
            quantity=0
            cart_items=None
            grand_total=0
            total=0
            print("/////////////////////////////")
            cart_id = _cart_id(request) #get or generate the cart_id
            try:
                print(".........")
                cart = Cart.objects.get(user=user)
                cart_items = CartItem.objects.filter(cart=cart,is_active=True)
                for cart_item in cart_items:
                    total += (cart_item.product.selling_price * cart_item.quantity)
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
    #     else:
    #         return redirect('cart_page')
    # else:
    #     return redirect('user_login')

def address_checkout(request):
    if 'useremail' in request.session:
        email=request.session['useremail']
        # getting the user associated with this username
        user = CustomUser.objects.get(email=email)
        address = Address.objects.filter(user_id=user.id,is_default=False)

        for i in address:
            print(i.recipient_name)
        default_address =Address.objects.get(is_default=True)  

        context={
            'address':address,
            'default_address': default_address
        }
        return render(request,'cart/address_selection.html',context)
    
def add_address_checkout(request,user_id):

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

        address = Address(    
            user_id = user_id,
            house_no = house_no,
            recipient_name = recipient_name,
            street_name = street_name,
            village_name = village_name,
            postal_code = postal_code,
            district = district,
            state = state,
            country = country
            )
        exists = Address.objects.filter(user=user).exists()
        print(exists)
        if exists is None:
            address.is_default=True

        address.save()
        return redirect('address_checkout')
    
def place_order(request):
    print("ffffffffffffffff")
    if request.method == 'POST':
        print("hdskjhkhjjkkhkhhhjkjhjhjhjjj")
        email = request.session['useremail']
        user = CustomUser.objects.get(email=email)
       
        selected_address_id = request.POST.get('selected_address')
       
        address = Address.objects.get(id=selected_address_id)

        order = Order()
        order.user = user
        order.address = address
        print(address.id)
        print(",,.,.><><><><><><><><><><><><><><><><><><><><><.")
        cart = Cart.objects.get(user=user)
        try:
            cart_item = CartItem.objects.filter(cart=cart, is_active=True)
        except:
            cart_item = CartItem.objects.filter(cart=cart, is_active=True)

        cart_total_price = 0
        for item in cart_item:
            cart_total_price = cart_total_price + item.product.selling_price * item.quantity
        order.total_price = cart_total_price
        trackno = 'pvkewt' + str(random.randint(1111111, 9999999))
        while Order.objects.filter(tracking_no=trackno) is None:
            trackno = 'pvkewt' + str(random.randint(1111111, 9999999))
        order.tracking_no = trackno

        payment_mode = request.POST.get('payment_mode')
        # if payment_mode == 'cod':

        if payment_mode == 'Paid by Razorpay':
            order.payment_mode = request.POST.get('payment_mode')
            order.payment_id = request.POST.get('payment_id')
        else:
            order.payment_mode = 'cod'
            order.payment_id = ' '
        order.save()

        neworderitems = CartItem.objects.filter(cart=cart, is_active=True)
        for item in neworderitems:

            OrderItem.objects.create(
                order=order,
                variant=item.product,
                product=item.product.product,
                price=item.product.selling_price,
                quantity=item.quantity,
            )
            # reduce the product quantity from available stock
            orderproduct = Variation.objects.filter(id=item.product.id).first()
            orderproduct.stock = orderproduct.stock - item.quantity
            orderproduct.save()
        Cart.objects.filter(cart_id=item.cart.cart_id).delete()
        # messages.success(request, "Your order has been placed successfully")

        payMode = request.POST.get('payment')
        if payMode == 'Paid by Razorpay':
            return JsonResponse({'status': 'Your order has been placed successfully'})
        else:
           pass

        return redirect('order_success')

def razorpay_check(request):
    try:
        user = request.user
        print("User:", user)
        
        try:
            user = CustomUser.objects.get(email=user)
        except ObjectDoesNotExist:
            # Handle the case where the user does not exist
            return JsonResponse({'error': 'User not found'}, status=400)

        try:
            cart = Cart.objects.get(user=user)
        except ObjectDoesNotExist:
            # Handle the case where the cart does not exist
            return JsonResponse({'error': 'Cart not found'}, status=400)

        cart_items = CartItem.objects.filter(cart=cart)
        total_price = 0

        for item in cart_items:
            print("Selling Price:", item.product.selling_price)
            total_price += item.product.selling_price * item.quantity

        print("Total Price:", total_price)

        return JsonResponse({
            'total_price': total_price
        })

    except Exception as e:
        # Handle other unexpected exceptions
        print("Error:", e)
        return JsonResponse({'error': 'Internal Server Error'}, status=500)

def order_success(request):


    return render(request,'cart/thankyou.html')
    