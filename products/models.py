from django.db import models
from django.utils.text import slugify
# Create your models here.

class Category(models.Model):
    name=models.CharField(max_length=255,unique=True)
    slug=models.SlugField(max_length=255,blank=True,null=True)
    parent=models.ForeignKey('self',on_delete=models.SET_NULL,related_name='children',blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural='Categories'

    def __str__(self) -> str:
        return self.name
    
    def save(self,*args,**kwargs):
        if not self.slug:
           self.slug=slugify(self.name)
        super().save(*args,**kwargs)   


class Product(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='products')
    name=models.CharField(max_length=255)
    slug=models.SlugField(max_length=255,blank=True,unique=True)
    description=models.TextField(blank=True,null=True)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    stock=models.PositiveIntegerField(default=0)
    low_stock=models.PositiveIntegerField(default=5)
    is_available=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name
    
    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug=slugify(self.name)
        if self.stock==0:
            self.is_available=False
        else:
            self.is_available=True
        super().save(*args,**kwargs)            


