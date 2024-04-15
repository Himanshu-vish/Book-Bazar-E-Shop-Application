from django.db import models
from django.contrib.auth.models import User,AbstractUser
from base.models import BaseModel
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from base.email import send_account_activation_email
from products.models import Product,ColorVarient,SizeVarient,Coupon
from django.conf import settings



class Profile(BaseModel):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    is_email_verified=models.BooleanField(default=False)
    email_token=models.CharField(max_length=500,null=True,blank=True)
    profile_image=models.ImageField(upload_to="profile")
    def get_cart_count(self):
        return CartItem.objects.filter(cart__is_paid=False,cart__user=self.user).count()
        # if hasattr(self, 'cart') and hasattr(self.cart, 'cart_item'):
        #     return self.cart.cart_item.count()
    
@receiver(post_save , sender = User)
def  send_email_token(sender , instance , created , **kwargs):
    try:
        if created:
            email_token = str(uuid.uuid4())
            Profile.objects.create(user=instance,email_token=email_token)
            email = instance.email
            send_account_activation_email(email , email_token)

    except Exception as e:
        print(e)

class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carts")
    coupon=models.ForeignKey(Coupon,on_delete=models.SET_NULL,null=True,blank=True)
    is_paid = models.BooleanField(default=False)
    razor_pay_order_id=models.CharField(max_length=100,null=True,blank=True)
    razor_pay_payment_id=models.CharField(max_length=100,null=True,blank=True)
    razor_pay_payment_signature=models.CharField(max_length=100,null=True,blank=True)
    
    def get_cart_total(self):
        cart_items = self.cart_item.all()
        price = []
        for cart_item in cart_items:
            price.append(cart_item.get_product_price())
        if self.coupon:
            return sum(price)-self.coupon.discount_price
        return sum(price)
class CartItem(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_item")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    color_varient = models.ForeignKey(ColorVarient, on_delete=models.SET_NULL, null=True, blank=True)
    size_varient = models.ForeignKey(SizeVarient, on_delete=models.SET_NULL, null=True, blank=True)

    def get_product_price(self):
        price = [self.product.product_price]
        if self.size_varient:
            size_varient_price = self.size_varient.price
            price.append(size_varient_price)
        return sum(price)
    
    
    