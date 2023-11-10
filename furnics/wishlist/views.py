from django.shortcuts import render
from .models import WishlistItem
# Create your views here.
def wishlist(request):

    if request.user:
        user=request.user

    wishlist_items=WishlistItem.objects.filter(user=user)
    context={
        'wishlist':wishlist_items
    }


    return render(request,'userprofile/wishlist.html',context)
def add_to_wishlist(request,product_id):


    