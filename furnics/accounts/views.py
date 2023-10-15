from datetime import datetime
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
import pyotp
from .models import CustomUser, CustomUserManager
from django.contrib import messages
from django.views.decorators.cache import cache_control
from .utils import  send_otp
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.hashers import make_password
# Create your views here.


# view function for user login
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def user_login(request):
    # Check if a user or admin is already logged in
    if 'useremail' in request.session:
        return redirect('homepage')
    if 'adminemail' in request.session:
        return redirect('admin_home')

    if request.method == 'POST':
        user_email = request.POST.get('email')
        user_password = request.POST.get('password')

        # Check if the user exists
        try:
            user = CustomUser.objects.get(email=user_email)
        except CustomUser.DoesNotExist:
            user = None

        if user is not None:
            # Check if the user is blocked
            if not user.is_active:
                messages.error(request, 'Your account has been blocked')
                return redirect('user_login')
                
            # Attempt to authenticate the user
            user = authenticate(request, email=user_email, password=user_password)

            if user is not None and not user.is_superuser:
                # Login the user and set the session variable
                login(request, user)
                request.session['useremail'] = user_email
                return redirect('homepage')
            else:
                messages.error(request, 'Email or password is incorrect')
        else:
            messages.error(request, 'User does not exist')

    return render(request, 'accounts/login.html')


# view function for user to signup   
def user_signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        user_email = request.POST.get('email')
        phone = request.POST.get('phone_no')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmpassword')
        
        email_checking = CustomUser.objects.filter(email = user_email)

        
        if  email_checking.exists():
            messages.error(request,"email is already taken") 
            return redirect('user_signup')
        elif password == confirm_password:
            otp=send_otp(request)
            subject = 'verify your email to continue to create an account at Furnics.4U'
            message = otp
            from_email = settings.EMAIL_HOST_USER   
            recipient_list = [ user_email ] 

            send_mail(subject, message, from_email, recipient_list)  

            request.session['useremail'] = user_email
            request.session['username'] = username
            request.session['phoneno'] = phone
            request.session['password'] = password

            return redirect('user_otp')
        else:
            messages.error( request,'passwords do not match')
            

    return render(request,'accounts/signup.html')

# view function for user to logout
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def user_logout(request):
    
    if 'useremail' in request.session:
         
        logout(request)
        
    return redirect('homepage')

# view function for otp verification of the user after signing up 
def otp_verification(request):
    if request.method=='POST':
        otp=request.POST.get('otp')

        user_email=request.session['useremail']
        username=request.session['username']
        phone=request.session['phoneno']
        password=request.session['password']
        
        otp_secret_key=request.session['otp_secret_key']
        otp_valid_date=request.session['otp_valid_date']

        if otp_secret_key and otp_valid_date is not None:
            valid_until =datetime.fromisoformat(otp_valid_date)

            if valid_until > datetime.now():
               totp=pyotp.TOTP(otp_secret_key,interval=60)

               if totp.verify(otp):
                    
                    
                    my_User=CustomUser.objects.create_user(email=user_email,password=password,username=username,phone=phone)
                    my_User.save()
                    
                    
                    del request.session['useremail'] 
                    del request.session['username']
                    del request.session['phoneno']
                    del request.session['password']
                    del request.session['otp_secret_key']
                    del request.session['otp_valid_date']
                    

                    return redirect('user_login')
               else:
                    messages.error(request,"entered otp is not correct!!!")
                    # return redirect('')
                   
            else:
                del request.session['useremail'] 
                del request.session['username']
                del request.session['phoneno']
                del request.session['password']
                del request.session['otp_secret_key']
                del request.session['otp_valid_date']
                messages.error(request,"time expired for otp validation!!!!")

    return render(request,'accounts/verify.html')


# view function for resending the otp  
def otp_resend(request):
    # deleting the session of existing one time password
    del request.session['otp_secret_key']

    otp=send_otp(request)

    user_email=request.session['useremail']
    username=request.session['username']
    phone=request.session['phoneno']
    password=request.session['password']

    subject = 'verify your email to continue to create an account at Furnics.4U'
    message = otp
    from_email = settings.EMAIL_HOST_USER   
    recipient_list = [ user_email ] 
    send_mail(subject, message, from_email, recipient_list) 

    otp_secret_key=request.session['otp_secret_key']
    otp_valid_date=request.session['otp_valid_date']

    if otp_secret_key and otp_valid_date is not None:
        valid_until =datetime.fromisoformat(otp_valid_date)

        if valid_until > datetime.now():
            totp=pyotp.TOTP(otp_secret_key,interval=60)

            if totp.verify(otp):
                
                
                my_User=CustomUser.objects.create_user(email=user_email,password=password,username=username,phone=phone)
                my_User.save()
                
                
                del request.session['useremail']
                del request.session['username']
                del request.session['phoneno']
                del request.session['password']
                del request.session['otp_secret_key']
                del request.session['otp_valid_date']
                

                return redirect('user_login')
    

    return render(request,'verify.html')

def forgot_pass(request):
    if request.method=='POST':
        email=request.POST.get('email')
        request.session['check_mail']=email
        if CustomUser.objects.filter(email=email).exists():
            user=CustomUser.objects.get(email=email)
            user_email=user.email

            otp=send_otp(request)
            subject = 'verify your email to continue to reset your password at  Furnics.4U'
            message = otp
            from_email = settings.EMAIL_HOST_USER   
            recipient_list = [ user_email ] 

            send_mail(subject, message, from_email, recipient_list) 

            return redirect('forgot_pass_otp') 
        else:
            messages.error(request,"There is no account linked with this email")
            return redirect('forgot_pass')

    return render(request,'accounts/forgotpass.html')

# function for validating the otp 
def forgot_pass_otp(request):

    if request.method=='POST':
        otp=request.POST.get('otp')
        
        otp_secret_key=request.session['otp_secret_key']
        otp_valid_date=request.session['otp_valid_date']

        if otp_secret_key and otp_valid_date is not None:
            valid_until =datetime.fromisoformat(otp_valid_date)

            if valid_until > datetime.now():
               totp=pyotp.TOTP(otp_secret_key,interval=60)

               if totp.verify(otp):
                   

                   del request.session['otp_valid_date']
                   del request.session['otp_secret_key']

                   return redirect('reset_pass')
               else:
                   messages.error(request,"OTP you have enterd is incorrect")
                   return redirect('forgot_pass_otp')
            else:
                messages.error(request,"Time limit exceeded")
                return redirect('forgot_pass_otp')


    return render(request,'accounts/forgotpass_verify.html')

# function for reseting the password



def reset_pass(request):
    if request.method == "POST":
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 == password2:
            email = request.session.get('check_mail')
            try:
                user = CustomUser.objects.get(email=email)
                user.set_password(password1)  # Use set_password to hash and set the password
                user.save()
                del request.session['check_mail']
                return redirect('user_login')
            except CustomUser.DoesNotExist:
                messages.error(request, "There is no account linked with this email")
                return redirect('reset_pass')
        else:
            messages.error(request, "Passwords do not match")

    return render(request, 'accounts/resetpass.html')
