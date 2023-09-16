from django.shortcuts import render,redirect
from django.views.decorators.cache import never_cache
# Create your views here.
# @never_cache  
def homepage(request):

   
    
    if 'adminemail' in request.session:
        return redirect('admin_home')




    return render(request,'home/index.html')

