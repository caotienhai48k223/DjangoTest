from django.db import models
from django.utils.text import slugify
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.contrib.postgres.fields import ArrayField
# Create your models here.

class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  date_modified = models.DateTimeField(User, auto_now=True)
  phone = models.CharField(max_length=20, blank=True)
  address1 = models.CharField(max_length=200, blank=True)
  address2 = models.CharField(max_length=200, blank=True)
  city = models.CharField(max_length=200, blank=True)
  state = models.CharField(max_length=200, blank=True)
  old_cart = models.CharField(max_length=200, blank=True, null=True)
  
  def __str__(self):
    return self.user.username
  
def create_profile(sender, instance, created, **kwargs):
  if created:
    user_profile = Profile(user=instance)
    user_profile.save()
post_save.connect(create_profile, sender=User)


class Customer(models.Model):
  first_name = models.CharField(max_length=100)
  last_name = models.CharField(max_length=100)
  phone = models.CharField(max_length=20)
  email = models.EmailField(max_length=150)
  password = models.CharField(max_length=100)
  
  def __str__(self):
    return f'{self.first_name} {self.last_name}'

class Category(models.Model):
  name = models.CharField(max_length=100)
  slug = models.SlugField(max_length=220, unique=True, blank=True)
  def save(self, *args, **kwargs):
    if not self.slug:
      self.slug = slugify(self.name)
    super(Category, self).save(*args, **kwargs)
    
  def __str__(self):
      return self.name

  
class Product(models.Model):
  title = models.CharField(max_length=200)
  category = models.ForeignKey(Category, on_delete=models.CASCADE)
  slug = models.SlugField(max_length=220, unique=True, blank=True)
  thumbnail= models.URLField(max_length=500, blank=True, null=True)
  description = models.TextField()
  images = ArrayField(models.URLField(), blank=True, null=True, default=list)
  size_chart = models.URLField(default='https://product.hstatic.net/200000284249/product/size_chart_2024_1536_x_2048_38b45007e2974e3dbc65d20e73557f89_master.jpg', null=True, blank=True)
  price = models.DecimalField(max_digits=10, decimal_places=0)
  created_date = models.DateTimeField(auto_now_add=True, blank=True)
  is_sale = models.BooleanField(default=False)
  discount = models.DecimalField(decimal_places=0, max_digits=3, blank=True, null=True)
  sale_price = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
  start_sale = models.DateField(blank=True, null=True)
  end_sale = models.DateField(blank=True, null=True)
  
  def clean(self):
    if not self.is_sale and (self.start_sale or self.end_sale or self.discount):
      raise ValidationError("Không thể nhập `start_sale` và `end_sale` khi `is_sale` là False.")
  
  def save(self, *args, **kwargs):
    if not self.slug:
      self.slug = slugify(self.title)
    if self.discount:
      self.sale_price = self.price - (self.discount / 100) * self.price
    self.clean()
    super(Product, self).save(*args, **kwargs)
  
  def __str__(self):
    return self.title


class ProductVariant(models.Model):
  product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
  color = models.CharField(max_length=20)
  size = models.CharField(max_length=10)
  quantity = models.DecimalField(max_digits=10, decimal_places=0, null=True)
  q_purchase = models.DecimalField(max_digits=10, decimal_places=0, null=True, default=0, blank=True)
  stock = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
  status = models.BooleanField(default=True)

  def save(self, *args, **kwargs):
    self.stock = self.quantity - self.q_purchase
    if self.stock == 5:
        self.status = False
    super(ProductVariant, self).save(*args, **kwargs)

  def __str__(self):
    return f"{self.product.title} - {self.color} - {self.size}"



class Order(models.Model):
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  customer = models.ForeignKey(User, on_delete=models.CASCADE)
  quantity = models.IntegerField(default=1)
  address = models.CharField(max_length= 100, default='', blank=True)
  phone = models.CharField(max_length=20, default='', blank=True)
  date = models.DateField(default=datetime.now)
  status = models.BooleanField(default=False)








class Room(models.Model):
  name = models.CharField(max_length=150)
  def __str__(self):
    return self.name
  
class Message(models.Model):
  content = models.TextField()
  user = models.CharField(max_length=150)
  room = models.CharField(max_length=150)
  created_date = models.DateTimeField(default=datetime.now, blank=True)
  
  
  
