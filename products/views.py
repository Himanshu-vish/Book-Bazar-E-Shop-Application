from django.shortcuts import render
from products.models import Product,SizeVarient
from django.http import HttpResponse
# Create your views here 
       
def get_product(request, slug):
    print('*****')
    print(request.user)
    print('user profile-->',request.user.profile)
    # Check if the user is authenticated and has a profile
        
    cart_count = request.user.profile.get_cart_count()
    print('Cart count:', cart_count)
    
    try:
        product = Product.objects.get(slug=slug)
        context = {'product': product}

        if request.GET.get('size'):
            size = request.GET.get('size')
            price = product.get_product_price_by_size(size)
            context['selected_size'] = size
            context['updated_price'] = price

        if request.GET.get('color'):
            color = request.GET.get('color')
            price = product.get_product_price_by_color(color)
            context['selected_color'] = color
            context['updated_price'] = price

        return render(request, 'product/product.html', context=context)
    
    except Exception as e:
        print(e)
        return HttpResponse("An error occurred while processing the request.")



