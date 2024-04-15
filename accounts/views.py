from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as auth_login,logout
from django.http import HttpResponseRedirect,HttpResponse
from .models import Profile
from products.models import Product,SizeVarient,Coupon
from accounts.models import Cart,CartItem,Profile
import razorpay
# Create your views here.



def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username=email)

        if not user_obj.exists():
            messages.warning(request, 'Account not found.')
            return HttpResponseRedirect(request.path_info)

        if not user_obj[0].profile.is_email_verified:
            messages.warning(request, 'Your account is not verified.')
            return HttpResponseRedirect(request.path_info)

        user_obj = authenticate(username=email, password=password)
        if user_obj:
            auth_login(request, user_obj)
            return redirect('/')
        messages.warning(request,'Your Email is incredential')
    return render(request, 'accounts/login.html')  # Replace 'login.html' with the actual template name

        

    #     messages.warning(request, 'Invalid credentials')
    #     return HttpResponseRedirect(request.path_info)


    # return render(request ,'accounts/login.html')



def register(request):

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username = email)

        if user_obj.exists():
            messages.warning(request, 'Email is already taken.')
            return HttpResponseRedirect(request.path_info)

        print(email)

        user_obj = User.objects.create(first_name = first_name , last_name= last_name , email = email , username = email)
        user_obj.set_password(password)
        user_obj.save()

        messages.success(request, 'An email has been sent on your mail.')
        return HttpResponseRedirect(request.path_info)


    return render(request ,'accounts/register.html')




def activate_email(request , email_token):
    try:
        user = Profile.objects.get(email_token= email_token)
        user.is_email_verified = True
        user.save()
        return redirect('/')
    except Exception as e:
        return HttpResponse('Invalid Email token')
    
    
def add_to_cart(request,uid):
    profile = Profile.objects.get(user=request.user)
    context = {'profile': profile}
    varient=request.GET.get('varient')
    product=Product.objects.get(uid=uid)
    user=request.user
    cart,_=Cart.objects.get_or_create(user=user,is_paid=False)
    cart_item=CartItem.objects.create(cart=cart,product=product)
    if varient:
        varient=request.GET.get('varient')
        size_varient=SizeVarient.objects.get(size_name=varient)
        cart_item.size_varient=size_varient
        cart_item.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
from django.conf import settings        

def cart(request):
    cart = Cart.objects.filter(is_paid=False, user=request.user).first()
    if request.method=='POST':
        coupon=request.POST.get('coupon')
        coupon_obj=Coupon.objects.filter(coupon_code__icontains=coupon)
        if not coupon_obj.exists():
            messages.warning(request,'invalid coupon')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        if cart.coupon:
            messages.warning(request,'coupon coupon alredy exists')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        if cart.get_cart_total()<coupon_obj[0].min_amt:
            messages.warning(request,f'Amount should be greater than {coupon_obj[0].min_amt}')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        if coupon_obj[0].is_expire:
            messages.warning(request,f'coupon expired')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        cart.coupon=coupon_obj[0]
        cart.save()    
        messages.success(request,'coupon Applyed')
    client = razorpay.Client(auth=(settings.KEY, settings.SECRET))
    # Create order
    payment_amount = int(cart.get_cart_total() * 100)  # Convert to paise
    payment = client.order.create({'amount': payment_amount, 'currency': 'INR', 'payment_capture': 1})
    cart.razor_pay_order_id = payment['id']
    cart.save()
    print('*****')
    print(payment)
    print(type(payment['amount']))
    print('*****')
    context={'cart':cart,'payment':payment}    
            
    
    if cart:
        print("Cart found:", cart)
        context = {'cart': cart}
        return render(request, 'accounts/cart.html', context)
    else:
        print("Cart not found for user:", request.user)
        # Handle the case when the cart is not found, redirect or show an empty cart page.
        return render(request, 'accounts/cart_empty.html')
 
def remove_coupon(request,cart_id):
    cart=Cart.objects.get(uid=cart_id)
    cart.coupon=None
    cart.save()
    messages.warning(request,f'Coupon removed')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
          