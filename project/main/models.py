from django.utils import timezone
from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    category_image = models.ImageField(upload_to='images')

    def category_count(self):
        return self.blog.count()

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=100)

    def brand_count(self):
        return self.blog.count()

    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100)


    def color_count(self):
        return self.blog.count()


    def __str__(self):
        return self.name

class Filter_Price(models.Model):
    
    FILTER_PRICE = (
        ('10-100', '10-100'),
        ('100-200', '100-200'),
        ('200-300', '200-300'),
        ('300-400', '300-400'),
        ('400-500', '400-500'),
        ('500-600', '500-600'),
        ('600-700', '600-700'),
        ('700-800', '700-800'),
        ('800-900', '800-900'),
        ('900-1000', '900-1000'),
        ('1000-1100', '1000-1100'),
        ('1100-1200', '1100-1200')

    )

    price = models.CharField(choices=FILTER_PRICE, max_length=68)

    def filter_price_count(self):
        return self.blog.count()


    def __str__(self):
        return self.price


class Product(models.Model):

    CONDITION = (('New','New'),('Old', 'Old'))
    STOCK = (('IN STOCK','IN STOCK'),('OUT OF STOCK','OUT OF STOCK'))
    STATUS = (('Publish','Publish'),('Draft','Draft'))
    name = models.CharField(max_length=200)
    price = models.IntegerField(default=0)
    condition = models.CharField(choices=CONDITION, max_length=100)
    information = RichTextField()
    description = models.TextField()
    image = models.ImageField(upload_to='images')
    stock = models.CharField(choices=STOCK, max_length=100)
    status = models.CharField(choices=STATUS, max_length=100)
    created_date = models.DateTimeField(default=timezone.now)
    favourite = models.ManyToManyField(User, related_name='favourite')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='productcategory')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='productbrand')
    color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='productcolor')
    filter_price = models.ForeignKey(Filter_Price, on_delete=models.CASCADE, related_name='productpricefilter')
    unique_id = models.CharField(unique=True, max_length=200, blank=True, null=True)


    def save(self, *args, **kwargs):
        if self.unique_id is None and self.created_date and self.id:
            self.unique_id = self.created_date.strftime('75%Y%m%d23') + str(self.id)
        return super().save(*args, **kwargs)
    

    def __str__(self):
        return self.name   

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviewuser')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviewproduct')
    comment = models.TextField()
    rate = models.IntegerField(default=0)
    date_modified = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str(self.id)




class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')
    image = models.ImageField(upload_to='images')



class Tag(models.Model):
    name = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_tages')


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orderuser')
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postcode = models.IntegerField()
    phone = models.IntegerField()
    email = models.EmailField()
    amount = models.CharField(max_length=100)
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    paid = models.BooleanField(default=False, null=True)
    date = models.DateTimeField(auto_now_add=True)  


    def __str__(self):
        return self.user.username 

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images')
    quantity = models.CharField(max_length=20)
    price = models.CharField(max_length=50)
    total = models.CharField(max_length=100)

    def __str__(self):
        return self.order.user.username

# class Profile(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userprofile')
#     phone = models.IntegerField()
#     address = models.TextField()
#     city = models.CharField(max_length=100)
#     state = models.CharField(max_length=100)
#     country = models.CharField(max_length=100)
#     postcode = models.IntegerField()
#     date = models.DateTimeField(auto_now_add=True)  

#     def __str__(self):
#         return self.user.username



class BannerList(models.Model):
    # product_image = models.ImageField(upload_to='images')
    title = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


    def __str__(self):
        return self.title
    


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Checkout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)


    def __str__(self):
        return self.user.username