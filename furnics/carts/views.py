import random
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import CustomUser
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
        else:
            return redirect('cart_page')
    else:
        return redirect('user_login')
    
def place_order(request):
    if request.method == 'POST':
        email = request.session['useremail']
        user = CustomUser.objects.get(email=email)
        recipient_name = request.POST.get('username')
        selected_address_id = request.POST.get('selectedAddress')
        if recipient_name is None:
            address = Address.objects.get(id=selected_address_id)
        else:
            address = Address.objects.get(recipient_name=recipient_name)

        order = Order()
        order.user = user
        order.address = address
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
                product=item.product.product,
                variant=item.product,
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

        return redirect('order_success  ')
            # return redirect('my_orders')
        # return redirect('home')

    # if 'useremail' in request.session:
    #     cart_id = _cart_id(request)  # Get or generate the cart_id
    #     tax = 0
    #     grand_total = 0
    #     total = 0
    #     quantity = 0
    #     cart_items = ''
    #     try:

    #         try:
    #             email = request.session['user-email']
    #             user = CustomUser.objects.get(email=email)
    #             cart_items = CartItem.objects.filter(user=user, is_active=True)
    #         except:
    #             cart = Cart.objects.get(cart_id=cart_id)
    #             cart_items = CartItem.objects.filter(cart=cart, is_active=True)
    #         for cart_item in cart_items:
    #             total += (cart_item.variant.selling_price * cart_item.quantity)
    #             quantity += cart_item.quantity
    #         tax = (2 * total) / 100
    #         grand_total = total + tax

    #     except ObjectDoesNotExist:
    #         pass
    #     try:
    #         email = request.session['user-email']
    #         user = CustomUser.objects.get(email=email)
    #         addresses = Address.objects.filter(user_id=user,is_default=False)
    #     except:
    #         pass
    #     try:
    #         default_address = Address.objects.get(user_id=user, is_default=True)
    #     except:
    #         default_address = Address.objects.filter(user_id=user).first()

    #     context = {
    #         'total': total,
    #         'quantity': quantity,
    #         'cart_items': cart_items,
    #         'addresses': addresses,
    #         'grand_total': grand_total,
    #         'default_address': default_address,

    #     }
    #     return render(request, 'user/checkout/checkout.html', context)
    # return redirect('user_signin')

def order_success(request):


    return render(request,'cart/thankyou.html')
    