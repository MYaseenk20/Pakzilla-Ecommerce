from django.db import models
from django.utils.text import slugify
import datetime
# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=100)
    slug=models.SlugField(null=True,blank=True)
    
    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug=slugify(self.title)
        super(Category, self).save(*args,**kwargs)
    def __str__(self):
        return self.name


class Product(models.Model):
    name=models.CharField(max_length=100)
    price=models.IntegerField(default=0)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,default=1,null=True,blank=True)
    description=models.CharField(max_length=200,default='',null=True,blank=True)
    image=models.ImageField(upload_to='uploads/products/')
    def __str__(self):
        return self.name
    @staticmethod
    def get_all_products():
        return Product.objects.all()

    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Product.objects.filter(category = category_id)
        else:
            return Product.get_all_products();

class Customer(models.Model):
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    phone=models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=500)

    @staticmethod
    def get_customer_by_email(email):
        try:
            Customer.objects.filter(email=email)
        except:
            return False

class Order(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    price=models.CharField(max_length=50)
    address=models.CharField(max_length=50)
    phone=models.CharField(max_length=50)
    complete=models.BooleanField(default=False)
    date=models.DateTimeField(default=datetime.datetime.now())

    def placeorder(self):
        self.save()
    def __str__(self):
        return self.product.name