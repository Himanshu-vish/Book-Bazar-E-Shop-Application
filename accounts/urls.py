from django.urls import path
from accounts.views import login, register, activate_email
from accounts.views import add_to_cart, cart,remove_coupon

urlpatterns = [
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('activate/<email_token>/', activate_email, name='activate_email'),
    path('cart/', cart, name='cart'),
    path('add-to-cart/<uid>/', add_to_cart, name='add_to_cart'),
    path('remove-coupon/<cart_id>/', remove_coupon, name='remove_coupon'),
]
