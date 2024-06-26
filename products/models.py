from django.db import models
from base.models import BaseModel
from django.utils.text import slugify

class Category(BaseModel):
    category_name=models.CharField(max_length=100)
    slug=models.SlugField(unique=True,null=True,blank=True)
    category_image=models.ImageField(upload_to="categories")
    
    def save(self,*args,**kwargs):
        self.slug=slugify(self.category_name)
        super(Category,self).save(*args,**kwargs)
        
    def __str__(self) -> str:
        return self.category_name    
    
    
class ColorVarient(BaseModel):
    color_name=models.CharField(max_length=100)
    price=models.IntegerField(default=0)
    
    def __str__(self) -> str:
        return self.color_name
    
    
class SizeVarient(BaseModel):
    size_name=models.CharField(max_length=100)
    price=models.IntegerField(default=0)
    
    def __str__(self) -> str:
        return self.size_name   
    
    
class Product(BaseModel):
    product_name=models.CharField(max_length=100)    
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name="products")
    slug=models.SlugField(unique=True,null=True,blank=True)
    product_price=models.IntegerField()    
    product_discription=models.CharField(max_length=500)
    color_varient=models.ManyToManyField(ColorVarient,blank=True)
    size_varient=models.ManyToManyField(SizeVarient,blank=True)
    
    def save(self,*args,**kwargs):
        self.slug=slugify(self.product_name)
        super(Product,self).save(*args,**kwargs)
        
    def __str__(self) -> str:
        return self.product_name
    
    def get_product_price_by_size(self,size):
        return self.product_price + SizeVarient.objects.get(size_name=size).price
    
    def get_product_price_by_color(self,color):
        return self.product_price + ColorVarient.objects.get(color_name=color).price
   
    
class ProductImage(BaseModel):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="product_image")
    product_image=models.ImageField(upload_to="product")
    
class Coupon(BaseModel):
    coupon_code=models.CharField(max_length=100)    
    is_expire=models.BooleanField(default=False)
    discount_price=models.IntegerField(default=100)
    min_amt=models.IntegerField(default=500)
    
